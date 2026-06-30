from uuid import UUID

from app.diagnoses.schemas import Diagnosis, FollowUpExchange, utc_now


class InMemoryDiagnosisRepository:
    def __init__(self) -> None:
        self._diagnoses: dict[UUID, Diagnosis] = {}

    def add(self, diagnosis: Diagnosis) -> Diagnosis:
        self._diagnoses[diagnosis.id] = diagnosis
        return diagnosis

    def get(self, diagnosis_id: UUID) -> Diagnosis | None:
        return self._diagnoses.get(diagnosis_id)

    def append_follow_up(self, diagnosis_id: UUID, exchange: FollowUpExchange) -> FollowUpExchange:
        diagnosis = self._diagnoses[diagnosis_id]
        diagnosis.follow_up_questions.append(exchange)
        diagnosis.updated_at = utc_now()
        return exchange

