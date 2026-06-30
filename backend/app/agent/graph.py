from uuid import UUID

try:
    from langgraph.graph import END, StateGraph
except ImportError:  # pragma: no cover - exercised only when dependencies are missing.
    END = "__end__"
    StateGraph = None

from app.agent.state import DiagnosisGraphState
from app.devices.service import DeviceService
from app.diagnoses.schemas import (
    Citation,
    Confidence,
    Device,
    Diagnosis,
    ErrorEvent,
    FollowUpExchange,
    FollowUpQuestionCreate,
    InitialDiagnosisResult,
    LogEvidence,
    PossibleCause,
    Priority,
    RecommendedAction,
    SourceType,
)
from app.log_analysis.service import LogAnalysisService
from app.log_collection.service import LogCollectionService
from app.retrieval.service import RetrievalService


class DiagnosisAgent:
    def __init__(
        self,
        device_service: DeviceService,
        log_collection: LogCollectionService,
        log_analysis: LogAnalysisService,
        retrieval: RetrievalService,
    ) -> None:
        self._device_service = device_service
        self._log_collection = log_collection
        self._log_analysis = log_analysis
        self._retrieval = retrieval

    def run_initial_diagnosis(
        self,
        *,
        diagnosis_id: UUID,
        error_event: ErrorEvent,
    ) -> tuple[Device, list[LogEvidence], InitialDiagnosisResult]:
        initial_state: DiagnosisGraphState = {
            "diagnosis_id": diagnosis_id,
            "error_event": error_event,
        }
        final_state = self._invoke_graph(initial_state)
        return (
            final_state["device"],
            final_state["log_evidence"],
            final_state["initial_diagnosis"],
        )

    def answer_follow_up(
        self,
        diagnosis: Diagnosis,
        payload: FollowUpQuestionCreate,
    ) -> FollowUpExchange:
        log_terms = [term for evidence in diagnosis.log_evidence for term in evidence.matched_terms]
        citations = self._retrieval.retrieve(
            device_id=diagnosis.device.device_id,
            error_code=diagnosis.error_event.error_code,
            message=diagnosis.error_event.message,
            log_terms=log_terms,
            question=payload.question,
        )
        if not citations:
            citations = diagnosis.initial_diagnosis.citations[:2]

        answer = (
            "Based on the existing Diagnosis, review the Initial Diagnosis first, then compare "
            "the cited Log Evidence with the relevant Knowledge Sources. Fresh log collection is "
            "not performed unless the operator explicitly requests it."
        )
        return FollowUpExchange(question=payload.question, answer=answer, citations=citations)

    def _invoke_graph(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        if StateGraph is None:
            return self._run_linear(state)

        graph = StateGraph(DiagnosisGraphState)
        graph.add_node("load_device", self._load_device)
        graph.add_node("collect_logs", self._collect_logs)
        graph.add_node("extract_log_evidence", self._extract_log_evidence)
        graph.add_node("retrieve_knowledge", self._retrieve_knowledge)
        graph.add_node("reason", self._reason)
        graph.set_entry_point("load_device")
        graph.add_edge("load_device", "collect_logs")
        graph.add_edge("collect_logs", "extract_log_evidence")
        graph.add_edge("extract_log_evidence", "retrieve_knowledge")
        graph.add_edge("retrieve_knowledge", "reason")
        graph.add_edge("reason", END)
        return graph.compile().invoke(state)

    def _run_linear(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        for node in (
            self._load_device,
            self._collect_logs,
            self._extract_log_evidence,
            self._retrieve_knowledge,
            self._reason,
        ):
            state.update(node(state))
        return state

    def _load_device(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        event = state["error_event"]
        return {"device": self._device_service.get_device(event.device_id)}

    def _collect_logs(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        event = state["error_event"]
        return {
            "log_lines": self._log_collection.collect(
                event.device_id,
                event.occurred_at,
                event.log_window_minutes,
            )
        }

    def _extract_log_evidence(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        event = state["error_event"]
        return {
            "log_evidence": self._log_analysis.extract_evidence(
                state.get("log_lines", []),
                event.error_code,
            )
        }

    def _retrieve_knowledge(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        event = state["error_event"]
        device = state["device"]
        log_terms = [
            term
            for evidence in state.get("log_evidence", [])
            for term in evidence.matched_terms
        ]
        return {
            "knowledge_citations": self._retrieval.retrieve(
                device_id=device.device_id,
                error_code=event.error_code,
                message=event.message,
                log_terms=log_terms,
            )
        }

    def _reason(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        event = state["error_event"]
        device = state["device"]
        log_evidence = state.get("log_evidence", [])
        knowledge_citations = state.get("knowledge_citations", [])
        log_text = " ".join(evidence.excerpt.lower() for evidence in log_evidence)

        if "timeout" in log_text or "timeout" in event.message.lower():
            cause = "Controller communication timeout or delayed device readiness."
            action = (
                "Check whether the device is idle, then retry the operation once after "
                "confirming motion state."
            )
        elif "temperature" in log_text or "temperature" in event.message.lower():
            cause = "Temperature control drift or sensor reading outside the expected range."
            action = "Pause the experiment and verify the temperature controller before continuing."
        else:
            cause = "Equipment state mismatch around the reported Error Event."
            action = (
                "Review the cited Log Evidence and compare the device state with the current SOP."
            )

        citations = [
            Citation(
                source_type=SourceType.log,
                source_id=evidence.id,
                title=f"Log Evidence {evidence.id}",
                excerpt=evidence.excerpt,
            )
            for evidence in log_evidence
        ]
        citations.extend(knowledge_citations)

        result = InitialDiagnosisResult(
            summary=(
                f"{device.device_id} reported {event.error_code}; "
                f"the first diagnosis found {cause}"
            ),
            possible_causes=[
                PossibleCause(
                    cause=cause,
                    confidence=Confidence.medium if log_evidence else Confidence.low,
                    evidence_refs=[citation.source_id for citation in citations],
                    reasoning=(
                        "The conclusion is based on the Error Event message, matched Log Evidence, "
                        "and the highest-scoring Knowledge Sources."
                    ),
                )
            ],
            recommended_actions=[
                RecommendedAction(
                    action=action,
                    priority=Priority.high if "critical" in log_text else Priority.medium,
                    requires_shutdown=False,
                    risk_note=(
                        "Do not issue repeated movement commands until the current device state "
                        "is confirmed."
                    ),
                )
            ],
            citations=citations,
            safety_notes=[
                "Treat this result as an operator support recommendation, not an automatic "
                "control command."
            ],
        )
        return {"initial_diagnosis": result}
