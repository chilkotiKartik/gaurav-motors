# Gaurav Motors - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Deploy to Vercel (Recommended for Serverless)

#### Prerequisites:
- GitHub account with repository pushed
- Vercel account (free at vercel.com)

#### Steps:
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Connect your GitHub account and select `gaurav-motors`
4. Configure:
   - **Framework**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty, Vercel auto-detects)
   - **Output Directory**: (leave empty)

5. Add Environment Variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-very-secure-random-key-here
   DATABASE_URL=your-database-url (if using remote DB)
   ```

6. Click "Deploy"

✅ **Done!** Your app will be live at `your-app.vercel.app`

---

### Option 2: Deploy to Heroku (Traditional PaaS)

#### Prerequisites:
- Heroku account (free tier available)
- Heroku CLI installed

#### Steps:
```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create gaurav-motors-app

# Add environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-very-secure-random-key-here

# Deploy using Procfile (already configured)
git push heroku main

# View logs
heroku logs --tail
```

✅ **Done!** Your app will be live at `gaurav-motors-app.herokuapp.com`

---

### Option 3: Deploy to PythonAnywhere (Python-Specific Hosting)

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload files via Git:
   ```bash
   git clone https://github.com/chilkotiKartik/gaurav-motors.git
   cd gaurav-motors
   ```
4. Create Web App → Flask
5. Configure WSGI file to import from `app.py`
6. Reload web app

✅ **Done!** Your app will be live

---

### Option 4: Deploy to AWS (EC2 + RDS)

#### Create EC2 Instance:
```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum install python3 pip nginx
pip3 install -r requirements.txt

# Clone repository
git clone https://github.com/chilkotiKartik/gaurav-motors.git
cd gaurav-motors

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Setup Nginx as reverse proxy
sudo nano /etc/nginx/conf.d/default.conf
# Add upstream configuration pointing to localhost:5000
```

✅ **Done!** Your app will be live on AWS

---

## 📋 Pre-Deployment Checklist

- [x] All dependencies in `requirements.txt`
- [x] Database configuration in `app.py`
- [x] Secret key configured
- [x] Static files organized
- [x] Templates updated
- [x] No debug mode in production
- [x] Gunicorn installed for production WSGI

## 🔐 Important: Environment Variables

**NEVER commit sensitive data!** Set these on your hosting platform:

```
FLASK_ENV=production
SECRET_KEY=<generate-secure-random-key>
DATABASE_URL=<your-database-connection-string>
MAIL_PASSWORD=<your-email-password>
```

## 🗄️ Database Setup

### For Vercel (with MongoDB/PostgreSQL):
```python
# Use MongoDB Atlas or AWS RDS
DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
```

### For Local SQLite (simple):
The app uses SQLite by default - database.db is created automatically.

## ✅ Post-Deployment Testing

1. **Test homepage**: `your-domain.com`
2. **Test contact form**: `your-domain.com/contact`
3. **Test booking**: `your-domain.com/book-service`
4. **Test admin**: `your-domain.com/admin` (username: admin, password: Admin@123456)

## 🔧 Troubleshooting

### 500 Error on Deploy:
- Check environment variables are set
- Verify database connection string
- Check logs on hosting platform

### Static files not loading:
- Ensure `static/` directory is committed to git
- Configure static file serving in production

### Database not initializing:
- SSH into server and run: `python init_automotive_db.py`
- Or use production database URL in config

## 📞 Support

For issues, check:
- Hosting platform logs
- Flask debug output
- Database connection
- Environment variables

---

**Current Status:** ✅ Ready to Deploy
- All code tested and working
- Database initialized
- Static files optimized
- Templates updated with improvements

Choose your preferred hosting platform above and follow the steps!
