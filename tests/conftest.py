import pytest
from backend.app import create_app
from backend.database.database import db


@pytest.fixture
def app():
    """Create a Flask app instance for testing with isolated in-memory DB."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a test client for API tests."""
    with app.test_client() as client:
        yield client
