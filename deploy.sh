#!/bin/bash

# Employee Attendance System Deployment Script

set -e

echo "🚀 Deploying Employee Attendance System..."

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t attendance-system:latest .

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start services
echo "▶️ Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec app alembic upgrade head

# Seed database if needed
echo "🌱 Seeding database..."
docker-compose exec app python -c "from app.utils.database_seeder import seed_database; seed_database()"

echo "✅ Deployment completed successfully!"
echo "🌐 Application is running at: http://localhost:8000"
