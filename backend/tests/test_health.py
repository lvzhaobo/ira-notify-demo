import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health_ok(client):
    r = client.get("/api/v1/notify/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("status") == "ok"


def test_rules_stub(client):
    r = client.get("/api/v1/notify/rules")
    assert r.status_code == 501
    data = r.get_json()
    assert data["error"]["code"] == "M4_NOT_IMPLEMENTED"
    assert "traceId" in data
