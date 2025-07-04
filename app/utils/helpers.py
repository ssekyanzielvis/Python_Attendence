from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import calendar

class DateHelper:
    @staticmethod
    def get_month_date_range(year: int, month: int) -> tuple:
        """Get first and last date of a month"""
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        return first_day, last_day
    
    @staticmethod
    def get_working_days(start_date: date, end_date: date, exclude_weekends: bool = True) -> int:
        """Calculate working days between two dates"""
        working_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if exclude_weekends and current_date.weekday() < 5:  # Monday = 0, Sunday = 6
                working_days += 1
            elif not exclude_weekends:
                working_days += 1
            current_date += timedelta(days=1)
        
        return working_days
    
    @staticmethod
    def get_week_dates(target_date: date) -> tuple:
        """Get start and end date of the week containing target_date"""
        days_since_monday = target_date.weekday()
        start_of_week = target_date - timedelta(days=days_since_monday)
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week
    
    @staticmethod
    def format_duration(minutes: int) -> str:
        """Format duration in minutes to human readable format"""
        if minutes < 60:
            return f"{minutes} minutes"
        
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        
        return f"{hours} hour{'s' if hours != 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"

class AttendanceHelper:
    @staticmethod
    def calculate_work_hours(check_in: datetime, check_out: datetime) -> float:
        """Calculate work hours between check-in and check-out"""
        if not check_out:
            return 0.0
        
        duration = check_out - check_in
        return round(duration.total_seconds() / 3600, 2)  # Convert to hours
    
    @staticmethod
    def calculate_overtime(work_hours: float, standard_hours: float = 8.0) -> float:
        """Calculate overtime hours"""
        return max(0, work_hours - standard_hours)
    
    @staticmethod
    def get_attendance_status(check_in: datetime, work_start_time: datetime) -> str:
        """Determine attendance status based on check-in time"""
        if not check_in:
            return "Absent"
        
        if check_in.time() <= work_start_time.time():
            return "On Time"
        elif check_in.time() <= (work_start_time + timedelta(minutes=15)).time():
            return "Late (Grace Period)"
        else:
            return "Late"

class ReportHelper:
    @staticmethod
    def calculate_attendance_percentage(present_days: int, total_working_days: int) -> float:
        """Calculate attendance percentage"""
        if total_working_days == 0:
            return 0.0
        return round((present_days / total_working_days) * 100, 2)
    
    @staticmethod
    def generate_monthly_summary(attendance_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate monthly attendance summary"""
        total_days = len(attendance_records)
        present_days = sum(1 for record in attendance_records if record.get('status') != 'Absent')
        late_days = sum(1 for record in attendance_records if 'Late' in record.get('status', ''))
        total_hours = sum(record.get('work_hours', 0) for record in attendance_records)
        
        return {
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': total_days - present_days,
            'late_days': late_days,
            'total_hours': round(total_hours, 2),
            'average_hours': round(total_hours / max(present_days, 1), 2),
            'attendance_percentage': ReportHelper.calculate_attendance_percentage(present_days, total_days)
        }

class NotificationHelper:
    @staticmethod
    def format_notification_message(notification_type: str, data: Dict[str, Any]) -> str:
        """Format notification message based on type"""
        if notification_type == "late_arrival":
            return f"You arrived late on {data.get('date')}. Please ensure punctuality."
        
        elif notification_type == "leave_approved":
            return f"Your {data.get('leave_type')} leave from {data.get('start_date')} to {data.get('end_date')} has been approved."
        
        elif notification_type == "leave_rejected":
            return f"Your {data.get('leave_type')} leave request has been rejected. Reason: {data.get('reason')}"
        
        elif notification_type == "leave_request":
            return f"New leave request from {data.get('employee_name')} for {data.get('leave_type')} leave."
        
        else:
            return "You have a new notification."
