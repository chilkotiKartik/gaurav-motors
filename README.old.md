# 🏥 GM Motors Hospital Management System - Enhanced Edition

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](https://render.com)

A comprehensive, production-ready Hospital Management System with 10+ advanced features including medical records, reviews, analytics, and more!

## ✨ Features

- 👥 **Multi-Role System**: Admin, Doctor, Patient portals
- 📅 **Appointment Management**: Book, reschedule, track appointments
- 📋 **Medical Records**: Upload and manage patient documents
- 🏥 **Medical History**: Comprehensive health tracking
- ⭐ **Reviews & Ratings**: 5-star doctor review system
- 📧 **Email Notifications**: Automated appointment confirmations
- 🔔 **Real-time Notifications**: In-app alert system
- 📊 **Advanced Analytics**: Beautiful charts and insights
- 💳 **Payment Tracking**: Revenue and transaction management
- 🔍 **Universal Search**: Search doctors, services, parts
- 📈 **Data Export**: CSV export functionality
- 🚗 **Auto Services**: Car service booking system
- 🔧 **Spare Parts**: Parts catalog and ordering
- 📱 **Responsive Design**: Works on all devices

## 🚀 Quick Start

### Deploy to Render (6 minutes)

1. **Clone & Push**
   ```bash
   git clone https://github.com/chilkotiKartik/gaurav-motors.git
   cd gaurav-motors
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://render.com)
   - New + → Web Service
   - Connect your repository
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

3. **Set Environment Variables** (in Render)
   ```
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

4. **Initialize Database** (in Render Shell)
   ```bash
   python setup_enhanced.py
   ```

5. **Done!** 🎉 Your app is live!

**Detailed Guide**: See [QUICK_START.md](QUICK_START.md)

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Fast deployment guide (6 minutes) |
| [DEPLOY_RENDER.md](DEPLOY_RENDER.md) | Complete deployment instructions |
| [README_FEATURES.md](README_FEATURES.md) | Full feature documentation |
| [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) | What's new in this version |
| [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) | Complete project overview |

## 🔑 Default Credentials

After running `setup_enhanced.py`:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Doctor | `dr.rajesh` | `doctor123` |
| Patient | `johndoe` | `patient123` |

⚠️ **Change these passwords in production!**

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Clone repository
git clone https://github.com/chilkotiKartik/gaurav-motors.git
cd gaurav-motors

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your settings

# Initialize database
python setup_enhanced.py

# Run application
python app.py
```

Visit: http://localhost:5000

## 📦 Tech Stack

- **Backend**: Flask 3.0, SQLAlchemy
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Email**: Flask-Mail
- **Server**: Gunicorn
- **Platform**: Render.com

## 🗄️ Database Models

- User, DoctorProfile, PatientProfile
- Appointment, Treatment, Availability
- Department, ServiceCategory, CarService
- SparePartCategory, SparePart
- MedicalRecord, MedicalHistory
- DoctorReview, ServiceReview
- Payment, Notification, EmailQueue

## 🌐 API Endpoints

### Analytics
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/appointments-by-month` - Chart data
- `GET /api/analytics/revenue-by-month` - Revenue data
- `GET /api/analytics/top-doctors` - Top rated doctors

### Notifications
- `GET /api/notifications` - User notifications
- `POST /api/notifications/<id>/read` - Mark as read

### Search
- `GET /search?q=keyword&category=type` - Universal search

### Export
- `GET /admin/export/appointments` - Export appointments CSV
- `GET /admin/export/revenue` - Export revenue CSV

## 🎨 Screenshots

*(Add your screenshots here after deployment)*

## 🔒 Security

- Password hashing (Werkzeug)
- Role-based access control
- SQL injection protection (SQLAlchemy)
- Secure file uploads
- CSRF protection ready
- Environment variable configuration

## 📈 Features in Detail

### Medical Records System
- Upload lab reports, X-rays, prescriptions
- Track medical history (allergies, conditions, medications)
- Secure document storage
- Blood type, insurance, emergency contacts

### Analytics Dashboard
- 12+ key performance metrics
- Beautiful charts (Chart.js)
- Monthly trends visualization
- Revenue analytics
- Top doctors leaderboard
- CSV export

### Review System
- 5-star rating for doctors
- Verified patient reviews
- Average rating calculation
- Service reviews
- Public review pages

## 🚀 Deployment

**Render.com** (Recommended):
- Free tier available
- Automatic HTTPS
- Continuous deployment
- See [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

**Other Platforms**:
- Heroku, Railway, Fly.io
- Any platform supporting Python/Gunicorn

## 🔮 Future Enhancements

- SMS notifications (Twilio)
- Real-time chat (Flask-SocketIO)
- Video consultations (WebRTC)
- PDF report generation
- Calendar integration
- Multi-language support
- Dark mode theme

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 👨‍💻 Author

**Kartik Chilkoti**
- GitHub: [@chilkotiKartik](https://github.com/chilkotiKartik)
- Repository: [gaurav-motors](https://github.com/chilkotiKartik/gaurav-motors)

## 🙏 Acknowledgments

- Flask team for the excellent framework
- Bootstrap for the UI components
- Chart.js for data visualizations
- Render.com for hosting platform

## 📞 Support

For issues or questions:
1. Check the [documentation](README_FEATURES.md)
2. Review [deployment guide](DEPLOY_RENDER.md)
3. Open an issue on GitHub

## ⭐ Star Us!

If you find this project helpful, please give it a star on GitHub!

---

**Built with ❤️ for healthcare and automotive industries**

*Production-ready • Fully documented • Easy to deploy*
