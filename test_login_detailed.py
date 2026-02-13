#!/usr/bin/env python3
"""Test login with error details"""
import sys
sys.path.insert(0, '.')

import traceback
from app import app

print("Testing login endpoint with Flask test client...\n")

with app.test_client() as client:
    try:
        # First get the login page
        response = client.get('/login')
        print(f"✓ GET /login: {response.status_code}")
        
        # Try to post login
        print("\nAttempting POST /login...")
        print("  Username: admin")
        print("  Password: admin123")
        
        response = client.post('/login', 
            data={'username': 'admin', 'password': 'admin123'},
            follow_redirects=False
        )
        
        print(f"\n✓ POST /login: {response.status_code}")
        
        if response.status_code == 302:
            print(f"✓ Redirected to: {response.location}")
        else:
            print(f"\n✗ Unexpected status code: {response.status_code}")
            print(f"Response: {response.data.decode()[:500]}")
                
    except Exception as e:
        print(f"\n✗ Exception occurred:")
        print(f"  {type(e).__name__}: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
