from pydantic import BaseModel

from app.diagnoses.schemas import SourceType


class KnowledgeChunk(BaseModel):
    id: str
    source_id: str
    source_type: SourceType
    title: str
    text: str
    device_id: str | None = None

