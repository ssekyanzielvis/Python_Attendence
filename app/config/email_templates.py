from typing import Dict, Any

class EmailTemplates:
    @staticmethod
    def late_arrival_template(employee_name: str, date: str) -> Dict[str, str]:
        """Template for late arrival notification"""
        subject = "Late Arrival Notification"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #e74c3c;">Late Arrival Notification</h2>
                <p>Dear {employee_name},</p>
                <p>This is to inform you that your late arrival has been recorded for <strong>{date}</strong>.</p>
                <p>Please ensure to arrive on time to maintain productivity and team coordination.</p>
                <p>If you have any concerns or need to discuss your schedule, please contact your supervisor.</p>
                <br>
                <p>Best regards,<br>
                <strong>HR Department</strong><br>
                Employee Attendance System</p>
            </div>
        </body>
        </html>
        """
        return {"subject": subject, "body": body}
    
    @staticmethod
    def leave_request_template(employee_name: str, leave_type: str, start_date: str, end_date: str, reason: str) -> Dict[str, str]:
        """Template for leave request notification to supervisors"""
        subject = f"New Leave Request - {employee_name}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #3498db;">New Leave Request</h2>
                <p>A new leave request has been submitted and requires your approval.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c3e50;">Request Details:</h3>
                    <p><strong>Employee:</strong> {employee_name}</p>
                    <p><strong>Leave Type:</strong> {leave_type.title()}</p>
                    <p><strong>Start Date:</strong> {start_date}</p>
                    <p><strong>End Date:</strong> {end_date}</p>
                    <p><strong>Reason:</strong> {reason}</p>
                </div>
                
                <p>Please review and approve/reject this request in the system.</p>
                <br>
                <p>Best regards,<br>
                <strong>HR System</strong></p>
            </div>
        </body>
        </html>
        """
        return {"subject": subject, "body": body}
    
    @staticmethod
    def leave_approval_template(employee_name: str, leave_type: str, start_date: str, end_date: str, duration: int) -> Dict[str, str]:
        """Template for leave approval notification"""
        subject = "Leave Request Approved"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #27ae60;">Leave Request Approved</h2>
                <p>Dear {employee_name},</p>
                <p>Great news! Your leave request has been approved.</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #27ae60;">
                    <h3 style="margin-top: 0; color: #155724;">Approved Leave Details:</h3>
                    <p><strong>Leave Type:</strong> {leave_type.title()}</p>
                    <p><strong>Start Date:</strong> {start_date}</p>
                    <p><strong>End Date:</strong> {end_date}</p>
                    <p><strong>Duration:</strong> {duration} day(s)</p>
                </div>
                
                <p>Please ensure to complete any pending work and hand over responsibilities before your leave begins.</p>
                <p>Enjoy your time off!</p>
                <br>
                <p>Best regards,<br>
                <strong>HR Department</strong></p>
            </div>
        </body>
        </html>
        """
# ... continuing from previous code

        return {"subject": subject, "body": body}
    
    @staticmethod
    def leave_rejection_template(employee_name: str, leave_type: str, start_date: str, end_date: str, rejection_reason: str) -> Dict[str, str]:
        """Template for leave rejection notification"""
        subject = "Leave Request Rejected"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #e74c3c;">Leave Request Rejected</h2>
                <p>Dear {employee_name},</p>
                <p>We regret to inform you that your leave request has been rejected.</p>
                
                <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #e74c3c;">
                    <h3 style="margin-top: 0; color: #721c24;">Request Details:</h3>
                    <p><strong>Leave Type:</strong> {leave_type.title()}</p>
                    <p><strong>Requested Dates:</strong> {start_date} to {end_date}</p>
                    <p><strong>Reason for Rejection:</strong> {rejection_reason}</p>
                </div>
                
                <p>If you have any questions or would like to discuss this decision, please contact your supervisor or HR department.</p>
                <p>You may also submit a new request with different dates if needed.</p>
                <br>
                <p>Best regards,<br>
                <strong>HR Department</strong></p>
            </div>
        </body>
        </html>
        """
        return {"subject": subject, "body": body}
    
    @staticmethod
    def daily_report_template(date: str, total_employees: int, present: int, absent: int, late: int) -> Dict[str, str]:
        """Template for daily attendance report"""
        subject = f"Daily Attendance Report - {date}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Daily Attendance Report</h2>
                <p><strong>Date:</strong> {date}</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c3e50;">Summary:</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span><strong>Total Employees:</strong></span>
                        <span>{total_employees}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span><strong>Present:</strong></span>
                        <span style="color: #27ae60;">{present}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span><strong>Absent:</strong></span>
                        <span style="color: #e74c3c;">{absent}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span><strong>Late Arrivals:</strong></span>
                        <span style="color: #f39c12;">{late}</span>
                    </div>
                </div>
                
                <p>For detailed information, please check the attendance system.</p>
                <br>
                <p>Best regards,<br>
                <strong>Attendance System</strong></p>
            </div>
        </body>
        </html>
        """
        return {"subject": subject, "body": body}
