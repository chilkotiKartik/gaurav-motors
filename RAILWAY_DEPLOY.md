# 🚀 Deploy to Railway in 5 Minutes

Railway is **FAST** - deploys in 1-2 minutes with automatic Python detection.

## Step 1: Prepare Your Repository
```bash
cd c:\Users\chilk\OneDrive\Desktop\hms

# Initialize Git if not already done
git init
git add .
git commit -m "Prepare for Railway deployment"

# Push to GitHub (required)
git remote add origin https://github.com/YOUR_USERNAME/gaurav-motors.git
git branch -M main
git push -u origin main
```

## Step 2: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (fastest option)
3. Authorize Railway to access your repositories

## Step 3: Deploy to Railway (ONE CLICK)
1. Click **New Project** on Railway dashboard
2. Select **Deploy from GitHub**
3. Choose your repository `gaurav-motors`
4. Railway auto-detects Python + Procfile ✅
5. Click **Deploy** - Done! ⏱️ 1-2 minutes

## Step 4: Set Environment Variables
Once deployed, click the project → **Variables**:

```
SECRET_KEY=your-super-secure-random-key-here

FLASK_ENV=production

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@gmmotors.com

DATABASE_URL=(Railway provides PostgreSQL automatically)
```

## Step 5: Connect Database
Railway **automatically provides PostgreSQL** - just add `DATABASE_URL` variable (it's pre-filled).

## Step 6: View Your Live App
- Find the domain in Railway dashboard
- Click the link → Your app is live! 🎉
- Example: `gaurav-motors-production.up.railway.app`

---

## Troubleshooting

**App not starting?**
```bash
# Check logs in Railway dashboard
# Look for errors in "Logs" tab
```

**Database connection error?**
- Railway auto-provides `DATABASE_URL`
- Make sure it's in Variables tab
- Restart deployment if needed

**Still having issues?**
- Check Railway logs for error messages
- Verify all required env variables are set
- Make sure requirements.txt has all dependencies

---

## Why Railway is Fast:
✅ Auto-detects Python from runtime.txt  
✅ Auto-detects WSGI from Procfile  
✅ No build steps needed  
✅ Automatic PostgreSQL included  
✅ Instant deployments (reload on push)  

**Total time: 2-5 minutes from GitHub push to live URL**
