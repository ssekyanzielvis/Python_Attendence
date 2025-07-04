import re
from typing import Optional
from datetime import date, datetime, time
from geopy.distance import geodesic
from ..config.settings import settings

class AttendanceValidator:
    @staticmethod
    def validate_location(employee_lat: float, employee_lng: float, office_lat: float, office_lng: float) -> bool:
        """Validate if employee is within allowed radius of office location"""
        employee_location = (employee_lat, employee_lng)
        office_location = (office_lat, office_lng)
        
        distance = geodesic(employee_location, office_location).meters
        return distance <= settings.ALLOWED_RADIUS_METERS
    
    @staticmethod
    def validate_work_hours(check_time: datetime) -> dict:
        """Validate work hours and determine if late/early"""
        work_start = time(hour=settings.WORK_START_HOUR, minute=settings.WORK_START_MINUTE)
        work_end = time(hour=settings.WORK_END_HOUR, minute=settings.WORK_END_MINUTE)
        
        current_time = check_time.time()
        
        return {
            'is_late': current_time > work_start,
            'is_early_checkout': current_time < work_end,
            'work_start': work_start,
            'work_end': work_end
        }
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        """Validate GPS coordinates"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180

class EmployeeValidator:
    @staticmethod
    def validate_employee_code(code: str) -> bool:
        """Validate employee code format"""
        pattern = r'^[A-Z]{2,4}\d{3,6}$'
        return bool(re.match(pattern, code))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

class LeaveValidator:
    @staticmethod
    def validate_leave_dates(start_date: date, end_date: date) -> dict:
        """Validate leave request dates"""
        errors = []
        
        if start_date < date.today():
            errors.append("Start date cannot be in the past")
        
        if end_date < start_date:
            errors.append("End date cannot be before start date")
        
        # Check for weekends (optional business rule)
        duration = (end_date - start_date).days + 1
        if duration > 30:
            errors.append("Leave duration cannot exceed 30 days")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'duration': duration
        }
    
    @staticmethod
    def validate_leave_balance(requested_days: int, available_balance: int) -> bool:
        """Validate if employee has sufficient leave balance"""
        return available_balance >= requested_days
