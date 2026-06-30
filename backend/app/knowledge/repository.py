from app.diagnoses.schemas import SourceType
from app.knowledge.schemas import KnowledgeChunk


class FixtureKnowledgeRepository:
    def __init__(self) -> None:
        self._chunks = [
            KnowledgeChunk(
                id="fault-code-timeout-1",
                source_id="fault-code-general",
                source_type=SourceType.fault_code,
                title="Controller timeout handling",
                text=(
                    "Controller timeout faults are commonly caused by temporary communication "
                    "delay, a busy motion controller, or an axis that did not report ready state."
                ),
            ),
            KnowledgeChunk(
                id="sop-safe-retry-1",
                source_id="sop-safe-retry",
                source_type=SourceType.sop,
                title="Safe retry after equipment error",
                text=(
                    "Before retrying an operation, confirm the device is idle, check current "
                    "sample state, and avoid repeated commands while motion is in progress."
                ),
            ),
            KnowledgeChunk(
                id="manual-log-window-1",
                source_id="manual-mxcube-general-v1",
                source_type=SourceType.manual,
                title="General log review",
                text=(
                    "Use the event timestamp as the center of the log review window and compare "
                    "warnings immediately before the error with recovery messages after the error."
                ),
            ),
        ]

    def list_chunks(self) -> list[KnowledgeChunk]:
        return self._chunks

