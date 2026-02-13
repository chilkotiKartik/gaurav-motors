from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import secrets
from io import BytesIO
from urllib.parse import quote

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hmsdevsecret-change-in-production')

# Database Configuration - supports PostgreSQL (Render/Vercel/Production) and SQLite (Local)
IS_VERCEL = os.environ.get('VERCEL', False)
IS_RENDER = os.environ.get('RENDER', False)
DATABASE_URL = os.environ.get('DATABASE_URL')

# For production (Vercel/Render), DATABASE_URL must be set
if DATABASE_URL:
    # Use PostgreSQL in production (Render, Heroku, Vercel, etc.)
    db_uri = DATABASE_URL
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
elif IS_VERCEL or IS_RENDER:
    # Production environment without DATABASE_URL - this will cause an error
    # Force user to set DATABASE_URL environment variable
    raise RuntimeError(
        "DATABASE_URL environment variable is required for production deployment. "
        "Please set DATABASE_URL in your Vercel/Render environment settings."
    )
else:
    # Use local SQLite for development
    DB_PATH = os.path.join(os.path.dirname(__file__), 'hms.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.replace(chr(92), '/')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@gmmotors.com')

# File Upload Configuration
if IS_VERCEL:
    UPLOAD_FOLDER = '/tmp/uploads'
else:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Session security (disable HTTPS requirement for development)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'technician', 'customer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ServiceDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(300))
    technicians = db.relationship('TechnicianProfile', backref='service_department', lazy=True)

class TechnicianProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)  # Engine, Transmission, Electrical etc.
    department_id = db.Column(db.Integer, db.ForeignKey('service_department.id'), nullable=True)
    availability = db.Column(db.String(300))  # simple text or JSON string of available days/times
    user = db.relationship('User', backref='technician_profile', uselist=False)
    service_bookings = db.relationship('ServiceBooking', backref='technician', lazy=True)
    avail_slots = db.relationship('Availability', backref='technician', lazy=True, cascade='all, delete-orphan')

class CustomerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(40))
    user = db.relationship('User', backref='customer_profile', uselist=False)

# Note: ServiceBooking model defined later in the file with enhanced fields

class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)


class ServiceWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_booking_id = db.Column(db.Integer, db.ForeignKey('service_booking.id'), nullable=False)
    assessment = db.Column(db.String(500))  # Issues found during inspection
    work_performed = db.Column(db.String(500))  # Services/repairs performed
    parts_used = db.Column(db.String(500))  # Parts replaced/installed
    recommendations = db.Column(db.String(500))  # Future maintenance recommendations
    labor_cost = db.Column(db.Float, default=0.0)
    parts_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    notes = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Spare Parts Models
class SparePartCategory(db.Model):
    __tablename__ = 'spare_part_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))  # Font Awesome icon name
    color = db.Column(db.String(20))  # Hex color code
    image_url = db.Column(db.String(500))  # Unsplash or local image URL
    description = db.Column(db.String(500))
    parts = db.relationship('SparePart', backref='category', lazy=True, cascade='all, delete-orphan')

class SparePart(db.Model):
    __tablename__ = 'spare_part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('spare_part_category.id'), nullable=False)
    part_number = db.Column(db.String(100), unique=True)
    brand = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    compatible_brands = db.Column(db.String(300))  # Comma-separated car brands
    warranty_months = db.Column(db.Integer, default=6)
    is_oem = db.Column(db.Boolean, default=False)  # Original Equipment Manufacturer
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    orders = db.relationship('PartOrder', backref='part', lazy=True)

class PartOrder(db.Model):
    __tablename__ = 'part_order'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)  # GM-PART-00001
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    advance_amount = db.Column(db.Float, nullable=False)  # 50% advance
    remaining_amount = db.Column(db.Float, nullable=False)  # 50% on delivery
    total_price = db.Column(db.Float, nullable=False)
    car_brand = db.Column(db.String(50))
    car_model = db.Column(db.String(100))
    car_year = db.Column(db.Integer)
    installation_required = db.Column(db.Boolean, default=False)
    installation_charges = db.Column(db.Float, default=0)
    delivery_address = db.Column(db.String(500))
    payment_status = db.Column(db.String(20), default='Pending')  # Pending/Advance Paid/Fully Paid
    order_status = db.Column(db.String(20), default='Pending')  # Pending/Confirmed/Processing/Shipped/Delivered/Cancelled
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    notes = db.Column(db.String(500))
    admin_notes = db.Column(db.String(500))

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)  # For guest users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # For logged-in users
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.id'))
    accessory_id = db.Column(db.Integer, db.ForeignKey('car_accessory.id'))
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    part = db.relationship('SparePart', backref='cart_items', foreign_keys=[part_id])
    accessory = db.relationship('CarAccessory', backref='cart_items', foreign_keys=[accessory_id])
    user = db.relationship('User', backref='cart_items')

# Car Accessories Models
class AccessoryCategory(db.Model):
    __tablename__ = 'accessory_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))  # Font Awesome icon name
    color = db.Column(db.String(20))  # Hex color code
    image_url = db.Column(db.String(500))  # Category image
    description = db.Column(db.String(500))
    accessories = db.relationship('CarAccessory', backref='category', lazy=True, cascade='all, delete-orphan')

class CarAccessory(db.Model):
    __tablename__ = 'car_accessory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('accessory_category.id'), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    features = db.Column(db.String(1000))  # JSON or comma-separated
    compatible_cars = db.Column(db.String(300))  # Universal or specific cars
    warranty_months = db.Column(db.Integer, default=6)
    is_featured = db.Column(db.Boolean, default=False)
    is_universal = db.Column(db.Boolean, default=True)  # Fits all cars
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Car Service Models
class ServiceCategory(db.Model):
    __tablename__ = 'service_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))  # Emoji or icon
    description = db.Column(db.String(500))
    services = db.relationship('CarService', backref='category', lazy=True, cascade='all, delete-orphan')

class CarService(db.Model):
    __tablename__ = 'car_service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)  # Service duration
    icon = db.Column(db.String(50))
    includes = db.Column(db.String(1000))  # JSON string or comma-separated list
    is_popular = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('ServiceBooking', backref='service', lazy=True)

class ServiceBooking(db.Model):
    __tablename__ = 'service_booking'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False)  # GM123456
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    vehicle_brand = db.Column(db.String(50), nullable=False)
    vehicle_model = db.Column(db.String(100), nullable=False)
    vehicle_year = db.Column(db.Integer)
    vehicle_registration = db.Column(db.String(50))
    service_id = db.Column(db.Integer, db.ForeignKey('car_service.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician_profile.id'), nullable=True)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending/Confirmed/In Progress/Completed/Cancelled
    payment_status = db.Column(db.String(20), default='Pending')  # Pending/Paid/Refunded
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class TimeSlot(db.Model):
    __tablename__ = 'time_slot'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    max_bookings = db.Column(db.Integer, default=3)  # Multiple bookings per slot
    current_bookings = db.Column(db.Integer, default=0)

# Vehicle Records System
class VehicleRecord(db.Model):
    __tablename__ = 'vehicle_record'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_profile.id'), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)  # Service Report, Inspection, Part Replacement, etc.
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))  # Path to uploaded file
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship('CustomerProfile', backref='vehicle_records')

# Vehicle History
class VehicleHistory(db.Model):
    __tablename__ = 'vehicle_history'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_profile.id'), nullable=False)
    make = db.Column(db.String(50))  # Toyota, Honda, etc.
    model = db.Column(db.String(100))  # Camry, Civic, etc.
    year = db.Column(db.Integer)
    vin = db.Column(db.String(17))  # Vehicle Identification Number
    license_plate = db.Column(db.String(20))
    mileage = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20))  # Gasoline, Diesel, Electric, etc.
    transmission = db.Column(db.String(20))  # Manual, Automatic, CVT
    engine_size = db.Column(db.String(20))  # 2.0L, 3.5L V6, etc.
    color = db.Column(db.String(30))
    last_service_date = db.Column(db.Date)
    next_service_due = db.Column(db.Date)
    insurance_company = db.Column(db.String(200))
    insurance_policy = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = db.relationship('CustomerProfile', backref='vehicle_history', uselist=False)

# Technician Reviews and Ratings
class TechnicianReview(db.Model):
    __tablename__ = 'technician_review'
    id = db.Column(db.Integer, primary_key=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician_profile.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_profile.id'), nullable=False)
    service_booking_id = db.Column(db.Integer, db.ForeignKey('service_booking.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=True)  # Verified customer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    technician_profile = db.relationship('TechnicianProfile', backref='reviews')
    customer = db.relationship('CustomerProfile', backref='reviews')

# Service Reviews
class ServiceReview(db.Model):
    __tablename__ = 'service_review'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('service_booking.id'), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    booking = db.relationship('ServiceBooking', backref='review', uselist=False)

# Payment Records
class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(100), unique=True, nullable=False)  # Razorpay/Stripe ID
    service_booking_id = db.Column(db.Integer, db.ForeignKey('service_booking.id'))
    part_order_id = db.Column(db.Integer, db.ForeignKey('part_order.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    payment_method = db.Column(db.String(50))  # Card, UPI, Net Banking
    status = db.Column(db.String(20), default='Pending')  # Pending/Success/Failed/Refunded
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    receipt_url = db.Column(db.String(500))

# Notifications System
class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # booking, payment, reminder, system
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notifications')

# Email Queue for async sending
class EmailQueue(db.Model):
    __tablename__ = 'email_queue'
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_sent = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Auto-initialize database on Vercel (ephemeral /tmp filesystem)
def init_vercel_db():
    """Create tables and seed data for Vercel deployment"""
    if not os.path.exists(DB_PATH):
        db.create_all()
        # Create default admin user
        admin = User(
            username='admin',
            email='admin@gauravmotors.com',
            password_hash=generate_password_hash('Admin@123456'),
            role='admin'
        )
        db.session.add(admin)
        
        # Create sample technician
        tech_user = User(
            username='drjohn',
            email='technician@gauravmotors.com',
            password_hash=generate_password_hash('doctor'),
            role='technician'
        )
        db.session.add(tech_user)
        db.session.flush()
        
        tech_profile = TechnicianProfile(
            user_id=tech_user.id,
            name='Rajesh Kumar',
            specialization='Engine Specialist',
            availability='Mon-Sat 9AM-6PM'
        )
        db.session.add(tech_profile)
        
        # Create sample customer
        cust_user = User(
            username='kar',
            email='customer@gauravmotors.com',
            password_hash=generate_password_hash('kar123'),
            role='customer'
        )
        db.session.add(cust_user)
        db.session.flush()
        
        cust_profile = CustomerProfile(
            user_id=cust_user.id,
            name='Karan Singh',
            contact='9998887770'
        )
        db.session.add(cust_profile)
        
        # Add sample services
        # Create a service category first
        svc_cat = ServiceCategory(name='General', icon='🔧', description='General automotive services')
        db.session.add(svc_cat)
        db.session.flush()
        
        services = [
            CarService(name='General Service', description='Complete car checkup and maintenance', price=2999.0, duration_minutes=120, category_id=svc_cat.id, is_popular=True),
            CarService(name='Brake Service', description='Brake pad replacement and inspection', price=3500.0, duration_minutes=90, category_id=svc_cat.id),
            CarService(name='AC Service', description='AC gas refill and cleaning', price=2000.0, duration_minutes=60, category_id=svc_cat.id, is_popular=True),
            CarService(name='Engine Repair', description='Engine diagnostics and repair', price=5000.0, duration_minutes=180, category_id=svc_cat.id),
            CarService(name='Oil Change', description='Engine oil and filter replacement', price=1500.0, duration_minutes=45, category_id=svc_cat.id, is_popular=True),
        ]
        db.session.add_all(services)
        
        db.session.commit()
        print("DB initialized with sample data")

# Auto-initialize DB on any deployment (Vercel, Railway, Render, etc.)
IS_PRODUCTION = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER') or IS_VERCEL
if IS_PRODUCTION:
    with app.app_context():
        init_vercel_db()

# Helpers
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

def is_technician():
    return current_user.is_authenticated and current_user.role == 'technician'

def is_customer():
    return current_user.is_authenticated and current_user.role == 'customer'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(recipient, subject, body, html=True):
    """Send email notification"""
    try:
        msg = Message(subject, recipients=[recipient])
        if html:
            msg.html = body
        else:
            msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        # Queue for retry
        email = EmailQueue(recipient=recipient, subject=subject, body=body)
        db.session.add(email)
        db.session.commit()
        return False

def send_service_confirmation(booking):
    """Send service booking confirmation email"""
    customer_email = booking.customer_email
    subject = f"Service Booking Confirmed - {booking.booking_date}"
    body = f"""
    <h2>Service Booking Confirmation</h2>
    <p>Dear {booking.customer_name},</p>
    <p>Your service booking has been confirmed with the following details:</p>
    <ul>
        <li><strong>Vehicle:</strong> {booking.vehicle_brand} {booking.vehicle_model} ({booking.vehicle_year})</li>
        <li><strong>Service:</strong> {booking.service.name if hasattr(booking, 'service') else 'Service Booking'}</li>
        <li><strong>Date:</strong> {booking.booking_date.strftime('%B %d, %Y')}</li>
        <li><strong>Time:</strong> {booking.booking_time.strftime('%I:%M %p')}</li>
        <li><strong>Total Amount:</strong> ₹{booking.total_amount}</li>
    </ul>
    <p>Please arrive 10 minutes before your scheduled time.</p>
    <p>Best regards,<br>Gaurav Motors Team</p>
    """
    send_email(customer_email, subject, body)

def create_notification(user_id, title, message, notification_type='system'):
    """Create in-app notification"""
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )
    db.session.add(notification)
    db.session.commit()

def calculate_technician_rating(technician_id):
    """Calculate average rating for a technician"""
    reviews = TechnicianReview.query.filter_by(technician_id=technician_id).all()
    if not reviews:
        return 0
    total = sum(review.rating for review in reviews)
    return round(total / len(reviews), 1)

def get_dashboard_stats():
    """Get comprehensive statistics for admin dashboard"""
    today = datetime.now().date()
    this_month = datetime.now().replace(day=1).date()
    
    stats = {
        'total_customers': CustomerProfile.query.count(),
        'total_technicians': TechnicianProfile.query.count(),
        'total_bookings': ServiceBooking.query.count(),
        'todays_bookings': ServiceBooking.query.filter_by(booking_date=today).count(),
        'pending_bookings': ServiceBooking.query.filter_by(status='Pending').count(),
        'completed_bookings': ServiceBooking.query.filter_by(status='Completed').count(),
        'monthly_bookings': ServiceBooking.query.filter(ServiceBooking.booking_date >= this_month).count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).filter_by(status='Success').scalar() or 0,
        'monthly_revenue': db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.status == 'Success',
            Payment.transaction_date >= datetime.now().replace(day=1)
        ).scalar() or 0,
        'service_bookings': ServiceBooking.query.count(),
        'pending_service_bookings': ServiceBooking.query.filter_by(status='Pending').count(),
        'spare_parts_orders': PartOrder.query.count(),
        'average_rating': db.session.query(db.func.avg(TechnicianReview.rating)).scalar() or 0
    }
    return stats

# Routes
@app.route('/')
def index():
    return render_template('hms/index_premium.html')

@app.route('/about')
def about():
    return render_template('hms/about_premium.html')

@app.route('/services')
def services():
    """Premium services page with modern design"""
    return render_template('hms/services_new.html')

@app.route('/book-car-service')
def book_car_service():
    """Redirect to WhatsApp for quick service booking"""
    phone = "919997612579"  # Gaurav Motors WhatsApp number
    message = ("🚗 *Hi Gaurav Motors!*\n\n"
               "I want to book a car service.\n\n"
               "📋 *My Details:*\n"
               "• Name: \n"
               "• Phone: \n"
               "• Car Model: \n"
               "• Service Needed: \n"
               "• Preferred Date: \n\n"
               "Please confirm availability. Thank you! 🙏")
    
    whatsapp_url = f"https://wa.me/{phone}?text={quote(message)}"
    return redirect(whatsapp_url)

@app.route('/book-service', methods=['POST'])
def confirm_car_service():
    """Process car service booking with 50% advance payment"""
    try:
        # Get form data
        service_type = request.form.get('service_type')
        service_price = float(request.form.get('service_price', 0))
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        preferred_date = request.form.get('preferred_date')
        car_make = request.form.get('car_make')
        car_model = request.form.get('car_model')
        registration_number = request.form.get('registration_number')
        manufacture_year = request.form.get('manufacture_year')
        mileage = request.form.get('mileage')
        fuel_type = request.form.get('fuel_type')
        pickup_service = 'pickup_service' in request.form
        wash_service = 'wash_service' in request.form
        additional_notes = request.form.get('additional_notes', '')
        payment_method = request.form.get('payment_method', 'COD')
        
        # Add wash service charge if selected
        if wash_service:
            service_price += 300
        
        # Calculate 50% advance
        advance_amount = service_price * 0.5
        remaining_amount = service_price * 0.5
        
        # Generate booking number
        import random
        booking_number = f'SRV-{datetime.now().year}-{random.randint(1000, 9999)}'
        
        # Create vehicle details string
        vehicle_details = f"{car_make} {car_model} ({registration_number})"
        if manufacture_year:
            vehicle_details += f" - {manufacture_year}"
        if fuel_type:
            vehicle_details += f" - {fuel_type}"
        if mileage:
            vehicle_details += f" - {mileage} km"
        
        # Create service booking notes
        booking_notes = f"Service Type: {service_type.title()}\n"
        booking_notes += f"Preferred Date: {preferred_date}\n"
        booking_notes += f"Vehicle: {vehicle_details}\n"
        if pickup_service:
            booking_notes += "Pickup Service: Yes\n"
        if wash_service:
            booking_notes += "Car Wash: Yes (+₹300)\n"
        if additional_notes:
            booking_notes += f"Notes: {additional_notes}\n"
        
        # In a real application, save this to database
        # For now, we'll just show success message
        
        # Send confirmation email if provided
        if customer_email:
            try:
                subject = f"Service Booking Confirmed - {booking_number}"
                body = f"""
                <h2>Service Booking Confirmation</h2>
                <p>Dear {customer_name},</p>
                <p>Your car service booking has been confirmed!</p>
                
                <h3>Booking Details:</h3>
                <ul>
                    <li><strong>Booking Number:</strong> {booking_number}</li>
                    <li><strong>Service Type:</strong> {service_type.title()} Service</li>
                    <li><strong>Preferred Date:</strong> {preferred_date}</li>
                    <li><strong>Vehicle:</strong> {vehicle_details}</li>
                    <li><strong>Total Amount:</strong> ₹{service_price}</li>
                    <li><strong>Advance (50%):</strong> ₹{advance_amount}</li>
                    <li><strong>After Service (50%):</strong> ₹{remaining_amount}</li>
                    <li><strong>Payment Method:</strong> {payment_method}</li>
                </ul>
                
                {f'<p><strong>Additional Services:</strong></p><ul>' if pickup_service or wash_service else ''}
                {f'<li>Free Pick-up & Drop Service</li>' if pickup_service else ''}
                {f'<li>Complimentary Car Wash</li>' if wash_service else ''}
                {'</ul>' if pickup_service or wash_service else ''}
                
                <p>We will contact you at {customer_phone} to confirm the booking.</p>
                
                <p>Thank you for choosing GM Motors!</p>
                <p>Best regards,<br>GM Motors Team</p>
                """
                send_email(customer_email, subject, body)
            except:
                pass
        
        flash(f'🎉 Service Booking Confirmed! Booking ID: {booking_number}. We will contact you shortly at {customer_phone}.', 'success')
        return redirect(url_for('services'))
        
    except Exception as e:
        flash(f'Error processing booking: {str(e)}', 'danger')
        return redirect(url_for('services'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # In a real app, you would save this to database or send email
        flash('Thank you for contacting us! We will get back to you soon. 🌿', 'success')
        return redirect(url_for('contact'))
    return render_template('hms/contact_premium.html')

@app.route('/faq')
def faq():
    return render_template('hms/faq.html')

# Auth
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form.get('name')
        contact = request.form.get('contact')
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, email=email, role='customer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        customer = CustomerProfile(user_id=user.id, name=name or username, contact=contact)
        db.session.add(customer)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('hms/register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'technician':
                return redirect(url_for('technician_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('hms/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

# Admin
@app.route('/admin')
@login_required
def admin_dashboard():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    num_technicians = TechnicianProfile.query.count()
    num_customers = CustomerProfile.query.count()
    num_service_bookings = ServiceBooking.query.count()
    technicians = TechnicianProfile.query.all()
    return render_template('hms/admin_dashboard.html', technicians=technicians, num_technicians=num_technicians, num_customers=num_customers, num_service_bookings=num_service_bookings)


@app.route('/admin/customers')
@login_required
def admin_customers():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    q = request.args.get('q')
    if q:
        customers = CustomerProfile.query.filter(CustomerProfile.name.contains(q)).all()
    else:
        customers = CustomerProfile.query.all()
    return render_template('hms/admin_customers.html', customers=customers)


@app.route('/admin/service-bookings')
@login_required
def admin_service_bookings():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    service_bookings = ServiceBooking.query.order_by(ServiceBooking.booking_date.desc(), ServiceBooking.booking_time.desc()).all()
    
    # Get booking statistics
    stats = {
        'scheduled': ServiceBooking.query.filter_by(status='Scheduled').count(),
        'in_progress': ServiceBooking.query.filter_by(status='In-Progress').count(),
        'completed': ServiceBooking.query.filter_by(status='Completed').count(),
        'cancelled': ServiceBooking.query.filter_by(status='Cancelled').count()
    }
    
    return render_template('hms/admin_service_bookings.html', service_bookings=service_bookings, stats=stats)


@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    # Use the enhanced analytics dashboard with real-time data
    return render_template('hms/admin_analytics_enhanced.html')


@app.route('/admin/add_customer', methods=['GET','POST'])
@login_required
def admin_add_customer():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        contact = request.form.get('contact')
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('User exists', 'danger')
            return redirect(url_for('admin_add_customer'))
        user = User(username=username, email=email, role='customer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        c = CustomerProfile(user_id=user.id, name=name, contact=contact)
        db.session.add(c)
        db.session.commit()
        flash('Customer added', 'success')
        return redirect(url_for('admin_customers'))
    return render_template('hms/admin_add_customer.html')


@app.route('/admin/edit_customer/<int:customer_id>', methods=['GET','POST'])
@login_required
def admin_edit_customer(customer_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    customer = CustomerProfile.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.contact = request.form.get('contact')
        db.session.commit()
        flash('Customer updated', 'success')
        return redirect(url_for('admin_customers'))
    return render_template('hms/admin_edit_customer.html', customer=customer)


@app.route('/admin/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def admin_delete_customer(customer_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    customer = CustomerProfile.query.get_or_404(customer_id)
    # check if customer has service bookings
    if ServiceBooking.query.filter_by(customer_email=customer.user.email).first():
        flash('Cannot delete customer with existing service bookings', 'danger')
        return redirect(url_for('admin_customers'))
    db.session.delete(customer.user)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted', 'success')
    return redirect(url_for('admin_customers'))

@app.route('/admin/add_technician', methods=['GET','POST'])
@login_required
def admin_add_technician():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        specialization = request.form['specialization']
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('User exists', 'danger')
            return redirect(url_for('admin_add_technician'))
        user = User(username=username, email=email, role='technician')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        tech = TechnicianProfile(user_id=user.id, name=name, specialization=specialization)
        db.session.add(tech)
        db.session.commit()
        flash('Technician added', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('hms/admin_add_technician.html')


@app.route('/admin/edit_technician/<int:technician_id>', methods=['GET','POST'])
@login_required
def admin_edit_technician(technician_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    technician = TechnicianProfile.query.get_or_404(technician_id)
    if request.method == 'POST':
        technician.name = request.form['name']
        technician.specialization = request.form['specialization']
        db.session.commit()
        flash('Technician updated', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('hms/admin_edit_technician.html', technician=technician)


@app.route('/admin/delete_technician/<int:technician_id>', methods=['POST'])
@login_required
def admin_delete_technician(technician_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    technician = TechnicianProfile.query.get_or_404(technician_id)
    # check if technician has service bookings
    if ServiceBooking.query.filter_by(technician_id=technician.id).first():
        flash('Cannot delete technician with existing service bookings', 'danger')
        return redirect(url_for('admin_dashboard'))
    db.session.delete(technician.user)
    db.session.delete(technician)
    db.session.commit()
    flash('Technician deleted', 'success')
    return redirect(url_for('admin_dashboard'))

# Customer Dashboard
@app.route('/customer')
@login_required
def customer_dashboard():
    if not is_customer():
        flash('Customer access required', 'danger')
        return redirect(url_for('index'))
    
    # Get customer profile - handle both single object and list
    customer = current_user.customer_profile
    if isinstance(customer, list):
        customer = customer[0] if customer else None
    
    if not customer:
        flash('Customer profile not found', 'danger')
        return redirect(url_for('index'))
    
    upcoming = ServiceBooking.query.filter_by(customer_email=current_user.email).filter(ServiceBooking.status.in_(['Pending', 'Confirmed', 'In Progress'])).order_by(ServiceBooking.booking_date.desc()).all()
    return render_template('hms/customer_dashboard.html', customer=customer, upcoming=upcoming)


@app.route('/customer/edit', methods=['GET','POST'])
@login_required
def customer_edit():
    if not is_customer():
        flash('Customer access required', 'danger')
        return redirect(url_for('index'))
    
    # Get customer profile - handle both single object and list
    customer = current_user.customer_profile
    if isinstance(customer, list):
        customer = customer[0] if customer else None
    
    if not customer:
        flash('Customer profile not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.contact = request.form.get('contact')
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('customer_dashboard'))
    return render_template('hms/customer_edit.html', customer=customer)

# Old spare-parts route removed - using Coming Soon page instead

@app.route('/book/<int:technician_id>', methods=['GET','POST'])
@login_required
def book(technician_id):
    if not is_customer():
        flash('Only customers can book services', 'danger')
        return redirect(url_for('index'))
    technician = TechnicianProfile.query.get_or_404(technician_id)
    # Show available slots for selected technician
    today = datetime.now().date()
    if request.method == 'POST':
        slot_id = int(request.form.get('slot_id'))
        slot = Availability.query.get_or_404(slot_id)
        if not slot.is_available:
            flash('Slot no longer available', 'danger')
            return redirect(url_for('book', technician_id=technician_id))
        # double-check no booking exists
        existing = ServiceBooking.query.filter_by(technician_id=technician.id, booking_date=slot.date, booking_time=slot.time, status='Scheduled').first()
        if existing:
            slot.is_available = False
            db.session.commit()
            flash('Selected slot not available', 'danger')
            return redirect(url_for('book', technician_id=technician_id))
        
        # Get customer profile - handle both single object and list
        customer_profile = current_user.customer_profile
        if isinstance(customer_profile, list):
            customer_profile = customer_profile[0] if customer_profile else None
        
        if not customer_profile:
            flash('Customer profile not found', 'danger')
            return redirect(url_for('index'))
        
        # Create service booking
        import random, string
        booking_id_str = 'GM' + ''.join(random.choices(string.digits, k=6))
        # Get first available service or default
        first_service = CarService.query.first()
        if not first_service:
            flash('No services available for booking at the moment', 'danger')
            return redirect(url_for('customer_dashboard'))
        service_id = first_service.id
        service_amount = first_service.price
        booking = ServiceBooking(
            booking_id=booking_id_str,
            customer_name=customer_profile.name,
            customer_email=current_user.email,
            customer_phone=customer_profile.contact or '',
            vehicle_brand='', vehicle_model='', vehicle_year=None, vehicle_registration='',
            service_id=service_id,
            technician_id=technician.id,
            booking_date=slot.date,
            booking_time=slot.time,
            status='Scheduled',
            total_amount=service_amount,
            notes=f'Booked with technician: {technician.name}'
        )
        slot.is_available = False
        db.session.add(booking)
        db.session.commit()
        flash('Service booked successfully!', 'success')
        return redirect(url_for('customer_dashboard'))

    days = [today + timedelta(days=i) for i in range(7)]
    # pull availability slots for next 7 days
    slots = Availability.query.filter_by(technician_id=technician.id, is_available=True).filter(Availability.date >= today).order_by(Availability.date, Availability.time).all()
    return render_template('hms/book.html', technician=technician, days=days, slots=slots)

@app.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel(booking_id):
    booking = ServiceBooking.query.get_or_404(booking_id)
    if current_user.role == 'customer' and booking.customer_email != current_user.email:
        flash('Not authorized', 'danger')
        return redirect(url_for('index'))
    booking.status = 'Cancelled'
    # free the availability slot if it exists
    slot = Availability.query.filter_by(technician_id=booking.technician_id, date=booking.booking_date, time=booking.booking_time).first()
    if slot:
        slot.is_available = True
    db.session.commit()
    flash('Service booking cancelled', 'info')
    return redirect(request.referrer or url_for('index'))


@app.route('/reschedule/<int:booking_id>', methods=['GET','POST'])
@login_required
def reschedule(booking_id):
    booking = ServiceBooking.query.get_or_404(booking_id)
    if current_user.role == 'customer' and booking.customer_email != current_user.email:
        flash('Not authorized', 'danger')
        return redirect(url_for('index'))
    if booking.status not in ['Scheduled', 'Confirmed']:
        flash('Can only reschedule scheduled bookings', 'danger')
        return redirect(url_for('customer_dashboard'))
    
    if request.method == 'POST':
        slot_id = request.form.get('slot_id')
        if not slot_id:
            flash('Please select a time slot', 'danger')
            return redirect(url_for('reschedule', booking_id=booking_id))
        
        slot_id = int(slot_id)
        new_slot = Availability.query.get_or_404(slot_id)
        if not new_slot.is_available or new_slot.technician_id != booking.technician_id:
            flash('Slot not available', 'danger')
            return redirect(url_for('reschedule', booking_id=booking_id))
        
        # free old slot
        old_slot = Availability.query.filter_by(technician_id=booking.technician_id, date=booking.booking_date, time=booking.booking_time).first()
        if old_slot:
            old_slot.is_available = True
        
        # take new slot
        booking.booking_date = new_slot.date
        booking.booking_time = new_slot.time
        new_slot.is_available = False
        db.session.commit()
        flash('Service booking rescheduled', 'success')
        return redirect(url_for('customer_dashboard'))
    
    # show available slots for same technician
    today = datetime.now().date()
    slots = Availability.query.filter_by(technician_id=booking.technician_id, is_available=True).filter(Availability.date >= today).order_by(Availability.date, Availability.time).all()
    return render_template('hms/reschedule.html', booking=booking, slots=slots)

# Technician Dashboard
@app.route('/technician')
@login_required
def technician_dashboard():
    if not is_technician():
        flash('Technician access required', 'danger')
        return redirect(url_for('index'))
    
    # Get technician profile - handle both single object and list
    technician = current_user.technician_profile
    if isinstance(technician, list):
        technician = technician[0] if technician else None
    
    if not technician:
        flash('Technician profile not found', 'danger')
        return redirect(url_for('index'))
    
    today = datetime.now().date()
    upcoming = ServiceBooking.query.filter_by(technician_id=technician.id).filter(ServiceBooking.status.in_(['Pending', 'Confirmed', 'In Progress'])).order_by(ServiceBooking.booking_date.desc()).all()
    return render_template('hms/technician_dashboard.html', technician=technician, upcoming=upcoming)

# Spare Parts Routes
@app.route('/part/<int:part_id>')
def part_detail(part_id):
    part = SparePart.query.get_or_404(part_id)
    related_parts = SparePart.query.filter_by(category_id=part.category_id).filter(SparePart.id != part_id).limit(4).all()
    return render_template('hms/part_detail.html', part=part, related_parts=related_parts)

@app.route('/order-part/<int:part_id>', methods=['GET', 'POST'])
def order_part(part_id):
    part = SparePart.query.get_or_404(part_id)
    
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        quantity = int(request.form.get('quantity', 1))
        car_brand = request.form.get('car_brand')
        car_model = request.form.get('car_model')
        car_year = request.form.get('car_year')
        installation = request.form.get('installation') == 'yes'
        notes = request.form.get('notes')
        
        # Check stock
        if part.stock_quantity < quantity:
            flash(f'Sorry, only {part.stock_quantity} units available in stock', 'warning')
            return redirect(url_for('order_part', part_id=part_id))
        
        # Calculate pricing
        unit_price = part.price
        subtotal = unit_price * quantity
        installation_charges = 500.0 if installation else 0.0
        total_price_final = subtotal + installation_charges
        advance_amount = round(total_price_final * 0.5, 2)
        remaining_amount = round(total_price_final - advance_amount, 2)
        
        # Generate order number
        import random, string
        order_number = 'GM-PART-' + ''.join(random.choices(string.digits, k=5))
        
        # Create order
        order = PartOrder(
            order_number=order_number,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            part_id=part.id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            advance_amount=advance_amount,
            remaining_amount=remaining_amount,
            total_price=total_price_final,
            installation_charges=installation_charges,
            car_brand=car_brand,
            car_model=car_model,
            car_year=int(car_year) if car_year else None,
            installation_required=installation,
            notes=notes
        )
        
        # Update stock
        part.stock_quantity -= quantity
        
        db.session.add(order)
        db.session.commit()
        
        flash(f'Order placed successfully! Order #{order.order_number}. We will contact you at {customer_phone}', 'success')
        return redirect(url_for('spare_parts_browse'))
    
    return render_template('hms/order_part.html', part=part)

@app.route('/admin/parts', methods=['GET', 'POST'])
@login_required
def admin_parts():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_part':
            part = SparePart(
                name=request.form.get('name'),
                category_id=int(request.form.get('category_id')),
                part_number=request.form.get('part_number'),
                brand=request.form.get('brand'),
                price=float(request.form.get('price')),
                stock_quantity=int(request.form.get('stock_quantity', 0)),
                image_url=request.form.get('image_url'),
                description=request.form.get('description'),
                compatible_brands=request.form.get('compatible_brands'),
                warranty_months=int(request.form.get('warranty_months', 6)),
                is_oem=request.form.get('is_oem') == 'on'
            )
            db.session.add(part)
            db.session.commit()
            flash('Part added successfully!', 'success')
    
    categories = SparePartCategory.query.all()
    parts = SparePart.query.order_by(SparePart.created_at.desc()).all()
    orders = PartOrder.query.order_by(PartOrder.order_date.desc()).limit(50).all()
    
    return render_template('hms/admin_parts.html', categories=categories, parts=parts, orders=orders)


@app.route('/technician/availability', methods=['GET','POST'])
@login_required
def technician_availability():
    if not is_technician():
        flash('Technician access required', 'danger')
        return redirect(url_for('index'))
    
    # Get technician profile - handle both single object and list
    technician = current_user.technician_profile
    if isinstance(technician, list):
        technician = technician[0] if technician else None
    
    if not technician:
        flash('Technician profile not found', 'danger')
        return redirect(url_for('index'))
    
    today = datetime.now().date()
    days = [today + timedelta(days=i) for i in range(7)]
    if request.method == 'POST':
        pass  # TODO: Handle POST request
    
    return render_template('hms/technician_availability.html', technician=technician, days=days)


# ============================================
# CAR SERVICE BOOKING API ENDPOINTS
# ============================================

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all available car services"""
    try:
        services = CarService.query.filter_by(is_active=True).all()
        services_data = []
        for service in services:
            services_data.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price,
                'duration': service.duration_minutes,
                'icon': service.icon,
                'includes': service.includes,
                'is_popular': service.is_popular,
                'category': service.category.name if service.category else None
            })
        return jsonify({'success': True, 'services': services_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service_detail(service_id):
    """Get specific service details"""
    try:
        service = CarService.query.get_or_404(service_id)
        return jsonify({
            'success': True,
            'service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price,
                'duration': service.duration_minutes,
                'icon': service.icon,
                'includes': service.includes,
                'is_popular': service.is_popular,
                'category': service.category.name if service.category else None
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    """Create a new service booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_phone', 'vehicle_model', 
                          'service_id', 'booking_date', 'booking_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Get service
        service = CarService.query.get(data['service_id'])
        if not service:
            return jsonify({'success': False, 'error': 'Service not found'}), 404
        
        # Generate unique booking ID
        import random
        booking_id = f"GM{random.randint(100000, 999999)}"
        while ServiceBooking.query.filter_by(booking_id=booking_id).first():
            booking_id = f"GM{random.randint(100000, 999999)}"
        
        # Parse date and time
        from datetime import datetime as dt
        booking_date = dt.strptime(data['booking_date'], '%Y-%m-%d').date()
        booking_time = dt.strptime(data['booking_time'], '%H:%M').time()
        
        # Create booking
        booking = ServiceBooking(
            booking_id=booking_id,
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            customer_email=data.get('customer_email', ''),
            vehicle_brand=data.get('vehicle_brand', ''),
            vehicle_model=data['vehicle_model'],
            vehicle_year=data.get('vehicle_year'),
            vehicle_registration=data.get('vehicle_registration', ''),
            service_id=service.id,
            booking_date=booking_date,
            booking_time=booking_time,
            total_amount=service.price,
            notes=data.get('notes', ''),
            status='Confirmed'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'message': 'Booking created successfully',
            'booking': {
                'id': booking.id,
                'booking_id': booking.booking_id,
                'customer_name': booking.customer_name,
                'service_name': service.name,
                'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                'booking_time': booking.booking_time.strftime('%H:%M'),
                'total_amount': booking.total_amount,
                'status': booking.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/booking/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get booking details"""
    try:
        booking = ServiceBooking.query.filter_by(booking_id=booking_id).first_or_404()
        return jsonify({
            'success': True,
            'booking': {
                'booking_id': booking.booking_id,
                'customer_name': booking.customer_name,
                'customer_phone': booking.customer_phone,
                'vehicle_model': booking.vehicle_model,
                'service_name': booking.service.name,
                'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                'booking_time': booking.booking_time.strftime('%H:%M'),
                'total_amount': booking.total_amount,
                'status': booking.status
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@app.route('/api/timeslots/<date>', methods=['GET'])
def get_available_timeslots(date):
    """Get available time slots for a specific date"""
    try:
        from datetime import datetime as dt
        target_date = dt.strptime(date, '%Y-%m-%d').date()
        
        # Define available time slots
        time_slots = [
            '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '14:00', '14:30', '15:00', '15:30',
            '16:00', '16:30', '17:00', '17:30'
        ]
        
        # Get existing bookings for this date
        bookings = ServiceBooking.query.filter_by(booking_date=target_date).all()
        booked_times = [b.booking_time.strftime('%H:%M') for b in bookings]
        
        available_slots = []
        for slot in time_slots:
            # Count bookings at this time (allow up to 3 bookings per slot)
            count = booked_times.count(slot)
            if count < 3:
                available_slots.append({
                    'time': slot,
                    'available': True,
                    'remaining': 3 - count
                })
        
        return jsonify({'success': True, 'date': date, 'slots': available_slots})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/booking/validate', methods=['POST'])
def validate_booking():
    """Validate booking data before creating"""
    try:
        data = request.get_json()
        errors = []

        # Validate phone number
        phone = data.get('customer_phone', '')
        if not phone or len(phone) < 10:
            errors.append('Valid phone number required')

        # Validate service
        service_id = data.get('service_id')
        if not service_id or not CarService.query.get(service_id):
            errors.append('Valid service selection required')

        # Validate date (must be future date)
        from datetime import datetime as dt
        try:
            booking_date = dt.strptime(data.get('booking_date', ''), '%Y-%m-%d').date()
            if booking_date < dt.now().date():
                errors.append('Booking date must be in the future')
        except:
            errors.append('Invalid date format')

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        return jsonify({'success': True, 'message': 'Validation passed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()

        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400

        # Simple chatbot responses based on keywords
        response = get_chatbot_response(user_message)

        return jsonify({
            'success': True,
            'response': response
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_chatbot_response(message):
    """Generate chatbot response based on user message"""
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon', 'good evening']):
        response = "👋 Hello! Welcome to Gaurav Motors!\n\nI'm your AI assistant. I can help you with:\n\n✓ Book car services\n✓ Find spare parts\n✓ Check prices\n✓ Get contact info\n✓ Learn about accessories\n✓ Emergency support\n\nWhat can I help you with today? 😊"
    
    # Service related queries
    elif any(word in message for word in ['service', 'services', 'repair', 'maintenance', 'fix']):
        services = CarService.query.filter_by(is_active=True).limit(5).all()
        if services:
            response = "Here are our available services:\n"
            for service in services:
                response += f"• {service.name} - ₹{service.price} ({service.duration_minutes} mins)\n"
            response += "\nYou can book a service through our website or contact us directly."
        else:
            response = "We offer various car services including maintenance, repairs, and detailing. Please visit our services page for more details."

    # Spare parts queries
    elif any(word in message for word in ['part', 'parts', 'spare', 'component']):
        categories = SparePartCategory.query.all()
        if categories:
            response = "We have spare parts in these categories:\n"
            for cat in categories:
                response += f"• {cat.name}\n"
            response += "\nBrowse our spare parts catalog on the website."
        else:
            response = "We stock a wide range of genuine spare parts for various car brands. Check our spare parts section."

    # Contact/About queries
    elif any(word in message for word in ['contact', 'phone', 'address', 'location']):
        response = "You can reach us at:\n📞 Phone: +91 9997612579\n📱 WhatsApp: +91 9997612579\n📍 Location: Lohaghat, Champawat, Uttarakhand\n⏰ Hours: Open 7 Days, 9 AM - 7 PM\n\nVisit our contact page for more details and map!"

    elif any(word in message for word in ['about', 'company', 'who', 'gaurav']):
        response = "🏆 Gaurav Motors - Uttarakhand's #1 Auto Workshop!\n\n✓ Established 2010\n✓ ISO Certified\n✓ 5000+ Happy Customers\n✓ Expert Technicians\n✓ Genuine Parts\n✓ Lifetime Warranty\n\nWe provide complete automotive solutions - from services to spare parts to accessories!"

    # Booking queries
    elif any(word in message for word in ['appointment', 'schedule', 'time', 'slot', 'booking', 'reserve']):
        response = "📅 Book Your Service:\n\n1. Click 'Book Service Now' button\n2. Choose your service\n3. Fill in your vehicle details\n4. Select preferred date/time\n5. Pay 50% advance\n\n✅ Quick & Easy!\n📞 Or call: +91 9997612579"

    # Price/Cost queries
    elif any(word in message for word in ['price', 'cost', 'fee', 'charge', 'rate']):
        response = "💰 Our Competitive Pricing:\n\n🔧 General Service: ₹2,500\n🛑 Brake Service: ₹3,500\n❄️ AC Service: ₹2,000\n⚙️ Engine Service: ₹4,500\n⚡ Electrical: ₹1,500\n\n💳 50% advance payment accepted\n📞 Call for custom quote: 9997612579"

    # Emergency/Urgent queries
    elif any(word in message for word in ['emergency', 'urgent', 'breakdown', 'tow', 'help']):
        response = "🚨 EMERGENCY SERVICES:\n\n📞 Call NOW: +91 9997612579\n💬 WhatsApp: +91 9997612579\n\n24/7 Emergency Support Available!\nRoadside Assistance • Towing • Quick Repairs\n\nWe're here to help! 🚗"

    # Accessories queries  
    elif any(word in message for word in ['accessory', 'accessories', 'upgrade', 'interior', 'exterior']):
        response = "🚗 Premium Car Accessories:\n\n✓ Interior: Seat covers, floor mats, steering covers\n✓ Electronics: Dashcams, GPS, Bluetooth devices\n✓ Exterior: LED lights, chrome parts, body covers\n✓ Safety: Alarms, TPMS, fire extinguishers\n✓ Performance: Air filters, exhausts\n✓ Care: Polish, wax, vacuum cleaners\n\n🛒 Shop Now! Free installation available!"

    # Default response
    else:
        response = "I'm here to help with information about our car services, spare parts, appointments, and more. You can ask me about:\n• Available services and pricing\n• Spare parts availability\n• Booking appointments\n• Contact information\n• Emergency services"

    return response

@app.route('/booking/<int:booking_id>', methods=['GET','POST'])
@login_required
def booking_detail(booking_id):
    booking = ServiceBooking.query.get_or_404(booking_id)
    if current_user.role == 'technician' and hasattr(booking, 'technician_id') and booking.technician_id:
        tech_profile = current_user.technician_profile
        if isinstance(tech_profile, list):
            tech_profile = tech_profile[0] if tech_profile else None
        if tech_profile and booking.technician_id != tech_profile.id:
            flash('Not authorized', 'danger')
            return redirect(url_for('index'))
    
    if request.method == 'POST':
        # technician marks completed and records work
        status = request.form.get('status')
        assessment = request.form.get('assessment')
        work_performed = request.form.get('work_performed')
        parts_used = request.form.get('parts_used')
        recommendations = request.form.get('recommendations')
        
        if status == 'Completed':
            booking.status = 'Completed'
            work = ServiceWork(
                service_booking_id=booking.id,
                assessment=assessment,
                work_performed=work_performed,
                parts_used=parts_used,
                recommendations=recommendations
            )
            db.session.add(work)
            db.session.commit()
            flash('Service booking completed and work saved', 'success')
            return redirect(url_for('technician_dashboard'))
        elif status == 'Cancelled':
            booking.status = 'Cancelled'
            db.session.commit()
            flash('Service booking cancelled', 'info')
            return redirect(url_for('technician_dashboard'))
    
    return render_template('hms/booking_detail.html', booking=booking)

# ===== NEW ADVANCED FEATURES =====

# Vehicle Records Routes
@app.route('/customer/vehicle-records')
@login_required
def customer_vehicle_records():
    """View customer's vehicle records"""
    if not is_customer():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    customer = current_user.customer_profile
    if isinstance(customer, list):
        customer = customer[0] if customer else None
    
    if not customer:
        flash('Customer profile not found', 'danger')
        return redirect(url_for('index'))
    
    records = VehicleRecord.query.filter_by(customer_id=customer.id).order_by(VehicleRecord.upload_date.desc()).all()
    history = VehicleHistory.query.filter_by(customer_id=customer.id).first()
    
    return render_template('hms/vehicle_records.html', records=records, history=history)

@app.route('/customer/vehicle-history', methods=['GET', 'POST'])
@login_required
def update_vehicle_history():
    """Update customer vehicle history"""
    if not is_customer():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    customer = current_user.customer_profile
    if isinstance(customer, list):
        customer = customer[0] if customer else None
    
    if not customer:
        flash('Customer profile not found', 'danger')
        return redirect(url_for('index'))
    
    history = VehicleHistory.query.filter_by(customer_id=customer.id).first()
    
    if request.method == 'POST':
        if not history:
            history = VehicleHistory(customer_id=customer.id)
        
        history.make = request.form.get('make')
        history.model = request.form.get('model')
        history.year = int(request.form.get('year')) if request.form.get('year') else None
        history.vin = request.form.get('vin')
        history.license_plate = request.form.get('license_plate')
        history.mileage = int(request.form.get('mileage')) if request.form.get('mileage') else None
        history.fuel_type = request.form.get('fuel_type')
        history.transmission = request.form.get('transmission')
        history.engine_size = request.form.get('engine_size')
        history.color = request.form.get('color')
        history.insurance_company = request.form.get('insurance_company')
        history.insurance_policy = request.form.get('insurance_policy')
        
        db.session.add(history)
        db.session.commit()
        flash('Vehicle history updated successfully', 'success')
        return redirect(url_for('customer_vehicle_records'))
    
    return render_template('hms/vehicle_history_form.html', history=history)

@app.route('/upload-vehicle-record', methods=['POST'])
@login_required
def upload_vehicle_record():
    """Upload vehicle record file"""
    if not is_customer():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    if 'file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(request.referrer or url_for('customer_vehicle_records'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer or url_for('customer_vehicle_records'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        customer = current_user.customer_profile
        if isinstance(customer, list):
            customer = customer[0] if customer else None
        
        if not customer:
            flash('Customer profile not found', 'danger')
            return redirect(url_for('index'))
        
        record = VehicleRecord(
            customer_id=customer.id,
            record_type=request.form.get('record_type', 'Service Report'),
            title=request.form.get('title', filename),
            description=request.form.get('description'),
            file_path=filename,
            uploaded_by=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        
        flash('Vehicle record uploaded successfully', 'success')
    else:
        flash('Invalid file type', 'danger')
    
    return redirect(url_for('customer_vehicle_records'))

# Technician Reviews Routes
@app.route('/technician/<int:technician_id>/reviews')
def technician_reviews(technician_id):
    """View technician reviews"""
    technician = TechnicianProfile.query.get_or_404(technician_id)
    reviews = TechnicianReview.query.filter_by(technician_id=technician_id).order_by(TechnicianReview.created_at.desc()).all()
    avg_rating = calculate_technician_rating(technician_id)
    
    return render_template('hms/technician_reviews.html', technician=technician, reviews=reviews, avg_rating=avg_rating)

@app.route('/booking/<int:booking_id>/review', methods=['GET', 'POST'])
@login_required
def submit_review(booking_id):
    """Submit review for completed service booking"""
    if not is_customer():
        flash('Only customers can submit reviews', 'danger')
        return redirect(url_for('index'))
    
    booking = ServiceBooking.query.get_or_404(booking_id)
    
    if booking.status != 'Completed':
        flash('Can only review completed service bookings', 'warning')
        return redirect(url_for('customer_dashboard'))
    
    # Check if already reviewed
    existing_review = TechnicianReview.query.filter_by(service_booking_id=booking_id).first()
    if existing_review:
        flash('You have already reviewed this service', 'info')
        return redirect(url_for('customer_dashboard'))
    
    if request.method == 'POST':
        rating = int(request.form.get('rating', 0))
        comment = request.form.get('comment')
        
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5', 'danger')
            return redirect(request.referrer)
        
        customer = current_user.customer_profile
        if isinstance(customer, list):
            customer = customer[0] if customer else None
        
        if not customer:
            flash('Customer profile not found', 'danger')
            return redirect(url_for('index'))
        
        # Get technician_id from booking if it exists
        technician_id = None
        if hasattr(booking, 'technician_id'):
            technician_id = booking.technician_id
        
        if not technician_id:
            flash('Cannot submit review: no technician assigned to this booking', 'warning')
            return redirect(url_for('customer_dashboard'))
        
        review = TechnicianReview(
            technician_id=technician_id,
            customer_id=customer.id,
            service_booking_id=booking_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('customer_dashboard'))
    
    return render_template('hms/submit_review.html', booking=booking)

# Notifications Routes
@app.route('/api/notifications')
@login_required
def get_notifications():
    """Get user notifications"""
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(20).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    
    return jsonify({
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for n in notifications],
        'unread_count': unread_count
    })

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

# Advanced Search Routes
@app.route('/search')
def search():
    """Universal search across technicians, services, and parts"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    results = {
        'technicians': [],
        'services': [],
        'parts': []
    }
    
    if query:
        if category in ['all', 'technicians']:
            technicians = TechnicianProfile.query.filter(
                (TechnicianProfile.name.ilike(f'%{query}%')) |
                (TechnicianProfile.specialization.ilike(f'%{query}%'))
            ).all()
            results['technicians'] = technicians
        
        if category in ['all', 'services']:
            services = CarService.query.filter(
                CarService.is_active == True,
                (CarService.name.ilike(f'%{query}%')) |
                (CarService.description.ilike(f'%{query}%'))
            ).all()
            results['services'] = services
        
        if category in ['all', 'parts']:
            parts = SparePart.query.filter(
                (SparePart.name.ilike(f'%{query}%')) |
                (SparePart.description.ilike(f'%{query}%')) |
                (SparePart.brand.ilike(f'%{query}%'))
            ).all()
            results['parts'] = parts
    
    return render_template('hms/search_results.html', query=query, results=results, category=category)

# Export Routes
@app.route('/admin/export/service-bookings')
@login_required
def export_service_bookings():
    """Export service bookings to CSV"""
    if not is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    bookings = ServiceBooking.query.order_by(ServiceBooking.booking_date.desc()).all()
    
    # Create CSV in memory
    output = BytesIO()
    output.write(b'ID,Customer Name,Email,Phone,Service ID,Date,Time,Status,Amount,Created At\n')
    
    for booking in bookings:
        line = f'{booking.id},{booking.customer_name},{booking.customer_email},{booking.customer_phone},{booking.service_id},{booking.booking_date},{booking.booking_time},{booking.status},{booking.total_amount},{booking.created_at}\n'
        output.write(line.encode('utf-8'))
    
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bookings_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/admin/export/revenue')
@login_required
def export_revenue():
    """Export revenue data to CSV"""
    if not is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    payments = Payment.query.filter_by(status='Success').order_by(Payment.transaction_date.desc()).all()
    
    output = BytesIO()
    output.write(b'ID,Payment ID,Amount,Currency,Method,Date,Type\n')
    
    for payment in payments:
        payment_type = 'Service' if payment.service_booking_id else 'Part Order' if payment.part_order_id else 'Other'
        line = f'{payment.id},{payment.payment_id},{payment.amount},{payment.currency},{payment.payment_method},{payment.transaction_date},{payment_type}\n'
        output.write(line.encode('utf-8'))
    
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'revenue_{datetime.now().strftime("%Y%m%d")}.csv'
    )

# API Routes for Analytics
@app.route('/api/analytics/dashboard')
@login_required
def analytics_dashboard():
    """Get comprehensive dashboard analytics"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/analytics/bookings-by-month')
@login_required
def bookings_by_month():
    """Get service bookings grouped by month for charts"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get last 12 months data
    monthly_data = db.session.query(
        db.func.strftime('%Y-%m', ServiceBooking.booking_date).label('month'),
        db.func.count(ServiceBooking.id).label('count')
    ).group_by('month').order_by('month').limit(12).all()
    
    return jsonify({
        'labels': [item.month for item in monthly_data],
        'data': [item.count for item in monthly_data]
    })

@app.route('/api/analytics/revenue-by-month')
@login_required
def revenue_by_month():
    """Get revenue grouped by month for charts"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    monthly_revenue = db.session.query(
        db.func.strftime('%Y-%m', Payment.transaction_date).label('month'),
        db.func.sum(Payment.amount).label('total')
    ).filter(Payment.status == 'Success').group_by('month').order_by('month').limit(12).all()
    
    return jsonify({
        'labels': [item.month for item in monthly_revenue],
        'data': [float(item.total) for item in monthly_revenue]
    })

@app.route('/api/analytics/top-technicians')
@login_required
def top_technicians():
    """Get top-rated technicians"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    technicians = TechnicianProfile.query.all()
    technician_ratings = []
    
    for technician in technicians:
        avg_rating = calculate_technician_rating(technician.id)
        review_count = TechnicianReview.query.filter_by(technician_id=technician.id).count()
        technician_ratings.append({
            'name': technician.name,
            'specialization': technician.specialization,
            'rating': avg_rating,
            'reviews': review_count
        })
    
    # Sort by rating
    technician_ratings.sort(key=lambda x: x['rating'], reverse=True)
    
    return jsonify(technician_ratings[:10])

# ===== SPARE PARTS ORDERING SYSTEM (Complete with Advance Payment) =====

@app.route('/spare-parts')
def spare_parts_browse():
    """Spare Parts Catalog"""
    return render_template('hms/spare_parts_new.html')

@app.route('/spare-parts/<int:part_id>')
def spare_part_detail(part_id):
    """Spare Part Detail - Coming Soon"""
    return render_template('hms/spare_part_detail.html')

@app.route('/cart')
def view_cart():
    """Cart - Coming Soon"""
    return render_template('hms/cart.html')

@app.route('/cart/add/<int:part_id>', methods=['POST'])
def add_to_cart(part_id):
    """Add item to cart"""
    part = SparePart.query.get_or_404(part_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > part.stock_quantity:
        flash('Not enough stock available', 'danger')
        return redirect(request.referrer or url_for('spare_parts_browse'))
    
    session_id = session.get('cart_session_id')
    if not session_id:
        session_id = secrets.token_urlsafe(16)
        session['cart_session_id'] = session_id
    
    # Check if item already in cart
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, part_id=part_id).first()
    else:
        cart_item = CartItem.query.filter_by(session_id=session_id, part_id=part_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            session_id=session_id,
            user_id=current_user.id if current_user.is_authenticated else None,
            part_id=part_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{part.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('spare_parts_browse'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Check stock based on whether it's a part or accessory
    if cart_item.part:
        max_stock = cart_item.part.stock_quantity
    elif cart_item.accessory:
        max_stock = cart_item.accessory.stock
    else:
        max_stock = 0
    
    if quantity > max_stock:
        flash('Not enough stock available', 'danger')
    elif quantity < 1:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart', 'info')
    else:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated', 'success')
    
    return redirect(url_for('view_cart'))

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_parts():
    """Checkout and place order"""
    session_id = session.get('cart_session_id')
    
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        if not session_id:
            flash('Your cart is empty', 'warning')
            return redirect(url_for('spare_parts_browse'))
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('spare_parts_browse'))
    
    if request.method == 'POST':
        # Create orders for each item
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        delivery_address = request.form.get('delivery_address')
        car_brand = request.form.get('car_brand')
        car_model = request.form.get('car_model')
        installation = request.form.get('installation') == 'on'
        
        total_amount = 0
        orders_created = []
        
        for item in cart_items:
            part = item.part
            accessory = item.accessory
            
            # Determine product details
            if part:
                product_name = part.name
                product_stock = part.stock_quantity
                product_price = part.price
            elif accessory:
                product_name = accessory.name
                product_stock = accessory.stock
                product_price = accessory.price
            else:
                continue
            
            # Check stock
            if item.quantity > product_stock:
                flash(f'Not enough stock for {product_name}', 'danger')
                return redirect(url_for('view_cart'))
            
            # Calculate pricing
            subtotal = product_price * item.quantity
            installation_charges = 500 if installation else 0
            total = subtotal + installation_charges
            advance = total * 0.5
            remaining = total - advance
            
            # Generate order number
            last_order = PartOrder.query.order_by(PartOrder.id.desc()).first()
            order_num = f"GM-PART-{str((last_order.id + 1) if last_order else 1).zfill(5)}"
            
            order = PartOrder(
                order_number=order_num,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                part_id=part.id if part else None,
                quantity=item.quantity,
                unit_price=product_price,
                subtotal=subtotal,
                installation_charges=installation_charges,
                total_price=total,
                advance_amount=advance,
                remaining_amount=remaining,
                car_brand=car_brand,
                car_model=car_model,
                installation_required=installation,
                delivery_address=delivery_address
            )
            
            # Update stock
            if part:
                part.stock_quantity -= item.quantity
            elif accessory:
                accessory.stock -= item.quantity
            
            db.session.add(order)
            orders_created.append(order.id)
            total_amount += advance
        
        # Clear cart
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        
        # Store order IDs in session for payment
        session['pending_part_orders'] = orders_created
        session['total_advance'] = total_amount
        
        return redirect(url_for('part_orders_payment'))
    
    subtotal = sum(
        (item.part.price if item.part else (item.accessory.price if item.accessory else 0)) * item.quantity
        for item in cart_items
    )
    
    return render_template('hms/checkout_parts.html', cart_items=cart_items, subtotal=subtotal)

@app.route('/orders/payment')
def part_orders_payment():
    """Payment page for part orders"""
    order_ids = session.get('pending_part_orders', [])
    total_advance = session.get('total_advance', 0)
    
    if not order_ids:
        flash('No pending orders', 'warning')
        return redirect(url_for('spare_parts_browse'))
    
    orders = PartOrder.query.filter(PartOrder.id.in_(order_ids)).all()
    
    return render_template('hms/part_payment.html', 
                         orders=orders, 
                         total_advance=total_advance)

@app.route('/orders/confirm-payment', methods=['POST'])
def confirm_part_payment():
    """Confirm payment and complete order"""
    order_ids = session.get('pending_part_orders', [])
    payment_method = request.form.get('payment_method', 'Cash on Delivery')
    
    if not order_ids:
        return jsonify({'success': False, 'error': 'No pending orders'}), 400
    
    orders = PartOrder.query.filter(PartOrder.id.in_(order_ids)).all()
    
    for order in orders:
        order.payment_status = 'Advance Paid'
        order.order_status = 'Confirmed'
        order.confirmed_date = datetime.now()
        
        # Create notification
        if current_user.is_authenticated:
            create_notification(
                current_user.id,
                'Order Confirmed',
                f'Your order {order.order_number} has been confirmed. Advance payment received.',
                'payment'
            )
        
        # Send email
        if order.customer_email:
            try:
                send_order_confirmation_email(order)
            except:
                pass
    
    db.session.commit()
    
    # Clear session
    session.pop('pending_part_orders', None)
    session.pop('total_advance', None)
    
    flash(f'{len(orders)} order(s) confirmed successfully! Check your email for details.', 'success')
    return redirect(url_for('my_part_orders'))

@app.route('/my-orders')
def my_part_orders():
    """View customer's part orders"""
    phone = request.args.get('phone', '')
    
    if current_user.is_authenticated and hasattr(current_user, 'customer_profile'):
        customer = current_user.customer_profile
        if isinstance(customer, list):
            customer = customer[0] if customer else None
        if customer and customer.contact:
            phone = customer.contact
    
    if request.method == 'GET' and not phone:
        return render_template('hms/my_orders_search.html')
    
    if phone:
        orders = PartOrder.query.filter_by(customer_phone=phone).order_by(PartOrder.order_date.desc()).all()
        return render_template('hms/my_orders.html', orders=orders, phone=phone)
    
    return render_template('hms/my_orders_search.html')

@app.route('/order/<int:order_id>')
def view_part_order(order_id):
    """View specific order details"""
    order = PartOrder.query.get_or_404(order_id)
    return render_template('hms/order_detail.html', order=order)

@app.route('/admin/part-orders')
@login_required
def admin_part_orders():
    """Admin view of all part orders"""
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    
    status_filter = request.args.get('status', 'all')
    
    query = PartOrder.query
    if status_filter != 'all':
        query = query.filter_by(order_status=status_filter)
    
    orders = query.order_by(PartOrder.order_date.desc()).all()
    
    # Statistics
    stats = {
        'total': PartOrder.query.count(),
        'pending': PartOrder.query.filter_by(order_status='Pending').count(),
        'confirmed': PartOrder.query.filter_by(order_status='Confirmed').count(),
        'processing': PartOrder.query.filter_by(order_status='Processing').count(),
        'shipped': PartOrder.query.filter_by(order_status='Shipped').count(),
        'delivered': PartOrder.query.filter_by(order_status='Delivered').count(),
        'total_revenue': db.session.query(db.func.sum(PartOrder.advance_amount)).filter(
            PartOrder.payment_status.in_(['Advance Paid', 'Fully Paid'])
        ).scalar() or 0
    }
    
    return render_template('hms/admin_part_orders.html', orders=orders, stats=stats, status_filter=status_filter)

@app.route('/admin/part-order/<int:order_id>/update', methods=['POST'])
@login_required
def update_part_order_status(order_id):
    """Update order status"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = PartOrder.query.get_or_404(order_id)
    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes')
    
    order.order_status = new_status
    if admin_notes:
        order.admin_notes = admin_notes
    
    if new_status == 'Delivered':
        order.delivery_date = datetime.now()
    
    db.session.commit()
    
    flash(f'Order {order.order_number} updated to {new_status}', 'success')
    return redirect(url_for('admin_part_orders'))

@app.route('/order/<int:order_id>/cancel', methods=['GET', 'POST'])
def cancel_part_order(order_id):
    """Cancel a part order"""
    order = PartOrder.query.get_or_404(order_id)
    
    if order.order_status in ['Delivered', 'Cancelled']:
        flash('This order cannot be cancelled', 'danger')
        return redirect(url_for('view_part_order', order_id=order_id))
    
    order.order_status = 'Cancelled'
    db.session.commit()
    
    flash(f'Order {order.order_number} has been cancelled', 'info')
    return redirect(url_for('my_part_orders'))

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    subject = f"Order Confirmed - {order.order_number}"
    body = f"""
    <h2>Order Confirmation</h2>
    <p>Dear {order.customer_name},</p>
    <p>Your spare part order has been confirmed!</p>
    
    <h3>Order Details:</h3>
    <ul>
        <li><strong>Order Number:</strong> {order.order_number}</li>
        <li><strong>Part:</strong> {order.part.name}</li>
        <li><strong>Quantity:</strong> {order.quantity}</li>
        <li><strong>Unit Price:</strong> ₹{order.unit_price}</li>
        <li><strong>Subtotal:</strong> ₹{order.subtotal}</li>
        <li><strong>Installation:</strong> {'Yes (₹' + str(order.installation_charges) + ')' if order.installation_required else 'No'}</li>
        <li><strong>Total Amount:</strong> ₹{order.total_price}</li>
        <li><strong>Advance Paid (50%):</strong> ₹{order.advance_amount}</li>
        <li><strong>Remaining (on delivery):</strong> ₹{order.remaining_amount}</li>
    </ul>
    
    <p><strong>Delivery Address:</strong><br>{order.delivery_address}</p>
    
    <p>We will process your order and contact you at {order.customer_phone} for delivery arrangements.</p>
    
    <p>Thank you for choosing GM Motors!</p>
    <p>Best regards,<br>GM Motors Team</p>
    """
    send_email(order.customer_email, subject, body)

# Car Accessories Routes
@app.route('/accessories')
def car_accessories():
    """Car Accessories - Coming Soon"""
    return render_template('hms/accessories.html')

@app.route('/accessories/<int:accessory_id>')
def accessory_detail(accessory_id):
    """Accessory Detail - Coming Soon"""
    return render_template('hms/accessories.html')

@app.route('/add-accessory-to-cart/<int:accessory_id>', methods=['POST'])
def add_accessory_to_cart(accessory_id):
    """Add accessory to cart"""
    accessory = CarAccessory.query.get_or_404(accessory_id)
    quantity = int(request.form.get('quantity', 1))
    
    if accessory.stock < quantity:
        flash('Insufficient stock available', 'danger')
        return redirect(url_for('accessory_detail', accessory_id=accessory_id))
    
    if current_user.is_authenticated:
        # Check if already in cart
        cart_item = CartItem.query.filter_by(user_id=current_user.id, accessory_id=accessory_id).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                accessory_id=accessory_id,
                quantity=quantity,
                session_id=session.get('session_id', secrets.token_hex(16))
            )
            db.session.add(cart_item)
        
        db.session.commit()
        flash(f'{accessory.name} added to cart!', 'success')
    else:
        flash('Please login to add items to cart', 'warning')
        return redirect(url_for('login'))
    
    return redirect(url_for('car_accessories'))

# Run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Auto-initialize with admin user if DB is empty
        if not User.query.first():
            from werkzeug.security import generate_password_hash
            admin = User(username='admin', email='admin@gauravmotors.com',
                        password_hash=generate_password_hash('Admin@123456'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Database initialized with admin user (admin / Admin@123456)")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
