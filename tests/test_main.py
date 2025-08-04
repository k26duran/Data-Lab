from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 404
    
def test_upload_departments():
    with open("data/departments.csv", "rb") as f:
        response = client.post("/upload/departments", files={"file": f})
        assert response.status_code == 200

def test_hired_by_quarter():
    response = client.get("/metrics/hired-by-quarter")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_hired_above_mean():
    response = client.get("/metrics/above-average-hires")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
