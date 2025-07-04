#!/bin/bash

# Employee Attendance System Setup Script

set -e

echo "🚀 Setting up Employee Attendance System..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set up environment variables
echo "🔧 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from template. Please update with your settings."
else
    echo "✅ .env file already exists"
fi

# Set up database
echo "🗄️ Setting up database..."
if command -v docker &> /dev/null; then
    echo "🐳 Starting PostgreSQL with Docker..."
    docker-compose up -d db
    sleep 5
else
    echo "⚠️ Docker not found. Please ensure PostgreSQL is running manually."
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Seed database
echo "🌱 Seeding database with initial data..."
python -c "from app.utils.database_seeder import seed_database; seed_database()"

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your configuration"
echo "3. Start the application: uvicorn app.main:app --reload"
echo "4. Visit http://localhost:8000 to see the API"
echo "5. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "👤 Default admin credentials:"
echo "   Email: admin@company.com"
echo "   Password: admin123"
