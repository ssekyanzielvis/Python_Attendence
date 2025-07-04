#!/usr/bin/env python3
"""
Script to run tests with coverage reporting
"""
import subprocess
import sys
import os

def run_tests():
    """Run tests with coverage"""
    try:
        # Install test dependencies
        print("Installing test dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov", "httpx"], check=True)
        
        # Run tests with coverage
        print("Running tests with coverage...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "app/tests/", 
            "-v", 
            "--cov=app", 
            "--cov-report=html", 
            "--cov-report=term-missing"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print("\n❌ Some tests failed!")
            
        return result.returncode
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
