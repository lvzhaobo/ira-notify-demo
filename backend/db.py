"""SQLite 连接；表结构由 migrations + 小组实现补充。"""
import os
import sqlite3
import uuid
from datetime import datetime, timezone

from flask import current_app, g


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def generate_uuid():
    return str(uuid.uuid4())


def get_db():
    if "db" not in g:
        path = current_app.config["DATABASE"]
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        g.db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db(app):
    """执行 migrations/001_init.sql（工作坊默认仅含注释，不建表）。"""
    db_path = os.path.join(os.path.dirname(__file__), "migrations", "001_init.sql")
    if not os.path.isfile(db_path):
        return
    with open(db_path, encoding="utf-8") as f:
        script = f.read().strip()
    if not script:
        return
    db = sqlite3.connect(app.config["DATABASE"])
    db.executescript(script)
    db.commit()
    db.close()
