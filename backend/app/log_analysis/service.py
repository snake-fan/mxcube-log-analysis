import re

from app.diagnoses.schemas import LogEvidence


class LogAnalysisService:
    _keywords = ("error", "exception", "fail", "failed", "timeout", "warning", "critical")
    _redactions = (
        (re.compile(r"(?i)(password|token|secret)=\S+"), r"\1=<redacted>"),
        (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "<ip>"),
    )

    def extract_evidence(
        self,
        lines: list[str],
        error_code: str,
        max_items: int = 5,
    ) -> list[LogEvidence]:
        matched: list[LogEvidence] = []
        terms = [error_code.lower(), *self._keywords]

        for line in lines:
            normalized = line.lower()
            matched_terms = [term for term in terms if term and term in normalized]
            if not matched_terms:
                continue

            matched.append(
                LogEvidence(
                    id=f"log-{len(matched) + 1}",
                    excerpt=self._truncate(self._redact(line)),
                    matched_terms=matched_terms,
                )
            )
            if len(matched) >= max_items:
                break

        if matched:
            return matched

        return [
            LogEvidence(id=f"log-{index + 1}", excerpt=self._truncate(self._redact(line)))
            for index, line in enumerate(lines[-3:])
        ]

    def _redact(self, text: str) -> str:
        redacted = text
        for pattern, replacement in self._redactions:
            redacted = pattern.sub(replacement, redacted)
        return redacted

    def _truncate(self, text: str, limit: int = 500) -> str:
        if len(text) <= limit:
            return text
        return f"{text[:limit]}..."

