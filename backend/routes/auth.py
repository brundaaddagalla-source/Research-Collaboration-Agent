"""
Faculty auth routes.

Two endpoints backing the Faculty Login page:
  POST /api/auth/faculty/grid  - faculty enters their Faculty ID, gets
                                  back two random grid cell positions
                                  to fill in.
  POST /api/auth/faculty/login - faculty submits Faculty ID + password
                                  + the two grid values, gets back a
                                  signed JWT on success.

This module is additive: registering `router` in main.py does not
change any existing endpoint's behavior, and no existing route
currently requires the token this issues. `get_current_faculty` below
is provided as a ready-to-use dependency for protecting routes later,
e.g.:

    from routes.auth import get_current_faculty

    @router.get("/api/something")
    def something(current_faculty=Depends(get_current_faculty)):
        ...
"""

from typing import Dict, Tuple

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from database.connection import SessionLocal
from models.models import FacultyCredential
from services.auth_service import (
    create_access_token,
    decode_access_token,
    pick_random_grid_positions,
    verify_password,
)

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


class GridRequest(BaseModel):
    faculty_id: str


class GridResponse(BaseModel):
    grid_positions: list[str]


class LoginRequest(BaseModel):
    faculty_id: str
    password: str
    grid_values: list[str]


class FacultyOut(BaseModel):
    faculty_id: str
    name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    faculty: FacultyOut


# Tracks which two positions were most recently issued per faculty_id,
# so /login can verify against the SAME challenge /grid handed out.
# In-memory and per-process - fine for local/dev use with a single
# backend instance; swap for a DB/Redis-backed store before running
# multiple backend workers or instances in production.
_issued_grid_positions: Dict[str, Tuple[str, str]] = {}


@router.post("/api/auth/faculty/grid", response_model=GridResponse, tags=["Faculty Auth"])
def request_grid(payload: GridRequest):
    """Step 1: look up the Faculty ID and issue two random grid positions."""
    db = SessionLocal()
    try:
        faculty_id = payload.faculty_id.strip()
        credential = (
            db.query(FacultyCredential)
            .filter(FacultyCredential.faculty_id == faculty_id)
            .first()
        )
        if not credential:
            raise HTTPException(status_code=404, detail="Unknown Faculty ID.")

        first, second = pick_random_grid_positions()
        _issued_grid_positions[credential.faculty_id] = (first, second)

        return {"grid_positions": [first, second]}
    finally:
        db.close()


@router.post("/api/auth/faculty/login", response_model=LoginResponse, tags=["Faculty Auth"])
def login(payload: LoginRequest):
    """Step 2: verify password + the two grid values, issue a JWT."""
    db = SessionLocal()
    try:
        faculty_id = payload.faculty_id.strip()
        credential = (
            db.query(FacultyCredential)
            .filter(FacultyCredential.faculty_id == faculty_id)
            .first()
        )

        invalid_credentials = HTTPException(status_code=401, detail="Invalid credentials.")

        if not credential:
            raise invalid_credentials

        if not verify_password(payload.password, credential.password_hash):
            raise invalid_credentials

        issued = _issued_grid_positions.get(faculty_id)
        if not issued:
            raise HTTPException(
                status_code=400,
                detail="Grid positions were not requested for this Faculty ID. Please start over.",
            )

        position_1, position_2 = issued
        expected_1 = credential.grid_secret.get(position_1)
        expected_2 = credential.grid_secret.get(position_2)

        submitted = payload.grid_values
        if (
            len(submitted) != 2
            or submitted[0].strip() != expected_1
            or submitted[1].strip() != expected_2
        ):
            raise invalid_credentials

        # One-time challenge - don't let the same positions be replayed.
        _issued_grid_positions.pop(faculty_id, None)

        token = create_access_token(credential.faculty_id, credential.name)

        return {
            "access_token": token,
            "token_type": "bearer",
            "faculty": {"faculty_id": credential.faculty_id, "name": credential.name},
        }
    finally:
        db.close()


def get_current_faculty(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Reusable dependency for protecting a route with the JWT issued above."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"faculty_id": payload["sub"], "name": payload.get("name")}