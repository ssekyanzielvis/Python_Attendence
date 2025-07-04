from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from ...config.database import get_db
from ...services.auth_service import AuthService
from ...services.attendance_service import AttendanceService
from ...utils.exceptions import AuthenticationError, ValidationError, BusinessLogicError

router = APIRouter(prefix="/attendance", tags=["attendance"])
security = HTTPBearer()

class CheckInRequest(BaseModel):
    latitude: float
    longitude: float
    qr_code_data: Optional[str] = None

class CheckOutRequest(BaseModel):
    latitude: float
    longitude: float
    qr_code_data: Optional[str] = None

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

@router.post("/check-in")
async def check_in(
    request: CheckInRequest,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Employee check-in"""
    try:
        attendance_service = AttendanceService(db)
        attendance = attendance_service.check_in(
            str(current_employee.id),
            request.latitude,
            request.longitude,
            request.qr_code_data
        )
        return {
            "message": "Check-in successful",
            "attendance": attendance.to_dict()
        }
    except (ValidationError, BusinessLogicError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/check-out")
async def check_out(
    request: CheckOutRequest,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Employee check-out"""
    try:
        attendance_service = AttendanceService(db)
        attendance = attendance_service.check_out(
            str(current_employee.id),
            request.latitude,
            request.longitude,
            request.qr_code_data
        )
        return {
            "message": "Check-out successful",
            "attendance": attendance.to_dict()
        }
    except (ValidationError, BusinessLogicError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/today")
async def get_today_attendance(
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get today's attendance for current employee"""
    attendance_service = AttendanceService(db)
    attendance = attendance_service.get_today_attendance(str(current_employee.id))
    
    return {
        "attendance": attendance.to_dict() if attendance else None
    }

@router.get("/history")
async def get_attendance_history(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get attendance history for current employee"""
    attendance_service = AttendanceService(db)
    history = attendance_service.get_employee_attendance_history(
        str(current_employee.id),
        start_date,
        end_date,
        skip,
        limit
    )
    
    return {
        "attendance_history": [record.to_dict() for record in history]
    }

@router.get("/stats/{year}/{month}")
async def get_monthly_stats(
    year: int,
    month: int,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get monthly attendance statistics"""
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid month"
        )
    
    attendance_service = AttendanceService(db)
    stats = attendance_service.get_monthly_stats(str(current_employee.id), year, month)
    
    return {"stats": stats}

@router.get("/report/daily/{report_date}")
async def get_daily_report(
    report_date: date,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get daily attendance report (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    attendance_service = AttendanceService(db)
    report = attendance_service.get_daily_attendance_report(report_date)
    
    return {"report": report}

@router.get("/report/late-arrivals")
async def get_late_arrivals_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get late arrivals report (supervisors only)"""
    if not current_employee.is_supervisor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Supervisor privileges required."
        )
    
    attendance_service = AttendanceService(db)
    late_arrivals = attendance_service.get_late_arrivals_report(start_date, end_date)
    
    return {
        "late_arrivals": [record.to_dict() for record in late_arrivals]
    }
