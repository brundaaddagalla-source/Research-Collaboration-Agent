"""
Agent 24 - Research Collaboration Agent
Phase 1: Backend foundation (mock data only, no AI logic).

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from routes import (
    dashboard,
    faculty,
    expertise,
    collaborations,
    opportunities,
    researchers,
    funding,
    mous,
    tracking,
)
from database.connection import engine, Base
from models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agent 24 - Research Collaboration Agent API",
    description="Phase 1 foundation API. Serves mock data only - no AI/recommendation logic yet.",
    version="0.1.0",
)

# Allow the local Vite dev server (and common alternates) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route modules. Each module owns one feature area.
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(faculty.router, tags=["Faculty"])
app.include_router(expertise.router, tags=["Expertise Map"])
app.include_router(collaborations.router, tags=["Collaboration Network"])
app.include_router(opportunities.router, tags=["Internal Opportunities"])
app.include_router(researchers.router, tags=["External Researchers"])
app.include_router(funding.router, tags=["Funding & Consortiums"])
app.include_router(mous.router, tags=["MoU Intelligence"])
app.include_router(tracking.router, tags=["Collaboration Tracking"])


@app.get("/")
def root():
    return {
        "service": "Agent 24 - Research Collaboration Agent",
        "phase": "Phase 1 - frontend/backend foundation with mock data",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "result": result.scalar(),
        }