from fastapi.testclient import TestClient
from delicious_scanner.app import app
def test_health()->None:
    r=TestClient(app).get("/health");assert r.status_code==200;assert r.json()["status"]=="healthy"
def test_api_health()->None:
    r=TestClient(app).get("/api/health");assert r.status_code==200;assert r.json()["service"]=="delicious-scanner"
