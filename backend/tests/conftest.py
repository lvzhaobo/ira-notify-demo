import pytest

from app import create_app


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("M4_DATABASE_PATH", str(tmp_path / "test.db"))
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()
