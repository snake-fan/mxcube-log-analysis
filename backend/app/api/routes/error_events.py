from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_diagnosis_service
from app.diagnoses.schemas import Diagnosis, ErrorEventCreate
from app.diagnoses.service import DiagnosisService

router = APIRouter()
DiagnosisServiceDep = Annotated[DiagnosisService, Depends(get_diagnosis_service)]


@router.post("/error-events", response_model=Diagnosis)
async def create_diagnosis_from_error_event(
    payload: ErrorEventCreate,
    service: DiagnosisServiceDep,
) -> Diagnosis:
    return service.create_from_error_event(payload)
