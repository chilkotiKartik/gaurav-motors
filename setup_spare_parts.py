"""
Initialize Spare Parts Database with Categories and Sample Products
Run this once to set up the spare parts system
"""
from app import app, db, SparePartCategory, SparePart

def init_spare_parts():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if categories already exist
        if SparePartCategory.query.count() > 0:
            print("Categories already exist. Skipping initialization.")
            return
        
        print("Initializing spare parts database...")
        
        # Define categories with professional data
        categories_data = [
            {
                'name': 'Engine Components',
                'icon': 'engine',
                'color': '#0d6efd',
                'image_url': 'https://images.unsplash.com/photo-1486262715619-e3bc71683773?w=600&q=80',
                'description': 'Complete range of engine parts including pistons, crankshafts, valves, timing belts and gaskets'
            },
            {
                'name': 'Brake Systems',
                'icon': 'circle-notch',
                'color': '#dc3545',
                'image_url': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=600&q=80',
                'description': 'Premium brake pads, rotors, calipers, drums and hydraulic components'
            },
            {
                'name': 'Filters & Fluids',
                'icon': 'filter',
                'color': '#198754',
                'image_url': 'https://images.unsplash.com/photo-1632823469620-fef1e4c85ab0?w=600&q=80',
                'description': 'Oil filters, air filters, cabin filters, engine oils, coolants and brake fluids'
            },
            {
                'name': 'Electrical Parts',
                'icon': 'bolt',
                'color': '#ffc107',
                'image_url': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=600&q=80',
                'description': 'Batteries, alternators, starters, spark plugs, sensors and wiring harnesses'
            },
            {
                'name': 'Suspension Parts',
                'icon': 'car-side',
                'color': '#6f42c1',
                'image_url': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=600&q=80',
                'description': 'Shock absorbers, struts, springs, control arms, ball joints and bushings'
            },
            {
                'name': 'Transmission',
                'icon': 'cog',
                'color': '#fd7e14',
                'image_url': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&q=80',
                'description': 'Clutch kits, gearboxes, torque converters, drive shafts and CV joints'
            },
            {
                'name': 'Body & Exterior',
                'icon': 'car',
                'color': '#20c997',
                'image_url': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=600&q=80',
                'description': 'Bumpers, fenders, headlights, taillights, mirrors and windshields'
            },
            {
                'name': 'Interior Parts',
                'icon': 'couch',
                'color': '#0dcaf0',
                'image_url': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=80',
                'description': 'Seat covers, dashboard components, door panels, floor mats and steering wheels'
            }
        ]
        
        # Create categories
        categories = {}
        for cat_data in categories_data:
            category = SparePartCategory(**cat_data)
            db.session.add(category)
            db.session.flush()
            categories[cat_data['name']] = category
            print(f"✓ Created category: {cat_data['name']}")
        
        # Sample parts data for each category
        sample_parts = [
            # Engine Components
            {'name': 'Piston Set (4 Cylinder)', 'category': 'Engine Components', 'part_number': 'ENG-PST-001', 'brand': 'Mahle', 'price': 8500, 'stock': 25, 'compatible': 'Maruti, Hyundai, Honda', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1486262715619-e3bc71683773?w=400&q=80'},
            {'name': 'Timing Belt Kit', 'category': 'Engine Components', 'part_number': 'ENG-TBK-002', 'brand': 'Gates', 'price': 3200, 'stock': 40, 'compatible': 'Maruti, Tata, Hyundai', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1486262715619-e3bc71683773?w=400&q=80'},
            {'name': 'Cylinder Head Gasket', 'category': 'Engine Components', 'part_number': 'ENG-GSK-003', 'brand': 'Elring', 'price': 1850, 'stock': 60, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1486262715619-e3bc71683773?w=400&q=80'},
            {'name': 'Crankshaft Pulley', 'category': 'Engine Components', 'part_number': 'ENG-CRP-004', 'brand': 'Bosch', 'price': 2400, 'stock': 30, 'compatible': 'Maruti, Honda, Toyota', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1486262715619-e3bc71683773?w=400&q=80'},
            
            # Brake Systems
            {'name': 'Front Brake Pads Set', 'category': 'Brake Systems', 'part_number': 'BRK-PAD-001', 'brand': 'Brembo', 'price': 2800, 'stock': 80, 'compatible': 'Maruti, Hyundai, Honda', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=400&q=80'},
            {'name': 'Brake Disc Rotor (Front)', 'category': 'Brake Systems', 'part_number': 'BRK-ROT-002', 'brand': 'ATE', 'price': 1850, 'stock': 50, 'compatible': 'All Brands', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=400&q=80'},
            {'name': 'Brake Caliper Assembly', 'category': 'Brake Systems', 'part_number': 'BRK-CAL-003', 'brand': 'TRW', 'price': 4500, 'stock': 20, 'compatible': 'Maruti, Tata, Mahindra', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=400&q=80'},
            {'name': 'Brake Master Cylinder', 'category': 'Brake Systems', 'part_number': 'BRK-MST-004', 'brand': 'Bosch', 'price': 3200, 'stock': 15, 'compatible': 'Maruti, Hyundai', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=400&q=80'},
            
            # Filters & Fluids
            {'name': 'Engine Oil Filter', 'category': 'Filters & Fluids', 'part_number': 'FLT-OIL-001', 'brand': 'Mann', 'price': 350, 'stock': 200, 'compatible': 'All Brands', 'warranty': 3, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1632823469620-fef1e4c85ab0?w=400&q=80'},
            {'name': 'Air Filter Element', 'category': 'Filters & Fluids', 'part_number': 'FLT-AIR-002', 'brand': 'K&N', 'price': 850, 'stock': 150, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1632823469620-fef1e4c85ab0?w=400&q=80'},
            {'name': 'Synthetic Engine Oil 5W-30 (4L)', 'category': 'Filters & Fluids', 'part_number': 'FLD-OIL-003', 'brand': 'Castrol', 'price': 2400, 'stock': 100, 'compatible': 'All Brands', 'warranty': 0, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1632823469620-fef1e4c85ab0?w=400&q=80'},
            {'name': 'Coolant Fluid (1L)', 'category': 'Filters & Fluids', 'part_number': 'FLD-CLT-004', 'brand': 'Motul', 'price': 450, 'stock': 180, 'compatible': 'All Brands', 'warranty': 0, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1632823469620-fef1e4c85ab0?w=400&q=80'},
            
            # Electrical Parts
            {'name': 'Car Battery 12V 65Ah', 'category': 'Electrical Parts', 'part_number': 'ELC-BAT-001', 'brand': 'Amaron', 'price': 5500, 'stock': 45, 'compatible': 'Maruti, Hyundai, Honda, Tata', 'warranty': 36, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&q=80'},
            {'name': 'Alternator Assembly', 'category': 'Electrical Parts', 'part_number': 'ELC-ALT-002', 'brand': 'Valeo', 'price': 8500, 'stock': 12, 'compatible': 'Maruti, Hyundai', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&q=80'},
            {'name': 'Spark Plugs Set (4pcs)', 'category': 'Electrical Parts', 'part_number': 'ELC-SPK-003', 'brand': 'NGK', 'price': 1200, 'stock': 100, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&q=80'},
            {'name': 'Starter Motor', 'category': 'Electrical Parts', 'part_number': 'ELC-STR-004', 'brand': 'Bosch', 'price': 6800, 'stock': 18, 'compatible': 'Maruti, Honda, Toyota', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&q=80'},
            
            # Suspension Parts
            {'name': 'Front Shock Absorber (Pair)', 'category': 'Suspension Parts', 'part_number': 'SUS-SHK-001', 'brand': 'Monroe', 'price': 5200, 'stock': 35, 'compatible': 'Maruti, Hyundai, Tata', 'warranty': 12, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400&q=80'},
            {'name': 'Coil Spring Set', 'category': 'Suspension Parts', 'part_number': 'SUS-SPR-002', 'brand': 'Sachs', 'price': 3800, 'stock': 28, 'compatible': 'All Brands', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400&q=80'},
            {'name': 'Control Arm Bushings', 'category': 'Suspension Parts', 'part_number': 'SUS-BSH-003', 'brand': 'Lemforder', 'price': 1850, 'stock': 50, 'compatible': 'Maruti, Hyundai', 'warranty': 6, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400&q=80'},
            {'name': 'Ball Joint Assembly', 'category': 'Suspension Parts', 'part_number': 'SUS-BLJ-004', 'brand': 'Moog', 'price': 2400, 'stock': 40, 'compatible': 'All Brands', 'warranty': 12, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400&q=80'},
            
            # Transmission
            {'name': 'Clutch Pressure Plate', 'category': 'Transmission', 'part_number': 'TRN-CLP-001', 'brand': 'Exedy', 'price': 4200, 'stock': 22, 'compatible': 'Maruti, Hyundai, Honda', 'warranty': 12, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&q=80'},
            {'name': 'Clutch Disc Kit', 'category': 'Transmission', 'part_number': 'TRN-CLD-002', 'brand': 'Valeo', 'price': 3800, 'stock': 30, 'compatible': 'All Brands', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&q=80'},
            {'name': 'CV Joint Boot Kit', 'category': 'Transmission', 'part_number': 'TRN-CVB-003', 'brand': 'GKN', 'price': 850, 'stock': 60, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&q=80'},
            {'name': 'Transmission Oil ATF (1L)', 'category': 'Transmission', 'part_number': 'TRN-OIL-004', 'brand': 'Shell', 'price': 680, 'stock': 120, 'compatible': 'All Brands', 'warranty': 0, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&q=80'},
            
            # Body & Exterior
            {'name': 'Front Bumper Assembly', 'category': 'Body & Exterior', 'part_number': 'BDY-BMP-001', 'brand': 'OEM', 'price': 6800, 'stock': 8, 'compatible': 'Maruti Swift, Baleno', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=400&q=80'},
            {'name': 'Headlight Assembly (LED)', 'category': 'Body & Exterior', 'part_number': 'BDY-HLT-002', 'brand': 'Hella', 'price': 5200, 'stock': 15, 'compatible': 'Maruti, Hyundai', 'warranty': 12, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=400&q=80'},
            {'name': 'Side Mirror (Power Adjust)', 'category': 'Body & Exterior', 'part_number': 'BDY-MIR-003', 'brand': 'OEM', 'price': 2400, 'stock': 25, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=400&q=80'},
            {'name': 'Windshield Glass', 'category': 'Body & Exterior', 'part_number': 'BDY-WND-004', 'brand': 'Saint-Gobain', 'price': 4500, 'stock': 12, 'compatible': 'Maruti, Hyundai, Honda', 'warranty': 12, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=400&q=80'},
            
            # Interior Parts
            {'name': 'Seat Cover Set (Leather)', 'category': 'Interior Parts', 'part_number': 'INT-SCT-001', 'brand': 'Autofurnish', 'price': 3200, 'stock': 40, 'compatible': 'All Brands', 'warranty': 6, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&q=80'},
            {'name': 'Dashboard Panel', 'category': 'Interior Parts', 'part_number': 'INT-DSH-002', 'brand': 'OEM', 'price': 5800, 'stock': 10, 'compatible': 'Maruti Swift, Dzire', 'warranty': 12, 'is_oem': True, 'image': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&q=80'},
            {'name': 'Floor Mat Set (Premium)', 'category': 'Interior Parts', 'part_number': 'INT-FLM-003', 'brand': 'Elegant', 'price': 1200, 'stock': 80, 'compatible': 'All Brands', 'warranty': 3, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&q=80'},
            {'name': 'Steering Wheel Cover', 'category': 'Interior Parts', 'part_number': 'INT-STR-004', 'brand': 'Sparco', 'price': 850, 'stock': 100, 'compatible': 'All Brands', 'warranty': 3, 'is_oem': False, 'image': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&q=80'},
        ]
        
        # Create parts
        for part_data in sample_parts:
            part = SparePart(
                name=part_data['name'],
                category_id=categories[part_data['category']].id,
                part_number=part_data['part_number'],
                brand=part_data['brand'],
                price=part_data['price'],
                stock_quantity=part_data['stock'],
                image_url=part_data['image'],
                description=f"High-quality {part_data['name']} from {part_data['brand']}. Compatible with {part_data['compatible']}.",
                compatible_brands=part_data['compatible'],
                warranty_months=part_data['warranty'],
                is_oem=part_data['is_oem']
            )
            db.session.add(part)
            print(f"  ✓ Added: {part_data['name']} ({part_data['brand']})")
        
        db.session.commit()
        print("\n✅ Spare parts database initialized successfully!")
        print(f"   - {len(categories_data)} categories created")
        print(f"   - {len(sample_parts)} parts added")

if __name__ == '__main__':
    init_spare_parts()
