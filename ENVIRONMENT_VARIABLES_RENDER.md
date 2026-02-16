# 🔐 Environment Variables - Complete Guide for Render Deployment

## ✅ Your Complete `.env` File (Copy & Paste Ready)

```env
# ===== FLASK CONFIGURATION =====
SECRET_KEY=sk-proj-Yd4kLm9Np2Qx8Zt5Vw3Hj6Bg1Cr7Fs0Et2Au4Dx9Cf5Ky8Lm3Np6Qx7Zt9Vw2Hj5
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_APP=app.py

# ===== DATABASE CONFIGURATION =====
# Render provides DATABASE_URL automatically - no need to configure
SQLALCHEMY_DATABASE_URI=sqlite:///hms.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# ===== EMAIL CONFIGURATION =====
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@gmmotors.com

# ===== FILE UPLOAD CONFIGURATION =====
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# ===== SECURITY CONFIGURATION =====
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PREFERRED_URL_SCHEME=https

# ===== APPLICATION CONFIGURATION =====
DEBUG=False
TESTING=False

# ===== LOGGING =====
LOG_LEVEL=INFO
```

---

## 📋 Variable Explanations & How to Get/Set Values

### 1. **SECRET_KEY** (REQUIRED)
**What it is**: Encryption key for sessions and cookies  
**Current value**: `sk-proj-Yd4kLm9Np2Qx8Zt5Vw3Hj6Bg1Cr7Fs0Et2Au4Dx9Cf5Ky8Lm3Np6Qx7Zt9Vw2Hj5`  
**Unique for you**: ✅ Generate new one:  
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

### 2. **FLASK_ENV** 
**Value**: `production`  
**Meaning**: Tells Flask to run in production mode (security features enabled)  
**Keep as**: `production`  

---

### 3. **FLASK_DEBUG**
**Value**: `False`  
**Meaning**: Disables debug mode in production (prevents info leaks)  
**Keep as**: `False`  

---

### 4. **FLASK_APP**
**Value**: `app.py`  
**Meaning**: Points to your main Flask application file  
**Keep as**: `app.py`  

---

### 5. **DATABASE_URL** (Auto-provided by Render)
**What it is**: PostgreSQL connection string  
**For Render**: ✅ **Automatic**  
❌ **Don't set manually** - Render provides it automatically  
**For Local**: Uses SQLite  

---

### 6. **MAIL_SERVER**
**Value**: `smtp.gmail.com`  
**Meaning**: Gmail's SMTP server for sending emails  
**Keep as**: `smtp.gmail.com`  

---

### 7. **MAIL_PORT**
**Value**: `587`  
**Meaning**: Gmail SMTP port (TLS)  
**Keep as**: `587`  

---

### 8. **MAIL_USE_TLS**
**Value**: `True`  
**Meaning**: Use encrypted connection to Gmail  
**Keep as**: `True`  

---

### 9. **MAIL_USERNAME** ⚠️ MUST CONFIGURE
**Value**: `your-email@gmail.com`  
**How to set**:
1. Use your Gmail email
2. Example: `myemail@gmail.com`

---

### 10. **MAIL_PASSWORD** ⚠️ MUST CONFIGURE
**Value**: `your-app-specific-password`  
**How to get**:
```
1. Go to https://myaccount.google.com/app-passwords
2. Select "Mail" and "Windows Computer"
3. Google generates a 16-character password
4. Copy & paste here (replace spaces)
```
**Example**: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

---

### 11. **MAIL_DEFAULT_SENDER**
**Value**: `noreply@gmmotors.com`  
**Meaning**: Email from address for automated emails  
**Can use**: Any email address (usually no-reply format)  

---

### 12. **MAX_CONTENT_LENGTH**
**Value**: `16777216`  
**Meaning**: Maximum file upload size in bytes (16 MB)  
**Keep as**: `16777216`  

---

### 13. **UPLOAD_FOLDER**
**Value**: `uploads`  
**Meaning**: Directory to store uploaded files  
**Keep as**: `uploads`  

---

### 14. **SESSION_COOKIE_SECURE**
**Value**: `True`  
**Meaning**: Only send cookies over HTTPS  
**Keep as**: `True`  

---

### 15. **SESSION_COOKIE_HTTPONLY**
**Value**: `True`  
**Meaning**: Cookies not accessible from JavaScript (XSS protection)  
**Keep as**: `True`  

---

### 16. **SESSION_COOKIE_SAMESITE**
**Value**: `Lax`  
**Meaning**: CSRF protection (Lax = stricter)  
**Options**: `Lax`, `Strict`, `None`  
**Keep as**: `Lax`  

---

### 17. **PREFERRED_URL_SCHEME**
**Value**: `https`  
**Meaning**: Force HTTPS URLs in app  
**Keep as**: `https`  

---

### 18. **DEBUG**
**Value**: `False`  
**Meaning**: Disable debug notifications  
**Keep as**: `False`  

---

### 19. **TESTING**
**Value**: `False`  
**Meaning**: Not in testing mode  
**Keep as**: `False`  

---

### 20. **LOG_LEVEL**
**Value**: `INFO`  
**Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`  
**Keep as**: `INFO`  

---

## 🚀 How to Set in Render

### Method 1: In Render Dashboard (EASIEST)

1. **Go to your app** on Render
2. **Settings** tab → **Environment**
3. **Add Environment Variables** one by one:
   - Key: `SECRET_KEY`
   - Value: `sk-proj-Yd4kLm9Np2Qx8Zt5Vw3Hj6Bg1Cr7Fs0Et2Au4Dx9Cf5Ky8Lm3Np6Qx7Zt9Vw2Hj5`
   - Click **Save**

4. **Repeat for all variables above**:
   ```
   FLASK_ENV = production
   FLASK_DEBUG = False
   FLASK_APP = app.py
   MAIL_SERVER = smtp.gmail.com
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = your-email@gmail.com
   MAIL_PASSWORD = your-app-password
   MAIL_DEFAULT_SENDER = noreply@gmmotors.com
   MAX_CONTENT_LENGTH = 16777216
   UPLOAD_FOLDER = uploads
   SESSION_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = Lax
   PREFERRED_URL_SCHEME = https
   DEBUG = False
   TESTING = False
   LOG_LEVEL = INFO
   ```

5. **Deploy** → Done! ✅

### Method 2: Via Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Add variables
render env set SECRET_KEY sk-proj-...
render env set FLASK_ENV production
# ... repeat for all variables
```

---

## ✅ Checklist Before Deploying to Render

- [ ] Generate unique SECRET_KEY
- [ ] Set MAIL_USERNAME to your Gmail
- [ ] Get Gmail app password (16 chars)
- [ ] Set MAIL_PASSWORD
- [ ] Add all 20 variables to Render
- [ ] Deploy on Render
- [ ] Test email sending
- [ ] Test booking system
- [ ] Check logs for errors

---

## 🔧 Variable Priority

### CRITICAL (Must Set)
- ✅ `SECRET_KEY` - Security critical
- ✅ `MAIL_USERNAME` - Emails won't work without
- ✅ `MAIL_PASSWORD` - Emails won't work without
- ✅ `FLASK_ENV` - Must be `production`

### IMPORTANT (Should Set)
- ✅ `SESSION_COOKIE_SECURE` - HTTPS only
- ✅ `PREFERRED_URL_SCHEME` - Force HTTPS

### AUTOMATIC (Render provides)
- ✅ `DATABASE_URL` - Render manages this

### OPTIONAL (Set if needed)
- ❌ Razorpay keys (if using payments)
- ❌ AWS keys (if using S3 storage)
- ❌ Twilio keys (if using SMS)

---

## 🧪 Test Your Configuration

### 1. Test Email Sending
```python
# In Flask shell:
from app import app, send_email
with app.app_context():
    send_email('test@gmail.com', 'Test', '<p>Test email</p>')
```

### 2. Check Environment Variables
```python
import os
print(os.environ.get('SECRET_KEY'))
print(os.environ.get('FLASK_ENV'))
```

### 3. View Logs (in Render)
- Dashboard → **Logs** tab
- Check for errors

---

## 🆘 Common Issues & Solutions

### Issue 1: "Email not sending"
**Solution**: Check MAIL_USERNAME & MAIL_PASSWORD are correct
- Lost password? Get new one from Google account

### Issue 2: "SECRET_KEY not set"
**Solution**: Add SECRET_KEY to Render environment
- Copy from `.env` file
- Add to Render dashboard

### Issue 3: "DATABASE connection error"
**Solution**: Render provides DATABASE_URL automatically
- Don't set manually
- Deploy again if missing

### Issue 4: "Session errors"
**Solution**: Check SESSION_COOKIE settings
- SECURE=True requires HTTPS
- SAMESITE=Lax for strict CSRF

---

## 📝 Copy-Paste Ready Commands

### Generate New SECRET_KEY
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(64))"
```

### Get Gmail App Password
1. https://myaccount.google.com/app-passwords
2. Select: Mail & Windows Computer
3. Copy 16-character password
4. Remove spaces

---

## 🎯 Quick Setup (5 minutes)

1. **Update `.env` locally**:
   - Change `MAIL_USERNAME` to your email
   - Change `MAIL_PASSWORD` to Gmail app password
   - Generate new `SECRET_KEY`

2. **Push to GitHub**:
   ```bash
   git add .env.example
   git commit -m "Update environment variables for Render"
   git push
   ```

3. **Add to Render**:
   - Copy all variables from updated `.env`
   - Add to Render dashboard
   - Deploy

4. **Test**:
   - Visit your Render app URL
   - Try booking
   - Check admin dashboard

**Done! ✅**

