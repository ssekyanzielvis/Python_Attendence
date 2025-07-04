# Employee Attendance System

A comprehensive employee attendance management system built with FastAPI, featuring QR code and location-based check-in/out functionality.

## 🚀 Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Attendance Tracking**: Location-based and QR code check-in/out
- **Leave Management**: Leave request submission and approval workflow
- **Employee Management**: Complete CRUD operations for employee data
- **Real-time Notifications**: System notifications for various events
- **Reporting**: Comprehensive attendance reports and analytics
- **QR Code Generation**: Dynamic QR codes for different office locations
- **Automated Tasks**: Scheduled tasks for marking absent employees and generating reports

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **Caching**: Redis (optional)
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Task Scheduling**: APScheduler
- **Testing**: Pytest
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL 12+
- Redis (optional, for caching)
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Option 1: Using Setup Script (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd employee-attendance-system

# Make scripts executable
chmod +x scripts/*.sh

# Run setup script
./scripts/setup.sh

# Start the application
./scripts/start.sh
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone <repository-url>
cd employee-attendance-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start PostgreSQL (using Docker)
docker-compose up -d db

# Run database migrations
alembic upgrade head

# Seed database with initial data
python -c "from app.utils.database_seeder import seed_database; seed_database()"

# Start the application
uvicorn app.main:app --reload
```

### Option 3: Using Docker

```bash
# Clone the repository
git clone <repository-url>
cd employee-attendance-system

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head

# Seed database
docker-compose exec app python -c "from app.utils.database_seeder import seed_database; seed_database()"
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 👤 Default Credentials

After seeding the database, you can use these default credentials:

- **Admin User**:
  - Email: `admin@company.com`
  - Password: `admin123`

## 🔧 Configuration

The application can be configured using environment variables. Copy `.env.example` to `.env` and modify the values:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/attendance_db

# JWT
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Work Hours
WORK_START_HOUR=9
WORK_END_HOUR=17

# Location Validation
ALLOWED_RADIUS_METERS=100
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_auth.py

# Run tests using the script
python run_tests.py
```

## 📊 Database Management

### Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### CLI Commands

```bash
# Create admin user
python manage.py create-admin

# Reset user password
python manage.py reset-password

# List all employees
python manage.py list-employees

# Deactivate employee
python manage.py deactivate-employee
```

## 🔄 Backup & Restore

```bash
# Create backup
./scripts/backup.sh

# Restore from backup
psql -h localhost -U postgres attendance_db < backups/attendance_backup_YYYYMMDD_HHMMSS.sql
```

## 🚀 Deployment

### Production Deployment

```bash
# Deploy using Docker
./scripts/deploy.sh

# Or manually
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production

````env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@prod-db:5432/attendance_db
# ... continuing from previous README.md content

# Enable production features
ENABLE_EMAIL_NOTIFICATIONS=True
ENABLE_SCHEDULER=True

# SMTP Configuration
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USERNAME=your-email@company.com
SMTP_PASSWORD=your-app-password
```

## 📱 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/change-password` - Change password

### Employees
- `GET /api/v1/employees/` - List employees (Admin)
- `POST /api/v1/employees/` - Create employee (Admin)
- `GET /api/v1/employees/{id}` - Get employee details
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Deactivate employee (Admin)

### Attendance
- `POST /api/v1/attendance/check-in` - Check in
- `POST /api/v1/attendance/check-out` - Check out
- `GET /api/v1/attendance/today` - Today's attendance
- `GET /api/v1/attendance/history` - Attendance history
- `GET /api/v1/attendance/reports/monthly` - Monthly report (Admin)

### Leave Management
- `POST /api/v1/leaves/request` - Submit leave request
- `GET /api/v1/leaves/` - Get leave requests
- `GET /api/v1/leaves/balance` - Get leave balance
- `PUT /api/v1/leaves/{id}/approve` - Approve leave (Supervisor)
- `PUT /api/v1/leaves/{id}/reject` - Reject leave (Supervisor)

### QR Codes
- `POST /api/v1/qr-codes/generate` - Generate QR code (Admin)
- `GET /api/v1/qr-codes/` - List QR codes (Admin)
- `POST /api/v1/qr-codes/validate` - Validate QR code
- `DELETE /api/v1/qr-codes/{id}` - Deactivate QR code (Admin)

## 🏗️ Project Structure

```
employee-attendance-system/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── employees.py
│   │   │   │   ├── attendance.py
│   │   │   │   ├── leaves.py
│   │   │   │   └── qr_codes.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── config/
│   │   ├── database.py
│   │   └── settings.py
│   ├── models/
│   │   ├── attendance.py
│   │   ├── employee.py
│   │   ├── leave_request.py
│   │   ├── notification.py
│   │   └── qr_code.py
│   ├── repositories/
│   │   ├── attendance_repository.py
│   │   ├── employee_repository.py
│   │   ├── leave_repository.py
│   │   └── qr_code_repository.py
│   ├── schemas/
│   │   ├── attendance.py
│   │   ├── employee.py
│   │   ├── leave.py
│   │   └── qr_code.py
│   ├── services/
│   │   ├── attendance_service.py
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── leave_service.py
│   │   ├── notification_service.py
│   │   └── qr_service.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_attendance.py
│   │   ├── test_employees.py
│   │   ├── test_leaves.py
│   │   └── test_qr_codes.py
│   ├── utils/
│   │   ├── database_seeder.py
│   │   ├── email_templates.py
│   │   ├── helpers.py
│   │   ├── scheduler.py
│   │   └── validators.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── scripts/
│   ├── setup.sh
│   ├── start.sh
│   ├── deploy.sh
│   └── backup.sh
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── alembic.ini
├── manage.py
├── run_tests.py
└── README.md
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for password security
- **Role-based Access Control**: Different permissions for different roles
- **Location Validation**: GPS-based attendance verification
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input validation and sanitization

## 📈 Monitoring & Logging

The application includes comprehensive logging:

```python
# View logs
tail -f logs/attendance.log

# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use type hints
- Run linting tools before committing

```bash
# Format code
black app/
isort app/

# Run linting
flake8 app/
mypy app/

# Run security checks
bandit -r app/
safety check
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart database
   docker-compose restart db
   ```

2. **Migration Issues**
   ```bash
   # Reset migrations (development only)
   alembic downgrade base
   alembic upgrade head
   ```

3. **Permission Denied**
   ```bash
   # Make scripts executable
   chmod +x scripts/*.sh
   ```

4. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   ```

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Review the test files for usage examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for the powerful ORM
- PostgreSQL for the robust database
- All contributors and users of this project

---

**Made with ❤️ for efficient attendance management**
```

```txt:requirements.txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation & Serialization
pydantic==2.5.0
pydantic-settings==2.1.0

# Date & Time
python-dateutil==2.8.2

# Location & Maps
geopy==2.4.0

# QR Code Generation
qrcode[pil]==7.4.2

# Email
aiosmtplib==3.0.1
jinja2==3.1.2

# Caching (Optional)
redis==5.0.1
aioredis==2.0.1

# Task Scheduling
apscheduler==3.10.4

# HTTP Client
httpx==0.25.2

# Environment Variables
python-dotenv==1.0.0

# Logging
structlog==23.2.0

# Image Processing
Pillow==10.1.0

# Development Dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1
bandit==1.7.5
safety==2.3.5

# Documentation
mkdocs==1.5.3
mkdocs-material==9.4.8
```

```txt:LICENSE
MIT License

Copyright (c) 2024 Employee Attendance System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

```yaml:docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-attendance_db}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - attendance_network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    networks:
      - attendance_network
    restart: unless-stopped

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL:-redis://redis:6379}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
    depends_on:
      - db
      - redis
    networks:
      - attendance_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - attendance_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  attendance_network:
    driver: bridge
```

```nginx:nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            access_log off;
            proxy_pass http://app;
        }
    }
}
```

This completes the comprehensive Employee Attendance System! The system includes:

## 🎯 **Key Features Implemented:**

1. **Complete Authentication System** with JWT tokens
2. **Location-based Attendance** with GPS validation
3. **QR Code Check-in/out** functionality
4. **Leave Management** with approval workflow
5. **Employee Management** with role-based access
6. **Real-time Notifications** system
7. **Comprehensive Reporting** and analytics
8. **Automated Scheduling** for daily tasks
9. **Email Notifications** for important events
10. **Complete Test Suite** with high coverage

## 🚀 **Production Ready Features:**

- Docker containerization
- Database migrations with Alembic
- CI/CD pipeline with GitHub Actions
- Security best practices
- Comprehensive logging
- Backup and restore scripts
- Production deployment configuration
- Nginx reverse proxy setup
- SSL/HTTPS support

## 📱 **API Capabilities:**

- RESTful API design
- OpenAPI/Swagger documentation
- Input validation and error handling
- Rate limiting and security measures
- Comprehensive test coverage

The system is now ready for deployment and can handle real-world attendance management requirements for organizations of various sizes!
