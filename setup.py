#!/usr/bin/env python3
"""
Quick Setup & Verification Script for Gaurav Motors
Ensures all dependencies are installed and the application is ready to run
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher required!")
        return False
    print("✅ Python version OK")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Checking Dependencies")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_mail',
        'werkzeug',
        'python-dotenv',
        'pillow',
        'reportlab',
        'pandas',
        'razorpay'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating Required Directories")
    
    directories = ['uploads', 'instance', 'logs', 'backups']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}/")
        else:
            print(f"✓  Exists: {directory}/")
    
    return True

def check_env_file():
    """Check if .env file exists"""
    print_header("Checking Environment Configuration")
    
    if Path('.env').exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        if Path('.env.example').exists():
            print("\nCreating .env from .env.example...")
            
            # Copy .env.example to .env
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  IMPORTANT: Edit .env with your actual configuration!")
            return True
        else:
            print("❌ .env.example not found")
            return False

def check_database():
    """Check if database exists"""
    print_header("Checking Database")
    
    if Path('hms.db').exists():
        print("✅ Database file found: hms.db")
        return True
    else:
        print("⚠️  Database not initialized")
        print("Run: python init_automotive_db.py")
        return False

def check_app_file():
    """Check if app.py exists and is valid"""
    print_header("Checking Application Files")
    
    if not Path('app.py').exists():
        print("❌ app.py not found!")
        return False
    
    print("✅ app.py found")
    
    # Check for syntax errors
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'app.py', 'exec')
        print("✅ No syntax errors in app.py")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False

def run_quick_test():
    """Run a quick import test"""
    print_header("Running Quick Test")
    
    try:
        print("Testing Flask app import...")
        import app as flask_app
        print("✅ Flask app imports successfully")
        
        print("Testing database models...")
        from app import db, User, CustomerProfile, TechnicianProfile
        print("✅ Database models import successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def display_next_steps(all_good):
    """Display next steps"""
    print_header("Setup Summary")
    
    if all_good:
        print("🎉 All checks passed! Your application is ready to run.\n")
        print("Next steps:")
        print("1. Review and update .env with your configuration")
        print("2. Initialize database: python init_automotive_db.py")
        print("3. Start application: python start.py")
        print("4. Access at: http://localhost:5000\n")
        print("Default admin credentials:")
        print("   Username: admin")
        print("   Password: Admin@123456")
        print("\n⚠️  CHANGE ADMIN PASSWORD AFTER FIRST LOGIN!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file from .env.example")
        print("3. Initialize database: python init_automotive_db.py")

def main():
    """Main setup function"""
    print("\n🚗 GAURAV MOTORS - Setup & Verification")
    print("=" * 60)
    
    checks = []
    
    # Run all checks
    checks.append(check_python_version())
    checks.append(check_dependencies())
    checks.append(create_directories())
    checks.append(check_env_file())
    checks.append(check_app_file())
    checks.append(check_database())
    
    # Only run import test if basic checks passed
    if all(checks):
        checks.append(run_quick_test())
    
    # Display results
    all_good = all(checks)
    display_next_steps(all_good)
    
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())
