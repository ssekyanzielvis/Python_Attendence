from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .base_repository import BaseRepository
from ..models.employee import Employee, EmployeeRole

class EmployeeRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Employee)
    
    def get_by_email(self, email: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(
            and_(Employee.email == email, Employee.is_active == True)
        ).first()
    
    def get_by_employee_code(self, employee_code: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(
            and_(Employee.employee_code == employee_code, Employee.is_active == True)
        ).first()
    
    def get_active_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.db.query(Employee).filter(
            Employee.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_department(self, department: str) -> List[Employee]:
        return self.db.query(Employee).filter(
            and_(Employee.department == department, Employee.is_active == True)
        ).all()
    
    def get_supervisors(self) -> List[Employee]:
        return self.db.query(Employee).filter(
            and_(
                Employee.role.in_([EmployeeRole.SUPERVISOR, EmployeeRole.ADMIN]),
                Employee.is_active == True
            )
        ).all()
    
    def search_employees(self, search_term: str) -> List[Employee]:
        return self.db.query(Employee).filter(
            and_(
                or_(
                    Employee.first_name.ilike(f"%{search_term}%"),
                    Employee.last_name.ilike(f"%{search_term}%"),
                    Employee.employee_code.ilike(f"%{search_term}%"),
                    Employee.email.ilike(f"%{search_term}%")
                ),
                Employee.is_active == True
            )
        ).all()
    
    def deactivate_employee(self, employee_id: str) -> bool:
        employee = self.get_by_id(employee_id)
        if employee:
            employee.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_departments(self) -> List[str]:
        result = self.db.query(Employee.department).filter(
            and_(Employee.department.isnot(None), Employee.is_active == True)
        ).distinct().all()
        return [dept[0] for dept in result if dept[0]]
