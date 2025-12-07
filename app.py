from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hmsdevsecret-change-in-production')
DB_PATH = os.path.join(os.path.dirname(__file__), 'hms.db')
DB_URI = f"sqlite:///{DB_PATH.replace('\\', '/')}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
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
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    car_brand = db.Column(db.String(50))
    car_model = db.Column(db.String(100))
    car_year = db.Column(db.Integer)
    installation_required = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='Pending')  # Pending/Confirmed/Completed/Cancelled
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(500))

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

# Routes
@app.route('/')
def index():
    return render_template('hms/index.html')

@app.route('/about')
def about():
    return render_template('hms/about.html')

@app.route('/services')
def services():
    return render_template('hms/services.html')

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
    num_doctors = DoctorProfile.query.count()
    num_patients = PatientProfile.query.count()
    num_appointments = Appointment.query.count()
    completed = Appointment.query.filter_by(status='Completed').count()
    booked = Appointment.query.filter_by(status='Booked').count()
    cancelled = Appointment.query.filter_by(status='Cancelled').count()
    return render_template('hms/admin_analytics.html', 
                         num_doctors=num_doctors, 
                         num_patients=num_patients, 
                         num_appointments=num_appointments,
                         completed=completed,
                         booked=booked,
                         cancelled=cancelled)


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
    today = datetime.utcnow().date()
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
    today = datetime.utcnow().date()
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
    today = datetime.utcnow().date()
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
    
    today = datetime.utcnow().date()
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
    
    today = datetime.utcnow().date()
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
    # Service related queries
    if any(word in message for word in ['service', 'services', 'booking', 'book', 'appointment']):
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
        response = "You can reach us at:\n📞 Phone: +91-XXXXXXXXXX\n📧 Email: info@gmmotors.com\n📍 Location: [Your Location]\n\nVisit our contact page for more details."

    elif any(word in message for word in ['about', 'company', 'who']):
        response = "GM Motors is your trusted partner for all automotive needs. We provide comprehensive car services, genuine spare parts, and expert maintenance solutions. With years of experience, we ensure your vehicle gets the best care possible."

    # Appointment queries
    elif any(word in message for word in ['appointment', 'schedule', 'time', 'slot']):
        response = "To book an appointment:\n1. Visit our services page\n2. Choose your preferred service\n3. Select a convenient date and time\n4. Fill in your details\n\nWe offer flexible timing from 9 AM to 6 PM."

    # Price/Cost queries
    elif any(word in message for word in ['price', 'cost', 'fee', 'charge']):
        response = "Our service prices vary based on the type of service and vehicle. Please check our services page for detailed pricing or contact us for a custom quote."

    # Emergency/Urgent queries
    elif any(word in message for word in ['emergency', 'urgent', 'breakdown', 'tow']):
        response = "For emergency services or breakdowns, please call our 24/7 helpline: +91-XXXXXXXXXX. We provide roadside assistance and towing services."

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

# Run
if __name__ == '__main__':
    # Start development server
    app.run(debug=True)
