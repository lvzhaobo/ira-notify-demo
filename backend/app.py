"""
M4 工作坊后端：仅保证 health 可用；业务路由见 blueprints/notify.py（stub）。
"""
import os

from flask import Flask, g
from flask_cors import CORS

from blueprints.notify import notify_bp
from db import init_db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "workshop-dev-secret-change-me")
    _default_db = os.path.join(os.path.dirname(__file__), "notify.db")
    app.config["DATABASE"] = os.environ.get("M4_DATABASE_PATH", _default_db)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(notify_bp, url_prefix="/api/v1")

    with app.app_context():
        init_db(app)

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app


app = create_app()

if __name__ == "__main__":
    print("Health: GET http://127.0.0.1:5000/api/v1/notify/health")
    app.run(host="0.0.0.0", port=5000, debug=True)
