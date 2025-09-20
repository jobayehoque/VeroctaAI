# 🚀 FinDash Deployment Guide

This guide covers various deployment options for the FinDash Financial Insight Platform.

## 📋 **Prerequisites**

- Python 3.8+
- OpenAI API Key
- 1GB+ available disk space
- Internet connection for AI processing

---

## 🖥️ **Local Development Deployment**

### **1. Quick Setup**
```bash
# Clone the repository
git clone <your-repository-url>
cd FinDash

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export SESSION_SECRET="your-secure-secret"

# Run the application
python main.py
```

### **2. Access Application**
- Open browser: `http://localhost:5000`
- Upload a CSV file from the `samples/` directory
- Review the analysis and download reports

---

## 🐳 **Docker Deployment**

### **1. Build and Run with Docker**
```bash
# Build the image
docker build -t findash .

# Run the container
docker run -d \
  --name findash-app \
  -p 5000:5000 \
  -e OPENAI_API_KEY="your-api-key" \
  -e SESSION_SECRET="your-secret" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  findash
```

### **2. Using Docker Compose**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key" > .env
echo "SESSION_SECRET=your-secret" >> .env

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## ☁️ **Cloud Deployment**

### **1. Heroku Deployment**

#### **Setup Heroku CLI**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-findash-app
```

#### **Configure Environment**
```bash
# Set environment variables
heroku config:set OPENAI_API_KEY="your-api-key"
heroku config:set SESSION_SECRET="your-secret"
heroku config:set FLASK_ENV="production"
```

#### **Deploy Application**
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
git add .
git commit -m "Deploy FinDash to Heroku"
git push heroku main

# Open application
heroku open
```

### **2. AWS EC2 Deployment**

#### **Launch EC2 Instance**
```bash
# Launch Ubuntu 22.04 LTS instance
# Configure security group: HTTP (80), HTTPS (443), SSH (22)
```

#### **Setup Application**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone repository
git clone <your-repository-url>
cd FinDash

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set environment variables
echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.bashrc
echo 'export SESSION_SECRET="your-secret"' >> ~/.bashrc
source ~/.bashrc

# Install and configure Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/findash.service
```

#### **Systemd Service Configuration**
```ini
[Unit]
Description=FinDash Financial Insight Platform
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/FinDash
Environment="PATH=/home/ubuntu/FinDash/.venv/bin"
Environment="OPENAI_API_KEY=your-api-key"
Environment="SESSION_SECRET=your-secret"
ExecStart=/home/ubuntu/FinDash/.venv/bin/gunicorn --workers 3 --bind unix:findash.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/FinDash/findash.sock;
        client_max_body_size 16M;
    }

    location /static {
        alias /home/ubuntu/FinDash/static;
    }
}
```

#### **Start Services**
```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl start findash
sudo systemctl enable findash

# Configure Nginx
sudo ln -s /etc/nginx/sites-available/findash /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
```

### **3. Google Cloud Platform (GCP)**

#### **Using Cloud Run**
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project your-project-id

# Build and deploy
gcloud builds submit --tag gcr.io/your-project-id/findash
gcloud run deploy findash \
  --image gcr.io/your-project-id/findash \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="your-api-key",SESSION_SECRET="your-secret"
```

---

## 🔧 **Production Configuration**

### **1. Environment Variables**
```bash
# Required
OPENAI_API_KEY="sk-your-openai-api-key"

# Recommended
SESSION_SECRET="your-secure-random-secret"
FLASK_ENV="production"
FLASK_DEBUG="False"

# Optional
PORT="5000"
WORKERS="4"
TIMEOUT="120"
```

### **2. Security Configuration**

#### **SSL/HTTPS Setup**
```bash
# Using Let's Encrypt (for domain-based deployment)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### **Firewall Configuration**
```bash
# Configure UFW
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
```

### **3. Monitoring and Logging**

#### **Application Logs**
```bash
# View application logs
sudo journalctl -u findash -f

# Application log files
tail -f /var/log/findash/app.log
```

#### **Health Monitoring**
```bash
# Health check endpoint
curl http://your-domain.com/api/health

# Response should be:
# {"status": "healthy", "message": "FinDash Financial Insight Platform is running"}
```

---

## 📊 **Performance Optimization**

### **1. Gunicorn Configuration**
```bash
# For production with 4 CPU cores
gunicorn --workers 8 --worker-class sync --timeout 120 --bind 0.0.0.0:5000 app:app
```

### **2. Nginx Optimization**
```nginx
# Add to nginx.conf for better performance
client_max_body_size 16M;
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

### **3. File System Optimization**
```bash
# Create separate volumes for uploads and outputs
mkdir -p /var/lib/findash/{uploads,outputs,logs}
chown -R ubuntu:www-data /var/lib/findash
chmod -R 755 /var/lib/findash
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Find process using port 5000
sudo netstat -tlnp | grep :5000
sudo kill -9 <process-id>

# Or use different port
python main.py --port 5001
```

#### **Permission Denied Errors**
```bash
# Fix file permissions
chmod +x main.py
chown -R $USER:$USER .
```

#### **Memory Issues**
```bash
# Monitor memory usage
free -h
top -p $(pgrep -f gunicorn)

# Reduce workers if needed
gunicorn --workers 2 app:app
```

#### **API Key Issues**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API connection
python -c "from gpt_utils import test_openai_connection; print(test_openai_connection())"
```

---

## 📈 **Scaling Considerations**

### **1. Horizontal Scaling**
- Use load balancer (Nginx, HAProxy)
- Deploy multiple application instances
- Share uploads/outputs via network storage

### **2. Database Integration**
- Add PostgreSQL for user management
- Store analysis history
- Cache frequent operations

### **3. Background Processing**
- Use Celery for async analysis
- Redis for task queue
- Separate analysis workers

---

## 🔄 **Maintenance**

### **1. Regular Updates**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart application
sudo systemctl restart findash
```

### **2. Backup Strategy**
```bash
# Backup critical files
tar -czf findash-backup-$(date +%Y%m%d).tar.gz uploads/ outputs/ logs/

# Automated backup script
echo "0 2 * * * /home/ubuntu/backup-findash.sh" | sudo crontab -
```

### **3. Log Rotation**
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/findash
```

---

**🎉 Your FinDash platform is now deployed and ready for production use!**