#!/bin/bash

# Employee Attendance System Start Script

set -e

echo "🚀 Starting Employee Attendance System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create one from .env.example"
    exit 1
fi

# Start database if using Docker
if command -v docker &> /dev/null && [ -f "docker-compose.yml" ]; then
    echo "🐳 Starting database services..."
    docker-compose up -d db redis
    sleep 3
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Start the application
echo "🌟 Starting the application..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API Documentation at: http://localhost:8000/docs"
echo "🔍 Alternative docs at: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
