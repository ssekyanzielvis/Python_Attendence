#!/bin/bash

# Database Backup Script

set -e

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="attendance_backup_$DATE.sql"

echo "💾 Creating database backup..."

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create database backup
if command -v docker &> /dev/null && docker-compose ps db | grep -q "Up"; then
    echo "🐳 Creating backup from Docker container..."
    docker-compose exec -T db pg_dump -U postgres attendance_db > "$BACKUP_DIR/$BACKUP_FILE"
else
    echo "🗄️ Creating backup from local PostgreSQL..."
    pg_dump -h localhost -U postgres attendance_db > "$BACKUP_DIR/$BACKUP_FILE"
fi

# Compress backup
echo "🗜️ Compressing backup..."
gzip "$BACKUP_DIR/$BACKUP_FILE"

echo "✅ Backup created: $BACKUP_DIR/$BACKUP_FILE.gz"

# Clean up old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find $BACKUP_DIR -name "attendance_backup_*.sql.gz" -mtime +7 -delete

echo "✅ Backup process completed!"
