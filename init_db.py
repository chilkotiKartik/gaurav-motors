#!/usr/bin/env python3
"""Initialize database"""
import sys
sys.path.insert(0, '.')

from app import app, db

print("Initializing database...")

with app.app_context():
    try:
        print("Creating all tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Now try to init with sample data
        print("\nInitializing with sample data...")
        from init_automotive_db import init_automotive_db
        init_automotive_db()
        print("✓ Sample data loaded!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
