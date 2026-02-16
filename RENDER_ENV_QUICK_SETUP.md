# 🚀 RENDER DEPLOYMENT - QUICK REFERENCE

## Copy & Paste These Environment Variables to Render Dashboard

### Step 1: Get Gmail App Password
1. Go to https://myaccount.google.com/app-passwords
2. Select "Mail" and "Windows Computer"
3. Google gives you a 16-character password
4. Write it down

### Step 2: Generate SECRET_KEY
Run this command:
```
python -c "import secrets; print(secrets.token_urlsafe(64))"
```
Copy the output

### Step 3: Open Render Dashboard
1. https://render.com
2. Your project → **Settings** → **Environment**
3. Click **"Add Environment Variable"**

### Step 4: Copy-Paste These (Replace values marked with ⚠️)

```
KEY: SECRET_KEY
VALUE: sk-proj-Yd4kLm9Np2Qx8Zt5Vw3Hj6Bg1Cr7Fs0Et2Au4Dx9Cf5Ky8Lm3Np6Qx7Zt9Vw2Hj5

KEY: FLASK_ENV
VALUE: production

KEY: FLASK_DEBUG
VALUE: False

KEY: FLASK_APP
VALUE: app.py

KEY: MAIL_SERVER
VALUE: smtp.gmail.com

KEY: MAIL_PORT
VALUE: 587

KEY: MAIL_USE_TLS
VALUE: True

KEY: MAIL_USERNAME
VALUE: your-email@gmail.com  ⚠️ CHANGE THIS

KEY: MAIL_PASSWORD
VALUE: abcdefghijklmnop  ⚠️ CHANGE THIS (your Google app password, no spaces)

KEY: MAIL_DEFAULT_SENDER
VALUE: noreply@gmmotors.com

KEY: MAX_CONTENT_LENGTH
VALUE: 16777216

KEY: UPLOAD_FOLDER
VALUE: uploads

KEY: SESSION_COOKIE_SECURE
VALUE: True

KEY: SESSION_COOKIE_HTTPONLY
VALUE: True

KEY: SESSION_COOKIE_SAMESITE
VALUE: Lax

KEY: PREFERRED_URL_SCHEME
VALUE: https

KEY: DEBUG
VALUE: False

KEY: TESTING
VALUE: False

KEY: LOG_LEVEL
VALUE: INFO
```

---

## ⚠️ MUST CONFIGURE THESE 2:

### 1. MAIL_USERNAME
```
Replace: your-email@gmail.com
With: your-actual-gmail@gmail.com
Example: chilkoti@gmail.com
```

### 2. MAIL_PASSWORD
```
Replace: abcdefghijklmnop
With: Your 16-char Google app password
Steps:
1. https://myaccount.google.com/app-passwords
2. Select Mail & Windows Computer
3. Copy the 16 characters (ignore spaces)
4. Paste here
```

---

## Step 5: Deploy
1. After adding all variables
2. Click **"Deploy"** or **"Redeploy"**
3. Wait 2-3 minutes
4. Your app goes live! ✅

---

## Step 6: Test It Works
1. Go to your Render URL
2. Try booking a service
3. Check if email sent
4. Check admin dashboard

---

## If Email Not Working:
1. Check MAIL_USERNAME is correct
2. Check MAIL_PASSWORD (16 chars, no spaces)
3. Check MAIL_SERVER = smtp.gmail.com
4. Check MAIL_PORT = 587
5. Redeploy and wait 2 minutes
6. Check Render logs for errors

---

## Save These Passwords Safely! 🔐
- SECRET_KEY: Use for production only
- Gmail app password: Don't share
- Never commit to GitHub with real values

