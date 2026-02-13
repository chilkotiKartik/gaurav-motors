#!/usr/bin/env python3
"""
Enhanced Start Script for Gaurav Motors
Includes automatic setup, error checking, and helpful messages
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Quick setup check before starting"""
    print("🚗 Starting Gaurav Motors Application...")
    print("=" * 60)
    
    # Check .env file
    if not Path('.env').exists():
        print("⚠️  .env file not found!")
        print("Creating from .env.example...")
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ .env created. Please update with your configuration.")
        else:
            print("❌ .env.example not found. Using defaults.")
    
    # Check database
    if not Path('hms.db').exists():
        print("\n⚠️  Database not found. Initializing...")
        try:
            import init_automotive_db
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"⚠️  Could not auto-initialize database: {e}")
            print("Please run: python init_automotive_db.py")
    
    # Create required directories
    for directory in ['uploads', 'instance', 'logs']:
        Path(directory).mkdir(exist_ok=True)
    
    print("=" * 60)

def main():
    """Start the Flask application"""
    try:
        # Run setup check
        check_setup()
        
        # Import and run Flask app
        from app import app, db
        
        # Get configuration
        debug = os.environ.get('FLASK_DEBUG', '1') == '1'
        host = os.environ.get('FLASK_HOST', '127.0.0.1')
        port = int(os.environ.get('FLASK_PORT', 5000))
        
        print(f"\n🚀 Starting server...")
        print(f"   URL: http://{host}:{port}")
        print(f"   Debug: {debug}")
        print(f"\n👤 Default Admin Login:")
        print(f"   Username: admin")
        print(f"   Password: Admin@123456")
        print(f"\n⚠️  CHANGE ADMIN PASSWORD AFTER FIRST LOGIN!")
        print(f"\n Press CTRL+C to stop the server\n")
        print("=" * 60 + "\n")
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if port 5000 is already in use")
        print("2. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify database is initialized: python init_automotive_db.py")
        print("4. Check error logs in logs/ directory")
        sys.exit(1)

if __name__ == '__main__':
    main()
