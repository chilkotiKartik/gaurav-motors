#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app import app

print("Testing login route with exception capture...")

# Override error handling to see actual exceptions
@app.errorhandler(Exception)
def handle_error(e):
    print(f"\n!!! EXCEPTION CAUGHT !!!")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    traceback.print_exc()
    raise

with app.test_client() as client:
    try:
        print("\nPosting login...\n")
        response = client.post('/login', 
            data={'username': 'admin', 'password': 'Admin@123456'},
            follow_redirects=False
        )
        print(f"Response status: {response.status_code}")
    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()
