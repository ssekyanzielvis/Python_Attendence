from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from ..config.database import Base

class NotificationType(enum.Enum):
    ATTENDANCE = "attendance"
    LEAVE = "leave"
    SYSTEM = "system"
    REMINDER = "reminder"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="notifications")
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "employee_id": str(self.employee_id),
            "title": self.title,
            "message": self.message,
            "type": self.type.value,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat()
        }
