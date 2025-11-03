from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_dict():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # spot-check a known activity from the seeded data
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # Ensure clean start: remove if already present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants
