from fastapi import APIRouter

from app.api.routes import diagnoses, error_events

api_router = APIRouter()
api_router.include_router(error_events.router, tags=["error-events"])
api_router.include_router(diagnoses.router, tags=["diagnoses"])

