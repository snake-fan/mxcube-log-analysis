# Knowledge Ingestion

The first phase treats manuals, SOPs, FAQs, historical cases, and fault-code references as Knowledge Sources.

## Source Types

- `manual`
- `sop`
- `faq`
- `case`
- `fault_code`

## Versioning

Manual updates are append-only. A new upload creates a new Manual Version associated with the same Device instead of replacing the old file. Historical Diagnoses can therefore keep citing the material that existed when the Initial Diagnosis was produced.

## Initial Storage Shape

Use two tables when persistence is added:

```text
knowledge_sources
knowledge_chunks
```

Each chunk should keep source metadata, text, embedding, and enough location data to render a useful citation in the frontend.

