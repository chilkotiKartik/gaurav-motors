"""
Setup script to populate car services database
"""
from app import app, db, ServiceCategory, CarService
from datetime import datetime

def setup_services():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if services already exist
        if ServiceCategory.query.count() > 0:
            print("Services already exist. Skipping setup.")
            return
        
        # Create Service Categories
        categories_data = [
            {
                'name': 'Routine Maintenance',
                'icon': '🔧',
                'description': 'Regular maintenance services to keep your vehicle running smoothly'
            },
            {
                'name': 'Engine Services',
                'icon': '⚙️',
                'description': 'Comprehensive engine diagnostics and repair services'
            },
            {
                'name': 'Brake & Safety',
                'icon': '🛑',
                'description': 'Brake system maintenance and safety inspections'
            },
            {
                'name': 'Tire Services',
                'icon': '🚗',
                'description': 'Complete tire care including rotation, balancing, and alignment'
            },
            {
                'name': 'Climate Control',
                'icon': '❄️',
                'description': 'AC and heating system services'
            },
            {
                'name': 'Electrical',
                'icon': '🔋',
                'description': 'Battery, alternator, and electrical system services'
            },
            {
                'name': 'Body & Paint',
                'icon': '🎨',
                'description': 'Denting, painting, and body repair services'
            },
            {
                'name': 'Specialized Services',
                'icon': '⭐',
                'description': 'Premium and specialized automotive services'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = ServiceCategory(**cat_data)
            db.session.add(category)
            db.session.flush()
            categories[cat_data['name']] = category
        
        # Create Car Services
        services_data = [
            # Routine Maintenance
            {
                'name': 'Oil Change & Filter',
                'category': 'Routine Maintenance',
                'description': 'Complete oil change service with premium quality oil',
                'price': 1500,
                'duration_minutes': 60,
                'icon': '🛢️',
                'includes': 'Premium synthetic oil, Oil filter replacement, 20-point inspection, Fluid top-up, Engine cleaning',
                'is_popular': True
            },
            {
                'name': 'Basic Service',
                'category': 'Routine Maintenance',
                'description': 'Essential maintenance for optimal vehicle performance',
                'price': 2500,
                'duration_minutes': 90,
                'icon': '🔧',
                'includes': 'Oil change, Air filter check, Brake inspection, Tire pressure check, Battery test',
                'is_popular': True
            },
            {
                'name': 'Standard Service',
                'category': 'Routine Maintenance',
                'description': 'Comprehensive service package for regular maintenance',
                'price': 4000,
                'duration_minutes': 150,
                'icon': '⚡',
                'includes': 'All basic service items, Spark plug check, Coolant top-up, Transmission fluid check, Suspension inspection',
                'is_popular': True
            },
            {
                'name': 'Full Service',
                'category': 'Routine Maintenance',
                'description': 'Complete bumper-to-bumper service for your vehicle',
                'price': 6500,
                'duration_minutes': 240,
                'icon': '💎',
                'includes': 'All standard service items, Complete fluid replacement, Timing belt inspection, Exhaust system check, Complete vehicle detailing',
                'is_popular': True
            },
            
            # Engine Services
            {
                'name': 'Engine Diagnostic',
                'category': 'Engine Services',
                'description': 'Advanced computer diagnostics for engine issues',
                'price': 1000,
                'duration_minutes': 90,
                'icon': '🔍',
                'includes': 'OBD-II scanning, Error code reading, Performance analysis, Detailed diagnostic report',
                'is_popular': False
            },
            {
                'name': 'Engine Tune-Up',
                'category': 'Engine Services',
                'description': 'Complete engine optimization for better performance',
                'price': 3500,
                'duration_minutes': 180,
                'icon': '⚙️',
                'includes': 'Spark plug replacement, Fuel injector cleaning, Throttle body cleaning, Engine timing adjustment',
                'is_popular': False
            },
            {
                'name': 'Engine Oil Flush',
                'category': 'Engine Services',
                'description': 'Deep engine cleaning with oil flush system',
                'price': 2000,
                'duration_minutes': 120,
                'icon': '🌊',
                'includes': 'Complete oil system flush, Sludge removal, New oil and filter, Engine performance test',
                'is_popular': False
            },
            
            # Brake & Safety
            {
                'name': 'Brake Pad Replacement',
                'category': 'Brake & Safety',
                'description': 'Replace worn brake pads for optimal safety',
                'price': 2500,
                'duration_minutes': 120,
                'icon': '🛑',
                'includes': 'Front/Rear brake pads, Brake rotor inspection, Brake fluid check, Road test',
                'is_popular': True
            },
            {
                'name': 'Complete Brake Service',
                'category': 'Brake & Safety',
                'description': 'Comprehensive brake system maintenance',
                'price': 4500,
                'duration_minutes': 180,
                'icon': '🚨',
                'includes': 'Brake pads replacement, Brake fluid flush, Rotor resurfacing, Caliper inspection, ABS check',
                'is_popular': False
            },
            {
                'name': 'Brake Fluid Change',
                'category': 'Brake & Safety',
                'description': 'Replace contaminated brake fluid',
                'price': 800,
                'duration_minutes': 60,
                'icon': '💧',
                'includes': 'Complete brake fluid replacement, System bleeding, Brake line inspection',
                'is_popular': False
            },
            
            # Tire Services
            {
                'name': 'Tire Rotation',
                'category': 'Tire Services',
                'description': 'Rotate tires for even wear and longer life',
                'price': 500,
                'duration_minutes': 45,
                'icon': '🔄',
                'includes': 'All 4 tires rotation, Tire pressure adjustment, Visual inspection',
                'is_popular': True
            },
            {
                'name': 'Wheel Alignment',
                'category': 'Tire Services',
                'description': 'Precision wheel alignment for better handling',
                'price': 1200,
                'duration_minutes': 90,
                'icon': '📐',
                'includes': '4-wheel computerized alignment, Steering adjustment, Test drive',
                'is_popular': True
            },
            {
                'name': 'Wheel Balancing',
                'category': 'Tire Services',
                'description': 'Balance wheels to eliminate vibration',
                'price': 800,
                'duration_minutes': 60,
                'icon': '⚖️',
                'includes': 'All 4 wheels computerized balancing, Weight adjustment, Vibration test',
                'is_popular': False
            },
            {
                'name': 'Tire Replacement',
                'category': 'Tire Services',
                'description': 'New tire installation with balancing',
                'price': 3500,
                'duration_minutes': 90,
                'icon': '🆕',
                'includes': 'New tire installation, Wheel balancing, Disposal of old tire, Alignment check',
                'is_popular': False
            },
            
            # Climate Control
            {
                'name': 'AC Service & Gas Refill',
                'category': 'Climate Control',
                'description': 'Complete AC maintenance with gas refill',
                'price': 2200,
                'duration_minutes': 120,
                'icon': '❄️',
                'includes': 'AC gas refill (R134a), Filter replacement, Coil cleaning, Performance test',
                'is_popular': True
            },
            {
                'name': 'AC Repair',
                'category': 'Climate Control',
                'description': 'Diagnose and repair AC system issues',
                'price': 3500,
                'duration_minutes': 180,
                'icon': '🔧',
                'includes': 'Complete AC diagnosis, Leak detection, Component repair/replacement, Gas refill',
                'is_popular': False
            },
            {
                'name': 'Heater Service',
                'category': 'Climate Control',
                'description': 'Heating system maintenance and repair',
                'price': 1500,
                'duration_minutes': 90,
                'icon': '🔥',
                'includes': 'Heater core inspection, Thermostat check, Coolant system check, Fan motor test',
                'is_popular': False
            },
            
            # Electrical
            {
                'name': 'Battery Replacement',
                'category': 'Electrical',
                'description': 'New battery installation with warranty',
                'price': 4500,
                'duration_minutes': 45,
                'icon': '🔋',
                'includes': 'Premium battery, Terminal cleaning, Battery test, 18-month warranty',
                'is_popular': True
            },
            {
                'name': 'Battery Service',
                'category': 'Electrical',
                'description': 'Battery testing and maintenance',
                'price': 500,
                'duration_minutes': 30,
                'icon': '⚡',
                'includes': 'Battery load test, Terminal cleaning, Water top-up (if applicable), Charging system check',
                'is_popular': False
            },
            {
                'name': 'Alternator Service',
                'category': 'Electrical',
                'description': 'Alternator testing and repair',
                'price': 2500,
                'duration_minutes': 120,
                'icon': '🔌',
                'includes': 'Alternator test, Belt inspection, Voltage regulator check, Charging system diagnosis',
                'is_popular': False
            },
            {
                'name': 'Complete Electrical Diagnostic',
                'category': 'Electrical',
                'description': 'Comprehensive electrical system diagnosis',
                'price': 1500,
                'duration_minutes': 120,
                'icon': '🔦',
                'includes': 'Complete system scan, Wiring inspection, Fuse box check, Component testing',
                'is_popular': False
            },
            
            # Body & Paint
            {
                'name': 'Denting & Painting',
                'category': 'Body & Paint',
                'description': 'Professional dent removal and painting',
                'price': 5000,
                'duration_minutes': 480,
                'icon': '🎨',
                'includes': 'Dent removal, Surface preparation, Professional painting, Clear coat application',
                'is_popular': False
            },
            {
                'name': 'Car Detailing',
                'category': 'Body & Paint',
                'description': 'Complete interior and exterior detailing',
                'price': 3000,
                'duration_minutes': 240,
                'icon': '✨',
                'includes': 'Deep interior cleaning, Exterior wash & wax, Polish & shine, Tire dressing, Glass cleaning',
                'is_popular': True
            },
            {
                'name': 'Scratch Removal',
                'category': 'Body & Paint',
                'description': 'Minor scratch and scuff removal',
                'price': 1500,
                'duration_minutes': 120,
                'icon': '🔧',
                'includes': 'Scratch assessment, Buffing & polishing, Touch-up paint, Protective coating',
                'is_popular': False
            },
            
            # Specialized Services
            {
                'name': 'Pre-Purchase Inspection',
                'category': 'Specialized Services',
                'description': 'Comprehensive vehicle inspection before buying',
                'price': 2000,
                'duration_minutes': 180,
                'icon': '🔍',
                'includes': '150-point inspection, Engine diagnostics, Body condition report, Test drive evaluation, Detailed report',
                'is_popular': False
            },
            {
                'name': 'Engine Carbon Cleaning',
                'category': 'Specialized Services',
                'description': 'Remove carbon deposits from engine',
                'price': 4000,
                'duration_minutes': 180,
                'icon': '🌪️',
                'includes': 'Carbon cleaning treatment, Fuel injector cleaning, Intake manifold cleaning, Performance improvement',
                'is_popular': False
            },
            {
                'name': 'Transmission Service',
                'category': 'Specialized Services',
                'description': 'Complete transmission maintenance',
                'price': 5500,
                'duration_minutes': 240,
                'icon': '⚙️',
                'includes': 'Transmission fluid change, Filter replacement, Pan gasket replacement, Road test',
                'is_popular': False
            },
            {
                'name': 'Suspension Repair',
                'category': 'Specialized Services',
                'description': 'Suspension system diagnosis and repair',
                'price': 4500,
                'duration_minutes': 240,
                'icon': '🔩',
                'includes': 'Complete suspension inspection, Shock absorber replacement, Spring check, Alignment after repair',
                'is_popular': False
            }
        ]
        
        for service_data in services_data:
            category_name = service_data.pop('category')
            service = CarService(
                category_id=categories[category_name].id,
                **service_data
            )
            db.session.add(service)
        
        db.session.commit()
        print("✅ Car services database initialized successfully!")
        print(f"   - Created {len(categories_data)} service categories")
        print(f"   - Created {len(services_data)} car services")

if __name__ == '__main__':
    setup_services()
