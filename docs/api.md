# API Contract

The first phase keeps the request flow simple: an Error Event request synchronously returns a Diagnosis with an Initial Diagnosis result.

## Create Diagnosis from Error Event

`POST /api/error-events`

Request:

```json
{
  "external_event_id": "central-2026-0001",
  "device_id": "device-01",
  "error_code": "E_TIMEOUT",
  "message": "controller timeout",
  "occurred_at": "2026-06-30T08:30:00Z",
  "log_window_minutes": 10
}
```

Response:

```json
{
  "id": "diagnosis-id",
  "error_event": {},
  "device": {},
  "log_evidence": [],
  "initial_diagnosis": {
    "summary": "short result",
    "possible_causes": [],
    "recommended_actions": [],
    "citations": [],
    "safety_notes": []
  },
  "follow_up_questions": []
}
```

## Get Diagnosis

`GET /api/diagnoses/{diagnosis_id}`

Returns the stored Diagnosis including the Initial Diagnosis and any Follow-up Questions.

## Ask Follow-up Question

`POST /api/diagnoses/{diagnosis_id}/messages`

Request:

```json
{
  "question": "Why is timeout the likely cause?",
  "refresh_logs": false
}
```

Response:

```json
{
  "id": "message-id",
  "question": "Why is timeout the likely cause?",
  "answer": "assistant answer",
  "citations": [],
  "created_at": "2026-06-30T08:31:00Z"
}
```

