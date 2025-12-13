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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hmsdevsecret-change-in-production')
DB_PATH = os.path.join(os.path.dirname(__file__), 'hms.db')
DB_URI = f"sqlite:///{DB_PATH.replace('\\', '/')}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@gmmotors.com')

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'doctor', 'patient'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(300))
    doctors = db.relationship('DoctorProfile', backref='department', lazy=True)

class DoctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    availability = db.Column(db.String(300))  # simple text or JSON string of available days/times
    user = db.relationship('User', backref='doctor_profile', uselist=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    avail_slots = db.relationship('Availability', backref='doctor', lazy=True, cascade='all, delete-orphan')

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(40))
    user = db.relationship('User', backref='patient_profile', uselist=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Booked')  # Booked/Completed/Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)


class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)


class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.String(500))
    prescription = db.Column(db.String(500))
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

# Medical Records System
class MedicalRecord(db.Model):
    __tablename__ = 'medical_record'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)  # Lab Report, X-Ray, Prescription, etc.
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))  # Path to uploaded file
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship('PatientProfile', backref='medical_records')

# Patient Medical History
class MedicalHistory(db.Model):
    __tablename__ = 'medical_history'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'), nullable=False)
    allergies = db.Column(db.Text)  # Known allergies
    chronic_conditions = db.Column(db.Text)  # Diabetes, Hypertension, etc.
    current_medications = db.Column(db.Text)  # Current medications
    past_surgeries = db.Column(db.Text)  # Previous surgeries
    blood_type = db.Column(db.String(10))  # A+, B-, O+, etc.
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    insurance_provider = db.Column(db.String(200))
    insurance_number = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = db.relationship('PatientProfile', backref='medical_history', uselist=False)

# Doctor Reviews and Ratings
class DoctorReview(db.Model):
    __tablename__ = 'doctor_review'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=True)  # Verified patient
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    doctor_profile = db.relationship('DoctorProfile', backref='reviews')
    patient = db.relationship('PatientProfile', backref='reviews')

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
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
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
    notification_type = db.Column(db.String(50))  # appointment, payment, reminder, system
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

# Helpers
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

def is_doctor():
    return current_user.is_authenticated and current_user.role == 'doctor'

def is_patient():
    return current_user.is_authenticated and current_user.role == 'patient'

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

def send_appointment_confirmation(appointment):
    """Send appointment confirmation email"""
    patient_email = appointment.patient.user.email
    subject = f"Appointment Confirmed - {appointment.date}"
    body = f"""
    <h2>Appointment Confirmation</h2>
    <p>Dear {appointment.patient.name},</p>
    <p>Your appointment has been confirmed with the following details:</p>
    <ul>
        <li><strong>Doctor:</strong> {appointment.doctor.name}</li>
        <li><strong>Specialization:</strong> {appointment.doctor.specialization}</li>
        <li><strong>Date:</strong> {appointment.date.strftime('%B %d, %Y')}</li>
        <li><strong>Time:</strong> {appointment.time.strftime('%I:%M %p')}</li>
    </ul>
    <p>Please arrive 10 minutes before your scheduled time.</p>
    <p>Best regards,<br>GM Motors Healthcare Team</p>
    """
    send_email(patient_email, subject, body)

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

def calculate_doctor_rating(doctor_id):
    """Calculate average rating for a doctor"""
    reviews = DoctorReview.query.filter_by(doctor_id=doctor_id).all()
    if not reviews:
        return 0
    total = sum(review.rating for review in reviews)
    return round(total / len(reviews), 1)

def get_dashboard_stats():
    """Get comprehensive statistics for admin dashboard"""
    today = datetime.now().date()
    this_month = datetime.now().replace(day=1).date()
    
    stats = {
        'total_patients': PatientProfile.query.count(),
        'total_doctors': DoctorProfile.query.count(),
        'total_appointments': Appointment.query.count(),
        'todays_appointments': Appointment.query.filter_by(date=today).count(),
        'pending_appointments': Appointment.query.filter_by(status='Booked').count(),
        'completed_appointments': Appointment.query.filter_by(status='Completed').count(),
        'monthly_appointments': Appointment.query.filter(Appointment.date >= this_month).count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).filter_by(status='Success').scalar() or 0,
        'monthly_revenue': db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.status == 'Success',
            Payment.transaction_date >= datetime.now().replace(day=1)
        ).scalar() or 0,
        'service_bookings': ServiceBooking.query.count(),
        'pending_service_bookings': ServiceBooking.query.filter_by(status='Pending').count(),
        'spare_parts_orders': PartOrder.query.count(),
        'average_rating': db.session.query(db.func.avg(DoctorReview.rating)).scalar() or 0
    }
    return stats

# Routes
@app.route('/')
def index():
    return render_template('hms/index.html')

@app.route('/about')
def about():
    return render_template('hms/about.html')

@app.route('/services')
def services():
    """Premium services page with modern design"""
    return render_template('hms/services_new.html')

@app.route('/book-car-service')
def book_car_service():
    """Enhanced car service booking page"""
    from datetime import date
    return render_template('hms/book_service.html', today=date.today().isoformat())

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
                
                <p>We will contact you at {customer_phone} to confirm the appointment.</p>
                
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
        return redirect(url_for('book_car_service'))

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
    return render_template('hms/contact.html')

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
        user = User(username=username, email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        patient = PatientProfile(user_id=user.id, name=name or username, contact=contact)
        db.session.add(patient)
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
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
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
    num_doctors = DoctorProfile.query.count()
    num_patients = PatientProfile.query.count()
    num_appointments = Appointment.query.count()
    doctors = DoctorProfile.query.all()
    return render_template('hms/admin_dashboard.html', doctors=doctors, num_doctors=num_doctors, num_patients=num_patients, num_appointments=num_appointments)


@app.route('/admin/patients')
@login_required
def admin_patients():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    q = request.args.get('q')
    if q:
        patients = PatientProfile.query.filter(PatientProfile.name.contains(q)).all()
    else:
        patients = PatientProfile.query.all()
    return render_template('hms/admin_patients.html', patients=patients)


@app.route('/admin/appointments')
@login_required
def admin_appointments():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('hms/admin_appointments.html', appointments=appointments)


@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    # Use the enhanced analytics dashboard with real-time data
    return render_template('hms/admin_analytics_enhanced.html')


@app.route('/admin/add_patient', methods=['GET','POST'])
@login_required
def admin_add_patient():
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
            return redirect(url_for('admin_add_patient'))
        user = User(username=username, email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        p = PatientProfile(user_id=user.id, name=name, contact=contact)
        db.session.add(p)
        db.session.commit()
        flash('Patient added', 'success')
        return redirect(url_for('admin_patients'))
    return render_template('hms/admin_add_patient.html')


@app.route('/admin/edit_patient/<int:patient_id>', methods=['GET','POST'])
@login_required
def admin_edit_patient(patient_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    patient = PatientProfile.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.contact = request.form.get('contact')
        db.session.commit()
        flash('Patient updated', 'success')
        return redirect(url_for('admin_patients'))
    return render_template('hms/admin_edit_patient.html', patient=patient)


@app.route('/admin/delete_patient/<int:patient_id>', methods=['POST'])
@login_required
def admin_delete_patient(patient_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    patient = PatientProfile.query.get_or_404(patient_id)
    # check if patient has appointments
    if Appointment.query.filter_by(patient_id=patient.id).first():
        flash('Cannot delete patient with existing appointments', 'danger')
        return redirect(url_for('admin_patients'))
    db.session.delete(patient.user)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted', 'success')
    return redirect(url_for('admin_patients'))

@app.route('/admin/add_doctor', methods=['GET','POST'])
@login_required
def add_doctor():
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
            return redirect(url_for('add_doctor'))
        user = User(username=username, email=email, role='doctor')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        doc = DoctorProfile(user_id=user.id, name=name, specialization=specialization)
        db.session.add(doc)
        db.session.commit()
        flash('Doctor added', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('hms/add_doctor.html')


@app.route('/admin/edit_doctor/<int:doctor_id>', methods=['GET','POST'])
@login_required
def admin_edit_doctor(doctor_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    doc = DoctorProfile.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doc.name = request.form['name']
        doc.specialization = request.form['specialization']
        db.session.commit()
        flash('Doctor updated', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('hms/admin_edit_doctor.html', doc=doc)


@app.route('/admin/delete_doctor/<int:doctor_id>', methods=['POST'])
@login_required
def admin_delete_doctor(doctor_id):
    if not is_admin():
        flash('Admin access required', 'danger')
        return redirect(url_for('index'))
    doc = DoctorProfile.query.get_or_404(doctor_id)
    # check if doctor has appointments
    if Appointment.query.filter_by(doctor_id=doc.id).first():
        flash('Cannot delete doctor with existing appointments', 'danger')
        return redirect(url_for('admin_dashboard'))
    db.session.delete(doc.user)
    db.session.delete(doc)
    db.session.commit()
    flash('Doctor deleted', 'success')
    return redirect(url_for('admin_dashboard'))

# Patient
@app.route('/patient')
@login_required
def patient_dashboard():
    if not is_patient():
        flash('Patient access required', 'danger')
        return redirect(url_for('index'))
    
    # Get patient profile - handle both single object and list
    patient = current_user.patient_profile
    if isinstance(patient, list):
        patient = patient[0] if patient else None
    
    if not patient:
        flash('Patient profile not found', 'danger')
        return redirect(url_for('index'))
    
    upcoming = Appointment.query.filter_by(patient_id=patient.id).filter(Appointment.status=='Booked').order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    return render_template('hms/patient_dashboard.html', patient=patient, upcoming=upcoming)


@app.route('/patient/edit', methods=['GET','POST'])
@login_required
def patient_edit():
    if not is_patient():
        flash('Patient access required', 'danger')
        return redirect(url_for('index'))
    
    # Get patient profile - handle both single object and list
    patient = current_user.patient_profile
    if isinstance(patient, list):
        patient = patient[0] if patient else None
    
    if not patient:
        flash('Patient profile not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.contact = request.form.get('contact')
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('patient_dashboard'))
    return render_template('hms/patient_edit.html', patient=patient)

@app.route('/spare-parts')
def list_doctors():
    q = request.args.get('q')
    category_filter = request.args.get('category')
    
    # Get all categories with part counts
    categories = SparePartCategory.query.all()
    
    # Get parts based on filters
    parts_query = SparePart.query
    
    if category_filter and category_filter != 'all':
        parts_query = parts_query.filter_by(category_id=int(category_filter))
    
    if q:
        parts_query = parts_query.filter(
            (SparePart.name.contains(q)) | 
            (SparePart.brand.contains(q)) | 
            (SparePart.compatible_brands.contains(q)) |
            (SparePart.description.contains(q))
        )
    
    parts = parts_query.all()
    
    # Legacy support - keep doctor data for backwards compatibility
    doctors = DoctorProfile.query.all()
    today = datetime.now().date()
    days = [today + timedelta(days=i) for i in range(7)]
    doc_avail = {}
    for d in doctors:
        slots = Availability.query.filter_by(doctor_id=d.id, is_available=True).filter(Availability.date >= today).all()
        doc_avail[d.id] = slots
    
    return render_template('hms/list_doctors.html', 
                         categories=categories, 
                         parts=parts,
                         doctors=doctors, 
                         days=days, 
                         doc_avail=doc_avail,
                         selected_category=category_filter)

@app.route('/book/<int:doctor_id>', methods=['GET','POST'])
@login_required
def book(doctor_id):
    if not is_patient():
        flash('Only patients can book', 'danger')
        return redirect(url_for('index'))
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    # Show available slots for selected doctor
    today = datetime.now().date()
    if request.method == 'POST':
        slot_id = int(request.form.get('slot_id'))
        slot = Availability.query.get_or_404(slot_id)
        if not slot.is_available:
            flash('Slot no longer available', 'danger')
            return redirect(url_for('book', doctor_id=doctor_id))
        # double-check no appointment exists
        existing = Appointment.query.filter_by(doctor_id=doctor.id, date=slot.date, time=slot.time, status='Booked').first()
        if existing:
            slot.is_available = True
            db.session.commit()
            flash('Selected slot not available', 'danger')
            return redirect(url_for('book', doctor_id=doctor_id))
        
        # Get patient profile - handle both single object and list
        patient_profile = current_user.patient_profile
        if isinstance(patient_profile, list):
            patient_profile = patient_profile[0] if patient_profile else None
        
        if not patient_profile:
            flash('Patient profile not found', 'danger')
            return redirect(url_for('index'))
        
        appointment = Appointment(patient_id=patient_profile.id, doctor_id=doctor.id, date=slot.date, time=slot.time)
        slot.is_available = False
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked', 'success')
        return redirect(url_for('patient_dashboard'))

    days = [today + timedelta(days=i) for i in range(7)]
    # pull availability slots for next 7 days
    slots = Availability.query.filter_by(doctor_id=doctor.id, is_available=True).filter(Availability.date >= today).order_by(Availability.date, Availability.time).all()
    return render_template('hms/book.html', doctor=doctor, days=days, slots=slots)

@app.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if current_user.role == 'patient' and appt.patient.user_id != current_user.id:
        flash('Not authorized', 'danger')
        return redirect(url_for('index'))
    appt.status = 'Cancelled'
    # free the availability slot if it exists
    slot = Availability.query.filter_by(doctor_id=appt.doctor_id, date=appt.date, time=appt.time).first()
    if slot:
        slot.is_available = True
    db.session.commit()
    flash('Appointment cancelled', 'info')
    return redirect(request.referrer or url_for('index'))


@app.route('/reschedule/<int:appointment_id>', methods=['GET','POST'])
@login_required
def reschedule(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if current_user.role == 'patient' and appt.patient.user_id != current_user.id:
        flash('Not authorized', 'danger')
        return redirect(url_for('index'))
    if appt.status != 'Booked':
        flash('Can only reschedule booked appointments', 'danger')
        return redirect(url_for('patient_dashboard'))
    
    if request.method == 'POST':
        slot_id = request.form.get('slot_id')
        if not slot_id:
            flash('Please select a time slot', 'danger')
            return redirect(url_for('reschedule', appointment_id=appointment_id))
        
        slot_id = int(slot_id)
        new_slot = Availability.query.get_or_404(slot_id)
        if not new_slot.is_available or new_slot.doctor_id != appt.doctor_id:
            flash('Slot not available', 'danger')
            return redirect(url_for('reschedule', appointment_id=appointment_id))
        
        # free old slot
        old_slot = Availability.query.filter_by(doctor_id=appt.doctor_id, date=appt.date, time=appt.time).first()
        if old_slot:
            old_slot.is_available = True
        
        # take new slot
        appt.date = new_slot.date
        appt.time = new_slot.time
        new_slot.is_available = False
        db.session.commit()
        flash('Appointment rescheduled', 'success')
        return redirect(url_for('patient_dashboard'))
    
    # show available slots for same doctor
    today = datetime.now().date()
    slots = Availability.query.filter_by(doctor_id=appt.doctor_id, is_available=True).filter(Availability.date >= today).order_by(Availability.date, Availability.time).all()
    return render_template('hms/reschedule.html', appt=appt, slots=slots)

# Doctor
@app.route('/doctor')
@login_required
def doctor_dashboard():
    if not is_doctor():
        flash('Doctor access required', 'danger')
        return redirect(url_for('index'))
    
    # Get doctor profile - handle both single object and list
    doc = current_user.doctor_profile
    if isinstance(doc, list):
        doc = doc[0] if doc else None
    
    if not doc:
        flash('Doctor profile not found', 'danger')
        return redirect(url_for('index'))
    
    today = datetime.now().date()
    upcoming = Appointment.query.filter_by(doctor_id=doc.id).filter(Appointment.status=='Booked').order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    return render_template('hms/doctor_dashboard.html', doc=doc, upcoming=upcoming)

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
        
        # Calculate total
        total_price = part.price * quantity
        
        # Create order
        order = PartOrder(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            part_id=part.id,
            quantity=quantity,
            total_price=total_price,
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
        
        flash(f'Order placed successfully! Order ID: #{order.id}. We will contact you at {customer_phone}', 'success')
        return redirect(url_for('list_doctors'))
    
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


@app.route('/doctor/availability', methods=['GET','POST'])
@login_required
def doctor_availability():
    if not is_doctor():
        flash('Doctor access required', 'danger')
        return redirect(url_for('index'))
    
    # Get doctor profile - handle both single object and list
    doc = current_user.doctor_profile
    if isinstance(doc, list):
        doc = doc[0] if doc else None
    
    if not doc:
        flash('Doctor profile not found', 'danger')
        return redirect(url_for('index'))
    
    today = datetime.now().date()
    days = [today + timedelta(days=i) for i in range(7)]
    if request.method == 'POST':
        pass  # TODO: Handle POST request
    
    return render_template('hms/doctor_availability.html', doctor=doc, days=days)


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
        response = "You can reach us at:\n📞 Phone: +91 9997612579\n📱 WhatsApp: +91 9997612579\n📍 Location: Lohaghat, Champawat, Uttarakhand\n⏰ Hours: Mon-Sat, 9 AM - 7 PM\n\nVisit our contact page for more details and map!"

    elif any(word in message for word in ['about', 'company', 'who', 'gaurav']):
        response = "🏆 Gaurav Motors - Uttarakhand's #1 Auto Workshop!\n\n✓ Established 2010\n✓ ISO Certified\n✓ 5000+ Happy Customers\n✓ Expert Technicians\n✓ Genuine Parts\n✓ Lifetime Warranty\n\nWe provide complete automotive solutions - from services to spare parts to accessories!"

    # Appointment queries
    elif any(word in message for word in ['appointment', 'schedule', 'time', 'slot', 'booking', 'reserve']):
        response = "📅 Book Your Appointment:\n\n1. Click 'Book Service Now' button\n2. Choose your service\n3. Fill in your vehicle details\n4. Select preferred date/time\n5. Pay 50% advance\n\n✅ Quick & Easy!\n📞 Or call: +91 9997612579"

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

@app.route('/appointment/<int:appointment_id>', methods=['GET','POST'])
@login_required
def appointment_detail(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if current_user.role == 'doctor' and appt.doctor.user_id != current_user.id:
        flash('Not authorized', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # doctor marks completed and records treatment
        status = request.form.get('status')
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        notes = request.form.get('notes')
        if status == 'Completed':
            appt.status = 'Completed'
            tr = Treatment(appointment_id=appt.id, diagnosis=diagnosis, prescription=prescription, notes=notes)
            db.session.add(tr)
            db.session.commit()
            flash('Appointment completed and treatment saved', 'success')
            return redirect(url_for('doctor_dashboard'))
        elif status == 'Cancelled':
            appt.status = 'Cancelled'
            db.session.commit()
            flash('Appointment cancelled', 'info')
            return redirect(url_for('doctor_dashboard'))
    return render_template('hms/appointment_detail.html', appt=appt)

# ===== NEW ADVANCED FEATURES =====

# Medical Records Routes
@app.route('/patient/medical-records')
@login_required
def patient_medical_records():
    """View patient's medical records"""
    if not is_patient():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    patient = current_user.patient_profile[0]
    records = MedicalRecord.query.filter_by(patient_id=patient.id).order_by(MedicalRecord.upload_date.desc()).all()
    history = MedicalHistory.query.filter_by(patient_id=patient.id).first()
    
    return render_template('hms/medical_records.html', records=records, history=history)

@app.route('/patient/medical-history', methods=['GET', 'POST'])
@login_required
def update_medical_history():
    """Update patient medical history"""
    if not is_patient():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    patient = current_user.patient_profile[0]
    history = MedicalHistory.query.filter_by(patient_id=patient.id).first()
    
    if request.method == 'POST':
        if not history:
            history = MedicalHistory(patient_id=patient.id)
        
        history.blood_type = request.form.get('blood_type')
        history.allergies = request.form.get('allergies')
        history.chronic_conditions = request.form.get('chronic_conditions')
        history.current_medications = request.form.get('current_medications')
        history.past_surgeries = request.form.get('past_surgeries')
        history.emergency_contact = request.form.get('emergency_contact')
        history.emergency_phone = request.form.get('emergency_phone')
        history.insurance_provider = request.form.get('insurance_provider')
        history.insurance_number = request.form.get('insurance_number')
        
        db.session.add(history)
        db.session.commit()
        flash('Medical history updated successfully', 'success')
        return redirect(url_for('patient_medical_records'))
    
    return render_template('hms/medical_history_form.html', history=history)

@app.route('/upload-medical-record', methods=['POST'])
@login_required
def upload_medical_record():
    """Upload medical record file"""
    if 'file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(request.referrer or url_for('patient_medical_records'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer or url_for('patient_medical_records'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        patient = current_user.patient_profile[0]
        record = MedicalRecord(
            patient_id=patient.id,
            record_type=request.form.get('record_type', 'Other'),
            title=request.form.get('title', filename),
            description=request.form.get('description'),
            file_path=filename,
            uploaded_by=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        
        flash('Medical record uploaded successfully', 'success')
    else:
        flash('Invalid file type', 'danger')
    
    return redirect(url_for('patient_medical_records'))

# Doctor Reviews Routes
@app.route('/doctor/<int:doctor_id>/reviews')
def doctor_reviews(doctor_id):
    """View doctor reviews"""
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    reviews = DoctorReview.query.filter_by(doctor_id=doctor_id).order_by(DoctorReview.created_at.desc()).all()
    avg_rating = calculate_doctor_rating(doctor_id)
    
    return render_template('hms/doctor_reviews.html', doctor=doctor, reviews=reviews, avg_rating=avg_rating)

@app.route('/appointment/<int:appointment_id>/review', methods=['GET', 'POST'])
@login_required
def submit_review(appointment_id):
    """Submit review for completed appointment"""
    if not is_patient():
        flash('Only patients can submit reviews', 'danger')
        return redirect(url_for('index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.status != 'Completed':
        flash('Can only review completed appointments', 'warning')
        return redirect(url_for('patient_dashboard'))
    
    # Check if already reviewed
    existing_review = DoctorReview.query.filter_by(appointment_id=appointment_id).first()
    if existing_review:
        flash('You have already reviewed this appointment', 'info')
        return redirect(url_for('patient_dashboard'))
    
    if request.method == 'POST':
        rating = int(request.form.get('rating', 0))
        comment = request.form.get('comment')
        
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5', 'danger')
            return redirect(request.referrer)
        
        patient = current_user.patient_profile[0]
        review = DoctorReview(
            doctor_id=appointment.doctor_id,
            patient_id=patient.id,
            appointment_id=appointment_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('patient_dashboard'))
    
    return render_template('hms/submit_review.html', appointment=appointment)

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
    """Universal search across doctors, services, and parts"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    results = {
        'doctors': [],
        'services': [],
        'parts': []
    }
    
    if query:
        if category in ['all', 'doctors']:
            doctors = DoctorProfile.query.filter(
                (DoctorProfile.name.ilike(f'%{query}%')) |
                (DoctorProfile.specialization.ilike(f'%{query}%'))
            ).all()
            results['doctors'] = doctors
        
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
@app.route('/admin/export/appointments')
@login_required
def export_appointments():
    """Export appointments to CSV"""
    if not is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    
    # Create CSV in memory
    output = BytesIO()
    output.write(b'ID,Patient,Doctor,Date,Time,Status,Created At\n')
    
    for appt in appointments:
        line = f'{appt.id},{appt.patient.name},{appt.doctor.name},{appt.date},{appt.time},{appt.status},{appt.created_at}\n'
        output.write(line.encode('utf-8'))
    
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'appointments_{datetime.now().strftime("%Y%m%d")}.csv'
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
        payment_type = 'Appointment' if payment.appointment_id else 'Service' if payment.service_booking_id else 'Part Order'
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

@app.route('/api/analytics/appointments-by-month')
@login_required
def appointments_by_month():
    """Get appointments grouped by month for charts"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get last 12 months data
    monthly_data = db.session.query(
        db.func.strftime('%Y-%m', Appointment.date).label('month'),
        db.func.count(Appointment.id).label('count')
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

@app.route('/api/analytics/top-doctors')
@login_required
def top_doctors():
    """Get top-rated doctors"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    doctors = DoctorProfile.query.all()
    doctor_ratings = []
    
    for doctor in doctors:
        avg_rating = calculate_doctor_rating(doctor.id)
        review_count = DoctorReview.query.filter_by(doctor_id=doctor.id).count()
        doctor_ratings.append({
            'name': doctor.name,
            'specialization': doctor.specialization,
            'rating': avg_rating,
            'reviews': review_count
        })
    
    # Sort by rating
    doctor_ratings.sort(key=lambda x: x['rating'], reverse=True)
    
    return jsonify(doctor_ratings[:10])

# ===== SPARE PARTS ORDERING SYSTEM (Complete with Advance Payment) =====

@app.route('/spare-parts')
def spare_parts_browse():
    """Browse all spare parts with categories"""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    brand = request.args.get('brand', '')
    sort_by = request.args.get('sort', 'name')
    
    query = SparePart.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            (SparePart.name.ilike(f'%{search}%')) |
            (SparePart.description.ilike(f'%{search}%')) |
            (SparePart.brand.ilike(f'%{search}%'))
        )
    
    if brand:
        query = query.filter(SparePart.brand.ilike(f'%{brand}%'))
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(SparePart.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(SparePart.price.desc())
    elif sort_by == 'popular':
        query = query.order_by(SparePart.is_featured.desc())
    else:
        query = query.order_by(SparePart.name.asc())
    
    parts = query.all()
    categories = SparePartCategory.query.all()
    brands = db.session.query(SparePart.brand).distinct().all()
    brands = [b[0] for b in brands if b[0]]
    
    # Get cart count
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('hms/spare_parts_new.html', 
                         parts=parts, 
                         categories=categories,
                         brands=brands,
                         selected_category=category_id,
                         search_query=search,
                         cart_count=cart_count)

@app.route('/spare-parts/<int:part_id>')
def spare_part_detail(part_id):
    """Detailed view of a spare part"""
    part = SparePart.query.get_or_404(part_id)
    related_parts = SparePart.query.filter(
        SparePart.category_id == part.category_id,
        SparePart.id != part_id
    ).limit(4).all()
    
    return render_template('hms/spare_part_detail.html', part=part, related_parts=related_parts)

@app.route('/cart')
def view_cart():
    """View shopping cart"""
    session_id = session.get('cart_session_id')
    if not session_id:
        session_id = secrets.token_urlsafe(16)
        session['cart_session_id'] = session_id
    
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    total = sum(item.part.price * item.quantity for item in cart_items)
    
    return render_template('hms/cart.html', cart_items=cart_items, total=total)

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
    
    if quantity > cart_item.part.stock_quantity:
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
            
            # Check stock
            if item.quantity > part.stock_quantity:
                flash(f'Not enough stock for {part.name}', 'danger')
                return redirect(url_for('view_cart'))
            
            # Calculate pricing
            subtotal = part.price * item.quantity
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
                part_id=part.id,
                quantity=item.quantity,
                unit_price=part.price,
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
            part.stock_quantity -= item.quantity
            
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
    
    subtotal = sum(item.part.price * item.quantity for item in cart_items)
    
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
    
    if current_user.is_authenticated and hasattr(current_user, 'patient_profile'):
        patient = current_user.patient_profile
        if isinstance(patient, list):
            patient = patient[0] if patient else None
        if patient and patient.contact:
            phone = patient.contact
    
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

@app.route('/order/<int:order_id>/cancel')
def cancel_part_order(order_id):
    """Cancel a part order"""
    order = PartOrder.query.get_or_404(order_id)
    
    if order.order_status in ['Delivered', 'Cancelled']:
        flash('This order cannot be cancelled', 'danger')
        return redirect(url_for('view_part_order', order_id=order_id))
    
    order.order_status = 'Cancelled'
    db.session.commit()
    
    flash(f'Order {order.order_number} has been cancelled', 'info')
    return redirect(url_for('my_part_orders_search'))

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
    """Browse car accessories"""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    brand = request.args.get('brand', '')
    sort_by = request.args.get('sort', 'name')
    
    query = CarAccessory.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            (CarAccessory.name.ilike(f'%{search}%')) |
            (CarAccessory.description.ilike(f'%{search}%')) |
            (CarAccessory.brand.ilike(f'%{search}%'))
        )
    
    if brand:
        query = query.filter(CarAccessory.brand.ilike(f'%{brand}%'))
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(CarAccessory.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(CarAccessory.price.desc())
    elif sort_by == 'popular':
        query = query.order_by(CarAccessory.is_featured.desc(), CarAccessory.rating.desc())
    else:
        query = query.order_by(CarAccessory.name.asc())
    
    accessories = query.all()
    categories = AccessoryCategory.query.all()
    brands = db.session.query(CarAccessory.brand).distinct().all()
    brands = [b[0] for b in brands if b[0]]
    
    # Get cart count
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('hms/accessories.html', 
                         accessories=accessories, 
                         categories=categories,
                         brands=brands,
                         selected_category=category_id,
                         search_query=search,
                         cart_count=cart_count)

@app.route('/accessories/<int:accessory_id>')
def accessory_detail(accessory_id):
    """View accessory details"""
    accessory = CarAccessory.query.get_or_404(accessory_id)
    related = CarAccessory.query.filter_by(category_id=accessory.category_id).filter(CarAccessory.id != accessory.id).limit(4).all()
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('hms/accessory_detail.html', accessory=accessory, related=related, cart_count=cart_count)

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
    # Start development server
    app.run(debug=True)
