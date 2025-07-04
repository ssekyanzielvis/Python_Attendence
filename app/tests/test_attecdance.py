import pytest
from datetime import datetime, date
from fastapi.testclient import TestClient

def test_check_in_success(client, auth_headers, db_session):
    """Test successful check-in"""
    response = client.post("/api/v1/attendance/check-in", 
                          headers=auth_headers,
                          json={
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Check-in successful"
    assert "attendance" in data

def test_check_in_duplicate(client, auth_headers):
    """Test duplicate check-in on same day"""
    # First check-in
    client.post("/api/v1/attendance/check-in", 
                headers=auth_headers,
                json={
                    "latitude": 40.7128,
                    "longitude": -74.0060
                })
    
    # Second check-in (should fail)
    response = client.post("/api/v1/attendance/check-in", 
                          headers=auth_headers,
                          json={
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 400

def test_check_out_success(client, auth_headers):
    """Test successful check-out"""
    # First check-in
    client.post("/api/v1/attendance/check-in", 
                headers=auth_headers,
                json={
                    "latitude": 40.7128,
                    "longitude": -74.0060
                })
    
    # Then check-out
    response = client.post("/api/v1/attendance/check-out", 
                          headers=auth_headers,
                          json={
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Check-out successful"

def test_check_out_without_check_in(client, auth_headers):
    """Test check-out without check-in"""
    response = client.post("/api/v1/attendance/check-out", 
                          headers=auth_headers,
                          json={
                              "latitude": 40.7128,
                              "longitude": -74.0060
                          })
    
    assert response.status_code == 400

# ... continuing from previous code

def test_get_attendance_history(client, auth_headers):
    """Test getting attendance history"""
    response = client.get("/api/v1/attendance/history", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "attendance_records" in data
    assert isinstance(data["attendance_records"], list)

def test_get_attendance_history_with_date_range(client, auth_headers):
    """Test getting attendance history with date range"""
    response = client.get("/api/v1/attendance/history?start_date=2024-01-01&end_date=2024-01-31", 
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "attendance_records" in data

def test_check_in_invalid_location(client, auth_headers):
    """Test check-in with invalid location (too far from office)"""
    response = client.post("/api/v1/attendance/check-in", 
                          headers=auth_headers,
                          json={
                              "latitude": 0.0,  # Far from office
                              "longitude": 0.0
                          })
    
    assert response.status_code == 400
    assert "location" in response.json()["detail"].lower()

def test_monthly_report_admin(client, admin_headers):
    """Test getting monthly report as admin"""
    response = client.get("/api/v1/attendance/reports/monthly?year=2024&month=1", 
                         headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "report" in data

def test_monthly_report_unauthorized(client, auth_headers):
    """Test getting monthly report as regular employee (should fail)"""
    response = client.get("/api/v1/attendance/reports/monthly?year=2024&month=1", 
                         headers=auth_headers)
    
    assert response.status_code == 403

