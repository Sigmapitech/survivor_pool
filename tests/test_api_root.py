from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_unknown_endpoint():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
