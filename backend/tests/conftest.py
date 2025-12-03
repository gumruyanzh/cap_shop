import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()
        return user
