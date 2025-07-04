from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session
from ..repositories.leave_repository import LeaveRepository
from ..repositories.employee_repository import EmployeeRepository
from ..models.leave_request import LeaveRequest, LeaveStatus, LeaveType
from ..utils.exceptions import ValidationError, BusinessLogicError
from .notification_service import NotificationService

class LeaveService:
    def __init__(self, db: Session):
        self.db = db
        self.leave_repo = LeaveRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.notification_service = NotificationService(db)
    
    def submit_leave_request(
        self, 
        employee_id: str, 
        leave_type: LeaveType,
        start_date: date,
        end_date: date,
        reason: str
    ) -> LeaveRequest:
        """Submit a new leave request"""
        
        # Validate dates
        if start_date > end_date:
            raise ValidationError("Start date cannot be after end date")
        
        if start_date < date.today():
            raise ValidationError("Cannot request leave for past dates")
        
        # Check for conflicts
        conflicts = self.leave_repo.check_leave_conflict(employee_id, start_date, end_date)
        if conflicts:
            raise BusinessLogicError("Leave request conflicts with existing approved/pending leave")
        
     # ... continuing from previous code

        # Check leave balance
        leave_balance = self.leave_repo.get_leave_balance(employee_id, start_date.year)
        duration = (end_date - start_date).days + 1
        
        if leave_balance[leave_type.value]['remaining'] < duration:
            raise BusinessLogicError(f"Insufficient {leave_type.value} leave balance")
        
        # Create leave request
        leave_data = {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "status": LeaveStatus.PENDING
        }
        
        leave_request = self.leave_repo.create(leave_data)
        
        # Notify supervisors
        self.notification_service.send_leave_request_notification(str(leave_request.id))
        
        return leave_request
    
    def approve_leave_request(self, request_id: str, approved_by: str) -> LeaveRequest:
        """Approve a leave request"""
        leave_request = self.leave_repo.approve_request(request_id, approved_by)
        if not leave_request:
            raise BusinessLogicError("Leave request not found or already processed")
        
        # Notify employee
        self.notification_service.send_leave_approval_notification(request_id)
        
        return leave_request
    
    def reject_leave_request(self, request_id: str, approved_by: str, reason: str) -> LeaveRequest:
        """Reject a leave request"""
        leave_request = self.leave_repo.reject_request(request_id, approved_by, reason)
        if not leave_request:
            raise BusinessLogicError("Leave request not found or already processed")
        
        # Notify employee
        self.notification_service.send_leave_rejection_notification(request_id, reason)
        
        return leave_request
    
    def get_employee_leave_requests(self, employee_id: str, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
        """Get leave requests for an employee"""
        return self.leave_repo.get_employee_leave_requests(employee_id, skip, limit)
    
    def get_pending_requests(self) -> List[LeaveRequest]:
        """Get all pending leave requests"""
        return self.leave_repo.get_pending_requests()
    
    def get_leave_balance(self, employee_id: str, year: Optional[int] = None) -> Dict[str, Any]:
        """Get leave balance for employee"""
        if not year:
            year = date.today().year
        return self.leave_repo.get_leave_balance(employee_id, year)
    
    def is_employee_on_leave(self, employee_id: str, check_date: date) -> bool:
        """Check if employee is on approved leave on specific date"""
        approved_leaves = self.leave_repo.get_approved_leaves_in_period(
            check_date, check_date, employee_id
        )
        return len(approved_leaves) > 0
    
    def get_team_leave_calendar(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get team leave calendar for date range"""
        approved_leaves = self.leave_repo.get_approved_leaves_in_period(start_date, end_date)
        
        calendar = []
        for leave in approved_leaves:
            employee = self.employee_repo.get_by_id(str(leave.employee_id))
            calendar.append({
                "employee": employee.to_dict() if employee else None,
                "leave": leave.to_dict()
            })
        
        return calendar
    
    def cancel_leave_request(self, request_id: str, employee_id: str) -> bool:
        """Cancel a leave request (only if pending)"""
        leave_request = self.leave_repo.get_by_id(request_id)
        if not leave_request:
            raise BusinessLogicError("Leave request not found")
        
        if str(leave_request.employee_id) != employee_id:
            raise BusinessLogicError("Unauthorized to cancel this request")
        
        if leave_request.status != LeaveStatus.PENDING:
            raise BusinessLogicError("Can only cancel pending requests")
        
        return self.leave_repo.delete(request_id)

