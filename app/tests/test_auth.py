import pytest
from fastapi.testclient import TestClient

def test_login_success(client, test_employee):
    """Test successful login"""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["employee"]["email"] == "test@example.com"

def test_login_invalid_credentials(client, test_employee):
    """Test login with invalid credentials"""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"

def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401

def test_change_password(client, auth_headers):
    """Test changing password"""
    response = client.post("/api/v1/auth/change-password", 
                          headers=auth_headers,
                          json={
                              "old_password": "testpass123",
                              "new_password": "newtestpass123"
                          })
    
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

def test_change_password_wrong_old_password(client, auth_headers):
    """Test changing password with wrong old password"""
    response = client.post("/api/v1/auth/change-password", 
                          headers=auth_headers,
                          json={
                              "old_password": "wrongpassword",
                              "new_password": "newtestpass123"
                          })
    
    assert response.status_code == 401
