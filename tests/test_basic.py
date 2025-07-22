import pytest
from backend import create_app

# This fixture sets up a fresh Flask app using the TestingConfig for each test run.
# It also creates all database tables before running tests.
@pytest.fixture
def app():
    app = create_app('TestingConfig')  # Use DevelopmentConfig, or TestingConfig for testing
    with app.app_context():
        from backend.models import db
        db.create_all()
    yield app

# This fixture provides a test client for making requests to the Flask app.
@pytest.fixture
def client(app):
    return app.test_client()

# Test that the root URL ("/") returns a 200 OK response.
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

# Test that the Swagger API documentation is served correctly.
def test_swagger_yaml(client):
    response = client.get("/swagger.yaml")
    assert response.status_code == 200

# Test that a non-existent route returns a 404 Not Found.
def test_404(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404

# Test the gyms endpoint. Should return 405 if only POST is allowed, or 200 if GET is implemented.
def test_gyms_get(client):
    response = client.get("/gyms/")
    assert response.status_code in (200, 405)

# Test the members endpoint. Should return 405 if only POST is allowed, or 200 if GET is implemented.
def test_members_get(client):
    response = client.get("/members/")
    assert response.status_code in (200, 405)

# Test the payments endpoint for gyms. Accepts several possible status codes depending on auth/data.
def test_payments_get(client):
    response = client.get("/payments/gym")
    assert response.status_code in (200, 400, 401, 403)  # Might require auth

# Test the subscriptions endpoint for gyms. Accepts several possible status codes depending on auth/data.
def test_subscriptions_get(client):
    response = client.get("/subscriptions/gym")
    assert response.status_code in (200, 400, 401, 403)  # Might require auth