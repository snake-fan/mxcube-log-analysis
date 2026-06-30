from uuid import UUID, uuid4

from app.agent.graph import DiagnosisAgent
from app.diagnoses.repository import InMemoryDiagnosisRepository
from app.diagnoses.schemas import (
    Diagnosis,
    ErrorEvent,
    ErrorEventCreate,
    FollowUpExchange,
    FollowUpQuestionCreate,
)


class DiagnosisService:
    def __init__(self, repository: InMemoryDiagnosisRepository, agent: DiagnosisAgent) -> None:
        self._repository = repository
        self._agent = agent

    def create_from_error_event(self, payload: ErrorEventCreate) -> Diagnosis:
        error_event = ErrorEvent(**payload.model_dump())
        diagnosis_id = uuid4()
        device, log_evidence, initial_diagnosis = self._agent.run_initial_diagnosis(
            diagnosis_id=diagnosis_id,
            error_event=error_event,
        )
        diagnosis = Diagnosis(
            id=diagnosis_id,
            error_event=error_event,
            device=device,
            log_evidence=log_evidence,
            initial_diagnosis=initial_diagnosis,
        )
        return self._repository.add(diagnosis)

    def get_diagnosis(self, diagnosis_id: UUID) -> Diagnosis | None:
        return self._repository.get(diagnosis_id)

    def answer_follow_up(
        self,
        diagnosis_id: UUID,
        payload: FollowUpQuestionCreate,
    ) -> FollowUpExchange:
        diagnosis = self._repository.get(diagnosis_id)
        if diagnosis is None:
            raise KeyError(diagnosis_id)

        exchange = self._agent.answer_follow_up(diagnosis, payload)
        return self._repository.append_follow_up(diagnosis_id, exchange)
