from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from adapters import source_adapter
from database.connection import SessionLocal
from models.models import Faculty, Publication, Project, Collaboration, FacultyResearchDocument
from routes.auth import get_current_faculty
from services import document_extraction, document_storage

router = APIRouter()


@router.get("/api/faculty")
def get_faculty():
    """Return the list of faculty members and their basic research profile."""
    return {"faculty": source_adapter.get_faculty()}


# ============================================================
# GET CURRENT FACULTY (spec section 4)
# ============================================================

def _get_faculty_or_404(db, faculty_id: int) -> Faculty:
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()

    if not faculty:
        raise HTTPException(
            status_code=404,
            detail="Faculty profile not found."
        )

    return faculty


@router.get("/api/faculty/me")
def get_my_faculty_profile(
    current_faculty: dict = Depends(get_current_faculty)
):
    """
    The logged-in faculty's full profile. Identity comes ONLY from the
    JWT (get_current_faculty) - never from a query/body parameter.
    """
    db = SessionLocal()

    try:
        faculty_id = int(current_faculty["faculty_id"])

        faculty = _get_faculty_or_404(db, faculty_id)

        publications = (
            db.query(Publication)
            .filter(Publication.faculty_name == faculty.name)
            .all()
        )

        projects = (
            db.query(Project)
            .filter(Project.faculty_name == faculty.name)
            .all()
        )

        collaborations = (
            db.query(Collaboration)
            .filter(
                (Collaboration.faculty_a == faculty.name)
                | (Collaboration.faculty_b == faculty.name)
            )
            .all()
        )

        return {
            "faculty_id": str(faculty.id),
            "name": faculty.name,
            "email": faculty.email,
            "department": faculty.department,
            "designation": faculty.designation,
            "research_interests": faculty.research_areas or [],
            "expertise": faculty.research_areas or [],

            "publications": [
                {
                    "id": p.id,
                    "title": p.title,
                    "year": p.year,
                    "venue": p.venue,
                    "doi": p.doi
                }
                for p in publications
            ],

            "projects": [
                {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "research_area": p.research_area,
                    "status": p.status,
                }
                for p in projects
            ],

            "collaborations": [
                {
                    "id": c.id,
                    "with": (
                        c.faculty_b
                        if c.faculty_a == faculty.name
                        else c.faculty_a
                    ),
                    "department": c.department,
                    "research_areas": c.research_areas or [],
                    "collaboration_type": c.collaboration_type,
                    "collaboration_strength": c.collaboration_strength,
                }
                for c in collaborations
            ],

            "publications_count": faculty.publications_count or 0,
            "collaboration_count": faculty.collaboration_count or 0,
        }

    finally:
        db.close()


# ============================================================
# FACULTY RESEARCH DOCUMENTS
# (spec sections 6-9, 46)
# ============================================================

class ResearchDocumentOut(BaseModel):
    id: int
    title: str
    file_name: str
    file_type: str
    keywords: list[str]
    extraction_status: str
    uploaded_at: Optional[datetime]


def _document_to_out(doc: FacultyResearchDocument) -> dict:
    return {
        "id": doc.id,
        "title": doc.title,
        "file_name": doc.file_name,
        "file_type": doc.file_type,
        "keywords": doc.keywords or [],
        "extraction_status": doc.extraction_status,
        "uploaded_at": (
            doc.uploaded_at.isoformat()
            if doc.uploaded_at
            else None
        ),
    }


@router.get("/api/faculty/research-documents")
def list_my_research_documents(
    current_faculty: dict = Depends(get_current_faculty)
):
    """A faculty member's own uploaded research documents only."""

    db = SessionLocal()

    try:
        faculty_id = int(current_faculty["faculty_id"])

        docs = (
            db.query(FacultyResearchDocument)
            .filter(FacultyResearchDocument.faculty_id == faculty_id)
            .order_by(FacultyResearchDocument.uploaded_at.desc())
            .all()
        )

        return {
            "documents": [
                _document_to_out(d)
                for d in docs
            ]
        }

    finally:
        db.close()


@router.post("/api/faculty/research-documents")
async def upload_research_document(
    title: str = Form(...),
    keywords: str = Form(""),  # comma-separated
    file: UploadFile = File(...),
    current_faculty: dict = Depends(get_current_faculty),
):
    faculty_id = int(current_faculty["faculty_id"])

    content = await file.read()

    try:
        file_type = document_storage.validate_upload(
            file.filename,
            file.content_type,
            len(content)
        )

    except document_storage.UploadValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    db = SessionLocal()

    try:
        # Ensures the JWT faculty_id maps to a real Faculty row
        _get_faculty_or_404(db, faculty_id)

        file_reference = document_storage.save_file(
            faculty_id,
            file.filename,
            content
        )

        extracted_text, extraction_status = (
            document_extraction.extract_text(
                file_reference,
                file_type
            )
        )

        keyword_list = [
            k.strip()
            for k in keywords.split(",")
            if k.strip()
        ]

        document = FacultyResearchDocument(
            faculty_id=faculty_id,
            title=title,
            keywords=keyword_list,
            file_name=file.filename,
            file_type=file_type,
            file_reference=file_reference,
            extracted_text=extracted_text,
            extraction_status=extraction_status,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return _document_to_out(document)

    finally:
        db.close()


@router.delete("/api/faculty/research-documents/{document_id}")
def delete_research_document(
    document_id: int,
    current_faculty: dict = Depends(get_current_faculty)
):
    faculty_id = int(current_faculty["faculty_id"])

    db = SessionLocal()

    try:
        document = (
            db.query(FacultyResearchDocument)
            .filter(
                FacultyResearchDocument.id == document_id
            )
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        # Ownership enforced on the backend, not just hidden in the UI
        # (spec section 9/34).
        if document.faculty_id != faculty_id:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own documents."
            )

        document_storage.delete_file(
            document.file_reference
        )

        db.delete(document)
        db.commit()

        return {
            "deleted": True,
            "id": document_id
        }

    finally:
        db.close()