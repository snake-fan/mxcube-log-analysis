from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_diagnosis_service
from app.diagnoses.schemas import Diagnosis, FollowUpExchange, FollowUpQuestionCreate
from app.diagnoses.service import DiagnosisService

router = APIRouter()
DiagnosisServiceDep = Annotated[DiagnosisService, Depends(get_diagnosis_service)]


@router.get("/diagnoses/{diagnosis_id}", response_model=Diagnosis)
async def get_diagnosis(
    diagnosis_id: UUID,
    service: DiagnosisServiceDep,
) -> Diagnosis:
    diagnosis = service.get_diagnosis(diagnosis_id)
    if diagnosis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")
    return diagnosis


@router.post("/diagnoses/{diagnosis_id}/messages", response_model=FollowUpExchange)
async def create_follow_up_question(
    diagnosis_id: UUID,
    payload: FollowUpQuestionCreate,
    service: DiagnosisServiceDep,
) -> FollowUpExchange:
    try:
        return service.answer_follow_up(diagnosis_id, payload)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis not found",
        ) from exc
