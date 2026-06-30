# Project Structure

```text
/
|-- backend/      # FastAPI, LangGraph, diagnosis services
|-- frontend/     # React/Vite diagnosis workbench
|-- infra/        # Docker Compose and PostgreSQL initialization
|-- docs/         # API, ingestion notes, ADRs, agent docs
|-- scripts/      # Maintenance scripts
|-- CONTEXT.md    # Domain glossary
`-- README.md
```

## Backend Boundaries

```text
backend/app/
|-- api/             # FastAPI routes and dependencies
|-- core/            # Settings and shared configuration
|-- diagnoses/       # Diagnosis lifecycle and schemas
|-- devices/         # Device lookup
|-- log_collection/  # Read-only log readers
|-- log_analysis/    # Evidence extraction and redaction
|-- knowledge/       # Knowledge Source repositories
|-- retrieval/       # Simple retrieval over Knowledge Sources
|-- agent/           # LangGraph orchestration
`-- storage/         # Database adapters
```

The current backend uses in-memory persistence and fixture log/knowledge readers so the application can run locally before SSH, database migrations, and embeddings are connected.

