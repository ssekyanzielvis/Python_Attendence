from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from .base_repository import BaseRepository
from ..models.leave_request import LeaveRequest, LeaveStatus, LeaveType

class LeaveRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, LeaveRequest)
    
    def get_employee_leave_requests(
        self, 
        employee_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[LeaveRequest]:
        return self.db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id
        ).order_by(desc(LeaveRequest.created_at)).offset(skip).limit(limit).all()
    
    def get_pending_requests(self) -> List[LeaveRequest]:
        return self.db.query(LeaveRequest).filter(
            LeaveRequest.status == LeaveStatus.PENDING
        ).order_by(LeaveRequest.created_at).all()
    
    def get_requests_by_status(self, status: LeaveStatus) -> List[LeaveRequest]:
        return self.db.query(LeaveRequest).filter(
            LeaveRequest.status == status
        ).order_by(desc(LeaveRequest.created_at)).all()
    
    def check_leave_conflict(
        self, 
        employee_id: str, 
        start_date: date, 
        end_date: date,
        exclude_request_id: Optional[str] = None
    ) -> List[LeaveRequest]:
        query = self.db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status.in_([LeaveStatus.PENDING, LeaveStatus.APPROVED]),
                or_(
                    and_(LeaveRequest.start_date <= start_date, LeaveRequest.end_date >= start_date),
                    and_(LeaveRequest.start_date <= end_date, LeaveRequest.end_date >= end_date),
                    and_(LeaveRequest.start_date >= start_date, LeaveRequest.end_date <= end_date)
                )
            )
        )
        
        if exclude_request_id:
            query = query.filter(LeaveRequest.id != exclude_request_id)
        
        return query.all()
    
# ... continuing from previous code

    def get_approved_leaves_in_period(
        self, 
        start_date: date, 
        end_date: date,
        employee_id: Optional[str] = None
    ) -> List[LeaveRequest]:
        query = self.db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.status == LeaveStatus.APPROVED,
                or_(
                    and_(LeaveRequest.start_date <= start_date, LeaveRequest.end_date >= start_date),
                    and_(LeaveRequest.start_date <= end_date, LeaveRequest.end_date >= end_date),
                    and_(LeaveRequest.start_date >= start_date, LeaveRequest.end_date <= end_date)
                )
            )
        )
        
        if employee_id:
            query = query.filter(LeaveRequest.employee_id == employee_id)
        
        return query.all()
    
    def get_leave_balance(self, employee_id: str, year: int) -> dict:
        from datetime import date
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        approved_leaves = self.db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status == LeaveStatus.APPROVED,
                LeaveRequest.start_date >= start_date,
                LeaveRequest.end_date <= end_date
            )
        ).all()
        
        leave_taken = {
            LeaveType.SICK: 0,
            LeaveType.VACATION: 0,
            LeaveType.PERSONAL: 0,
            LeaveType.EMERGENCY: 0,
            LeaveType.MATERNITY: 0,
            LeaveType.PATERNITY: 0
        }
        
        for leave in approved_leaves:
            leave_taken[leave.leave_type] += leave.duration_days
        
        # Default leave allowances (can be configured per employee)
        leave_allowances = {
            LeaveType.SICK: 10,
            LeaveType.VACATION: 21,
            LeaveType.PERSONAL: 5,
            LeaveType.EMERGENCY: 3,
            LeaveType.MATERNITY: 90,
            LeaveType.PATERNITY: 15
        }
        
        leave_balance = {}
        for leave_type in LeaveType:
            taken = leave_taken.get(leave_type, 0)
            allowance = leave_allowances.get(leave_type, 0)
            leave_balance[leave_type.value] = {
                'allowance': allowance,
                'taken': taken,
                'remaining': max(0, allowance - taken)
            }
        
        return leave_balance
    
    def approve_request(self, request_id: str, approved_by: str) -> Optional[LeaveRequest]:
        leave_request = self.get_by_id(request_id)
        if leave_request and leave_request.status == LeaveStatus.PENDING:
            leave_request.status = LeaveStatus.APPROVED
            leave_request.approved_by = approved_by
            leave_request.approved_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(leave_request)
        return leave_request
    
    def reject_request(self, request_id: str, approved_by: str, reason: str) -> Optional[LeaveRequest]:
        leave_request = self.get_by_id(request_id)
        if leave_request and leave_request.status == LeaveStatus.PENDING:
            leave_request.status = LeaveStatus.REJECTED
            leave_request.approved_by = approved_by
            leave_request.approved_at = datetime.utcnow()
            leave_request.rejection_reason = reason
            self.db.commit()
            self.db.refresh(leave_request)
        return leave_request

