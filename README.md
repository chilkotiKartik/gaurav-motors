# 🚗 GAURAV MOTORS - Complete Hospital Management System (HMS)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-All%20Passing-brightgreen.svg)]()

A comprehensive, feature-rich Hospital Management System built with Flask. Includes patient management, doctor scheduling, appointments, medical records, **spare parts ordering with 50% advance payment**, reviews, analytics, notifications, and much more!

---

## ✨ Complete Feature List

### 🏥 Core Medical Features
- ✅ **Patient Registration & Management** - Complete patient profiles with medical history
- ✅ **Doctor Management** - Doctor profiles, specializations, availability schedules
- ✅ **Appointment Booking** - Real-time appointment scheduling with conflict detection
- ✅ **Medical Records** - Digital medical record management with file uploads
- ✅ **Medical History Tracking** - Comprehensive patient health timeline
- ✅ **Prescription Management** - Digital prescriptions with PDF generation

### 🛒 Spare Parts E-Commerce (NEW!)
- ✅ **Spare Parts Catalog** - Browse 100+ automotive spare parts
- ✅ **Advanced Search & Filters** - Filter by category, brand, price, availability
- ✅ **Product Details** - Comprehensive product information with images
- ✅ **Shopping Cart** - Add multiple items, update quantities, view subtotal
- ✅ **50% Advance Payment** - Book parts with 50% advance, pay remaining on delivery
- ✅ **Checkout System** - Customer info, delivery address, vehicle details
- ✅ **Payment Options** - Cash on Delivery, Online Payment (Razorpay), Bank Transfer
- ✅ **Order Tracking** - Track order status from pending to delivered
- ✅ **Installation Service** - Optional installation with charges
- ✅ **Order Management** - Admin panel for order processing and updates

### 💳 Payment & Billing
- ✅ **Razorpay Integration** - Secure online payment gateway (test mode FREE)
- ✅ **Multiple Payment Methods** - COD, Online, Bank Transfer
- ✅ **Payment Tracking** - Track advance and remaining payments
- ✅ **Invoice Generation** - Automatic PDF invoice creation

### 📧 Communication Features
- ✅ **Email Notifications** - Order confirmations, appointment reminders
- ✅ **In-App Notifications** - Real-time alerts for appointments and orders
- ✅ **SMS Integration** - Optional SMS notifications (Twilio/MSG91/Fast2SMS)
- ✅ **Email Queue System** - Reliable email delivery with retry mechanism

### ⭐ Reviews & Ratings
- ✅ **Doctor Reviews** - Patients can rate and review doctors
- ✅ **Service Reviews** - Review hospital services
- ✅ **Star Ratings** - 5-star rating system with comments
- ✅ **Review Moderation** - Admin approval system

### 📊 Analytics & Reporting
- ✅ **Admin Dashboard** - Comprehensive analytics with charts
- ✅ **Appointment Analytics** - Daily, weekly, monthly statistics
- ✅ **Revenue Tracking** - Payment analytics and trends
- ✅ **Patient Statistics** - New registrations, active patients
- ✅ **Doctor Performance** - Appointment and review metrics
- ✅ **Data Export** - Export data to CSV/Excel

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chilkotiKartik/gaurav-motors.git
   cd gaurav-motors
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-super-secret-key-change-this
   DATABASE_URL=sqlite:///hms.db
   
   # Email (Gmail)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   
   # Razorpay (Test Mode - FREE)
   RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXXXXX
   RAZORPAY_KEY_SECRET=XXXXXXXXXXXXXXXX
   ```

4. **Initialize the database**
   ```bash
   python setup_db.py
   python setup_services.py
   python setup_spare_parts.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   
   Open your browser and go to: `http://localhost:5000`

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_features.py
```

This verifies:
- ✅ All dependencies installed
- ✅ All templates exist
- ✅ All routes functioning
- ✅ Database models correct
- ✅ Configuration valid

---

## 📋 Default Login Credentials

### Admin Account
- **Email:** `admin@gmmotors.com`
- **Password:** `admin123`
- **Access:** Full system access, analytics, user management

### Test Doctor Account
- **Email:** `doctor@gmmotors.com`
- **Password:** `doctor123`
- **Access:** Doctor dashboard, appointments, medical records

### Test Patient Account
- **Email:** `patient@gmmotors.com`
- **Password:** `patient123`
- **Access:** Book appointments, view records, order parts

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-Login 0.6.3** - Authentication
- **Flask-Mail 0.9.1** - Email service
- **Werkzeug 3.0.1** - Security utilities

### Frontend
- **Bootstrap 5** - UI framework
- **Font Awesome 6** - Icons
- **Chart.js** - Analytics charts
- **Animate.css** - Animations

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production database (Render)

### Payments
- **Razorpay** - Payment gateway integration

### Additional Libraries
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **Pandas** - Data analysis
- **OpenPyXL** - Excel export

---

## 🌟 Key Features in Detail

### Spare Parts Ordering System

#### Customer Flow
1. **Browse Catalog** - View all available spare parts with images, prices, stock status
2. **Search & Filter** - Find parts by category (Engine, Brakes, Filters, Electrical, etc.)
3. **Product Details** - See specifications, warranty, compatibility
4. **Add to Cart** - Select quantity, add multiple items
5. **Checkout** - Provide customer details, vehicle info, delivery address
6. **Payment** - Choose payment method (50% advance required)
7. **Track Order** - Monitor order status from pending to delivered
8. **Installation** - Opt for professional installation service

#### Admin Management
1. **View All Orders** - Dashboard with statistics and filters
2. **Update Status** - Change order status (Pending → Confirmed → Processing → Shipped → Delivered)
3. **Payment Tracking** - Monitor advance and remaining payments
4. **Customer Info** - Access complete customer and delivery details
5. **Analytics** - Track order trends, revenue, popular parts

### Payment System (50% Advance)

When a customer places an order:
- **Total Amount:** ₹10,000 (example)
- **Advance (50%):** ₹5,000 (paid during order)
- **Remaining:** ₹5,000 (paid on delivery)

Payment options:
1. **Cash on Delivery** - Pay advance now, remaining on delivery
2. **Online Payment** - Razorpay integration for instant payment
3. **Bank Transfer** - Direct transfer with verification

---

## 🔧 Configuration

### Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Gmail
2. Generate an App Password:
   - Go to Google Account → Security
   - 2-Step Verification → App passwords
   - Select "Mail" and generate
3. Add credentials to `.env` file

### Razorpay Setup (FREE Test Mode)

1. Sign up at https://razorpay.com (free, no credit card)
2. Get test API keys from dashboard
3. Add to `.env` file
4. Test with card: 4111 1111 1111 1111

See `FREE_API_SETUP.md` for detailed guides on all integrations!

---

## 🚀 Deployment

### Deploy to Render.com (FREE)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Web Service on Render**
   - Go to https://render.com
   - New → Web Service
   - Connect your GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables**
   - Add all variables from `.env` to Render dashboard
   - Change `DATABASE_URL` to PostgreSQL (Render provides free)

4. **Deploy!**
   - Render automatically deploys your app
   - Get your URL: `https://your-app.onrender.com`

---

## 📊 Database Schema

### Main Models
- **User** - Authentication and base user info
- **Patient** - Patient profiles and medical history
- **Doctor** - Doctor profiles, specializations, schedules
- **Appointment** - Appointment bookings and status
- **Service** - Hospital services catalog
- **SparePart** - Spare parts inventory
- **CartItem** - Shopping cart items
- **PartOrder** - Spare parts orders with payment tracking
- **MedicalRecord** - Patient medical records
- **DoctorReview** - Doctor ratings and reviews
- **Notification** - In-app notifications
- **Payment** - Payment transactions

---

## 🆘 Support

- 📧 Email: support@gmmotors.com
- 📱 Phone: +91-XXXXXXXXXX
- 🌐 Website: https://gmmotors.onrender.com

---

## 📈 Version History

### v2.0.0 (Current) - Complete Feature Release
- ✅ Spare parts ordering system with 50% advance payment
- ✅ Shopping cart and checkout flow
- ✅ Payment integration (Razorpay)
- ✅ Order tracking system
- ✅ Admin order management
- ✅ Email notifications
- ✅ Medical records management
- ✅ Reviews and ratings system
- ✅ Advanced analytics dashboard
- ✅ Universal search
- ✅ Data export functionality

### v1.0.0 - Initial Release
- ✅ Basic patient management
- ✅ Doctor scheduling
- ✅ Appointment booking
- ✅ User authentication

---

## 🔥 Quick Links

- [Free API Setup Guide](FREE_API_SETUP.md) - Set up all free integrations
- [Test Script](test_features.py) - Verify your installation
- [Setup Scripts](setup_spare_parts.py) - Initialize sample data

---

**Made with ❤️ by Gaurav Motors Team**

⭐ Star this repo if you find it helpful!
