import os
import tempfile

from fastapi.testclient import TestClient


temp_dir = tempfile.TemporaryDirectory()
os.environ["DATA_FILE"] = os.path.join(temp_dir.name, "users.json")

from main import app
from store import save_users


client = TestClient(app)
ADMIN_HEADERS = {"X-User-Id": "1", "X-User-Name": "Nakul"}


def setup_function():
    save_users([
        {"id": 1, "name": "Nakul", "age": 21},
        {"id": 2, "name": "John", "age": 25},
    ])


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_authentication():
    response = client.post("/api/authenticate", headers=ADMIN_HEADERS)
    assert response.status_code == 200
    assert response.json()["user"]["permissions"] == ["read", "write"]


def test_crud_lifecycle():
    created = client.post(
        "/api/users",
        headers=ADMIN_HEADERS,
        json={"name": "Priya", "age": 24},
    )
    assert created.status_code == 201
    assert created.json() == {"id": 3, "name": "Priya", "age": 24}

    updated = client.patch(
        "/api/users/3",
        headers=ADMIN_HEADERS,
        json={"age": 25},
    )
    assert updated.status_code == 200
    assert updated.json()["age"] == 25

    deleted = client.delete("/api/users/3", headers=ADMIN_HEADERS)
    assert deleted.status_code == 200
    assert deleted.json()["user"]["name"] == "Priya"


def test_missing_authentication_and_user():
    assert client.get("/api/users").status_code == 422
    missing = client.get("/api/users/999", headers=ADMIN_HEADERS)
    assert missing.status_code == 404
