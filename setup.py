#!/usr/bin/env python3
"""
Pet Management System - Setup Script
Automated setup and installation script
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print setup header"""
    print("🐕 Pet Management System Setup")
    print("=" * 50)
    print("This script will help you set up the Pet Management System")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    print("\nSetting up environment file...")
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_example.txt'):
        try:
            with open('env_example.txt', 'r') as src:
                content = src.read()
            
            with open('.env', 'w') as dst:
                dst.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your database credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def setup_database():
    """Setup database"""
    print("\nDatabase setup options:")
    print("1. Use SQL script (create_tables.sql)")
    print("2. Use Flask-Migrate")
    print("3. Skip database setup")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        print("📝 Please run the following commands manually:")
        print("   mysql -u root -p")
        print("   CREATE DATABASE pet_management;")
        print("   exit")
        print("   mysql -u root -p pet_management < create_tables.sql")
        return True
    elif choice == "2":
        print("📝 Please run the following commands manually:")
        print("   flask db init")
        print("   flask db migrate -m 'Initial migration'")
        print("   flask db upgrade")
        return True
    elif choice == "3":
        print("⏭️  Skipping database setup")
        return True
    else:
        print("❌ Invalid choice")
        return False

def seed_database():
    """Ask if user wants to seed database"""
    print("\nWould you like to populate the database with sample data?")
    choice = input("This will add sample pets, donations, and users (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        try:
            print("Seeding database with sample data...")
            subprocess.check_call([sys.executable, "seed_data.py"])
            print("✅ Database seeded successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to seed database: {e}")
            return False
    else:
        print("⏭️  Skipping database seeding")
        return True

def run_tests():
    """Ask if user wants to run tests"""
    print("\nWould you like to run the test suite?")
    choice = input("This will verify the installation (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        try:
            print("Running tests...")
            subprocess.check_call([sys.executable, "run_tests.py"])
            print("✅ All tests passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False
    else:
        print("⏭️  Skipping tests")
        return True

def print_final_instructions():
    """Print final setup instructions"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("To start the application:")
    print("  python run.py")
    print("  or")
    print("  flask run")
    print("\nThe application will be available at: http://localhost:5000")
    print("\nDefault login credentials:")
    print("  Admin: admin / password123")
    print("  Employee: employee1 / password123")
    print("\nFor more information, see README.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Seed database
    if not seed_database():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup can continue")
    
    # Print final instructions
    print_final_instructions()

if __name__ == '__main__':
    main()
