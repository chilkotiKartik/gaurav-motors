# 🚀 DEPLOY GAURAV MOTORS TO RENDER - COMPLETE GUIDE

## ⏱️ Estimated Time: 10 minutes

---

## 📋 Pre-Deployment Verification

✅ All code committed to GitHub  
✅ render.yaml configuration file ready  
✅ requirements.txt with all dependencies  
✅ PostgreSQL support enabled in app.py  
✅ Environment variables configured  

---

## 🎯 Step-by-Step Deployment

### STEP 1: Prepare GitHub Repository
```bash
# Verify repository is clean and pushed
git status           # Should show "nothing to commit"
git log --oneline -5 # Shows recent commits
```

✅ **Current Status**: Repository is clean and pushed to `chilkotiKartik/gaurav-motors`

---

### STEP 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub account (recommended)
3. Authorize GitHub access
4. Go to Dashboard: https://dashboard.render.com

---

### STEP 3: Create PostgreSQL Database
1. In Render Dashboard, click **New +**
2. Select **PostgreSQL**
3. Fill in:
   - **Name**: `gaurav-motors-db`
   - **Database**: `gaurav_motors`
   - **User**: `postgres` (auto-generated)
   - **Region**: N. California (or near you)
   - **Plan**: Standard ($15/month)

4. Click **Create Database**
5. ⏳ **Wait 2-3 minutes** for database to initialize
6. **IMPORTANT**: Copy the Connection String (looks like:)
   ```
   postgresql://user:password@host:5432/gaurav_motors
   ```
8. Save this for next step

---

### STEP 4: Create Web Service
1. Click **New +** → **Web Service**
2. Select **Deploy from Git repository**
3. Click **Connect GitHub** if first time
4. Search for `gaurav-motors` repository
5. Click **Connect**

6. **Configure Service**:
   | Field | Value |
   |-------|-------|
   | **Name** | `gaurav-motors` |
   | **Environment** | `Python 3` |
   | **Region** | Same as database |
   | **Branch** | `main` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120` |

---

### STEP 5: Add Environment Variables
Scroll down to **Environment** section:

Click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | Generate below ⬇️ |
| `DATABASE_URL` | Paste from Step 3 |

**Generate SECRET_KEY** (run in terminal):
```python
import secrets
print(secrets.token_urlsafe(32))
```

Example output: `4X-7kL9mN2pQ8rS1tU5vW3xYzAbCdEfGhIjKlMnOpQr`  
(Use this for SECRET_KEY value)

---

### STEP 6: Connect Database to Web Service
1. Find your PostgreSQL database in Dashboard
2. Go to its settings
3. Click **Connect this database to other services**
4. Select `gaurav-motors` web service
5. Click **Connect**

(This auto-adds DATABASE_URL environment variable)

---

### STEP 7: Deploy
1. Verify all settings are correct
2. Click blue **Deploy** button
3. ⏳ **Wait 2-5 minutes** for deployment
4. Check logs for messages like:
   ```
   Building requirements
   Successfully installed all packages
   Running on 0.0.0.0:port
   ```

✅ **Deployment Complete!** You should see a green status.

---

## 🔗 After Deployment

### 1. Get Your URL
- Go to your service dashboard
- Under **Redirects**, find the URL
- Format: `https://gaurav-motors-xxxx.onrender.com`

### 2. Initialize Database
1. Go to **Shell** tab in service dashboard
2. Run:
   ```bash
   python init_automotive_db.py
   ```
3. Should see: `✅ Database initialized with admin user`

### 3. Test the Application
1. **Homepage**: https://your-url.onrender.com
2. **Contact Page**: https://your-url.onrender.com/contact
3. **Services**: https://your-url.onrender.com/services
4. **Admin Login**: https://your-url.onrender.com/admin
   - Username: `admin`
   - Password: `Admin@123456`

---

## 📊 Monitoring After Deployment

### View Logs
- Dashboard → **Logs** tab
- Real-time application output
- Check for errors

### Monitor Resources
- Dashboard → **Metrics** tab
- CPU usage
- Memory usage
- Request count

### Set Up Alerts
- Dashboard → **Notifications**
- Add email for deployment failures
- Add Slack webhook (optional)

---

## 💰 Pricing Overview

| Service | Tier | Monthly Cost |
|---------|------|-------------|
| **Web Service** | Free | $0 (sleeps after 15 min) |
| **Web Service** | Standard | $7+/month (always on) |
| **PostgreSQL** | Standard | $15+/month |
| **Total** | Minimum | $22/month (recommended) |

**Note**: Free tier suitable for testing. Upgrade to Standard for production.

---

## ✅ Deployment Checklist

- [ ] GitHub repository updated
- [ ] render.yaml file present
- [ ] requirements.txt includes psycopg2-binary
- [ ] PostgreSQL database created
- [ ] Web service created
- [ ] Environment variables set:
  - [ ] FLASK_ENV=production
  - [ ] SECRET_KEY=xxxxx
  - [ ] DATABASE_URL=postgresql://...
  - [ ] PYTHON_VERSION=3.11.0
- [ ] Database connected to web service
- [ ] Deployment successful (green status)
- [ ] Database initialized
- [ ] Application tested
- [ ] Admin login works

---

## 🆘 Troubleshooting

### Issue: 503 Service Unavailable
**Solution**: 
- Check build logs for errors
- Verify all environment variables are set
- Wait 1-2 minutes for service to fully start

### Issue: Database Connection Error
**Solution**:
- Verify DATABASE_URL is correct
- Check PostgreSQL database is running (green status)
- Wait 2 minutes after creating database

### Issue: Static Files Not Loading
**Solution**:
- Clear browser cache (Ctrl+Shift+Delete)
- Check files are in `/static` directory
- Verify build included static files

### Issue: Admin Login Fails
**Solution**:
- Run `python init_automotive_db.py` in Shell
- Default credentials: admin / Admin@123456
- Check logs for SQL errors

### Issue: Email Not Sending
**Solution**:
- Set up environment variables:
  - `MAIL_SERVER=smtp.gmail.com`
  - `MAIL_USERNAME=your-email@gmail.com`
  - `MAIL_PASSWORD=app-specific-password`
- Generate app password from Gmail

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs
- **GitHub Issues**: https://github.com/chilkotiKartik/gaurav-motors/issues

---

## 🎉 Congratulations!

Your Gaurav Motors application is now live on Render!

**App URL**: https://gaurav-motors-xxxx.onrender.com  
**Admin Panel**: https://gaurav-motors-xxxx.onrender.com/admin  
**Status**: ✅ Production Ready

---

**Last Updated**: February 14, 2026  
**Version**: 1.0.0  
**Maintained By**: Gaurav Motors
