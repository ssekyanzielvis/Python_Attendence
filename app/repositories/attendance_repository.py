from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from .base_repository import BaseRepository
from ..models.attendance import Attendance, AttendanceStatus

class AttendanceRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Attendance)
    
    def get_by_employee_and_date(self, employee_id: str, attendance_date: date) -> Optional[Attendance]:
        return self.db.query(Attendance).filter(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date == attendance_date
            )
        ).first()
    
    def get_employee_attendance_history(
        self, 
        employee_id: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        query = self.db.query(Attendance).filter(Attendance.employee_id == employee_id)
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        return query.order_by(desc(Attendance.date)).offset(skip).limit(limit).all()
    
    def get_daily_attendance(self, attendance_date: date) -> List[Attendance]:
        return self.db.query(Attendance).filter(Attendance.date == attendance_date).all()
    
    def get_attendance_by_date_range(
        self, 
        start_date: date, 
        end_date: date,
        employee_id: Optional[str] = None
    ) -> List[Attendance]:
        query = self.db.query(Attendance).filter(
            and_(Attendance.date >= start_date, Attendance.date <= end_date)
        )
        
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        
        return query.order_by(desc(Attendance.date)).all()
    
    def get_monthly_stats(self, employee_id: str, year: int, month: int) -> dict:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        stats = self.db.query(
            func.count(Attendance.id).label('total_days'),
            func.sum(func.case([(Attendance.status == AttendanceStatus.ON_TIME, 1)], else_=0)).label('on_time_days'),
            func.sum(func.case([(Attendance.status == AttendanceStatus.LATE, 1)], else_=0)).label('late_days'),
            func.sum(func.case([(Attendance.status == AttendanceStatus.ABSENT, 1)], else_=0)).label('absent_days'),
            func.avg(
                func.case([
                    (Attendance.check_out_time.isnot(None), 
                     func.extract('epoch', Attendance.check_out_time - Attendance.check_in_time) / 3600)
                ], else_=0)
            ).label('avg_hours_worked')
        ).filter(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date < end_date
            )
        ).first()
        
        return {
            'total_days': stats.total_days or 0,
            'on_time_days': stats.on_time_days or 0,
            'late_days': stats.late_days or 0,
            'absent_days': stats.absent_days or 0,
            'avg_hours_worked': round(stats.avg_hours_worked or 0, 2)
        }
    
    def get_late_arrivals(self, start_date: date, end_date: date) -> List[Attendance]:
        return self.db.query(Attendance).filter(
            and_(
                Attendance.status == AttendanceStatus.LATE,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).order_by(desc(Attendance.date)).all()
    
    def get_absent_employees_today(self) -> List[str]:
        today = date.today()
        present_employees = self.db.query(Attendance.employee_id).filter(
            Attendance.date == today
        ).subquery()
        
        from ..models.employee import Employee
        absent_employees = self.db.query(Employee.id).filter(
            and_(
                Employee.is_active == True,
                ~Employee.id.in_(present_employees)
            )
        ).all()
        
        return [emp[0] for emp in absent_employees]
