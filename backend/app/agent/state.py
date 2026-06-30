from typing import TypedDict
from uuid import UUID

from app.diagnoses.schemas import (
    Citation,
    Device,
    ErrorEvent,
    InitialDiagnosisResult,
    LogEvidence,
)


class DiagnosisGraphState(TypedDict, total=False):
    diagnosis_id: UUID
    error_event: ErrorEvent
    device: Device
    log_lines: list[str]
    log_evidence: list[LogEvidence]
    knowledge_citations: list[Citation]
    initial_diagnosis: InitialDiagnosisResult

