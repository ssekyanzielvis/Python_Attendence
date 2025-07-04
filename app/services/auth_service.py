from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..repositories.employee_repository import EmployeeRepository
from ..models.employee import Employee
from ..config.settings import settings
from ..utils.exceptions import AuthenticationError, AuthorizationError

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def authenticate_employee(self, email: str, password: str) -> Optional[Employee]:
        employee = self.employee_repo.get_by_email(email)
        if not employee:
            return None
        if not self.verify_password(password, employee.password_hash):
            return None
        return employee
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise AuthenticationError("Invalid token")
    
    def get_current_employee(self, token: str) -> Employee:
        try:
            payload = self.verify_token(token)
            employee_id: str = payload.get("sub")
            if employee_id is None:
                raise AuthenticationError("Invalid token")
        except JWTError:
            raise AuthenticationError("Invalid token")
        
        employee = self.employee_repo.get_by_id(employee_id)
        if employee is None:
            raise AuthenticationError("Employee not found")
        return employee
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        employee = self.authenticate_employee(email, password)
        if not employee:
            raise AuthenticationError("Invalid email or password")
        
        access_token = self.create_access_token(data={"sub": str(employee.id)})
        refresh_token = self.create_refresh_token(data={"sub": str(employee.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "employee": employee.to_dict()
        }
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        try:
            payload = self.verify_token(refresh_token)
            if payload.get("type") != "refresh":
                raise AuthenticationError("Invalid refresh token")
            
            employee_id = payload.get("sub")
            employee = self.employee_repo.get_by_id(employee_id)
            if not employee:
                raise AuthenticationError("Employee not found")
            
            access_token = self.create_access_token(data={"sub": str(employee.id)})
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except JWTError:
            raise AuthenticationError("Invalid refresh token")
    
    def change_password(self, employee_id: str, old_password: str, new_password: str) -> bool:
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise AuthenticationError("Employee not found")
        
        if not self.verify_password(old_password, employee.password_hash):
            raise AuthenticationError("Invalid old password")
        
        new_password_hash = self.get_password_hash(new_password)
        self.employee_repo.update(employee_id, {"password_hash": new_password_hash})
        return True
