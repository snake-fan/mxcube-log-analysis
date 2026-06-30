from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(UTC)


class Confidence(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Priority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class SourceType(StrEnum):
    manual = "manual"
    sop = "sop"
    faq = "faq"
    case = "case"
    fault_code = "fault_code"
    log = "log"


class ErrorEventCreate(BaseModel):
    external_event_id: str | None = None
    device_id: str = Field(min_length=1)
    error_code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    occurred_at: datetime = Field(default_factory=utc_now)
    log_window_minutes: int = Field(default=10, ge=1, le=120)


class ErrorEvent(ErrorEventCreate):
    id: UUID = Field(default_factory=uuid4)
    received_at: datetime = Field(default_factory=utc_now)


class Device(BaseModel):
    device_id: str
    display_name: str | None = None


class LogEvidence(BaseModel):
    id: str
    excerpt: str
    matched_terms: list[str] = Field(default_factory=list)
    source_path: str | None = None


class Citation(BaseModel):
    source_type: SourceType
    source_id: str
    title: str
    excerpt: str


class PossibleCause(BaseModel):
    cause: str
    confidence: Confidence
    evidence_refs: list[str] = Field(default_factory=list)
    reasoning: str


class RecommendedAction(BaseModel):
    action: str
    priority: Priority
    requires_shutdown: bool = False
    risk_note: str | None = None


class InitialDiagnosisResult(BaseModel):
    summary: str
    possible_causes: list[PossibleCause]
    recommended_actions: list[RecommendedAction]
    citations: list[Citation]
    safety_notes: list[str] = Field(default_factory=list)


class FollowUpQuestionCreate(BaseModel):
    question: str = Field(min_length=1)
    refresh_logs: bool = False
    log_window_minutes: int | None = Field(default=None, ge=1, le=120)


class FollowUpExchange(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    question: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class Diagnosis(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    error_event: ErrorEvent
    device: Device
    log_evidence: list[LogEvidence]
    initial_diagnosis: InitialDiagnosisResult
    follow_up_questions: list[FollowUpExchange] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
