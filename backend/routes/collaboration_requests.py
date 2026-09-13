"""
Collaboration request lifecycle.

Supports both:

Faculty -> Faculty
Faculty -> External Researcher

Both use the same:

Request
    -> Email
    -> Accept / Reject
    -> Authority Review
    -> Approve / Reject
    -> Active
"""

import os

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from database.connection import SessionLocal

from models.models import (
    Faculty,
    ExternalResearcher,
    FundingCall,
    MoU,
    CollaborationRequest,
    CollaborationResponseToken,
    TrackingRecord,
)

from routes.auth import get_current_faculty

from services import (
    email_service,
    matching_service,
    token_service,
)


router = APIRouter(prefix="/api/collaboration-requests")

FRONTEND_BASE_URL = os.getenv(
    "FRONTEND_BASE_URL",
    "http://localhost:5173",
)

AUTHORITY_API_KEY = os.getenv("AUTHORITY_API_KEY")


# ============================================================
# HELPERS
# ============================================================

def _faculty_or_404(db, faculty_id: int) -> Faculty:
    faculty = (
        db.query(Faculty)
        .filter(Faculty.id == faculty_id)
        .first()
    )

    if not faculty:
        raise HTTPException(
            status_code=404,
            detail="Faculty not found.",
        )

    return faculty


def _external_or_404(
    db,
    external_researcher_id: int,
) -> ExternalResearcher:

    researcher = (
        db.query(ExternalResearcher)
        .filter(
            ExternalResearcher.id == external_researcher_id
        )
        .first()
    )

    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="External researcher not found.",
        )

    return researcher


def _funding_label(
    db,
    funding_id: Optional[int],
) -> Optional[str]:

    if not funding_id:
        return None

    call = (
        db.query(FundingCall)
        .filter(FundingCall.id == funding_id)
        .first()
    )

    return call.name if call else None


def _mou_label(
    db,
    mou_id: Optional[int],
) -> str:

    if not mou_id:
        return "No active/relevant MoU found."

    mou = (
        db.query(MoU)
        .filter(MoU.id == mou_id)
        .first()
    )

    return (
        mou.institution
        if mou
        else "No active/relevant MoU found."
    )


def _target_info(db, req: CollaborationRequest) -> dict:

    if req.target_faculty_id is not None:

        target = (
            db.query(Faculty)
            .filter(Faculty.id == req.target_faculty_id)
            .first()
        )

        if not target:
            return {
                "type": "faculty",
                "faculty_id": str(req.target_faculty_id),
                "name": "Unknown Faculty",
                "department": None,
                "institution": None,
                "email": None,
            }

        return {
            "type": "faculty",
            "faculty_id": str(target.id),
            "name": target.name,
            "department": target.department,
            "institution": None,
            "email": target.email,
        }

    if req.target_external_researcher_id is not None:

        target = (
            db.query(ExternalResearcher)
            .filter(
                ExternalResearcher.id
                == req.target_external_researcher_id
            )
            .first()
        )

        if not target:
            return {
                "type": "external",
                "external_researcher_id": str(
                    req.target_external_researcher_id
                ),
                "name": "Unknown External Researcher",
                "department": None,
                "institution": None,
                "email": None,
            }

        return {
            "type": "external",
            "external_researcher_id": str(target.id),
            "name": target.name,
            "department": None,
            "institution": target.institution,
            "email": target.email,
        }

    return {
        "type": "unknown",
        "name": "Unknown Target",
        "department": None,
        "institution": None,
        "email": None,
    }


def _serialize_summary(
    db,
    req: CollaborationRequest,
    other,
) -> dict:

    if isinstance(other, Faculty):

        target = {
            "type": "faculty",
            "faculty_id": str(other.id),
            "name": other.name,
            "department": other.department,
        }

    else:

        target = {
            "type": "external",
            "external_researcher_id": str(other.id),
            "name": other.name,
            "institution": other.institution,
            "country": other.country,
        }

    return {
        "id": req.id,
        "faculty": target,
        "target": target,
        "topic": req.topic,
        "matching_score": req.matching_score,
        "faculty_status": req.faculty_status,
        "authority_status": req.authority_status,
        "stage": req.stage,
        "created_at": (
            req.created_at.isoformat()
            if req.created_at
            else None
        ),
        "updated_at": (
            req.updated_at.isoformat()
            if req.updated_at
            else None
        ),
    }


def _serialize_detail(
    db,
    req: CollaborationRequest,
    requester: Faculty,
) -> dict:

    evidence = req.matching_evidence or {}

    target = _target_info(db, req)

    return {
        "id": req.id,

        "requester": {
            "faculty_id": str(requester.id),
            "name": requester.name,
            "department": requester.department,
        },

        "target": target,

        "topic": req.topic,
        "proposal": req.proposal,
        "reason": req.reason,

        "matching_score": req.matching_score,

        "matching_evidence": evidence,

        "funding": (
            {
                "id": req.funding_id,
                "label": _funding_label(
                    db,
                    req.funding_id,
                ),
            }
            if req.funding_id
            else None
        ),

        "mou": (
            {
                "id": req.mou_id,
                "label": _mou_label(
                    db,
                    req.mou_id,
                ),
            }
            if req.mou_id
            else None
        ),

        "university_benefit": req.university_benefit,

        "faculty_status": req.faculty_status,
        "faculty_comments": req.faculty_comments,

        "faculty_responded_at": (
            req.faculty_responded_at.isoformat()
            if req.faculty_responded_at
            else None
        ),

        "authority_status": req.authority_status,
        "authority_comments": req.authority_comments,

        "authority_responded_at": (
            req.authority_responded_at.isoformat()
            if req.authority_responded_at
            else None
        ),

        "stage": req.stage,

        "created_at": (
            req.created_at.isoformat()
            if req.created_at
            else None
        ),

        "updated_at": (
            req.updated_at.isoformat()
            if req.updated_at
            else None
        ),
    }


def _issue_token(
    db,
    request_id: int,
    action: str,
    recipient_faculty_id: Optional[int] = None,
    recipient_external_researcher_id: Optional[int] = None,
) -> str:

    raw = token_service.generate_raw_token()

    db.add(
        CollaborationResponseToken(
            request_id=request_id,
            recipient_faculty_id=recipient_faculty_id,
            recipient_external_researcher_id=(
                recipient_external_researcher_id
            ),
            action=action,
            token_hash=token_service.hash_token(raw),
            expires_at=token_service.default_expiry(),
        )
    )

    return raw


def _send_recipient_request_email(
    db,
    req: CollaborationRequest,
    requester: Faculty,
    target_name: str,
    target_email: str,
    target_faculty_id: Optional[int] = None,
    target_external_researcher_id: Optional[int] = None,
):

    if not target_email:

        return {
            "sent": False,
            "error": "Target does not have an email address.",
        }

    accept_raw = _issue_token(
        db=db,
        request_id=req.id,
        action="faculty_accept",
        recipient_faculty_id=target_faculty_id,
        recipient_external_researcher_id=(
            target_external_researcher_id
        ),
    )

    reject_raw = _issue_token(
        db=db,
        request_id=req.id,
        action="faculty_reject",
        recipient_faculty_id=target_faculty_id,
        recipient_external_researcher_id=(
            target_external_researcher_id
        ),
    )

    db.commit()

    evidence = req.matching_evidence or {}

    subject, html = (
        email_service.build_collaboration_request_email(
            requester_name=requester.name,
            target_name=target_name,
            topic=req.topic,
            proposal=req.proposal,
            reason=req.reason,
            matching_score=req.matching_score,
            matching_expertise=evidence.get(
                "matching_expertise",
                [],
            ),
            relevant_publications=evidence.get(
                "relevant_publications",
                [],
            ),
            relevant_projects=evidence.get(
                "relevant_projects",
                [],
            ),
            relevant_research_work=evidence.get(
                "relevant_research_work",
                [],
            ),
            funding_label=_funding_label(
                db,
                req.funding_id,
            ),
            mou_label=(
                _mou_label(db, req.mou_id)
                if req.mou_id
                else None
            ),
            university_benefit=req.university_benefit,
            accept_url=(
                f"{FRONTEND_BASE_URL}"
                f"/collaboration-response/{accept_raw}"
            ),
            reject_url=(
                f"{FRONTEND_BASE_URL}"
                f"/collaboration-response/{reject_raw}"
            ),
        )
    )

    return email_service.send_email(
        target_email,
        subject,
        html,
    )


def _send_authority_review_email(
    db,
    req: CollaborationRequest,
    requester: Faculty,
):

    target = _target_info(db, req)

    approve_raw = _issue_token(
        db=db,
        request_id=req.id,
        action="authority_approve",
    )

    reject_raw = _issue_token(
        db=db,
        request_id=req.id,
        action="authority_reject",
    )

    db.commit()

    evidence = req.matching_evidence or {}

    target_department = (
        target.get("department")
        or target.get("institution")
        or "External Researcher"
    )

    subject, html = (
        email_service.build_authority_review_email(
            requester_name=requester.name,
            target_name=target.get("name"),
            requester_department=requester.department,
            target_department=target_department,
            topic=req.topic,
            proposal=req.proposal,
            reason=req.reason,
            matching_score=req.matching_score,
            matching_expertise=evidence.get(
                "matching_expertise",
                [],
            ),
            relevant_publications=evidence.get(
                "relevant_publications",
                [],
            ),
            relevant_projects=evidence.get(
                "relevant_projects",
                [],
            ),
            relevant_research_work=evidence.get(
                "relevant_research_work",
                [],
            ),
            funding_label=_funding_label(
                db,
                req.funding_id,
            ),
            mou_label=(
                _mou_label(db, req.mou_id)
                if req.mou_id
                else None
            ),
            university_benefit=req.university_benefit,
            approve_url=(
                f"{FRONTEND_BASE_URL}"
                f"/collaboration-response/{approve_raw}"
            ),
            reject_url=(
                f"{FRONTEND_BASE_URL}"
                f"/collaboration-response/{reject_raw}"
            ),
        )
    )

    authority_email = os.getenv("AUTHORITY_EMAIL")

    return email_service.send_email(
        authority_email,
        subject,
        html,
    )


def _activate_tracking(
    db,
    requester: Faculty,
    req: CollaborationRequest,
):

    today = datetime.utcnow().date()

    target = _target_info(db, req)

    if target["type"] == "faculty":

        target_name = target["name"]

        record = (
            db.query(TrackingRecord)
            .filter(
                TrackingRecord.faculty_a == requester.name,
                TrackingRecord.faculty_b == target_name,
                TrackingRecord.topic == req.topic,
            )
            .first()
        )

        if record:

            record.current_stage = "Active"

            history = record.history or []

            history.append(
                {
                    "stage": "Active",
                    "date": today.isoformat(),
                }
            )

            record.history = history
            record.last_updated = today

        else:

            db.add(
                TrackingRecord(
                    faculty_a=requester.name,
                    faculty_b=target_name,
                    topic=req.topic,
                    current_stage="Active",
                    history=[
                        {
                            "stage": "Active",
                            "date": today.isoformat(),
                        }
                    ],
                    last_updated=today,
                )
            )

    else:

        external_id = req.target_external_researcher_id

        record = (
            db.query(TrackingRecord)
            .filter(
                TrackingRecord.faculty_a == requester.name,
                TrackingRecord.external_researcher_id
                == external_id,
                TrackingRecord.topic == req.topic,
            )
            .first()
        )

        if record:

            record.current_stage = "Active"

            history = record.history or []

            history.append(
                {
                    "stage": "Active",
                    "date": today.isoformat(),
                }
            )

            record.history = history
            record.last_updated = today

        else:

            db.add(
                TrackingRecord(
                    faculty_a=requester.name,
                    external_researcher_id=external_id,
                    external_institution=target.get(
                        "institution"
                    ),
                    topic=req.topic,
                    current_stage="Active",
                    history=[
                        {
                            "stage": "Active",
                            "date": today.isoformat(),
                        }
                    ],
                    last_updated=today,
                )
            )


# ============================================================
# CREATE
# ============================================================

class CreateRequestIn(BaseModel):

    target_faculty_id: Optional[str] = None

    target_external_researcher_id: Optional[int] = None

    topic: str

    proposal: Optional[str] = None
    reason: Optional[str] = None

    funding_id: Optional[int] = None
    mou_id: Optional[int] = None

    university_benefit: Optional[str] = None


@router.post("")
def create_collaboration_request(
    payload: CreateRequestIn,
    current_faculty: dict = Depends(
        get_current_faculty
    ),
):

    db = SessionLocal()

    try:

        requester_id = int(
            current_faculty["faculty_id"]
        )

        if (
            payload.target_faculty_id is None
            and payload.target_external_researcher_id is None
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Either target_faculty_id or "
                    "target_external_researcher_id is required."
                ),
            )

        if (
            payload.target_faculty_id is not None
            and payload.target_external_researcher_id is not None
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Choose either a faculty target "
                    "or an external researcher target."
                ),
            )

        requester = _faculty_or_404(
            db,
            requester_id,
        )

        target_faculty = None
        target_external = None

        target_faculty_id = None
        target_external_id = None

        if payload.target_faculty_id is not None:

            target_faculty_id = int(
                payload.target_faculty_id
            )

            if requester_id == target_faculty_id:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "You cannot send a collaboration "
                        "request to yourself."
                    ),
                )

            target_faculty = _faculty_or_404(
                db,
                target_faculty_id,
            )

        else:

            target_external_id = (
                payload.target_external_researcher_id
            )

            target_external = _external_or_404(
                db,
                target_external_id,
            )

            if not target_external.email:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "This external researcher "
                        "does not have an email address."
                    ),
                )

        # ----------------------------------------------------
        # Score computed server-side
        # ----------------------------------------------------

        if target_faculty_id is not None:

            match = (
                matching_service.score_candidate(
                    db,
                    target_faculty_id,
                    payload.topic,
                )
                or {}
            )

        else:

            # External researcher matching is already represented
            # in the unified search result. For the request flow,
            # preserve the supplied topic and calculate a simple
            # evidence score from the external researcher's stored
            # fit score.
            match = {
                "score": target_external.research_fit,
                "matching_expertise": (
                    target_external.research_interests
                    or []
                ),
                "relevant_publications": [],
                "relevant_projects": [],
                "relevant_research_work": (
                    target_external.skills
                    or []
                ),
                "reason": (
                    "External researcher selected "
                    "from collaboration search."
                ),
            }

        req = CollaborationRequest(

            requester_faculty_id=requester_id,

            target_faculty_id=target_faculty_id,

            target_external_researcher_id=target_external_id,

            topic=payload.topic,

            proposal=payload.proposal,

            reason=payload.reason,

            matching_score=match.get("score"),

            matching_evidence={
                "matching_expertise": match.get(
                    "matching_expertise",
                    [],
                ),
                "relevant_publications": match.get(
                    "relevant_publications",
                    [],
                ),
                "relevant_projects": match.get(
                    "relevant_projects",
                    [],
                ),
                "relevant_research_work": match.get(
                    "relevant_research_work",
                    [],
                ),
                "reason": match.get("reason"),
            },

            funding_id=payload.funding_id,

            mou_id=payload.mou_id,

            university_benefit=(
                payload.university_benefit
            ),
        )

        db.add(req)

        db.commit()
        db.refresh(req)

        # ----------------------------------------------------
        # Send email
        # ----------------------------------------------------

        if target_faculty is not None:

            email_result = (
                _send_recipient_request_email(
                    db=db,
                    req=req,
                    requester=requester,
                    target_name=target_faculty.name,
                    target_email=target_faculty.email,
                    target_faculty_id=target_faculty.id,
                )
            )

        else:

            email_result = (
                _send_recipient_request_email(
                    db=db,
                    req=req,
                    requester=requester,
                    target_name=target_external.name,
                    target_email=target_external.email,
                    target_external_researcher_id=(
                        target_external.id
                    ),
                )
            )

        return {
            "request": _serialize_detail(
                db,
                req,
                requester,
            ),
            "email_sent": email_result.get(
                "sent",
                False,
            ),
        }

    finally:
        db.close()


# ============================================================
# SENT
# ============================================================

@router.get("/sent")
def list_sent_requests(
    current_faculty: dict = Depends(
        get_current_faculty
    ),
):

    db = SessionLocal()

    try:

        faculty_id = int(
            current_faculty["faculty_id"]
        )

        requests = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.requester_faculty_id
                == faculty_id
            )
            .order_by(
                CollaborationRequest.created_at.desc()
            )
            .all()
        )

        out = []

        for req in requests:

            if req.target_faculty_id is not None:

                target = (
                    db.query(Faculty)
                    .filter(
                        Faculty.id
                        == req.target_faculty_id
                    )
                    .first()
                )

            else:

                target = (
                    db.query(ExternalResearcher)
                    .filter(
                        ExternalResearcher.id
                        == req.target_external_researcher_id
                    )
                    .first()
                )

            if target:

                out.append(
                    _serialize_summary(
                        db,
                        req,
                        target,
                    )
                )

        return {
            "requests": out
        }

    finally:
        db.close()


# ============================================================
# RECEIVED
# ============================================================

@router.get("/received")
def list_received_requests(
    current_faculty: dict = Depends(
        get_current_faculty
    ),
):

    db = SessionLocal()

    try:

        faculty_id = int(
            current_faculty["faculty_id"]
        )

        # Only internal faculty can receive through
        # the logged-in faculty workflow.
        requests = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.target_faculty_id
                == faculty_id
            )
            .order_by(
                CollaborationRequest.created_at.desc()
            )
            .all()
        )

        out = []

        for req in requests:

            requester = (
                db.query(Faculty)
                .filter(
                    Faculty.id
                    == req.requester_faculty_id
                )
                .first()
            )

            if requester:

                out.append(
                    _serialize_detail(
                        db,
                        req,
                        requester,
                    )
                )

        return {
            "requests": out
        }

    finally:
        db.close()


# ============================================================
# DETAIL
# ============================================================

@router.get("/{request_id}")
def get_request_detail(
    request_id: int,
    current_faculty: dict = Depends(
        get_current_faculty
    ),
):

    db = SessionLocal()

    try:

        faculty_id = int(
            current_faculty["faculty_id"]
        )

        req = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.id
                == request_id
            )
            .first()
        )

        if not req:

            raise HTTPException(
                status_code=404,
                detail="Collaboration request not found.",
            )

        # External targets don't have a faculty login.
        # Therefore only the requester can access an
        # external-target request from the authenticated API.
        if faculty_id != req.requester_faculty_id:

            if (
                req.target_faculty_id is None
                or faculty_id != req.target_faculty_id
            ):

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "You do not have access "
                        "to this request."
                    ),
                )

        requester = (
            db.query(Faculty)
            .filter(
                Faculty.id
                == req.requester_faculty_id
            )
            .first()
        )

        return _serialize_detail(
            db,
            req,
            requester,
        )

    finally:
        db.close()


# ============================================================
# FACULTY RESPONSE
# ============================================================

class FacultyResponseIn(BaseModel):

    status: str

    comments: Optional[str] = None


@router.patch("/{request_id}/faculty-response")
def faculty_response(
    request_id: int,
    payload: FacultyResponseIn,
    current_faculty: dict = Depends(
        get_current_faculty
    ),
):

    db = SessionLocal()

    try:

        faculty_id = int(
            current_faculty["faculty_id"]
        )

        req = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.id
                == request_id
            )
            .first()
        )

        if not req:

            raise HTTPException(
                status_code=404,
                detail="Collaboration request not found.",
            )

        # This endpoint is only for internal faculty.
        if req.target_faculty_id != faculty_id:

            raise HTTPException(
                status_code=403,
                detail=(
                    "Only the target faculty may "
                    "respond to this request."
                ),
            )

        if (
            req.stage != "REQUESTED"
            or req.faculty_status != "PENDING"
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "This collaboration request "
                    "has already been processed."
                ),
            )

        status_value = (
            payload.status
            .strip()
            .lower()
        )

        if status_value not in (
            "approved",
            "rejected",
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "status must be "
                    "'approved' or 'rejected'."
                ),
            )

        req.faculty_comments = payload.comments
        req.faculty_responded_at = datetime.utcnow()

        if status_value == "approved":

            req.faculty_status = "APPROVED"
            req.stage = "ACCEPTED"

        else:

            req.faculty_status = "REJECTED"
            req.stage = "FACULTY_REJECTED"

        db.commit()
        db.refresh(req)

        requester = (
            db.query(Faculty)
            .filter(
                Faculty.id
                == req.requester_faculty_id
            )
            .first()
        )

        if status_value == "approved":

            _send_authority_review_email(
                db,
                req,
                requester,
            )

        return _serialize_detail(
            db,
            req,
            requester,
        )

    finally:
        db.close()


# ============================================================
# AUTHORITY RESPONSE
# ============================================================

class AuthorityResponseIn(BaseModel):

    status: str

    comments: Optional[str] = None


@router.patch("/{request_id}/authority-response")
def authority_response(
    request_id: int,
    payload: AuthorityResponseIn,
    x_authority_key: Optional[str] = Header(
        default=None
    ),
):

    if not AUTHORITY_API_KEY:

        raise HTTPException(
            status_code=501,
            detail=(
                "Authority API is not configured. "
                "Set AUTHORITY_API_KEY to enable "
                "this endpoint."
            ),
        )

    if x_authority_key != AUTHORITY_API_KEY:

        raise HTTPException(
            status_code=403,
            detail="Invalid authority credentials.",
        )

    db = SessionLocal()

    try:

        req = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.id
                == request_id
            )
            .first()
        )

        if not req:

            raise HTTPException(
                status_code=404,
                detail="Collaboration request not found.",
            )

        if req.stage != "ACCEPTED":

            raise HTTPException(
                status_code=409,
                detail=(
                    "This collaboration request "
                    "has already been processed."
                ),
            )

        status_value = (
            payload.status
            .strip()
            .lower()
        )

        if status_value not in (
            "approved",
            "rejected",
            "more_information",
        ):

            raise HTTPException(
                status_code=400,
                detail="Invalid status.",
            )

        req.authority_comments = payload.comments
        req.authority_responded_at = datetime.utcnow()

        requester = (
            db.query(Faculty)
            .filter(
                Faculty.id
                == req.requester_faculty_id
            )
            .first()
        )

        if status_value == "approved":

            req.authority_status = "APPROVED"
            req.stage = "ACTIVE"

            _activate_tracking(
                db,
                requester,
                req,
            )

        elif status_value == "rejected":

            req.authority_status = "REJECTED"
            req.stage = "AUTHORITY_REJECTED"

        else:

            req.authority_status = "MORE_INFORMATION"

        db.commit()
        db.refresh(req)

        return _serialize_detail(
            db,
            req,
            requester,
        )

    finally:
        db.close()


# ============================================================
# PUBLIC EMAIL TOKEN RESPONSE
# ============================================================

@router.get("/respond/{token}")
def respond_via_token(token: str):

    db = SessionLocal()

    try:

        token_hash = token_service.hash_token(
            token
        )

        record = (
            db.query(CollaborationResponseToken)
            .filter(
                CollaborationResponseToken.token_hash
                == token_hash
            )
            .first()
        )

        if not record:

            return {
                "result": "invalid",
                "message": (
                    "Invalid collaboration "
                    "response link."
                ),
            }

        if record.used_at is not None:

            return {
                "result": "used",
                "message": (
                    "This response link has "
                    "already been used."
                ),
            }

        if record.expires_at < datetime.utcnow():

            return {
                "result": "expired",
                "message": (
                    "This response link has "
                    "expired."
                ),
            }

        req = (
            db.query(CollaborationRequest)
            .filter(
                CollaborationRequest.id
                == record.request_id
            )
            .first()
        )

        if not req:

            return {
                "result": "invalid",
                "message": (
                    "Invalid collaboration "
                    "response link."
                ),
            }

        requester = (
            db.query(Faculty)
            .filter(
                Faculty.id
                == req.requester_faculty_id
            )
            .first()
        )

        # ----------------------------------------------------
        # FACULTY / EXTERNAL ACCEPT OR REJECT
        # ----------------------------------------------------

        if record.action in (
            "faculty_accept",
            "faculty_reject",
        ):

            valid_recipient = False

            # Internal faculty
            if req.target_faculty_id is not None:

                valid_recipient = (
                    record.recipient_faculty_id
                    == req.target_faculty_id
                )

            # External researcher
            elif (
                req.target_external_researcher_id
                is not None
            ):

                valid_recipient = (
                    record.recipient_external_researcher_id
                    == req.target_external_researcher_id
                )

            if not valid_recipient:

                return {
                    "result": "invalid",
                    "message": (
                        "Invalid collaboration "
                        "response link."
                    ),
                }

            if (
                req.stage != "REQUESTED"
                or req.faculty_status != "PENDING"
            ):

                return {
                    "result": "already_processed",
                    "message": (
                        "This collaboration request "
                        "has already been processed."
                    ),
                }

            req.faculty_responded_at = datetime.utcnow()

            if record.action == "faculty_accept":

                req.faculty_status = "APPROVED"
                req.stage = "ACCEPTED"

                message = (
                    "Invitation accepted. "
                    "Collaboration request status: "
                    "ACCEPTED."
                )

            else:

                req.faculty_status = "REJECTED"
                req.stage = "FACULTY_REJECTED"

                message = (
                    "Collaboration request rejected."
                )

            record.used_at = datetime.utcnow()

            db.commit()
            db.refresh(req)

            if record.action == "faculty_accept":

                _send_authority_review_email(
                    db,
                    req,
                    requester,
                )

            return {
                "result": "success",
                "message": message,
                "stage": req.stage,
            }

        # ----------------------------------------------------
        # AUTHORITY APPROVE / REJECT
        # ----------------------------------------------------

        if record.action in (
            "authority_approve",
            "authority_reject",
        ):

            if req.stage != "ACCEPTED":

                return {
                    "result": "already_processed",
                    "message": (
                        "This collaboration request "
                        "has already been processed."
                    ),
                }

            req.authority_responded_at = datetime.utcnow()

            if record.action == "authority_approve":

                req.authority_status = "APPROVED"
                req.stage = "ACTIVE"

                _activate_tracking(
                    db,
                    requester,
                    req,
                )

                message = (
                    "Collaboration request approved. "
                    "The collaboration is now active."
                )

            else:

                req.authority_status = "REJECTED"
                req.stage = "AUTHORITY_REJECTED"

                message = (
                    "Collaboration request rejected."
                )

            record.used_at = datetime.utcnow()

            db.commit()

            return {
                "result": "success",
                "message": message,
                "stage": req.stage,
            }

        return {
            "result": "invalid",
            "message": (
                "Invalid collaboration "
                "response link."
            ),
        }

    finally:
        db.close()