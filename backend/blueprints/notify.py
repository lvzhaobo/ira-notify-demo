"""
Notify API：US-M4-001 规则 CRUD；其余端点仍为 stub。
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from flask import Blueprint, jsonify, request

from db import generate_uuid, get_db, now_iso

notify_bp = Blueprint("notify", __name__)


def _trace_id() -> str:
    return str(uuid.uuid4())


def _error_json(code: str, message: str, status: int):
    body = {
        "error": {"code": code, "message": message},
        "traceId": _trace_id(),
    }
    return jsonify(body), status


def _not_implemented(message: str):
    return _error_json("M4_NOT_IMPLEMENTED", message, 501)


def _parse_json_body() -> dict[str, Any] | None:
    if not request.data:
        return {}
    try:
        return request.get_json(silent=False)
    except Exception:
        return None


def _row_to_rule(row) -> dict[str, Any]:
    cond = json.loads(row["condition_json"] or "{}")
    ch = json.loads(row["channel_ids_json"] or "[]")
    return {
        "ruleId": row["rule_id"],
        "name": row["name"],
        "enabled": bool(row["enabled"]),
        "triggerType": row["trigger_type"],
        "scheduleCron": row["schedule_cron"],
        "condition": cond,
        "templateId": row["template_id"],
        "channelIds": ch,
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def _validate_channel_ids(db, channel_ids: list[str]) -> bool:
    if not isinstance(channel_ids, list) or not channel_ids:
        return False
    if not all(isinstance(x, str) and x for x in channel_ids):
        return False
    uniq = list(dict.fromkeys(channel_ids))
    placeholders = ",".join("?" * len(uniq))
    cur = db.execute(
        f"SELECT channel_id FROM notify_channel_configs WHERE channel_id IN ({placeholders}) AND enabled = 1",
        uniq,
    )
    found = {r["channel_id"] for r in cur.fetchall()}
    return len(found) == len(uniq)


@notify_bp.get("/notify/health")
def health():
    return jsonify({"status": "ok", "module": "M4"})


@notify_bp.get("/notify/rules")
def list_rules():
    db = get_db()
    try:
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return _error_json("M4_VALIDATION_ERROR", "limit 必须为整数", 400)
    limit = max(1, min(limit, 100))
    enabled_only = request.args.get("enabledOnly")
    if enabled_only is not None:
        enabled_only = enabled_only.lower() in ("1", "true", "yes")

    where = []
    params: list[Any] = []
    if enabled_only:
        where.append("enabled = 1")
    wh = (" WHERE " + " AND ".join(where)) if where else ""

    cur = db.execute(
        f"SELECT * FROM notify_rules{wh} ORDER BY created_at DESC LIMIT ?",
        (*params, limit + 1),
    )
    rows = cur.fetchall()
    has_more = len(rows) > limit
    if has_more:
        rows = rows[:limit]
    items = [_row_to_rule(r) for r in rows]
    next_cursor = items[-1]["ruleId"] if has_more and items else None
    return jsonify({"items": items, "nextCursor": next_cursor, "hasMore": has_more})


@notify_bp.post("/notify/rules")
def create_rule():
    body = _parse_json_body()
    if body is None:
        return _error_json("M4_VALIDATION_ERROR", "请求体须为 JSON", 400)

    name = body.get("name")
    if not isinstance(name, str) or not name.strip():
        return _error_json("M4_VALIDATION_ERROR", "name 必填且为非空字符串", 400)
    if "enabled" not in body or not isinstance(body["enabled"], bool):
        return _error_json("M4_VALIDATION_ERROR", "enabled 须为布尔值", 400)
    trigger_type = body.get("triggerType", "manual")
    if trigger_type not in ("manual", "schedule", "event"):
        return _error_json("M4_VALIDATION_ERROR", "triggerType 非法", 400)
    schedule_cron = body.get("scheduleCron")
    if schedule_cron is not None and not isinstance(schedule_cron, str):
        return _error_json("M4_VALIDATION_ERROR", "scheduleCron 须为字符串或 null", 400)
    condition = body.get("condition")
    if condition is None:
        condition = {}
    if not isinstance(condition, dict):
        return _error_json("M4_VALIDATION_ERROR", "condition 须为对象", 400)
    template_id = body.get("templateId")
    if template_id is not None and not isinstance(template_id, str):
        return _error_json("M4_VALIDATION_ERROR", "templateId 须为字符串或 null", 400)
    channel_ids = body.get("channelIds")
    if not isinstance(channel_ids, list):
        return _error_json("M4_VALIDATION_ERROR", "channelIds 须为字符串数组", 400)

    db = get_db()
    if not _validate_channel_ids(db, channel_ids):
        return _error_json(
            "M4_VALIDATION_ERROR",
            "channelIds 须引用已存在且已启用的渠道配置",
            400,
        )

    rule_id = generate_uuid()
    ts = now_iso()
    db.execute(
        """INSERT INTO notify_rules (
            rule_id, name, enabled, trigger_type, schedule_cron,
            condition_json, template_id, channel_ids_json, created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (
            rule_id,
            name.strip(),
            1 if body["enabled"] else 0,
            trigger_type,
            schedule_cron,
            json.dumps(condition, ensure_ascii=False),
            template_id,
            json.dumps(channel_ids, ensure_ascii=False),
            ts,
            ts,
        ),
    )
    db.commit()
    cur = db.execute("SELECT * FROM notify_rules WHERE rule_id = ?", (rule_id,))
    row = cur.fetchone()
    return jsonify({"rule": _row_to_rule(row)}), 201


@notify_bp.get("/notify/rules/<rule_id>")
def get_rule(rule_id: str):
    db = get_db()
    cur = db.execute("SELECT * FROM notify_rules WHERE rule_id = ?", (rule_id,))
    row = cur.fetchone()
    if row is None:
        return _error_json("M4_RULE_NOT_FOUND", "规则不存在", 404)
    return jsonify({"rule": _row_to_rule(row)})


@notify_bp.patch("/notify/rules/<rule_id>")
def update_rule(rule_id: str):
    body = _parse_json_body()
    if body is None:
        return _error_json("M4_VALIDATION_ERROR", "请求体须为 JSON", 400)

    db = get_db()
    cur = db.execute("SELECT * FROM notify_rules WHERE rule_id = ?", (rule_id,))
    row = cur.fetchone()
    if row is None:
        return _error_json("M4_RULE_NOT_FOUND", "规则不存在", 404)

    name = row["name"]
    enabled = bool(row["enabled"])
    trigger_type = row["trigger_type"]
    schedule_cron = row["schedule_cron"]
    condition = json.loads(row["condition_json"] or "{}")
    template_id = row["template_id"]
    channel_ids = json.loads(row["channel_ids_json"] or "[]")

    if "name" in body:
        if not isinstance(body["name"], str) or not body["name"].strip():
            return _error_json("M4_VALIDATION_ERROR", "name 非法", 400)
        name = body["name"].strip()
    if "enabled" in body:
        if not isinstance(body["enabled"], bool):
            return _error_json("M4_VALIDATION_ERROR", "enabled 须为布尔值", 400)
        enabled = body["enabled"]
    if "triggerType" in body:
        if body["triggerType"] not in ("manual", "schedule", "event"):
            return _error_json("M4_VALIDATION_ERROR", "triggerType 非法", 400)
        trigger_type = body["triggerType"]
    if "scheduleCron" in body:
        sc = body["scheduleCron"]
        if sc is not None and not isinstance(sc, str):
            return _error_json("M4_VALIDATION_ERROR", "scheduleCron 非法", 400)
        schedule_cron = sc
    if "condition" in body:
        if not isinstance(body["condition"], dict):
            return _error_json("M4_VALIDATION_ERROR", "condition 须为对象", 400)
        condition = body["condition"]
    if "templateId" in body:
        tid = body["templateId"]
        if tid is not None and not isinstance(tid, str):
            return _error_json("M4_VALIDATION_ERROR", "templateId 非法", 400)
        template_id = tid
    if "channelIds" in body:
        ch = body["channelIds"]
        if not isinstance(ch, list):
            return _error_json("M4_VALIDATION_ERROR", "channelIds 须为字符串数组", 400)
        if not _validate_channel_ids(db, ch):
            return _error_json(
                "M4_VALIDATION_ERROR",
                "channelIds 须引用已存在且已启用的渠道配置",
                400,
            )
        channel_ids = ch

    ts = now_iso()
    db.execute(
        """UPDATE notify_rules SET
            name=?, enabled=?, trigger_type=?, schedule_cron=?,
            condition_json=?, template_id=?, channel_ids_json=?, updated_at=?
        WHERE rule_id=?""",
        (
            name,
            1 if enabled else 0,
            trigger_type,
            schedule_cron,
            json.dumps(condition, ensure_ascii=False),
            template_id,
            json.dumps(channel_ids, ensure_ascii=False),
            ts,
            rule_id,
        ),
    )
    db.commit()
    cur = db.execute("SELECT * FROM notify_rules WHERE rule_id = ?", (rule_id,))
    return jsonify({"rule": _row_to_rule(cur.fetchone())})


@notify_bp.delete("/notify/rules/<rule_id>")
def delete_rule(rule_id: str):
    db = get_db()
    cur = db.execute("DELETE FROM notify_rules WHERE rule_id = ?", (rule_id,))
    db.commit()
    if cur.rowcount == 0:
        return _error_json("M4_RULE_NOT_FOUND", "规则不存在", 404)
    return "", 204


@notify_bp.post("/notify/dispatch")
def dispatch():
    return _not_implemented("实现 US-M4-002：POST /notify/dispatch（注意 dryRun 默认）")


@notify_bp.get("/notify/deliveries")
def list_deliveries():
    return _not_implemented("实现 US-M4-002：GET /notify/deliveries")


@notify_bp.post("/notify/channels/<string:ch_type>/test")
def test_channel(ch_type: str):
    return _not_implemented(f"实现 US-M4-003：POST /notify/channels/{ch_type}/test")
