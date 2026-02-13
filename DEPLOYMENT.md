# 🚀 DEPLOYMENT GUIDE - Gaurav Motors

## **Quick Start (Development)**

```bash
# 1. Clone and setup
cd gaurav-motors
cp .env.example .env

# 2. Edit .env with your settings
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_automotive_db.py

# 5. Run development server
python start.py
# or
flask run

# Access at: http://localhost:5000
```

---

## **Production Deployment**

### **Option 1: Traditional Server (Ubuntu/Debian)**

#### **1. Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx supervisor -y

# Create application directory
sudo mkdir -p /var/www/gaurav-motors
cd /var/www/gaurav-motors
```

#### **2. Application Setup**
```bash
# Clone repository
git clone https://github.com/chilkotiKartik/gaurav-motors.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit with production values
```

#### **3. Database Setup**
```bash
# For PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres psql
CREATE DATABASE gaurav_motors;
CREATE USER gmadmin WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE gaurav_motors TO gmadmin;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://gmadmin:your_secure_password@localhost/gaurav_motors

# Initialize database
python init_automotive_db.py
```

#### **4. Gunicorn Setup**
```bash
# Create Gunicorn config
sudo nano /var/www/gaurav-motors/gunicorn_config.py
```

**gunicorn_config.py:**
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gaurav-motors/gunicorn-error.log"
accesslog = "/var/log/gaurav-motors/gunicorn-access.log"
loglevel = "info"
```

#### **5. Supervisor Configuration**
```bash
sudo nano /etc/supervisor/conf.d/gauravmotors.conf
```

**gauravmotors.conf:**
```ini
[program:gauravmotors]
directory=/var/www/gaurav-motors
command=/var/www/gaurav-motors/venv/bin/gunicorn -c gunicorn_config.py app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/gaurav-motors/stderr.log
stdout_logfile=/var/log/gaurav-motors/stdout.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/gaurav-motors
sudo chown www-data:www-data /var/log/gaurav-motors

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gauravmotors
```

#### **6. Nginx Configuration**
```bash
sudo nano /etc/nginx/sites-available/gauravmotors
```

**gauravmotors:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/gaurav-motors/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/gaurav-motors/uploads;
        expires 7d;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gauravmotors /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### **7. SSL Certificate (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

### **Option 2: Docker Deployment**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./uploads:/app/uploads
      - ./hms.db:/app/hms.db
    restart: unless-stopped
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/usr/share/nginx/html/static
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    restart: unless-stopped
    depends_on:
      - web
```

**Deploy with Docker:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

### **Option 3: Cloud Deployment (Heroku)**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create gaurav-motors

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Initialize database
heroku run python init_automotive_db.py

# Open app
heroku open
```

---

### **Option 4: Cloud Deployment (AWS/DigitalOcean)**

**AWS Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 gaurav-motors

# Create environment
eb create gaurav-motors-env

# Deploy
eb deploy

# Open
eb open
```

**DigitalOcean App Platform:**
1. Connect GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy automatically on push

---

## **Post-Deployment Checklist**

### **Security**
- [ ] Change default admin password
- [ ] Update SECRET_KEY to random value
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (UFW/iptables)
- [ ] Set up fail2ban for brute force protection
- [ ] Enable automatic security updates

### **Monitoring**
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring
- [ ] Enable application logs
- [ ] Set up database backups
- [ ] Configure email alerts

### **Performance**
- [ ] Enable Redis caching
- [ ] Configure CDN for static files
- [ ] Optimize database queries
- [ ] Enable gzip compression
- [ ] Set up database connection pooling

### **Backup Strategy**
```bash
# Database backup script
#!/bin/bash
BACKUP_DIR="/backups/gaurav-motors"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump gaurav_motors > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Delete backups older than 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
```

**Cron job:**
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## **Monitoring & Maintenance**

### **Check Application Status**
```bash
# Supervisor
sudo supervisorctl status gauravmotors

# Nginx
sudo systemctl status nginx

# Logs
tail -f /var/log/gaurav-motors/gunicorn-error.log
tail -f /var/log/nginx/error.log
```

### **Update Application**
```bash
cd /var/www/gaurav-motors
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart gauravmotors
```

### **Database Migrations**
```bash
# Backup first!
pg_dump gaurav_motors > backup_before_migration.sql

# Run migrations
python manage.py db upgrade

# Restart application
sudo supervisorctl restart gauravmotors
```

---

## **Troubleshooting**

### **Application won't start**
```bash
# Check logs
sudo supervisorctl tail gauravmotors stderr

# Manual test
cd /var/www/gaurav-motors
source venv/bin/activate
python app.py
```

### **502 Bad Gateway**
```bash
# Check if Gunicorn is running
sudo supervisorctl status gauravmotors

# Check if port 8000 is listening
sudo netstat -tlnp | grep 8000

# Restart services
sudo supervisorctl restart gauravmotors
sudo systemctl restart nginx
```

### **Database Connection Errors**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U gmadmin -d gaurav_motors -h localhost
```

---

## **Support & Resources**

- **Documentation:** README.md
- **Improvements:** IMPROVEMENTS.md
- **Issues:** CRITICAL_ISSUES.md (resolved)
- **GitHub:** https://github.com/chilkotiKartik/gaurav-motors

**Need Help?** Create an issue on GitHub or contact support.

---

**🎉 Congratulations! Your Gaurav Motors application is now deployed and running in production!**
