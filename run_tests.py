#!/usr/bin/env python3
"""
Pet Management System - Test Runner
Run this file to execute all tests
"""

import sys
import os
import subprocess

def run_tests():
    """Run all tests using pytest"""
    print("🧪 Running Pet Management System Tests")
    print("=" * 50)
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("❌ pytest is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
        print("✅ pytest installed successfully")
    
    # Set environment variables for testing
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['FLASK_DEBUG'] = 'False'
    
    # Run tests
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], check=True)
        
        print("\n✅ All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
