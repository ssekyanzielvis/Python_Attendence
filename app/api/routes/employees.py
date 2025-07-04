from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ...config.database import get_db
from ...services.auth_service import AuthService
from ...repositories.employee_repository import EmployeeRepository
from ...models.employee import EmployeeRole
from ...utils.exceptions import AuthenticationError

router = APIRouter(prefix="/employees", tags=["employees"])
security = HTTPBearer()

class EmployeeCreate(BaseModel):
    employee_code: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    role: EmployeeRole = EmployeeRole.EMPLOYEE
    password: str

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    role: Optional[EmployeeRole] = None

def get_current_employee(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Dependency to get current employee"""
    try:
        auth_service = AuthService(db)
        return auth_service.get_current_employee(credentials.credentials)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Create a new employee (admin only)"""
    if not current_employee.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    employee_repo = EmployeeRepository(db)
    auth_service = AuthService(db)
    
    # Check if employee code or email already exists
    if employee_repo.get_by_employee_code(employee_data.employee_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee code already exists"
        )
    
    if employee_repo.get_by_email(employee_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Hash password
    password_hash = auth_service.get_password_hash(employee_data.password)
    
    # Create employee
    employee_dict = employee_data.dict()
    employee_dict.pop('password')
    employee_dict['password_hash'] = password_hash
    
    employee = employee_repo.create(employee_dict)
    
    return {
        "message": "Employee created successfully",
        "employee": employee.to_dict()
    }

@router.get("/")
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    department: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get list of employees"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    employee_repo = EmployeeRepository(db)
    
    if search:
        employees = employee_repo.search_employees(search)
    elif department:
        employees = employee_repo.get_by_department(department)
    else:
        employees = employee_repo.get_active_employees(skip, limit)
    
    return {
        "employees": [emp.to_dict() for emp in employees]
    }

@router.get("/{employee_id}")
async def get_employee(
    employee_id: str,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get employee by ID"""
    # Employees can view their own profile, supervisors can view all
    if str(current_employee.id) != employee_id and not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    employee_repo = EmployeeRepository(db)
    employee = employee_repo.get_by_id(employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {"employee": employee.to_dict()}

@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Update employee information"""
    # Employees can update their own profile (limited fields), admins can update all
    if str(current_employee.id) != employee_id and not current_employee.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    employee_repo = EmployeeRepository(db)
    
    # If not admin, restrict updatable fields
    if not current_employee.is_admin:
        update_data = {
            k: v for k, v in employee_data.dict(exclude_unset=True).items()
            if k in ['first_name', 'last_name', 'phone_number']
        }
    else:
        update_data = employee_data.dict(exclude_unset=True)
    
    employee = employee_repo.update(employee_id, update_data)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {
        "message": "Employee updated successfully",
        "employee": employee.to_dict()
    }

@router.delete("/{employee_id}")
async def deactivate_employee(
    employee_id: str,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Deactivate employee (admin only)"""
    if not current_employee.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    employee_repo = EmployeeRepository(db)
    success = employee_repo.deactivate_employee(employee_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {"message": "Employee deactivated successfully"}

@router.get("/departments/list")
async def get_departments(
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get list of departments"""
    employee_repo = EmployeeRepository(db)
    departments = employee_repo.get_departments()
    
    return {"departments": departments}
