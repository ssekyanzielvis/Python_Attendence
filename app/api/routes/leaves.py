from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from ...config.database import get_db
from ...services.auth_service import AuthService
from ...services.leave_service import LeaveService
from ...models.leave_request import LeaveType, LeaveStatus
from ...utils.exceptions import AuthenticationError, ValidationError, BusinessLogicError

router = APIRouter(prefix="/leaves", tags=["leaves"])
security = HTTPBearer()

class LeaveRequestCreate(BaseModel):
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str

class LeaveRequestResponse(BaseModel):
    approved_by: str
    rejection_reason: Optional[str] = None

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

@router.post("/request")
async def submit_leave_request(
    request: LeaveRequestCreate,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Submit a new leave request"""
    try:
        leave_service = LeaveService(db)
        leave_request = leave_service.submit_leave_request(
            str(current_employee.id),
            request.leave_type,
            request.start_date,
            request.end_date,
            request.reason
        )
        return {
            "message": "Leave request submitted successfully",
            "leave_request": leave_request.to_dict()
        }
    except (ValidationError, BusinessLogicError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/my-requests")
async def get_my_leave_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get current employee's leave requests"""
    leave_service = LeaveService(db)
    requests = leave_service.get_employee_leave_requests(
        str(current_employee.id), skip, limit
    )
    
    return {
        "leave_requests": [req.to_dict() for req in requests]
    }

@router.get("/balance")
async def get_leave_balance(
    year: Optional[int] = Query(None),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get leave balance for current employee"""
    leave_service = LeaveService(db)
    balance = leave_service.get_leave_balance(str(current_employee.id), year)
    
    return {"leave_balance": balance}

# ... continuing from previous code

@router.get("/pending")
async def get_pending_requests(
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get pending leave requests (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    leave_service = LeaveService(db)
    pending_requests = leave_service.get_pending_requests()
    
    return {
        "pending_requests": [req.to_dict() for req in pending_requests]
    }

@router.put("/{request_id}/approve")
async def approve_leave_request(
    request_id: str,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Approve a leave request (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    try:
        leave_service = LeaveService(db)
        leave_request = leave_service.approve_leave_request(
            request_id, str(current_employee.id)
        )
        return {
            "message": "Leave request approved successfully",
            "leave_request": leave_request.to_dict()
        }
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{request_id}/reject")
async def reject_leave_request(
    request_id: str,
    response: LeaveRequestResponse,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Reject a leave request (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    if not response.rejection_reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection reason is required"
        )
    
    try:
        leave_service = LeaveService(db)
        leave_request = leave_service.reject_leave_request(
            request_id, str(current_employee.id), response.rejection_reason
        )
        return {
            "message": "Leave request rejected successfully",
            "leave_request": leave_request.to_dict()
        }
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{request_id}")
async def cancel_leave_request(
    request_id: str,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Cancel a leave request"""
    try:
        leave_service = LeaveService(db)
        success = leave_service.cancel_leave_request(request_id, str(current_employee.id))
        
        if success:
            return {"message": "Leave request cancelled successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/calendar")
async def get_team_leave_calendar(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get team leave calendar (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    leave_service = LeaveService(db)
    calendar = leave_service.get_team_leave_calendar(start_date, end_date)
    
    return {"leave_calendar": calendar}
