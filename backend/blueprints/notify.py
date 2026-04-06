"""
Notify API：除 health 外均为工作坊 stub（501 + 统一错误体）。
实现时请替换各视图函数，并对照 spec/09。
"""
from __future__ import annotations

import uuid

from flask import Blueprint, jsonify

notify_bp = Blueprint("notify", __name__)


def _trace_id() -> str:
    return str(uuid.uuid4())


def _not_implemented(message: str):
    tid = _trace_id()
    body = {
        "error": {
            "code": "M4_NOT_IMPLEMENTED",
            "message": message,
        },
        "traceId": tid,
    }
    return jsonify(body), 501


@notify_bp.get("/notify/health")
def health():
    """工作坊：唯一须保持可用的端点（用于 CI / 前端探测）。"""
    return jsonify(
        {
            "status": "ok",
            "module": "ira-notify",
            "hint": "业务路由仍为 stub，请按 spec/09 实现",
        }
    )


@notify_bp.post("/notify/rules")
def create_rule():
    return _not_implemented("实现 US-M4-001：POST /notify/rules")


@notify_bp.get("/notify/rules")
def list_rules():
    return _not_implemented("实现 US-M4-001：GET /notify/rules")


@notify_bp.patch("/notify/rules/<rule_id>")
def update_rule(rule_id: str):
    return _not_implemented(f"实现 US-M4-001：PATCH /notify/rules/{rule_id}")


@notify_bp.delete("/notify/rules/<rule_id>")
def delete_rule(rule_id: str):
    return _not_implemented(f"实现 US-M4-001：DELETE /notify/rules/{rule_id}")


@notify_bp.post("/notify/dispatch")
def dispatch():
    return _not_implemented("实现 US-M4-002：POST /notify/dispatch（注意 dryRun 默认）")


@notify_bp.get("/notify/deliveries")
def list_deliveries():
    return _not_implemented("实现 US-M4-002：GET /notify/deliveries")


@notify_bp.post("/notify/channels/<string:ch_type>/test")
def test_channel(ch_type: str):
    return _not_implemented(f"实现 US-M4-003：POST /notify/channels/{ch_type}/test")
