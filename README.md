# mxcube-log-analysis

A fault diagnosis Agent service for MXCuBE equipment operations. After a Device emits an Error Event, the system reads relevant Log Evidence, retrieves Knowledge Sources, and returns an Initial Diagnosis that supports Follow-up Questions.

## Stack

- Backend: FastAPI, Pydantic, LangGraph
- Frontend: React, Vite, TypeScript
- Storage target: PostgreSQL with pgvector

## Local Development

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Infrastructure:

```bash
cd infra
docker compose up --build
```

## First-phase Scope

- Error Event intake synchronously returns an Initial Diagnosis.
- Follow-up Questions reuse the existing Diagnosis context by default.
- Log collection and Knowledge Source retrieval are fixture-backed until real SSH and pgvector adapters are connected.
- Audit Events are intentionally deferred from the first phase.

See [CONTEXT.md](./CONTEXT.md) for domain language and [docs/adr](./docs/adr) for decisions.
