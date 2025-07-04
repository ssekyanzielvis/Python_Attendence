from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..repositories.employee_repository import EmployeeRepository
from ..repositories.leave_repository import LeaveRepository
from ..models.notification import Notification, NotificationType
from ..models.employee import EmployeeRole
from ..config.database import Base
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config.settings import settings

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.leave_repo = LeaveRepository(db)
    
    def create_notification(
        self, 
        employee_id: str, 
        title: str, 
        message: str, 
        notification_type: NotificationType
    ) -> Notification:
        """Create a new notification"""
        notification_data = {
            "employee_id": employee_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False
        }
        
        notification = Notification(**notification_data)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def send_email_notification(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USERNAME
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.SMTP_USERNAME, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_late_arrival_notification(self, employee_id: str):
        """Send notification for late arrival"""
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            return
        
        title = "Late Arrival Recorded"
        message = f"Your late arrival has been recorded for {datetime.now().strftime('%Y-%m-%d')}. Please ensure to arrive on time."
        
        # Create in-app notification
        self.create_notification(employee_id, title, message, NotificationType.ATTENDANCE)
        
        # Send email notification
        email_body = f"""
        <html>
        <body>
            <h2>Late Arrival Notification</h2>
            <p>Dear {employee.first_name},</p>
            <p>{message}</p>
            <p>If you have any concerns, please contact your supervisor.</p>
            <br>
            <p>Best regards,<br>HR Department</p>
        </body>
        </html>
        """
        
        self.send_email_notification(employee.email, title, email_body)
    
    def send_leave_request_notification(self, leave_request_id: str):
        """Send notification to supervisors about new leave request"""
        leave_request = self.leave_repo.get_by_id(leave_request_id)
        if not leave_request:
            return
        
        employee = self.employee_repo.get_by_id(str(leave_request.employee_id))
        if not employee:
            return
        
        # Get all supervisors
        supervisors = self.employee_repo.get_supervisors()
        
        title = "New Leave Request"
        message = f"{employee.full_name} has submitted a new {leave_request.leave_type.value} leave request from {leave_request.start_date} to {leave_request.end_date}."
        
        for supervisor in supervisors:
            # Create in-app notification
            self.create_notification(str(supervisor.id), title, message, NotificationType.LEAVE)
            
            # Send email notification
            email_body = f"""
            <html>
            <body>
                <h2>New Leave Request</h2>
                <p>Dear {supervisor.first_name},</p>
                <p><strong>Employee:</strong> {employee.full_name}</p>
                <p><strong>Leave Type:</strong> {leave_request.leave_type.value.title()}</p>
                <p><strong>Duration:</strong> {leave_request.start_date} to {leave_request.end_date}</p>
                <p><strong>Reason:</strong> {leave_request.reason}</p>
                <p>Please review and approve/reject this request in the system.</p>
                <br>
                <p>Best regards,<br>HR System</p>
            </body>
            </html>
            """
            
            self.send_email_notification(supervisor.email, title, email_body)
    
    def send_leave_approval_notification(self, leave_request_id: str):
        """Send notification about leave approval"""
        leave_request = self.leave_repo.get_by_id(leave_request_id)
        if not leave_request:
            return
        
        employee = self.employee_repo.get_by_id(str(leave_request.employee_id))
        if not employee:
            return
        
        title = "Leave Request Approved"
        message = f"Your {leave_request.leave_type.value} leave request from {leave_request.start_date} to {leave_request.end_date} has been approved."
        
        # Create in-app notification
        self.create_notification(str(employee.id), title, message, NotificationType.LEAVE)
        
        # Send email notification
        email_body = f"""
        <html>
        <body>
            <h2>Leave Request Approved</h2>
            <p>Dear {employee.first_name},</p>
            <p>Your leave request has been approved with the following details:</p>
            <p><strong>Leave Type:</strong> {leave_request.leave_type.value.title()}</p>
            <p><strong>Duration:</strong> {leave_request.start_date} to {leave_request.end_date}</p>
            <p><strong>Total Days:</strong> {leave_request.duration_days}</p>
            <p>Enjoy your time off!</p>
            <br>
            <p>Best regards,<br>HR Department</p>
        </body>
        </html>
        """
        
        self.send_email_notification(employee.email, title, email_body)
    
    def send_leave_rejection_notification(self, leave_request_id: str, rejection_reason: str):
        """Send notification about leave rejection"""
        leave_request = self.leave_repo.get_by_id(leave_request_id)
        if not leave_request:
            return
        
        employee = self.employee_repo.get_by_id(str(leave_request.employee_id))
        if not employee:
            return
        
        title = "Leave Request Rejected"
        message = f"Your {leave_request.leave_type.value} leave request from {leave_request.start_date} to {leave_request.end_date} has been rejected. Reason: {rejection_reason}"
        
        # Create in-app notification
        self.create_notification(str(employee.id), title, message, NotificationType.LEAVE)
        
        # Send email notification
        email_body = f"""
        <html>
        <body>
            <h2>Leave Request Rejected</h2>
            <p>Dear {employee.first_name},</p>
            <p>Unfortunately, your leave request has been rejected with the following details:</p>
            <p><strong>Leave Type:</strong> {leave_request.leave_type.value.title()}</p>
            <p><strong>Duration:</strong> {leave_request.start_date} to {leave_request.end_date}</p>
            <p><strong>Reason for Rejection:</strong> {rejection_reason}</p>
            <p>Please contact your supervisor if you have any questions.</p>
            <br>
            <p>Best regards,<br>HR Department</p>
        </body>
        </html>
        """
        
        self.send_email_notification(employee.email, title, email_body)
    
    def get_employee_notifications(self, employee_id: str, skip: int = 0, limit: int = 50) -> List[Notification]:
        """Get notifications for an employee"""
        return self.db.query(Notification).filter(
            Notification.employee_id == employee_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    def mark_notification_as_read(self, notification_id: str, employee_id: str) -> bool:
        """Mark notification as read"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.employee_id == employee_id
        ).first()
        
        if notification:
            notification.is_read = True
            self.db.commit()
            return True
        return False
    
    def get_unread_count(self, employee_id: str) -> int:
        """Get count of unread notifications"""
        return self.db.query(Notification).filter(
            Notification.employee_id == employee_id,
            Notification.is_read == False
        ).count()
