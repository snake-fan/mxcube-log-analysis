import re

from app.diagnoses.schemas import Citation
from app.knowledge.repository import FixtureKnowledgeRepository


class RetrievalService:
    def __init__(self, repository: FixtureKnowledgeRepository) -> None:
        self._repository = repository

    def retrieve(
        self,
        *,
        device_id: str,
        error_code: str,
        message: str,
        log_terms: list[str],
        question: str | None = None,
        limit: int = 4,
    ) -> list[Citation]:
        query_text = " ".join([device_id, error_code, message, *log_terms, question or ""])
        query_terms = self._terms(query_text)
        scored = []
        for chunk in self._repository.list_chunks():
            haystack = self._terms(" ".join([chunk.title, chunk.text, chunk.device_id or ""]))
            score = len(query_terms & haystack)
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            Citation(
                source_type=chunk.source_type,
                source_id=chunk.source_id,
                title=chunk.title,
                excerpt=chunk.text,
            )
            for _, chunk in scored[:limit]
        ]

    def _terms(self, text: str) -> set[str]:
        return {term.lower() for term in re.findall(r"[a-zA-Z0-9_]+", text) if len(term) > 2}
