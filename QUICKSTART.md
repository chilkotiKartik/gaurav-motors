# 🚀 QUICK START GUIDE

## Easy 3-Minute Setup

### **Step 1: Install Dependencies** (1 minute)
```bash
pip install -r requirements.txt
```

### **Step 2: Run Setup Script** (30 seconds)
```bash
python setup.py
```
This will:
- ✅ Check Python version
- ✅ Verify all dependencies
- ✅ Create required directories
- ✅ Set up .env file
- ✅ Validate configuration

### **Step 3: Start the Application** (30 seconds)
```bash
python start.py
```

That's it! 🎉

---

## **Access Your Application**

Open your browser and visit: **http://localhost:5000**

### **Login Credentials**

**Admin Account:**
- Username: `admin`
- Password: `Admin@123456`

⚠️ **Change this password immediately after first login!**

---

## **What Can You Do?**

### **As Admin:**
1. View comprehensive analytics dashboard
2. Manage customers and technicians
3. Track all service bookings
4. Process part orders
5. View revenue reports
6. Export data to CSV

### **As Customer:**
1. Book car services online
2. Track service history
3. order spare parts (50% advance payment)
4. Review technicians
5. Manage vehicle records

### **As Technician:**
1. View assigned service bookings
2. Update service status
3. Record work performed
4. Manage availability schedule

---

## **Troubleshooting**

### **Port Already in Use?**
```bash
# Use a different port
FLASK_PORT=5001 python start.py
```

### **Database Issues?**
```bash
# Reinitialize database
rm hms.db
python init_automotive_db.py
```

### **Missing Dependencies?**
```bash
# Force reinstall
pip install -r requirements.txt --upgrade --force-reinstall
```

### **Still Not Working?**
1. Check Python version: `python --version` (need 3.8+)
2. Check logs in `logs/` directory
3. Run: `python setup.py` to see what's missing
4. Check `.env` file exists and has valid configuration

---

## **Next Steps**

1. ✅ **Change Admin Password** - Security first!
2. ✅ **Configure Email** - Edit `.env` with your SMTP settings
3. ✅ **Add Services** - Customize your service offerings
4. ✅ **Add Spare Parts** - Update your parts catalog
5. ✅ **Test Everything** - Run `pytest tests.py -v`
6. ✅ **Go Live** - See `DEPLOYMENT.md` for production setup

---

## **Important Files**

- **`app.py`** - Main application file
- **`config.py`** - Configuration management (NEW!)
- **`validators.py`** - Input validation (NEW!)
- **`error_handlers.py`** - Error handling (NEW!)
- **`tests.py`** - Test suite (NEW!)
- **`.env`** - Your secret configuration
- **`IMPROVEMENTS.md`** - All enhancements made
- **`DEPLOYMENT.md`** - Production deployment guide

---

## **Development Commands**

```bash
# Run in development mode with auto-reload
python start.py

# Run tests
pytest tests.py -v

# Run tests with coverage
pytest tests.py -v --cov=app --cov-report=html

# Check code quality
flake8 app.py

# Format code
black app.py

# Initialize database (fresh start)
python init_automotive_db.py

# Verify setup
python setup.py
```

---

## **Support**

📖 **Full Documentation:** See `README.md`
🚀 **Deployment Guide:** See `DEPLOYMENT.md`
✨ **New Features:** See `IMPROVEMENTS.md`
🐛 **Issues:** Create an issue on GitHub

---

## **Feature Highlights**

✅ **Customer Management** - Complete customer profiles with vehicle history
✅ **Service Booking** - Real-time scheduling with conflict detection
✅ **Spare Parts E-Commerce** - 100+ parts with 50% advance payment
✅ **Payment Gateway** - Razorpay integration (test mode free)
✅ **Email Notifications** - Automated confirmations and reminders
✅ **Reviews & Ratings** - Customer feedback system
✅ **Admin Analytics** - Comprehensive dashboard with charts
✅ **Mobile Ready** - Responsive design works on all devices
✅ **Secure** - CSRF protection, input validation, XSS prevention
✅ **Production Ready** - Complete configuration and deployment guides

---

**🎊 Enjoy building with Gaurav Motors!**

Got more than 5 minutes? Read the full `README.md` for detailed documentation.
