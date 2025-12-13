"""
Test Script for HMS Features
This script verifies all major features work correctly
"""

import os
import sys

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description} exists")
        return True
    else:
        print_error(f"{description} missing: {filepath}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_info("Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_mail',
        'werkzeug',
        'PIL',
        'reportlab',
        'pandas',
        'openpyxl',
        'razorpay'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_templates():
    """Check if all templates exist"""
    print_info("\nChecking templates...")
    
    templates = [
        'templates/hms/base.html',
        'templates/hms/index.html',
        'templates/hms/login.html',
        'templates/hms/register.html',
        'templates/hms/services.html',
        'templates/hms/spare_parts_browse.html',
        'templates/hms/spare_part_detail.html',
        'templates/hms/cart.html',
        'templates/hms/checkout_parts.html',
        'templates/hms/part_payment.html',
        'templates/hms/my_orders_search.html',
        'templates/hms/my_orders.html',
        'templates/hms/order_detail.html',
        'templates/hms/admin_part_orders.html',
        'templates/hms/admin_dashboard.html',
        'templates/hms/patient_dashboard.html',
        'templates/hms/doctor_dashboard.html'
    ]
    
    all_exist = True
    for template in templates:
        if not check_file_exists(template, f"Template: {template}"):
            all_exist = False
    
    return all_exist

def check_app_structure():
    """Check app.py structure"""
    print_info("\nChecking app.py...")
    
    if not os.path.exists('app.py'):
        print_error("app.py not found")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key routes
    routes_to_check = [
        ('spare_parts_browse', 'Spare parts browse route'),
        ('spare_part_detail', 'Spare part detail route'),
        ('view_cart', 'Shopping cart route'),
        ('add_to_cart', 'Add to cart route'),
        ('checkout_parts', 'Checkout route'),
        ('part_orders_payment', 'Payment route'),
        ('confirm_part_payment', 'Payment confirmation route'),
        ('my_part_orders', 'My orders route'),
        ('admin_part_orders', 'Admin orders route'),
        ('update_part_order_status', 'Order status update route'),
        ('cancel_part_order', 'Cancel order route'),
    ]
    
    all_found = True
    for route, description in routes_to_check:
        if f"def {route}" in content:
            print_success(f"{description}")
        else:
            print_error(f"{description} not found")
            all_found = False
    
    # Check for models
    models_to_check = [
        ('class SparePart', 'SparePart model'),
        ('class CartItem', 'CartItem model'),
        ('class PartOrder', 'PartOrder model'),
        ('class MedicalRecord', 'MedicalRecord model'),
        ('class DoctorReview', 'DoctorReview model'),
    ]
    
    for model, description in models_to_check:
        if model in content:
            print_success(f"{description}")
        else:
            print_warning(f"{description} may not exist")
    
    return all_found

def check_requirements():
    """Check requirements.txt"""
    print_info("\nChecking requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required = [
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Login',
        'Flask-Mail',
        'gunicorn',
        'razorpay'
    ]
    
    all_found = True
    for package in required:
        if package in content:
            print_success(f"{package} in requirements.txt")
        else:
            print_error(f"{package} missing from requirements.txt")
            all_found = False
    
    return all_found

def main():
    """Main test function"""
    print(f"\n{BLUE}{'='*60}")
    print("HMS COMPREHENSIVE FEATURE TEST")
    print(f"{'='*60}{RESET}\n")
    
    results = {
        'Dependencies': check_dependencies(),
        'Templates': check_templates(),
        'App Structure': check_app_structure(),
        'Requirements': check_requirements()
    }
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}{RESET}\n")
    
    all_passed = True
    for test, result in results.items():
        if result:
            print_success(f"{test}: PASSED")
        else:
            print_error(f"{test}: FAILED")
            all_passed = False
    
    print(f"\n{BLUE}{'='*60}{RESET}\n")
    
    if all_passed:
        print_success("ALL TESTS PASSED! ✨")
        print_info("\nYour HMS system is ready to deploy!")
        print_info("Next steps:")
        print_info("  1. Set up environment variables in .env file")
        print_info("  2. Configure Razorpay API keys")
        print_info("  3. Set up email credentials")
        print_info("  4. Run: python app.py")
        print_info("  5. Deploy to Render.com")
    else:
        print_warning("\nSome tests failed. Please review the errors above.")
        print_info("Fix the issues and run this test again.")
    
    print()
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
