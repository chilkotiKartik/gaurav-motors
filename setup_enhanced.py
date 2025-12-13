"""
Quick Setup Script for GM Motors HMS
Run this after first deployment to initialize the database with sample data
"""

from app import app, db
from app import (User, DoctorProfile, PatientProfile, Department, 
                 MedicalHistory, Notification, ServiceCategory, CarService,
                 SparePartCategory, SparePart)
from datetime import datetime, timedelta
import random

def setup_enhanced_system():
    """Setup database with enhanced features"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if User.query.first():
            print("Database already contains data. Skipping setup.")
            return
        
        print("Setting up enhanced system...")
        
        # Create Admin User
        admin = User(username='admin', email='admin@gmmotors.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Departments
        departments = [
            Department(name='Cardiology', description='Heart and cardiovascular care'),
            Department(name='Orthopedics', description='Bone and joint specialists'),
            Department(name='Pediatrics', description='Children healthcare'),
            Department(name='Dermatology', description='Skin care specialists'),
            Department(name='General Medicine', description='General health and wellness')
        ]
        for dept in departments:
            db.session.add(dept)
        db.session.commit()
        
        # Create Doctor Users and Profiles
        doctors_data = [
            ('Dr. Rajesh Kumar', 'Cardiology', 'dr.rajesh@gmmotors.com'),
            ('Dr. Priya Sharma', 'Pediatrics', 'dr.priya@gmmotors.com'),
            ('Dr. Amit Patel', 'Orthopedics', 'dr.amit@gmmotors.com'),
            ('Dr. Neha Singh', 'Dermatology', 'dr.neha@gmmotors.com'),
            ('Dr. Vikram Mehta', 'General Medicine', 'dr.vikram@gmmotors.com')
        ]
        
        for name, spec, email in doctors_data:
            username = email.split('@')[0]
            user = User(username=username, email=email, role='doctor')
            user.set_password('doctor123')
            db.session.add(user)
            db.session.commit()
            
            dept = Department.query.filter_by(name=spec).first()
            profile = DoctorProfile(
                user_id=user.id,
                name=name,
                specialization=spec,
                department_id=dept.id if dept else None,
                availability='Mon-Fri: 9AM-5PM'
            )
            db.session.add(profile)
        
        # Create Sample Patients
        patients_data = [
            ('John Doe', 'john.doe@email.com', '+91-9876543210'),
            ('Jane Smith', 'jane.smith@email.com', '+91-9876543211'),
            ('Robert Johnson', 'robert.j@email.com', '+91-9876543212'),
            ('Emily Davis', 'emily.d@email.com', '+91-9876543213'),
            ('Michael Wilson', 'michael.w@email.com', '+91-9876543214')
        ]
        
        for name, email, contact in patients_data:
            username = email.split('@')[0].replace('.', '')
            user = User(username=username, email=email, role='patient')
            user.set_password('patient123')
            db.session.add(user)
            db.session.commit()
            
            profile = PatientProfile(
                user_id=user.id,
                name=name,
                contact=contact
            )
            db.session.add(profile)
            db.session.commit()
            
            # Add sample medical history
            history = MedicalHistory(
                patient_id=profile.id,
                blood_type=random.choice(['A+', 'B+', 'O+', 'AB+', 'A-', 'B-', 'O-', 'AB-']),
                allergies='None reported',
                emergency_contact=name.split()[0] + ' Family',
                emergency_phone='+91-9876500000'
            )
            db.session.add(history)
        
        # Create Service Categories
        service_categories = [
            ServiceCategory(name='Maintenance', icon='🔧', description='Regular vehicle maintenance'),
            ServiceCategory(name='Repairs', icon='🔨', description='Vehicle repairs and fixes'),
            ServiceCategory(name='Detailing', icon='✨', description='Car cleaning and detailing'),
            ServiceCategory(name='Diagnostics', icon='🔍', description='Vehicle diagnostics')
        ]
        for cat in service_categories:
            db.session.add(cat)
        db.session.commit()
        
        # Create Sample Services
        services_data = [
            ('Oil Change', 1, 'Complete engine oil replacement', 1500, 30, True),
            ('Brake Service', 2, 'Brake pad replacement and inspection', 3500, 60, True),
            ('Full Detailing', 3, 'Complete interior and exterior cleaning', 5000, 120, True),
            ('Engine Diagnostics', 4, 'Computer diagnostics for engine issues', 2000, 45, False),
            ('Tire Rotation', 1, 'Tire rotation and balancing', 1000, 30, True)
        ]
        
        for name, cat_id, desc, price, duration, popular in services_data:
            service = CarService(
                name=name,
                category_id=cat_id,
                description=desc,
                price=price,
                duration_minutes=duration,
                is_popular=popular,
                is_active=True
            )
            db.session.add(service)
        
        # Create Spare Part Categories
        part_categories = [
            SparePartCategory(name='Engine Parts', icon='fa-cog', color='#dc3545'),
            SparePartCategory(name='Brake System', icon='fa-circle', color='#fd7e14'),
            SparePartCategory(name='Electrical', icon='fa-bolt', color='#ffc107'),
            SparePartCategory(name='Body Parts', icon='fa-car', color='#0d6efd')
        ]
        for cat in part_categories:
            db.session.add(cat)
        db.session.commit()
        
        # Create Sample Spare Parts
        parts_data = [
            ('Engine Oil Filter', 1, 'EOF-123', 'Bosch', 450, 50, True, False),
            ('Brake Pads Set', 2, 'BP-456', 'Brembo', 2500, 30, True, True),
            ('Headlight Assembly', 4, 'HL-789', 'Philips', 3500, 15, True, True),
            ('Battery 12V', 3, 'BAT-012', 'Exide', 5500, 20, True, False),
            ('Air Filter', 1, 'AF-345', 'Mann', 650, 40, False, False)
        ]
        
        for name, cat_id, part_num, brand, price, stock, featured, oem in parts_data:
            part = SparePart(
                name=name,
                category_id=cat_id,
                part_number=part_num,
                brand=brand,
                price=price,
                stock_quantity=stock,
                is_featured=featured,
                is_oem=oem,
                compatible_brands='Universal',
                description=f'High quality {name.lower()} from {brand}'
            )
            db.session.add(part)
        
        # Create sample notifications for admin
        notifications = [
            Notification(
                user_id=1,
                title='Welcome to Enhanced HMS',
                message='Your system has been upgraded with 10+ new features including medical records, reviews, analytics, and more!',
                notification_type='system'
            ),
            Notification(
                user_id=1,
                title='System Setup Complete',
                message='Database initialized with sample data. Ready for production use.',
                notification_type='system'
            )
        ]
        for notif in notifications:
            db.session.add(notif)
        
        db.session.commit()
        
        print("\n✅ Enhanced system setup complete!")
        print("\n📊 Sample Data Created:")
        print(f"  - Admin User: admin / admin123")
        print(f"  - {len(doctors_data)} Doctors (password: doctor123)")
        print(f"  - {len(patients_data)} Patients (password: patient123)")
        print(f"  - {len(departments)} Departments")
        print(f"  - {len(services_data)} Car Services")
        print(f"  - {len(parts_data)} Spare Parts")
        print(f"  - Medical History for all patients")
        print(f"  - Notification system ready")
        print("\n🚀 System ready for deployment!")
        print("\n⚠️  Remember to:")
        print("  1. Configure environment variables (.env)")
        print("  2. Set up email SMTP settings")
        print("  3. Update SECRET_KEY for production")
        print("  4. Configure payment gateway (optional)")

if __name__ == '__main__':
    setup_enhanced_system()
