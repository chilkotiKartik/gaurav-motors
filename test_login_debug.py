#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app import app
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Enable Flask debug mode to get better error messages
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

print("Testing login with debug enabled...\n")

with app.test_client() as client:
    try:
        print("1. Getting login page...")
        response = client.get('/login')
        print(f"   ✓ Status: {response.status_code}\n")
        
        print("2. Attempting login...")
        print("   Username: admin")
        print("   Password: Admin@123456")
        
        response = client.post('/login', 
            data={'username': 'admin', 'password': 'Admin@123456'},
            follow_redirects=False
        )
        
        print(f"\n   ✓ Status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ✓ SUCCESS! Redirected to: {response.location}")
        else:
            print(f"   Response: {response.data.decode()[:1000]}")
                
    except Exception as e:
        print(f"\n✗ Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
