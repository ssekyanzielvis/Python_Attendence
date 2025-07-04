from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..services.attendance_service import AttendanceService
import logging

logger = logging.getLogger(__name__)

class AttendanceScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Setup scheduled jobs"""
        # Mark absent employees daily at 6 PM
        self.scheduler.add_job(
            func=self.mark_absent_employees,
            trigger=CronTrigger(hour=18, minute=0),
            id='mark_absent_employees',
            name='Mark absent employees',
            replace_existing=True
        )
        
        # Generate daily attendance report at 7 PM
        self.scheduler.add_job(
            func=self.generate_daily_report,
            trigger=CronTrigger(hour=19, minute=0),
            id='generate_daily_report',
            name='Generate daily attendance report',
            replace_existing=True
        )
    
    def mark_absent_employees(self):
        """Mark employees as absent who haven't checked in"""
        try:
            db: Session = SessionLocal()
            attendance_service = AttendanceService(db)
            count = attendance_service.mark_absent_employees()
            logger.info(f"Marked {count} employees as absent")
            db.close()
        except Exception as e:
            logger.error(f"Error marking absent employees: {str(e)}")
    
    def generate_daily_report(self):
        """Generate daily attendance report"""
        try:
            from datetime import date
            db: Session = SessionLocal()
            attendance_service = AttendanceService(db)
            report = attendance_service.get_daily_attendance_report(date.today())
            logger.info(f"Generated daily report with {len(report)} records")
            # Here you could send the report via email or save to file
            db.close()
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
    
    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        logger.info("Attendance scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Attendance scheduler stopped")

# Global scheduler instance
scheduler = AttendanceScheduler()
