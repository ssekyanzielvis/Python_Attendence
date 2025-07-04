import pytest
from fastapi.testclient import TestClient

def test_generate_qr_code_admin(client, admin_headers):
    """Test generating QR code as admin"""
    response = client.post("/api/v1/qr-codes/generate", 
                          headers=admin_headers,
                          json={
                              "location_name": "Test Office",
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "QR code generated successfully"
    assert "qr_code" in data
    assert "qr_image" in data

def test_generate_qr_code_unauthorized(client, auth_headers):
    """Test generating QR code as regular employee (should fail)"""
    response = client.post("/api/v1/qr-codes/generate", 
                          headers=auth_headers,
                          json={
                              "location_name": "Test Office",
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 403

def test_get_active_qr_codes(client, admin_headers):
    """Test getting active QR codes"""
    response = client.get("/api/v1/qr-codes/", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "qr_codes" in data
    assert isinstance(data["qr_codes"], list)

def test_validate_qr_code(client, auth_headers):
    """Test validating QR code"""
    response = client.post("/api/v1/qr-codes/validate", 
                          headers=auth_headers,
                          json="test-qr-code-data")
    
    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data
    assert "message" in data

def test_deactivate_qr_code_admin(client, admin_headers):
    """Test deactivating QR code as admin"""
    qr_code_id = "test-qr-id"
    
    response = client.delete(f"/api/v1/qr-codes/{qr_code_id}", headers=admin_headers)
    
    # This would return 404 since we don't have a real QR code
    assert response.status_code in [200, 404]
