def test_health_ok(client):
    r = client.get("/api/v1/notify/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("status") == "ok"
    assert data.get("module") == "M4"
