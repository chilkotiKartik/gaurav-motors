#!/usr/bin/env python3
"""Captures the exact exception from login POST"""
import sys, os, traceback as tb
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User

app.config['TESTING'] = True
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

with app.app_context():
    # Step 1: Check DB has admin user
    try:
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"[OK] Admin user exists, role={admin.role}")
            print(f"[OK] Password check: {admin.check_password('Admin@123456')}")
        else:
            print("[FAIL] No admin user in DB!")
            print("  Users:", [u.username for u in User.query.all()])
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] DB query error: {e}")
        tb.print_exc()
        sys.exit(1)

# Step 2: Test POST /login with test client (catches exceptions)
print("\n--- Testing POST /login ---")
with app.test_client() as client:
    try:
        resp = client.post('/login',
            data={'username': 'admin', 'password': 'Admin@123456'},
            follow_redirects=False)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 302:
            print(f"[OK] Redirect to: {resp.headers.get('Location')}")
        elif resp.status_code == 500:
            print(f"[FAIL] 500 error!")
            print(resp.data.decode()[:2000])
        else:
            # Check if it's the login page (invalid credentials)
            data = resp.data.decode()
            if 'Invalid credentials' in data:
                print("[FAIL] Invalid credentials - password mismatch")
            else:
                print(f"[INFO] Got {resp.status_code}, checking response...")
                print(data[:500])
    except Exception as e:
        print(f"[FAIL] Exception: {type(e).__name__}: {e}")
        tb.print_exc()

# Step 3: Test login + follow redirect to admin_dashboard
print("\n--- Testing login + redirect to admin dashboard ---")
with app.test_client() as client:
    try:
        resp = client.post('/login',
            data={'username': 'admin', 'password': 'Admin@123456'},
            follow_redirects=True)
        print(f"Final status: {resp.status_code}")
        if resp.status_code == 500:
            print("[FAIL] 500 on admin dashboard!")
            # The error is in the HTML
            data = resp.data.decode()
            if 'Traceback' in data:
                start = data.index('Traceback')
                print(data[start:start+2000])
            else:
                print(data[:1000])
        elif resp.status_code == 200:
            print("[OK] Admin dashboard loaded successfully")
    except Exception as e:
        print(f"[FAIL] Exception: {type(e).__name__}: {e}")
        tb.print_exc()
