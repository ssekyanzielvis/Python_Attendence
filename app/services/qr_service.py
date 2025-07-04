import qrcode
import io
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.qr_code import QRCode
from ..config.settings import settings
from ..utils.exceptions import ValidationError

class QRService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_qr_code(self, location_name: str, latitude: float, longitude: float) -> QRCode:
        """Generate a new QR code for a location"""
        
        # Create unique code
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        code = f"{settings.QR_CODE_PREFIX}{location_name.upper()}_{timestamp}"
        
        qr_data = {
            "code": code,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "is_active": True
        }
        
        qr_code_obj = QRCode(**qr_data)
        self.db.add(qr_code_obj)
        self.db.commit()
        self.db.refresh(qr_code_obj)
        
        return qr_code_obj
    
# ... continuing from previous code

    def generate_qr_image(self, qr_code_data: str) -> str:
        """Generate QR code image as base64 string"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def validate_qr_code(self, code: str) -> bool:
        """Validate QR code"""
        qr_code = self.db.query(QRCode).filter(
            QRCode.code == code,
            QRCode.is_active == True
        ).first()
        
        if not qr_code:
            return False
        
        # Check if QR code is expired (optional)
        expiry_time = qr_code.created_at + timedelta(hours=settings.QR_CODE_EXPIRY_HOURS)
        if datetime.utcnow() > expiry_time:
            return False
        
        return True
    
    def get_qr_code_by_code(self, code: str) -> Optional[QRCode]:
        """Get QR code by code string"""
        return self.db.query(QRCode).filter(QRCode.code == code).first()
    
    def deactivate_qr_code(self, qr_code_id: str) -> bool:
        """Deactivate a QR code"""
        qr_code = self.db.query(QRCode).filter(QRCode.id == qr_code_id).first()
        if qr_code:
            qr_code.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_active_qr_codes(self) -> list[QRCode]:
        """Get all active QR codes"""
        return self.db.query(QRCode).filter(QRCode.is_active == True).all()

