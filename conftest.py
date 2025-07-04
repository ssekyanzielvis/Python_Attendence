import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import Base, get_db
from app.services.auth_service import AuthService
from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import EmployeeRole

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create test database session"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_employee(db_session):
    """Create test employee"""
    employee_repo = EmployeeRepository(db_session)
    auth_service = AuthService(db_session)
    
    password_hash = auth_service.get_password_hash("testpass123")
    
    employee_data = {
        'employee_code': 'TEST001',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'department': 'IT',
        'position': 'Developer',
        'role': EmployeeRole.EMPLOYEE,
        'password_hash': password_hash,
        'is_active': True
    }
    
    return employee_repo.create(employee_data)

@pytest.fixture
def test_admin(db_session):
    """Create test admin"""
    employee_repo = EmployeeRepository(db_session)
    auth_service = AuthService(db_session)
    
    password_hash = auth_service.get_password_hash("adminpass123")
    
    admin_data = {
        'employee_code': 'ADMIN001',
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'department': 'IT',
        'position': 'Administrator',
        'role': EmployeeRole.ADMIN,
        'password_hash': password_hash,
        'is_active': True
    }
    
    return employee_repo.create(admin_data)

@pytest.fixture
def auth_headers(client, test_employee):
    """Get authentication headers for test employee"""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client, test_admin):
    """Get authentication headers for test admin"""
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
