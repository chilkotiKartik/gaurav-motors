import sys
from app import app

# Enable debug mode for Flask
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True

with app.app_context():
    with app.test_request_context():
        try:
            from flask import render_template
            print("DEBUG: Importing template...")
            result = render_template('hms/spare_parts_new.html')
            print(f"SUCCESS: Template rendered, length={len(result)}")
        except Exception as e:
            print(f"ERROR: {type(e).__name__}")
            print(f"Message: {str(e)}")
            import traceback
            traceback.print_exc()
