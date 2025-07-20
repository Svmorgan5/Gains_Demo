import pytest
from backend import create_app

@pytest.fixture
def app():
    app = create_app('TestingConfig')
    with app.app_context():
        from backend.models import db
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_swagger_yaml(client):
    response = client.get("/swagger.yaml")
    assert response.status_code == 200

def test_404(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_gyms_get(client):
    response = client.get("/gyms/")
    # Should be 405 if only POST is allowed, or 200 if GET is implemented
    assert response.status_code in (200, 405)

def test_members_get(client):
    response = client.get("/members/")
    assert response.status_code in (200, 405)

def test_payments_get(client):
    response = client.get("/payments/gym")
    assert response.status_code in (200, 400, 401, 403)  # Might require auth

def test_subscriptions_get(client):
    response = client.get("/subscriptions/gym")
    assert response.status_code in (200, 400, 401, 403)  # Might require auth