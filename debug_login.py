#!/usr/bin/env python3
"""Debug login error"""
import sys
sys.path.insert(0, '.')

from app import app, db, User
from werkzeug.security import check_password_hash

# Enable debug mode
app.config['DEBUG'] = True

print("=" * 60)
print("🔍 Debugging Login Issue")
print("=" * 60)

with app.app_context():
    print("\n1. Checking database connection...")
    try:
        # Test database
        user_count = User.query.count()
        print(f"   ✓ Database connected. Users: {user_count}")
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        sys.exit(1)
    
    print("\n2. Checking admin user...")
    try:
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"   ✓ Admin user found")
            print(f"     - Username: {admin.username}")
            print(f"     - Role: {admin.role}")
            print(f"     - Password hash: {admin.password_hash[:20]}...")
        else:
            print("   ✗ Admin user not found")
            all_users = User.query.all()
            print(f"   Total users: {len(all_users)}")
            for user in all_users:
                print(f"     - {user.username} ({user.role})")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n3. Testing login endpoint...")
print("   Starting Flask server for testing...\n")

# Start the app in a test mode
with app.test_client() as client:
    try:
        # Get login page
        response = client.get('/login')
        print(f"   ✓ GET /login: {response.status_code}")
        
        # Try to post login
        print("   • Posting login credentials...")
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'Admin@123456'
        }, follow_redirects=False)
        
        print(f"   ✓ POST /login: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ✓ Redirect location: {response.location}")
        elif response.status_code != 200:
            print(f"   ✗ Unexpected response")
            print(f"   Response: {response.data.decode()[:500]}")
    except Exception as e:
        print(f"   ✗ Error during login test: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
