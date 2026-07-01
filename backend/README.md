# MXCuBE Fault Diagnosis Backend

FastAPI and LangGraph service for Error Event intake, Initial Diagnosis generation, and Follow-up Questions.

## Development

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
```

## Checks

```bash
uv run pytest
uv run ruff check app tests
```
