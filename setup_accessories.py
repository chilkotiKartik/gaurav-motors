"""
Setup script for car accessories
Run this to populate the database with sample accessories
"""
from app import app, db, AccessoryCategory, CarAccessory

def setup_accessories():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if categories already exist
        if AccessoryCategory.query.first():
            print("✓ Accessories already set up")
            return
        
        print("Setting up car accessories...")
        
        # Create categories
        categories = [
            {
                'name': 'Interior Accessories',
                'icon': 'fas fa-couch',
                'color': '#0dcaf0',
                'image_url': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80',
                'description': 'Enhance your car interior with premium accessories'
            },
            {
                'name': 'Exterior Accessories',
                'icon': 'fas fa-car-side',
                'color': '#0d6efd',
                'image_url': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&q=80',
                'description': 'Upgrade your car exterior styling and protection'
            },
            {
                'name': 'Electronics & Gadgets',
                'icon': 'fas fa-microchip',
                'color': '#6f42c1',
                'image_url': 'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&q=80',
                'description': 'Latest automotive electronics and smart gadgets'
            },
            {
                'name': 'Safety & Security',
                'icon': 'fas fa-shield-alt',
                'color': '#dc3545',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
                'description': 'Keep your vehicle safe and secure'
            },
            {
                'name': 'Performance Parts',
                'icon': 'fas fa-tachometer-alt',
                'color': '#ffc107',
                'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80',
                'description': 'Boost your car performance'
            },
            {
                'name': 'Car Care Products',
                'icon': 'fas fa-spray-can',
                'color': '#20c997',
                'image_url': 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?w=800&q=80',
                'description': 'Keep your car clean and shiny'
            }
        ]
        
        for cat_data in categories:
            cat = AccessoryCategory(**cat_data)
            db.session.add(cat)
        
        db.session.commit()
        print("✓ Categories created")
        
        # Create sample accessories
        accessories = [
            # Interior Accessories
            {
                'name': 'Premium Leather Seat Covers (Set of 5)',
                'category_id': 1,
                'brand': 'AutoCraft',
                'price': 4999,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1449426468159-d96dbf08f19f?w=800&q=80',
                'description': 'High-quality leather seat covers with cushion padding. Universal fit for most cars.',
                'features': 'Waterproof, Easy to clean, Breathable material, Anti-slip backing',
                'compatible_cars': 'Universal fit - All cars',
                'warranty_months': 12,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.5,
                'review_count': 128
            },
            {
                'name': '7D Car Floor Mats (Beige)',
                'category_id': 1,
                'brand': 'MatPro',
                'price': 2499,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800&q=80',
                'description': '7D textured floor mats with raised edges for maximum protection.',
                'features': 'Waterproof, Odorless, Anti-slip, Easy to install',
                'compatible_cars': 'Custom fit available for most models',
                'warranty_months': 6,
                'is_featured': False,
                'is_universal': False,
                'rating': 4.3,
                'review_count': 89
            },
            {
                'name': 'Car Dashboard Camera HD 1080P',
                'category_id': 3,
                'brand': 'TechDrive',
                'price': 3499,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&q=80',
                'description': 'Full HD dashcam with night vision, loop recording, and G-sensor.',
                'features': 'Night vision, 170° wide angle, Loop recording, Motion detection',
                'compatible_cars': 'Universal',
                'warranty_months': 12,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.6,
                'review_count': 245
            },
            {
                'name': 'Steering Wheel Cover (Leather)',
                'category_id': 1,
                'brand': 'AutoCraft',
                'price': 599,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1449426468159-d96dbf08f19f?w=800&q=80',
                'description': 'Premium leather steering wheel cover with anti-slip grip.',
                'features': 'Breathable leather, Anti-slip, Easy installation, Sweat absorbent',
                'compatible_cars': 'Universal - Fits most cars',
                'warranty_months': 6,
                'is_featured': False,
                'is_universal': True,
                'rating': 4.2,
                'review_count': 67
            },
            # Exterior Accessories
            {
                'name': 'Chrome Door Handle Covers (Set of 4)',
                'category_id': 2,
                'brand': 'ChromeStyle',
                'price': 899,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=800&q=80',
                'description': 'Premium chrome finish door handle covers for enhanced styling.',
                'features': 'Easy installation, Weather resistant, Premium finish',
                'compatible_cars': 'Model specific - specify your car',
                'warranty_months': 12,
                'is_featured': False,
                'is_universal': False,
                'rating': 4.1,
                'review_count': 45
            },
            {
                'name': 'LED Fog Lights (Pair)',
                'category_id': 2,
                'brand': 'BrightLite',
                'price': 1899,
                'stock': 18,
                'image_url': 'https://images.unsplash.com/photo-1517524206127-48bbd363f3d7?w=800&q=80',
                'description': 'High-power LED fog lights for better visibility in fog and rain.',
                'features': 'High brightness, Low power consumption, Weather proof, Easy wiring',
                'compatible_cars': 'Universal mounting',
                'warranty_months': 12,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.4,
                'review_count': 156
            },
            {
                'name': 'Car Body Cover (Waterproof)',
                'category_id': 2,
                'brand': 'ShieldPro',
                'price': 1299,
                'stock': 22,
                'image_url': 'https://images.unsplash.com/photo-1626668011725-c60c8d6b43f4?w=800&q=80',
                'description': 'Heavy-duty waterproof car cover with UV protection.',
                'features': 'Waterproof, UV resistant, Dust proof, Storage bag included',
                'compatible_cars': 'Available in multiple sizes',
                'warranty_months': 6,
                'is_featured': False,
                'is_universal': True,
                'rating': 4.0,
                'review_count': 34
            },
            # Electronics & Gadgets
            {
                'name': 'Bluetooth Car FM Transmitter',
                'category_id': 3,
                'brand': 'AudioLink',
                'price': 799,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1603481546665-20144716b905?w=800&q=80',
                'description': 'Wireless Bluetooth FM transmitter with USB charging ports.',
                'features': 'Hands-free calls, USB charging, FM transmission, LED display',
                'compatible_cars': 'Universal',
                'warranty_months': 12,
                'is_featured': False,
                'is_universal': True,
                'rating': 4.3,
                'review_count': 198
            },
            {
                'name': 'Reverse Parking Camera (Night Vision)',
                'category_id': 3,
                'brand': 'VisionTech',
                'price': 2299,
                'stock': 16,
                'image_url': 'https://images.unsplash.com/photo-1563298723-dcfebaa392e3?w=800&q=80',
                'description': 'HD reverse parking camera with night vision and wide-angle lens.',
                'features': 'HD quality, Night vision, 170° view, Waterproof, Easy installation',
                'compatible_cars': 'Universal mounting',
                'warranty_months': 12,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.5,
                'review_count': 112
            },
            {
                'name': 'Tire Pressure Monitoring System (TPMS)',
                'category_id': 3,
                'brand': 'SafeDrive',
                'price': 3999,
                'stock': 12,
                'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80',
                'description': 'Real-time tire pressure and temperature monitoring system.',
                'features': 'Real-time monitoring, Visual & audio alerts, LCD display, Solar powered',
                'compatible_cars': 'Universal',
                'warranty_months': 18,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.7,
                'review_count': 89
            },
            # Safety & Security
            {
                'name': 'Car Alarm System with Central Lock',
                'category_id': 4,
                'brand': 'SecureCar',
                'price': 2999,
                'stock': 14,
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
                'description': 'Advanced car alarm system with remote central locking.',
                'features': 'Remote lock/unlock, Shock sensor, Anti-theft, Emergency unlock',
                'compatible_cars': 'Universal - Professional installation required',
                'warranty_months': 24,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.6,
                'review_count': 145
            },
            {
                'name': 'Fire Extinguisher (1kg ABC)',
                'category_id': 4,
                'brand': 'SafetyFirst',
                'price': 499,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1582139329536-e7284fece509?w=800&q=80',
                'description': 'Compact car fire extinguisher with mounting bracket.',
                'features': 'ABC type, 1kg capacity, ISI certified, Easy to use',
                'compatible_cars': 'Universal',
                'warranty_months': 60,
                'is_featured': False,
                'is_universal': True,
                'rating': 4.8,
                'review_count': 67
            },
            # Performance Parts
            {
                'name': 'K&N Air Filter (High Performance)',
                'category_id': 5,
                'brand': 'K&N',
                'price': 3499,
                'stock': 10,
                'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80',
                'description': 'High-flow air filter for improved engine performance and mileage.',
                'features': 'Washable, Reusable, Improved airflow, Better mileage',
                'compatible_cars': 'Model specific - check compatibility',
                'warranty_months': 120,
                'is_featured': True,
                'is_universal': False,
                'rating': 4.7,
                'review_count': 234
            },
            {
                'name': 'Sport Exhaust Muffler',
                'category_id': 5,
                'brand': 'RacePro',
                'price': 5999,
                'stock': 8,
                'image_url': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&q=80',
                'description': 'Stainless steel sport muffler for enhanced exhaust note and performance.',
                'features': 'Stainless steel, Better exhaust flow, Sporty sound, Rust resistant',
                'compatible_cars': 'Universal fit with adapter',
                'warranty_months': 24,
                'is_featured': False,
                'is_universal': False,
                'rating': 4.4,
                'review_count': 78
            },
            # Car Care Products
            {
                'name': '3M Car Polish & Wax (500ml)',
                'category_id': 6,
                'brand': '3M',
                'price': 799,
                'stock': 60,
                'image_url': 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?w=800&q=80',
                'description': 'Premium car polish and wax for showroom shine.',
                'features': 'UV protection, Scratch filling, Long lasting, Easy application',
                'compatible_cars': 'All cars',
                'warranty_months': 0,
                'is_featured': False,
                'is_universal': True,
                'rating': 4.5,
                'review_count': 456
            },
            {
                'name': 'Car Vacuum Cleaner (12V)',
                'category_id': 6,
                'brand': 'CleanPro',
                'price': 1499,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&q=80',
                'description': 'Portable car vacuum cleaner with powerful suction.',
                'features': 'HEPA filter, Wet & dry, 12V power, Multiple attachments',
                'compatible_cars': 'Universal',
                'warranty_months': 12,
                'is_featured': True,
                'is_universal': True,
                'rating': 4.3,
                'review_count': 189
            }
        ]
        
        for acc_data in accessories:
            acc = CarAccessory(**acc_data)
            db.session.add(acc)
        
        db.session.commit()
        print(f"✓ Created {len(accessories)} sample accessories")
        print("✓ Car accessories setup complete!")

if __name__ == '__main__':
    setup_accessories()
