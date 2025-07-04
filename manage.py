#!/usr/bin/env python3
"""
Management script for Employee Attendance System
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.cli.commands import cli

if __name__ == '__main__':
    cli()
