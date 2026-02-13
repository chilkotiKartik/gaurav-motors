"""
Database initialization script for Gaurav Motors Car Service Center
Transforms the HMS database to automotive service management
"""

from app import app, db
from app import (User, ServiceDepartment, TechnicianProfile, CustomerProfile, 
                ServiceBooking, ServiceWork, Availability, VehicleRecord, 
                VehicleHistory, TechnicianReview, ServiceReview, SparePartCategory, 
                SparePart, PartOrder, Payment, Notification)
from werkzeug.security import generate_password_hash

def init_automotive_db():
    """Initialize the automotive service database with sample data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("Creating default admin user...")
            admin_user = User(
                username='admin',
                email='admin@gauravmotors.com',
                password_hash=generate_password_hash('Admin@123456'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.flush()
            
        # Create service departments
        departments = [
            {'name': 'Engine Services', 'description': 'Engine diagnostics, repair, and maintenance'},
            {'name': 'Transmission & Drivetrain', 'description': 'Transmission, clutch, and gearbox services'},
            {'name': 'Electrical & Electronics', 'description': 'AC, electrical systems, and automotive electronics'},
            {'name': 'Body & Paint', 'description': 'Denting, painting, and bodywork services'},
            {'name': 'Wheels & Alignment', 'description': 'Wheel alignment, balancing, and tire services'},
            {'name': 'Brakes & Suspension', 'description': 'Brake system and suspension services'}
        ]
        
        for dept_data in departments:
            existing_dept = ServiceDepartment.query.filter_by(name=dept_data['name']).first()
            if not existing_dept:
                dept = ServiceDepartment(**dept_data)
                db.session.add(dept)
                
        # Create sample technician user
        tech_user = User.query.filter_by(username='drjohn').first()
        if not tech_user:
            print("Creating sample technician user...")
            tech_user = User(
                username='drjohn',
                email='technician@gauravmotors.com',
                password_hash=generate_password_hash('doctor'),
                role='technician'
            )
            db.session.add(tech_user)
            db.session.flush()  # Get the user ID
            
            # Create technician profile
            tech_profile = TechnicianProfile(
                user_id=tech_user.id,
                name='Rajesh Kumar',
                specialization='Engine & Transmission',
                department_id=1,  # Engine Services
                availability='Monday-Saturday 9AM-6PM'
            )
            db.session.add(tech_profile)
            
        # Create sample customer user  
        customer_user = User.query.filter_by(username='kar').first()
        if not customer_user:
            print("Creating sample customer user...")
            customer_user = User(
                username='kar',
                email='customer@gauravmotors.com',
                password_hash=generate_password_hash('kar123'),
                role='customer'
            )
            db.session.add(customer_user)
            db.session.flush()
            
            # Create customer profile
            customer_profile = CustomerProfile(
                user_id=customer_user.id,
                name='Amit Sharma',
                contact='+91 9876543210'
            )
            db.session.add(customer_profile)
            db.session.flush()  # Get customer_profile.id
            
            # Create vehicle history
            vehicle_history = VehicleHistory(
                customer_id=customer_profile.id,
                make='Maruti Suzuki',
                model='Swift',
                year=2020,
                license_plate='UK 01 AB 1234',
                mileage=25000,
                fuel_type='Petrol',
                transmission='Manual',
                engine_size='1.2L',
                color='Red'
            )
            db.session.add(vehicle_history)
        
        # Create spare part categories
        categories = [
            {'name': 'Engine Parts', 'icon': 'fas fa-cog', 'color': '#dc3545', 'description': 'Engine components and accessories'},
            {'name': 'Electrical Parts', 'icon': 'fas fa-bolt', 'color': '#ffc107', 'description': 'Electrical and electronic components'},
            {'name': 'Body & Exterior', 'icon': 'fas fa-car', 'color': '#28a745', 'description': 'Body panels, lights, and exterior parts'},
            {'name': 'Suspension & Brakes', 'icon': 'fas fa-compress-alt', 'color': '#6f42c1', 'description': 'Suspension and brake system parts'},
            {'name': 'Filters & Fluids', 'icon': 'fas fa-tint', 'color': '#17a2b8', 'description': 'Oil filters, air filters, and fluids'},
            {'name': 'Tires & Wheels', 'icon': 'fas fa-circle', 'color': '#fd7e14', 'description': 'Tires, wheels, and related accessories'}
        ]
        
        for cat_data in categories:
            existing_cat = SparePartCategory.query.filter_by(name=cat_data['name']).first()
            if not existing_cat:
                category = SparePartCategory(**cat_data)
                db.session.add(category)
        
        try:
            db.session.commit()
            print("✅ Database initialized successfully!")
            print("📋 Login Credentials:")
            print("   Admin: admin / Admin@123456")
            print("   Technician: drjohn / doctor") 
            print("   Customer: kar / kar123")
            print("\n🚗 Gaurav Motors Service Center is ready!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error initializing database: {e}")

if __name__ == '__main__':
    init_automotive_db()