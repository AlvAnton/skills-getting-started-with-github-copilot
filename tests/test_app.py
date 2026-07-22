from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Mergington High School" in response.text


def test_get_activities_returns_activity_list():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_for_activity_adds_participant():
    email = "teststudent@mergington.edu"
    response = client.post("/activities/Basketball Team/signup", params={"email": email})
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_unregister_from_activity_removes_participant():
    email = "teststudent@mergington.edu"
    client.post("/activities/Basketball Team/signup", params={"email": email})
    response = client.post("/activities/Basketball Team/unregister", params={"email": email})
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
