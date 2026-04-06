"""US-M4-001：规则 CRUD 与 channelIds 校验。"""

import json

VALID_CHANNEL = "550e8400-e29b-41d4-a716-446655440000"


def _rule_body(**overrides):
    base = {
        "name": "测试规则",
        "enabled": True,
        "triggerType": "manual",
        "scheduleCron": None,
        "condition": {"keywords": ["k"]},
        "templateId": None,
        "channelIds": [VALID_CHANNEL],
    }
    base.update(overrides)
    return base


def test_create_list_get_patch_delete(client):
    # create
    r = client.post(
        "/api/v1/notify/rules",
        data=json.dumps(_rule_body(name="早间摘要")),
        content_type="application/json",
    )
    assert r.status_code == 201
    rule = r.get_json()["rule"]
    rid = rule["ruleId"]
    assert rule["name"] == "早间摘要"
    assert rule["channelIds"] == [VALID_CHANNEL]

    # list
    r = client.get("/api/v1/notify/rules")
    assert r.status_code == 200
    body = r.get_json()
    assert "items" in body
    assert any(x["ruleId"] == rid for x in body["items"])

    # get one
    r = client.get(f"/api/v1/notify/rules/{rid}")
    assert r.status_code == 200
    assert r.get_json()["rule"]["ruleId"] == rid

    # patch
    r = client.patch(
        f"/api/v1/notify/rules/{rid}",
        data=json.dumps({"enabled": False, "name": "改名"}),
        content_type="application/json",
    )
    assert r.status_code == 200
    assert r.get_json()["rule"]["enabled"] is False
    assert r.get_json()["rule"]["name"] == "改名"

    # delete
    r = client.delete(f"/api/v1/notify/rules/{rid}")
    assert r.status_code == 204

    r = client.get(f"/api/v1/notify/rules/{rid}")
    assert r.status_code == 404
    assert r.get_json()["error"]["code"] == "M4_RULE_NOT_FOUND"


def test_create_invalid_channel_returns_400(client):
    r = client.post(
        "/api/v1/notify/rules",
        data=json.dumps(_rule_body(channelIds=["00000000-0000-0000-0000-000000000099"])),
        content_type="application/json",
    )
    assert r.status_code == 400
    assert r.get_json()["error"]["code"] == "M4_VALIDATION_ERROR"


def test_get_not_found(client):
    r = client.get("/api/v1/notify/rules/00000000-0000-0000-0000-000000000099")
    assert r.status_code == 404
    assert r.get_json()["error"]["code"] == "M4_RULE_NOT_FOUND"


def test_other_endpoints_still_501(client):
    r = client.post("/api/v1/notify/dispatch", json={})
    assert r.status_code == 501
