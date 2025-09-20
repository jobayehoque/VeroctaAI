# 🚀 VeroctaAI Deployment Guide

This guide covers deploying VeroctaAI to various platforms for production use.

## 📋 Prerequisites

- Node.js 16+ and Python 3.11+
- Git repository with your code
- Environment variables configured
- Domain name (optional)

## 🌐 Render Deployment (Recommended)

### 1. Connect Repository
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository containing VeroctaAI

### 2. Configure Service
```yaml
# Use the provided render.yaml or configure manually:
Name: verocta-ai
Environment: Python
Build Command: pip install -r requirements.txt && cd frontend && npm install && npm run build
Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 4 backend.app:app
```

### 3. Environment Variables
Set these in Render dashboard:
```
FLASK_ENV=production
SESSION_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-key (optional)
SUPABASE_URL=your-supabase-url (optional)
SUPABASE_PASSWORD=your-supabase-password (optional)
SUPABASE_ANON_KEY=your-supabase-anon-key (optional)
```

### 4. Deploy
- Click "Create Web Service"
- Render will automatically build and deploy
- Your app will be available at `https://your-app-name.onrender.com`

## 🐳 Docker Deployment

### 1. Build Production Image
```bash
docker build -f Dockerfile.production -t verocta-ai:latest .
```

### 2. Run Container
```bash
docker run -d \
  --name verocta-ai \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SESSION_SECRET=your-secret \
  -e OPENAI_API_KEY=your-key \
  verocta-ai:latest
```

### 3. Docker Compose (Production)
```bash
# Copy environment template
cp env.production.template .env

# Edit .env with your values
nano .env

# Deploy with compose
docker-compose -f docker-compose.production.yml up -d
```

## ☁️ AWS Deployment

### 1. EC2 Instance
```bash
# Launch Ubuntu 22.04 LTS instance
# Install dependencies
sudo apt update
sudo apt install python3.11 python3.11-pip nodejs npm nginx

# Clone repository
git clone <your-repo-url>
cd VeroctaAI/verocta-ai-unified

# Install dependencies
pip3 install -r requirements.txt
cd frontend && npm install && npm run build

# Configure Nginx
sudo nano /etc/nginx/sites-available/verocta-ai
```

### 2. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/verocta-ai.service
```

```ini
[Unit]
Description=VeroctaAI Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/VeroctaAI/verocta-ai-unified
Environment=FLASK_ENV=production
Environment=SESSION_SECRET=your-secret
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔒 SSL/HTTPS Setup

### 1. Let's Encrypt (Certbot)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Cloudflare (Alternative)
1. Add your domain to Cloudflare
2. Update nameservers
3. Enable SSL/TLS encryption
4. Configure proxy settings

## 📊 Monitoring & Logging

### 1. Application Logs
```bash
# View logs
docker logs verocta-ai

# Follow logs
docker logs -f verocta-ai

# Systemd logs
journalctl -u verocta-ai -f
```

### 2. Health Checks
```bash
# Test health endpoint
curl https://your-domain.com/api/health

# Expected response:
{
  "status": "healthy",
  "message": "VeroctaAI Financial Intelligence Platform is running",
  "version": "2.0.0"
}
```

### 3. Performance Monitoring
- Use Render's built-in metrics
- Set up Uptime Robot for monitoring
- Configure alerts for downtime

## 🔧 Environment Variables

### Required
```bash
FLASK_ENV=production
SESSION_SECRET=your-super-secret-key
```

### Optional
```bash
OPENAI_API_KEY=your-openai-key
SUPABASE_URL=your-supabase-url
SUPABASE_PASSWORD=your-supabase-password
SUPABASE_ANON_KEY=your-supabase-anon-key
CUSTOM_DOMAIN=your-domain.com
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check Node.js version
   node --version  # Should be 16+
   
   # Clear npm cache
   npm cache clean --force
   ```

2. **Python Dependencies**
   ```bash
   # Update pip
   pip install --upgrade pip
   
   # Install with no cache
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Port Issues**
   ```bash
   # Check if port is in use
   lsof -i :5000
   
   # Kill process if needed
   sudo kill -9 <PID>
   ```

4. **Database Connection**
   - Verify Supabase credentials
   - Check network connectivity
   - Review firewall settings

### Logs Location
- **Docker**: `docker logs <container-name>`
- **Systemd**: `journalctl -u verocta-ai`
- **Render**: Dashboard → Logs tab
- **Local**: `./verocta.log`

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple instances
- Configure session storage (Redis)

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use CDN for static assets

## 🔄 Updates & Maintenance

### 1. Code Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### 2. Database Migrations
```bash
# Run migrations if needed
python backend/setup_database.py
```

### 3. Backup Strategy
- Regular database backups
- Code repository backups
- Environment variable backups

## 📞 Support

- **Documentation**: Check `/docs/` folder
- **API Reference**: `/api/docs` endpoint
- **Health Check**: `/api/health` endpoint
- **Issues**: GitHub Issues page

---

**Ready to deploy?** Choose your preferred method and follow the steps above. For questions, check the troubleshooting section or create an issue on GitHub.
