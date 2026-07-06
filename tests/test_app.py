import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_state():
    original_participants = {
        name: list(details["participants"])
        for name, details in activities.items()
    }
    yield
    for name, details in activities.items():
        details["participants"] = list(original_participants[name])


client = TestClient(app)


def test_unregister_participant_removes_from_activity():
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants/{participant_email}"
    )

    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_when_missing():
    response = client.delete(
        "/activities/Chess Club/participants/does-not-exist@example.com"
    )

    assert response.status_code == 404
