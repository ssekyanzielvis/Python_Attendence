from typing import List, Optional, Dict, Any
from datetime import date, datetime, time
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from ..repositories.attendance_repository import AttendanceRepository
from ..repositories.employee_repository import EmployeeRepository
from ..models.attendance import Attendance, AttendanceStatus
from ..config.settings import settings
from ..utils.exceptions import ValidationError, BusinessLogicError
from .notification_service import NotificationService

class AttendanceService:
    def __init__(self, db: Session):
        self.db = db
        self.attendance_repo = AttendanceRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.notification_service = NotificationService(db)
    
    def validate_location(self, latitude: float, longitude: float) -> bool:
        """Validate if the employee is within the allowed distance from office"""
        office_location = (settings.OFFICE_LATITUDE, settings.OFFICE_LONGITUDE)
        employee_location = (latitude, longitude)
        distance = geodesic(office_location, employee_location).meters
        return distance <= settings.MAX_DISTANCE_METERS
    
    def determine_attendance_status(self, check_in_time: datetime) -> AttendanceStatus:
        """Determine attendance status based on check-in time"""
        work_start = datetime.strptime(settings.WORK_START_TIME, "%H:%M").time()
        check_in_time_only = check_in_time.time()
        
        if check_in_time_only < work_start:
            return AttendanceStatus.EARLY
        elif check_in_time_only <= time(
            work_start.hour, 
            work_start.minute + settings.LATE_THRESHOLD_MINUTES
        ):
            return AttendanceStatus.ON_TIME
        else:
            return AttendanceStatus.LATE
    
    def check_in(
        self, 
        employee_id: str, 
        latitude: float, 
        longitude: float, 
        qr_code_data: Optional[str] = None
    ) -> Attendance:
        """Record employee check-in"""
        today = date.today()
        
        # Check if already checked in today
        existing_attendance = self.attendance_repo.get_by_employee_and_date(employee_id, today)
        if existing_attendance and existing_attendance.check_in_time:
            raise BusinessLogicError("Already checked in today")
        
        # Validate location
        if not self.validate_location(latitude, longitude):
            raise ValidationError("You are not within the allowed office area")
        
        # Validate QR code if provided
        if qr_code_data:
            from .qr_service import QRService
            qr_service = QRService(self.db)
            if not qr_service.validate_qr_code(qr_code_data):
                raise ValidationError("Invalid QR code")
        
        check_in_time = datetime.now()
        status = self.determine_attendance_status(check_in_time)
        
        if existing_attendance:
            # Update existing record
            attendance = self.attendance_repo.update(str(existing_attendance.id), {
                "check_in_time": check_in_time,
                "status": status,
                "latitude": latitude,
                "longitude": longitude,
                "qr_code_data": qr_code_data
            })
        else:
            # Create new record
            attendance_data = {
                "employee_id": employee_id,
                "date": today,
                "check_in_time": check_in_time,
                "status": status,
                "latitude": latitude,
                "longitude": longitude,
                "qr_code_data": qr_code_data
            }
            attendance = self.attendance_repo.create(attendance_data)
        
        # Send notification for late arrival
        if status == AttendanceStatus.LATE:
            self.notification_service.send_late_arrival_notification(employee_id)
        
        return attendance
    
    def check_out(
        self, 
        employee_id: str, 
        latitude: float, 
        longitude: float,
        qr_code_data: Optional[str] = None
    ) -> Attendance:
        """Record employee check-out"""
        today = date.today()
        
        # Get today's attendance record
        attendance = self.attendance_repo.get_by_employee_and_date(employee_id, today)
        if not attendance:
            raise BusinessLogicError("No check-in record found for today")
        
        if attendance.check_out_time:
            raise BusinessLogicError("Already checked out today")
        
        # Validate location
        if not self.validate_location(latitude, longitude):
            raise ValidationError("You are not within the allowed office area")
        
        # Validate QR code if provided
        if qr_code_data:
            from .qr_service import QRService
            qr_service = QRService(self.db)
            if not qr_service.validate_qr_code(qr_code_data):
                raise ValidationError("Invalid QR code")
        
        check_out_time = datetime.now()
        
        # Update attendance record
        updated_attendance = self.attendance_repo.update(str(attendance.id), {
            "check_out_time": check_out_time,
            "qr_code_data": qr_code_data or attendance.qr_code_data
        })
        
        return updated_attendance
    
    def get_employee_attendance_history(
        self, 
        employee_id: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """Get employee's attendance history"""
        return self.attendance_repo.get_employee_attendance_history(
            employee_id, start_date, end_date, skip, limit
        )
    
    def get_today_attendance(self, employee_id: str) -> Optional[Attendance]:
        """Get today's attendance record for employee"""
        return self.attendance_repo.get_by_employee_and_date(employee_id, date.today())
    
    def get_monthly_stats(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get monthly attendance statistics for employee"""
        return self.attendance_repo.get_monthly_stats(employee_id, year, month)
    
    def get_daily_attendance_report(self, report_date: date) -> List[Dict[str, Any]]:
        """Get daily attendance report for all employees"""
        attendance_records = self.attendance_repo.get_daily_attendance(report_date)
        all_employees = self.employee_repo.get_active_employees()
        
        # Create a map of employee attendance
        attendance_map = {record.employee_id: record for record in attendance_records}
        
        report = []
        for employee in all_employees:
            attendance = attendance_map.get(str(employee.id))
            report.append({
                "employee": employee.to_dict(),
                "attendance": attendance.to_dict() if attendance else None,
                "status": attendance.status.value if attendance else "absent"
            })
        
        return report
    
    def mark_absent_employees(self, target_date: Optional[date] = None) -> int:
        """Mark employees as absent who haven't checked in"""
        if not target_date:
            target_date = date.today()
        
        absent_employee_ids = self.attendance_repo.get_absent_employees_today()
        count = 0
        
        for employee_id in absent_employee_ids:
            # Check if employee is on approved leave
            from .leave_service import LeaveService
            leave_service = LeaveService(self.db)
            if not leave_service.is_employee_on_leave(employee_id, target_date):
                attendance_data = {
                    "employee_id": employee_id,
                    "date": target_date,
                    "status": AttendanceStatus.ABSENT
                }
                self.attendance_repo.create(attendance_data)
                count += 1
        
        return count
    
    def get_late_arrivals_report(
        self, 
        start_date: date, 
        end_date: date
    ) -> List[Attendance]:
        """Get report of late arrivals in date range"""
        return self.attendance_repo.get_late_arrivals(start_date, end_date)
    
    def calculate_overtime(self, employee_id: str, target_date: date) -> float:
        """Calculate overtime hours for employee on specific date"""
        attendance = self.attendance_repo.get_by_employee_and_date(employee_id, target_date)
        if not attendance or not attendance.check_out_time:
            return 0.0
        
        hours_worked = attendance.hours_worked
        standard_hours = 8.0  # Standard work day
        
        return max(0.0, hours_worked - standard_hours)
