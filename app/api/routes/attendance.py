from sqlalchemy import Column, String, DateTime, Enum, Float, Text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid
import enum
from ..config.database import Base

class AttendanceStatus(enum.Enum):
    EARLY = "early"
    ON_TIME = "on_time"
    LATE = "late"
    ABSENT = "absent"
    PLANNED_ABSENCE = "planned_absence"
    ON_LEAVE = "on_leave"

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    status = Column(Enum(AttendanceStatus), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    qr_code_data = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")
    
    @property
    def hours_worked(self):
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return round(delta.total_seconds() / 3600, 2)
        return 0
    
    @property
    def is_late(self):
        return self.status == AttendanceStatus.LATE
    
    @property
    def is_present(self):
        return self.status in [AttendanceStatus.EARLY, AttendanceStatus.ON_TIME, AttendanceStatus.LATE]
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "employee_id": str(self.employee_id),
            "date": self.date.isoformat(),
            "check_in_time": self.check_in_time.isoformat() if self.check_in_time else None,
            "check_out_time": self.check_out_time.isoformat() if self.check_out_time else None,
            "status": self.status.value,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "qr_code_data": self.qr_code_data,
            "notes": self.notes,
            "hours_worked": self.hours_worked,
            "is_late": self.is_late,
            "is_present": self.is_present,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
