# 🚗 GAURAV MOTORS - COMPLETE PROJECT DOCUMENTATION

---

## 📋 TABLE OF CONTENTS
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Features](#features)
5. [Database Models](#database-models)
6. [Routes & Endpoints](#routes--endpoints)
7. [Configuration](#configuration)
8. [How to Use](#how-to-use)

---

## 🎯 PROJECT OVERVIEW

**Project Name:** GAURAV MOTORS  
**Type:** Automotive Service Management System  
**Location:** Lohaghat, Champawat, Uttarakhand - India  
**Built With:** Python Flask  
**Database:** SQLite (Local) / PostgreSQL (Production)  
**Deployment:** Ready for Render.com  

**What It Does:**
- Manages car service bookings
- Tracks spare parts inventory
- Handles customer profiles
- Manages technician profiles
- Processes payments
- Sends email notifications
- Admin dashboard for management
- SEO optimized for search engines

---

## 💻 TECHNOLOGY STACK

### Backend Framework
```
Flask 3.0.0              → Web framework (Python)
Flask-SQLAlchemy 3.1.1   → Database ORM (Object-Relational Mapping)
Flask-Login 0.6.3        → User authentication & session management
Flask-Mail 0.9.1         → Email sending
Flask-WTF 1.2.1          → Form handling & CSRF protection
```

### Database
```
SQLite                   → Local development database
PostgreSQL               → Production database (Render)
SQLAlchemy               → Database query builder & ORM
```

### Frontend
```
Bootstrap 5.3.0          → Responsive UI framework
Font Awesome 6.4.0       → Icons library
Google Fonts (Inter)     → Professional typography
Custom CSS               → clean.css (413 lines)
```

### Security
```
Werkzeug                 → Password hashing & security utils
python-dotenv 1.0.0      → Environment variables management
CSRF Protection          → Built-in with Flask-WTF
```

### Utilities
```
psycopg2-binary 2.9.9    → PostgreSQL driver for Python
email-validator 2.1.0    → Email format validation
Gunicorn                 → WSGI server for production
```

---

## 📁 PROJECT STRUCTURE

```
gaurav-motors/
│
├── 📄 app.py                    → MAIN APPLICATION FILE (2,574 lines)
│                                  • All routes defined here
│                                  • Database models defined
│                                  • Flask configuration
│
├── 📄 config.py                 → Configuration settings
│                                  • Development config
│                                  • Production config
│                                  • Database settings
│
├── 📄 requirements.txt           → Python dependencies list
│                                  • All packages needed
│                                  • Version specifications
│
├── 📄 .env                       → Environment variables (SENSITIVE)
│                                  • SECRET_KEY
│                                  • Database URL
│                                  • Email credentials
│                                  • API keys
│
├── 📄 .gitignore                 → Git ignore rules
│                                  • Excludes .env, __pycache__, etc
│
├── 📄 Procfile                   → Render deployment config
│                                  • Tells Render how to start app
│                                  • gunicorn configuration
│
├── 📄 runtime.txt                → Python version for deployment
│
├── 📄 setup.py                   → Package setup configuration
│
├── 📄 validators.py              → Custom validation functions
│
├── 📄 README.md                  → Project documentation
│
├── 📁 static/                    → Static files (Not processed by server)
│   ├── css/
│   │   ├── clean.css             → MAIN CSS (413 lines) - What you see!
│   │   ├── hms.css               → Original styling
│   │   ├── modern-ui.css         → Modern UI components
│   │   ├── traditional.css       → Traditional design
│   │   ├── beautiful-ui.css      → Dark theme design
│   │   └── dark-theme-override.css
│   │
│   ├── js/
│   │   ├── dynamic-ui.js         → Dynamic interface features
│   │   └── dynamic-ui-light.js   → Light theme JS
│   │
│   └── images/                   → Logo, icons, graphics
│       └── (image files)
│
├── 📁 templates/                 → HTML Templates (Rendered by server)
│   └── hms/
│       ├── base.html             → BASE TEMPLATE (Master template)
│       │                           • Navbar, footer, meta tags
│       │                           • Extended by all other templates
│       │                           • 4,301 lines of HTML
│       │
│       ├── index_premium.html    → Homepage
│       ├── services.html         → Services page
│       ├── about.html            → About page
│       ├── contact.html          → Contact form
│       ├── faq.html              → FAQ page
│       │
│       ├── admin_dashboard.html  → Admin panel home
│       ├── admin_customers.html  → Manage customers
│       ├── admin_parts.html      → Manage spare parts
│       ├── admin_service_bookings.html  → View bookings
│       │
│       ├── customer_dashboard.html    → Customer home
│       ├── book_car_service.html      → Book a service
│       ├── my_orders.html            → Customer's bookings
│       │
│       ├── login.html            → User login page
│       ├── register.html         → User registration
│       │
│       ├── cart.html             → Shopping cart for parts
│       ├── checkout_parts.html   → Part checkout
│       │
│       └── [50+ other templates] → Different pages & features
│
├── 📁 api/                       → API endpoints
│   └── index.py                  → API routes for Vercel/external services
│
├── 📁 instance/                  → Instance-specific files
│                                  • SQLite database (when created)
│                                  • Session data
│
├── 📁 logs/                      → Application logs
│                                  • Error logs
│                                  • Activity logs
│
├── 📁 uploads/                   → User-uploaded files
│                                  • Customer documents
│                                  • Service photos
│                                  • Invoices
│
└── 📁 backups/                   → Database backups
                                   • SQL database backups
```

---

## ⭐ FEATURES IMPLEMENTED

### 🔐 Authentication & Users
- User registration (customer, technician, admin)
- Login with password hashing
- Session management
- Role-based access control
- Password reset via email
- User profile management

### 🚗 Service Management
- Browse available services
- Book car service appointments
- View booking history
- Cancel bookings
- Rate and review services
- Monthly service reminders

### 🔧 Spare Parts Module
- Browse spare parts catalog
- Add parts to cart
- Order spare parts
- Track part orders
- Part availability tracking
- Order status updates

### 💰 Payment System
- 50% advance payment system
- Online payment gateway integration
- Payment tracking
- Invoice generation
- Payment history

### 👥 Customer Features
- Customer dashboard
- Profile management
- Service booking history
- Part order tracking
- Payment history
- Communication with admin

### 📊 Admin Dashboard
- View all bookings
- Manage customers
- Manage technicians
- Manage spare parts
- Revenue reports
- Analytics & statistics
- Send notifications

### 📧 Notifications
- Email confirmations
- Booking reminders
- Payment receipts
- Order status updates
- Newsletter (optional)

### 🔍 SEO Optimization
- Meta tags (43 total)
- JSON-LD structured data
- Sitemap.xml generation
- Robots.txt configuration
- Open Graph tags
- Mobile-friendly design

---

## 🗄️ DATABASE MODELS

### User Model
```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password: String (Hashed)
- role: String (customer, technician, admin)
- phone: String
- address: String
- created_at: DateTime
- updated_at: DateTime
```

### ServiceBooking Model
```python
- id: Integer (Primary Key)
- customer_id: Foreign Key → User
- service_type: String (Full Service, Oil Change, etc)
- vehicle_model: String
- booking_date: DateTime
- status: String (pending, completed, cancelled)
- total_cost: Float
- advance_payment: Float
- notes: Text
- created_at: DateTime
```

### SparePart Model
```python
- id: Integer (Primary Key)
- name: String
- category: String
- price: Float
- stock: Integer
- description: Text
- image_url: String
- supplier_id: Foreign Key → Supplier
- created_at: DateTime
```

### PartOrder Model
```python
- id: Integer (Primary Key)
- customer_id: Foreign Key → User
- parts: ManyToMany → SparePart
- total_price: Float
- advance_payment: Float (50%)
- status: String (pending, shipped, delivered)
- payment_date: DateTime
- created_at: DateTime
```

### Payment Model
```python
- id: Integer (Primary Key)
- customer_id: Foreign Key → User
- amount: Float
- payment_method: String (online, cash, bank transfer)
- booking_id: Foreign Key → ServiceBooking
- status: String (pending, completed, failed)
- transaction_id: String
- created_at: DateTime
```

### TechnicianProfile Model
```python
- id: Integer (Primary Key)
- user_id: Foreign Key → User
- experience_years: Integer
- specialization: String (Engine, Electrical, etc)
- rating: Float
- total_jobs: Integer
- availability: String
- certifications: Text
```

(+10 more models for features, bookings, reviews, notifications, etc.)

---

## 🛣️ ROUTES & ENDPOINTS

### Public Routes (No Login Required)
```
GET  /                          → Homepage
GET  /services                  → Services page
GET  /about                     → About page
GET  /contact                   → Contact form
GET  /faq                       → FAQ
GET  /login                     → Login page
POST /login                     → Process login
GET  /register                  → Registration page
POST /register                  → Create new user
GET  /logout                    → Logout user
```

### Customer Routes (Login Required)
```
GET  /customer/dashboard        → Customer home
GET  /book-service              → Book a service
POST /api/booking/create        → Create booking
GET  /my-orders                 → View bookings
GET  /booking/<id>              → Booking details
POST /booking/<id>/cancel       → Cancel booking
POST /booking/<id>/rate         → Rate service

GET  /parts                     → Browse parts
GET  /parts/<id>                → Part details
POST /cart/add                  → Add to cart
GET  /cart                      → View cart
POST /checkout                  → Checkout parts
GET  /my-orders-parts           → Order history
```

### Admin Routes (Admin Role Only)
```
GET  /admin/dashboard           → Admin home
GET  /admin/customers           → Manage customers
GET  /admin/services            → Manage services
GET  /admin/parts               → Manage spare parts
GET  /admin/bookings            → View all bookings
GET  /admin/payments            → Payment tracking
GET  /admin/add-customer        → Add new customer
GET  /admin/edit-customer/<id>  → Edit customer
GET  /admin/analytics           → Analytics & reports
POST /admin/export-revenue      → Export revenue data
```

### API Routes
```
GET  /api/services              → List all services (JSON)
GET  /api/services/<id>         → Service details (JSON)
POST /api/booking/validate      → Validate booking dates
GET  /api/timeslots             → Available time slots
GET  /api/parts                 → List parts (JSON)
POST /api/parts/search          → Search parts
```

### System Routes
```
GET  /                          → Homepage
GET  /sitemap.xml               → SEO sitemap
GET  /robots.txt                → Robots file for search engines
GET  /static/<path>             → Static files (CSS, JS, Images)
```

---

## ⚙️ CONFIGURATION

### Environment Variables (.env)
```
FLASK_ENV=production           # production or development
FLASK_DEBUG=False              # True for development
SECRET_KEY=...                 # 32+ character random string

# Database
SQLALCHEMY_DATABASE_URI=...    # SQLite or PostgreSQL URL

# Email (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com     # Gmail SMTP server
MAIL_PORT=587                  # TLS port
MAIL_USE_TLS=True              # Use TLS encryption
MAIL_USERNAME=...              # Your Gmail
MAIL_PASSWORD=...              # App-specific password

# Session Security
SESSION_COOKIE_SECURE=True     # HTTPS only
SESSION_COOKIE_HTTPONLY=True   # No JavaScript access
SESSION_COOKIE_SAMESITE=Lax    # CSRF protection

# URL Scheme
PREFERRED_URL_SCHEME=https     # Use HTTPS
```

### app.py Configuration
```python
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file
```

---

## 🚀 HOW TO USE

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (create .env file)
# Copy .env.example or create new with required variables

# 3. Initialize database
python -c "from app import db; db.create_all()"

# 4. Run the app
python -m flask run --host=0.0.0.0 --port=5000

# 5. Open browser
# Visit: http://localhost:5000
```

### Production Deployment (Render.com)
```bash
# 1. Create account on render.com
# 2. Connect GitHub repository
# 3. Add environment variables in Render dashboard
# 4. Deploy
# 5. App will be live at: https://your-app-name.onrender.com
```

### User Roles & Access

**Customer:**
- Browse services
- Book appointments
- View order history
- Rate services
- Order spare parts

**Technician:**
- View assigned jobs
- Update job status
- Add service notes
- Track ratings

**Admin:**
- Full system access
- Manage all users
- Manage inventory
- View analytics
- Generate reports

---

## 🎨 UI/UX Design

### Color Scheme
```
Primary Blue:      #1e3a8a
Secondary Blue:    #2563eb
Success Green:     #16a34a
Danger Red:        #dc2626
Warning Orange:    #f59e0b
Light Gray:        #f8fafc
Dark Gray:         #1f2937
Border Gray:       #e5e7eb
```

### CSS Components
- **Navbar** - Navigation with branding
- **Cards** - Content containers with shadows
- **Buttons** - CTA buttons with hover effects
- **Forms** - Clean input fields with validation
- **Tables** - Sortable data display
- **Alerts** - Success/error/warning messages
- **Footer** - Multi-column footer with links

### Responsive Design
- Mobile-first approach
- Breakpoints: 320px, 768px, 1024px, 1200px
- Fully responsive on all devices
- Touch-friendly buttons (48px minimum)

---

## 📊 Statistics

- **Total Lines of Code:** 2,574 (app.py)
- **HTML Templates:** 58 files
- **CSS Stylesheets:** 9 files
- **Database Models:** 15+
- **API Endpoints:** 40+
- **Routes Implemented:** 30+
- **Meta Tags:** 43 tags
- **JSON-LD Schemas:** 3 schemas

---

## 🔒 Security Features

✅ Password Hashing (Werkzeug)  
✅ CSRF Protection (Flask-WTF)  
✅ XSS Prevention  
✅ SQL Injection Prevention (SQLAlchemy)  
✅ Secure Session Cookies  
✅ HTTPS Ready  
✅ Security Headers Implemented  
✅ Email Validation  
✅ Rate Limiting Ready  
✅ Admin Role Protection  

---

## 📈 Performance Features

✅ Database Query Optimization  
✅ Caching Strategy  
✅ Compression Enabled  
✅ CDN-ready (external resources)  
✅ Image Optimization  
✅ CSS/JS Minification Ready  
✅ Lazy Loading Support  
✅ Fast Response Times  

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm instance/hms.db
python -c "from app import db; db.create_all()"
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
# Use different port
python -m flask run --port=5001
```

---

## 📞 Contact & Support

**Business:** Gaurav Motors  
**Location:** Lohaghat, Uttarakhand, India  
**Phone:** +91 9997612579  

---

**Last Updated:** February 17, 2026  
**Status:** ✅ READY FOR PRODUCTION  
**Version:** 1.0.0  

