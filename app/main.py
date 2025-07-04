from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from .config.database import engine, Base
from .api.routes import auth, attendance, leaves, employees, notifications, qr_codes
from .utils.exceptions import ValidationError, BusinessLogicError, AuthenticationError
from .config.settings import settings

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Employee Attendance System...")
    yield
    # Shutdown
    print("Shutting down Employee Attendance System...")

app = FastAPI(
    title="Employee Attendance System",
    description="A comprehensive employee attendance management system with QR code and location-based check-in/out",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(attendance.router, prefix="/api/v1")
app.include_router(leaves.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(qr_codes.router, prefix="/api/v1")

# Global exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "validation_error"}
    )

@app.exception_handler(BusinessLogicError)
async def business_logic_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "business_logic_error"}
    )

@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc), "type": "authentication_error"}
    )

@app.get("/")
async def root():
    return {
        "message": "Employee Attendance System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
