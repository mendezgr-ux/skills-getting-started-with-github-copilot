import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Main endpoint: List activities
def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Main endpoint: Successful signup
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")

# Edge case: Duplicate signup
def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

# Main endpoint: Unregister participant
def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json().get("message", "")

# Edge case: Unregister non-existent participant
def test_unregister_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@example.com"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json().get("detail", "")

# Edge case: Signup for non-existent activity
def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")

# Edge case: Unregister from non-existent activity
def test_unregister_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@example.com"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
