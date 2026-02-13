# 🚀 Render Deployment Guide - Gaurav Motors

## Quick Deploy (5 minutes)

### Step 1: Push Latest Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Select **Deploy from Git repository**
4. Connect your GitHub account if not already connected
5. Select repository: `gaurav-motors`

### Step 3: Configure Service
Fill in the form with:

| Field | Value |
|-------|-------|
| **Name** | `gaurav-motors` |
| **Environment** | `Python 3` |
| **Region** | `N. (Oregon)` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120` |

### Step 4: Add Environment Variables
Click **Advanced** → **Add Environment Variable** for each:

```
FLASK_ENV = production
SECRET_KEY = your-very-secure-random-key-here-min-32-chars
```

Generate a secure key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Step 5: Create PostgreSQL Database
1. In Render Dashboard, click **New +** → **PostgreSQL**
2. Fill in:
   - **Name**: `gaurav-motors-db`
   - **Database**: `gaurav_motors`
   - **User**: `postgres` (or custom)
   - **Plan**: Free or Standard

3. Once created, copy the **External Database URL**
4. Go to Web Service settings
5. Add Environment Variable:
   ```
   DATABASE_URL = (paste the PostgreSQL URL)
   ```

### Step 6: Deploy
Click the blue **Deploy** button and wait 2-3 minutes.

✅ **Done!** Your app will be live at `https://gaurav-motors.onrender.com`

---

## Database Initialization

After first deployment, you need to initialize the database:

### Option A: Via Render Console
1. Go to your Web Service dashboard
2. Click **Shell** tab
3. Run:
   ```bash
   python init_automotive_db.py
   ```

### Option B: Via Python Script
Create a file `init_prod.py`:
```python
from app import app, db
from app import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@gauravmotors.com',
            password_hash=generate_password_hash('Admin@123456'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Database initialized with admin user")
```

Run via Shell:
```bash
python init_prod.py
```

---

## ✅ Verify Deployment

1. **Homepage**: https://gaurav-motors.onrender.com
2. **Contact**: https://gaurav-motors.onrender.com/contact
3. **Services**: https://gaurav-motors.onrender.com/services
4. **Admin Login**: https://gaurav-motors.onrender.com/admin
   - Username: `admin`
   - Password: `Admin@123456`

---

## Features Included

✅ PostgreSQL database automatically provisioned
✅ SSL/HTTPS enabled by default
✅ Auto-scaling (horizontal)
✅ Zero-downtime deployments
✅ Health checks enabled
✅ Environment variable management
✅ Logs and monitoring built-in
✅ Custom domain support (paid)

---

## Pricing

| Service | Tier | Cost |
|---------|------|------|
| **Web Service** | Free | $0/mo (may sleep after 15 min inactivity) |
| **Web Service** | Standard | $7+/mo (always on) |
| **PostgreSQL** | Free | $0/mo (deprecated, use Standard) |
| **PostgreSQL** | Standard | $15+/mo |

**Recommendation**: Start with Free tier to test, upgrade to Standard ($7-15/mo) for production.

---

## Troubleshooting

### 500 Internal Server Error
- Check **Logs** tab for errors
- Verify `DATABASE_URL` is set correctly
- Run `python init_prod.py` to initialize database

### Static files not loading
- Clear browser cache
- Verify files in `/static` directory
- Check Render logs for 404 errors

### Database connection refused
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL database is running (green status in Dashboard)
- Wait 1-2 minutes after creating database

### App keeps restarting
- Check memory usage (may need Standard plan)
- Look for infinite loops in code
- Check error logs

---

## Auto-Deploy Setup

Every time you push to `main` branch:
```bash
git add .
git commit -m "Update app"
git push origin main
```

Render automatically deploys! ✅

---

## Custom Domain Setup

1. Go to Web Service settings
2. Scroll to **Custom Domains**
3. Enter your domain (e.g., `gauravmotors.com`)
4. Follow DNS instructions to add CNAME record
5. SSL certificate auto-generates

---

## Monitoring & Logs

### View Logs:
- Dashboard → **Logs** tab
- Real-time streaming of application output
- Filter by timeframe

### Monitor Performance:
- Dashboard → **Metrics** tab
- CPU usage
- Memory usage
- Request count
- Response time

### Set Up Alerts:
- Dashboard → **Notifications**
- Email alerts for deployment failures
- Slack integration available

---

## Next Steps

1. ✅ Deploy to Render (5 min)
2. ✅ Initialize database (2 min)
3. ✅ Test all pages (3 min)
4. ✅ Add custom domain (optional)
5. ✅ Monitor performance

**Your app is production-ready!** 🎉

---

## Support Links

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com
- PostgreSQL Docs: https://www.postgresql.org/docs
- Gunicorn Docs: https://gunicorn.org

---

**Last Updated**: February 14, 2026
**Status**: ✅ Ready to Deploy
