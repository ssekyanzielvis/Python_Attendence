from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..services.auth_service import AuthService
from ..repositories.employee_repository import EmployeeRepository
from ..models.employee import EmployeeRole
from ..services.qr_service import QRService
import logging

logger = logging.getLogger(__name__)

class DatabaseSeeder:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.employee_repo = EmployeeRepository(self.db)
        self.auth_service = AuthService(self.db)
        self.qr_service = QRService(self.db)
    
    def seed_admin_user(self):
        """Create default admin user"""
        try:
            # Check if admin already exists
            admin = self.employee_repo.get_by_email("admin@company.com")
            if admin:
                logger.info("Admin user already exists")
                return
            
            password_hash = self.auth_service.get_password_hash("admin123")
            
            admin_data = {
                'employee_code': 'ADMIN001',
                'email': 'admin@company.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'department': 'IT',
                'position': 'System Administrator',
                'role': EmployeeRole.ADMIN,
                'password_hash': password_hash,
                'is_active': True
            }
            
            admin = self.employee_repo.create(admin_data)
            logger.info(f"Admin user created: {admin.email}")
            
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
    
    def seed_sample_employees(self):
        """Create sample employees for testing"""
        try:
            sample_employees = [
                {
                    'employee_code': 'EMP001',
                    'email': 'john.doe@company.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'department': 'Engineering',
                    'position': 'Software Developer',
                    'role': EmployeeRole.EMPLOYEE,
                    'password': 'password123'
                },
                {
                    'employee_code': 'SUP001',
                    'email': 'jane.smith@company.com',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'department': 'Engineering',
                    'position': 'Team Lead',
                    'role': EmployeeRole.SUPERVISOR,
                    'password': 'password123'
                },
                {
                    'employee_code': 'EMP002',
                    'email': 'bob.johnson@company.com',
                    'first_name': 'Bob',
                    'last_name': 'Johnson',
                    'department': 'Marketing',
                    'position': 'Marketing Specialist',
                    'role': EmployeeRole.EMPLOYEE,
                    'password': 'password123'
                }
            ]
            
            for emp_data in sample_employees:
                # Check if employee already exists
                if self.employee_repo.get_by_email(emp_data['email']):
                    continue
                
                password = emp_data.pop('password')
                password_hash = self.auth_service.get_password_hash(password)
                emp_data['password_hash'] = password_hash
                emp_data['is_active'] = True
                
                employee = self.employee_repo.create(emp_data)
                logger.info(f"Sample employee created: {employee.email}")
                
        except Exception as e:
            logger.error(f"Error creating sample employees: {str(e)}")
    
    def seed_qr_codes(self):
        """Create sample QR codes"""
        try:
            qr_locations = [
                {
                    'location_name': 'Main Office',
                    'latitude': 40.7128,
                    'longitude': -74.0060
                },
                {
                    'location_name': 'Branch Office',
                    'latitude': 40.7589,
                    'longitude': -73.9851
                }
            ]
            
            for location in qr_locations:
                qr_code = self.qr_service.generate_qr_code(
                    location['location_name'],
                    location['latitude'],
                    location['longitude']
                )
                logger.info(f"QR code created for {location['location_name']}")
                
        except Exception as e:
            logger.error(f"Error creating QR codes: {str(e)}")
    
    def seed_all(self):
        """Seed all data"""
        logger.info("Starting database seeding...")
        
        self.seed_admin_user()
        self.seed_sample_employees()
        self.seed_qr_codes()
        
        logger.info("Database seeding completed")
        self.db.close()

def seed_database():
    """Function to seed the database"""
    seeder = DatabaseSeeder()
    seeder.seed_all()

if __name__ == "__main__":
    seed_database()
