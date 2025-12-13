# Free API Integration Guide

## 🎉 All Free - No Credit Card Required!

This guide shows you how to set up **completely free** API integrations for your HMS system.

---

## 1. Razorpay Payment Gateway (FREE Test Mode)

### Setup (2 minutes)
1. Go to https://razorpay.com/
2. Click "Sign Up" - No credit card needed!
3. After signup, go to Settings → API Keys
4. You'll see **Test Mode** keys (completely free)

### Add to .env file:
```env
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXXXXX
RAZORPAY_KEY_SECRET=XXXXXXXXXXXXXXXX
RAZORPAY_MODE=test
```

### Features (Free Forever):
- ✅ Test payments with card: 4111 1111 1111 1111
- ✅ UPI testing
- ✅ Wallet testing
- ✅ Net Banking simulation
- ✅ No transaction limits in test mode

---

## 2. Flask-Mail with Gmail (FREE)

### Setup (3 minutes)
1. Use any Gmail account
2. Enable 2-Factor Authentication
3. Generate App Password:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Scroll down, click "App passwords"
   - Generate password for "Mail"

### Add to .env file:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Features:
- ✅ Send 500 emails/day (FREE)
- ✅ Order confirmations
- ✅ Appointment reminders
- ✅ Password resets

---

## 3. SMS Notifications (FREE Options)

### Option A: Twilio (FREE Trial)
**Get $15 credit - 100+ SMS free**

1. Sign up: https://www.twilio.com/try-twilio
2. Verify your phone number
3. Get Trial credentials

```env
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Option B: MSG91 (FREE)
**Get 100 SMS credits free**

1. Sign up: https://msg91.com/signup
2. Get API key from dashboard

```env
MSG91_AUTH_KEY=your_auth_key
MSG91_SENDER_ID=GMHMS
```

### Option C: Fast2SMS (FREE for India)
**Get 50 SMS/day free**

1. Sign up: https://www.fast2sms.com/
2. Get API key

```env
FAST2SMS_API_KEY=your_api_key
```

---

## 4. Image Storage (FREE)

### Option A: Cloudinary (FREE)
**25 GB storage + 25 GB bandwidth/month**

1. Sign up: https://cloudinary.com/users/register/free
2. Get your credentials from Dashboard

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Option B: ImgBB (FREE)
**Unlimited image hosting**

1. Sign up: https://imgbb.com/
2. Get API key from: https://api.imgbb.com/

```env
IMGBB_API_KEY=your_api_key
```

---

## 5. Database (FREE Production)

### PostgreSQL on Render.com (FREE)
**Free PostgreSQL database**

1. Your Render account already has this!
2. In Render dashboard, create "New PostgreSQL"
3. Choose Free plan (no credit card)
4. Copy the connection string

```env
DATABASE_URL=postgresql://user:pass@host/dbname
```

---

## Complete .env File Template

Create `.env` file in your project root:

```env
# Flask Secret Key
SECRET_KEY=your-super-secret-random-key-change-this-123456789

# Database (Use SQLite for dev, PostgreSQL for production)
# Development:
DATABASE_URL=sqlite:///hms.db
# Production (from Render):
# DATABASE_URL=postgresql://user:pass@host/dbname

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Razorpay (Test Mode - FREE)
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXXXXX
RAZORPAY_KEY_SECRET=XXXXXXXXXXXXXXXX
RAZORPAY_MODE=test

# SMS (Choose one - all have free tier)
# Option 1: Twilio
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Option 2: MSG91
MSG91_AUTH_KEY=your_auth_key
MSG91_SENDER_ID=GMHMS

# Option 3: Fast2SMS
FAST2SMS_API_KEY=your_api_key

# Image Storage (Optional)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Application Settings
FLASK_ENV=development
DEBUG=True
```

---

## 🚀 Quick Start

1. **Copy the template above** to create `.env` file
2. **Sign up for FREE accounts** (5 minutes total):
   - Razorpay (test mode)
   - Gmail (app password)
   - Choose ONE SMS provider
3. **Replace placeholder values** with your actual keys
4. **Run the app**:
   ```bash
   python app.py
   ```

---

## Testing Payment Integration

### Test Card Details (Razorpay Test Mode):
```
Card Number: 4111 1111 1111 1111
CVV: Any 3 digits
Expiry: Any future date
```

### Test UPI:
```
UPI ID: success@razorpay
```

### Test Wallets:
- All test wallet payments automatically succeed

---

## 💰 Cost Breakdown

| Service | Free Tier | Perfect For |
|---------|-----------|-------------|
| Razorpay Test | Unlimited | Development & Testing |
| Gmail SMTP | 500 emails/day | Order confirmations |
| Twilio Trial | $15 credit (~100 SMS) | SMS notifications |
| MSG91 | 100 SMS credits | Indian SMS |
| Fast2SMS | 50 SMS/day | Daily notifications |
| Cloudinary | 25 GB storage | Image uploads |
| Render PostgreSQL | 90 days free | Production database |

**Total Cost: ₹0 (FREE!)** 🎉

---

## Production Deployment on Render

1. Push code to GitHub
2. Create Web Service on Render
3. Add PostgreSQL database (free)
4. Set environment variables in Render dashboard
5. Deploy!

**No credit card needed for testing!**

---

## Need Help?

- Razorpay Docs: https://razorpay.com/docs/
- Flask-Mail: https://pythonhosted.org/Flask-Mail/
- Twilio: https://www.twilio.com/docs/
- Render Deploy: https://render.com/docs

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file to GitHub
- Add `.env` to `.gitignore`
- Use different keys for production
- Enable 2FA on all accounts
- Rotate keys regularly

---

## What You Get FREE:

✅ Payment gateway (test mode unlimited)
✅ Email notifications (500/day)
✅ SMS notifications (50-100/day)
✅ Image storage (25 GB)
✅ PostgreSQL database (90 days, renewable)
✅ Web hosting on Render

**Everything you need to run a complete HMS system - ABSOLUTELY FREE!** 🎉
