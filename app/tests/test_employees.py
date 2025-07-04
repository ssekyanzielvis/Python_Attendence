import pytest
from fastapi.testclient import TestClient

def test_create_employee_admin(client, admin_headers):
    """Test creating employee as admin"""
    response = client.post("/api/v1/employees/", 
                          headers=admin_headers,
                          json={
                              "employee_code": "EMP002",
                              "email": "newemployee@example.com",
                              "first_name": "New",
                              "last_name": "Employee",
                              "department": "HR",
                              "position": "HR Specialist",
                              "password": "password123"
                          })
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Employee created successfully"
    assert data["employee"]["email"] == "newemployee@example.com"

def test_create_employee_unauthorized(client, auth_headers):
    """Test creating employee as regular user (should fail)"""
    response = client.post("/api/v1/employees/", 
                          headers=auth_headers,
                          json={
                              "employee_code": "EMP003",
                              "email": "another@example.com",
                              "first_name": "Another",
                              "last_name": "Employee",
                              "password": "password123"
                          })
    
    assert response.status_code == 403

def test_get_employees_list(client, admin_headers):
    """Test getting employees list"""
    response = client.get("/api/v1/employees/", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert isinstance(data["employees"], list)

def test_get_employee_by_id(client, auth_headers, test_employee):
    """Test getting employee by ID"""
    response = client.get(f"/api/v1/employees/{test_employee.id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["email"] == "test@example.com"

def test_update_employee_profile(client, auth_headers, test_employee):
    """Test updating own employee profile"""
    response = client.put(f"/api/v1/employees/{test_employee.id}", 
                         headers=auth_headers,
                         json={
                             "first_name": "Updated",
                             "phone_number": "+1234567890"
                         })
    
    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["first_name"] == "Updated"

def test_deactivate_employee_admin(client, admin_headers, test_employee):
    """Test deactivating employee as admin"""
    response = client.delete(f"/api/v1/employees/{test_employee.id}", headers=admin_headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Employee deactivated successfully"

def test_get_departments(client, auth_headers):
    """Test getting departments list"""
    response = client.get("/api/v1/employees/departments/list", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "departments" in data
