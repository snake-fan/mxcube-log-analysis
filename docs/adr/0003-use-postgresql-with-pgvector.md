# Use PostgreSQL with pgvector

The initial system uses PostgreSQL with pgvector for both operational records and simple retrieval over knowledge chunks. This keeps Error Events, Diagnoses, evidence, conversations, audit history, and vector-search metadata in one database while the RAG requirements are still small, avoiding a separate vector database until retrieval scale or ranking needs justify it.
