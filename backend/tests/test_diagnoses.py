from fastapi.testclient import TestClient

from app.main import create_app


def test_error_event_returns_initial_diagnosis() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/error-events",
        json={
            "device_id": "device-01",
            "error_code": "E_TIMEOUT",
            "message": "controller timeout",
            "log_window_minutes": 5,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["error_event"]["device_id"] == "device-01"
    assert payload["initial_diagnosis"]["possible_causes"]
    assert payload["initial_diagnosis"]["citations"]


def test_follow_up_question_uses_same_diagnosis() -> None:
    client = TestClient(create_app())
    diagnosis = client.post(
        "/api/error-events",
        json={
            "device_id": "device-01",
            "error_code": "E_TIMEOUT",
            "message": "controller timeout",
        },
    ).json()

    response = client.post(
        f"/api/diagnoses/{diagnosis['id']}/messages",
        json={"question": "Why is this timeout likely?"},
    )

    assert response.status_code == 200
    assert response.json()["question"] == "Why is this timeout likely?"
