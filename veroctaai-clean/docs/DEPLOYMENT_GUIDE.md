# 🚀 VeroctaAI Deployment Guide

This guide covers deploying the VeroctaAI backend API service to various platforms.

## 📋 Prerequisites

- Python 3.13+
- Git repository access
- Required environment variables
- OpenAI API key (optional, for AI features)

## 🌐 Platform-Specific Deployment

### 1. Render.com (Recommended)

Render.com provides seamless deployment with automatic builds and scaling.

#### Step 1: Connect Repository
1. Sign up/login to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the VeroctaAI repository

#### Step 2: Configure Service
```yaml
# render.yaml (already configured)
services:
  - type: web
    name: verocta-ai-api
    env: python
    plan: starter
    region: oregon
    branch: main
    buildCommand: |
      echo "🚀 Starting VeroctaAI API deployment..."
      echo "📦 Installing Python dependencies..."
      pip install -r requirements.txt
      echo "✅ Backend API build complete!"
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
```

#### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `FLASK_ENV` | `production` | Yes |
| `SESSION_SECRET` | `your-secret-key-here` | Yes |
| `OPENAI_API_KEY` | `sk-...` | No |
| `SUPABASE_URL` | `https://...` | No |
| `SUPABASE_PASSWORD` | `your-password` | No |
| `SUPABASE_ANON_KEY` | `eyJ...` | No |

#### Step 4: Deploy
- Click "Create Web Service"
- Render will automatically build and deploy
- Your API will be available at: `https://verocta-ai-api.onrender.com`

### 2. Heroku

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Create Heroku App
```bash
heroku create veroctaai-api
```

#### Step 3: Configure Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SESSION_SECRET=your-secret-key-here
heroku config:set OPENAI_API_KEY=sk-...
```

#### Step 4: Deploy
```bash
git push heroku main
```

### 3. Railway

#### Step 1: Connect Repository
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your VeroctaAI repository

#### Step 2: Configure Environment
Add environment variables in Railway dashboard:
- `FLASK_ENV=production`
- `SESSION_SECRET=your-secret-key-here`
- `OPENAI_API_KEY=sk-...`

#### Step 3: Deploy
Railway will automatically detect Python and deploy.

### 4. DigitalOcean App Platform

#### Step 1: Create App
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository

#### Step 2: Configure App Spec
```yaml
# .do/app.yaml
name: veroctaai-api
services:
- name: api
  source_dir: /
  github:
    repo: your-username/veroctaai
    branch: main
  run_command: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: FLASK_ENV
    value: production
  - key: SESSION_SECRET
    value: your-secret-key-here
```

### 5. AWS Elastic Beanstalk

#### Step 1: Install EB CLI
```bash
pip install awsebcli
```

#### Step 2: Initialize EB Application
```bash
eb init veroctaai-api
eb create production
```

#### Step 3: Configure Environment Variables
```bash
eb setenv FLASK_ENV=production
eb setenv SESSION_SECRET=your-secret-key-here
eb setenv OPENAI_API_KEY=sk-...
```

#### Step 4: Deploy
```bash
eb deploy
```

### 6. Google Cloud Run

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "app:app"]
```

#### Step 2: Build and Deploy
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/veroctaai-api

# Deploy to Cloud Run
gcloud run deploy veroctaai-api \
  --image gcr.io/PROJECT-ID/veroctaai-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SESSION_SECRET=your-secret-key-here
```

## 🐳 Docker Deployment

### Local Docker Development

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

#### Step 2: Build and Run
```bash
# Build image
docker build -t veroctaai-api .

# Run container
docker run -p 5000:5000 \
  -e SESSION_SECRET=your-secret-key-here \
  -e OPENAI_API_KEY=sk-... \
  veroctaai-api
```

### Docker Compose

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SESSION_SECRET=your-secret-key-here
      - OPENAI_API_KEY=sk-...
      - SUPABASE_URL=https://...
      - SUPABASE_PASSWORD=your-password
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
```

#### Run with Docker Compose
```bash
docker-compose up -d
```

## 🔧 Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `SESSION_SECRET` | Flask session secret | `your-secret-key-here` |
| `PORT` | Port number (auto-set by platform) | `5000` |

### Optional Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |
| `SUPABASE_URL` | Supabase database URL | `https://...` |
| `SUPABASE_PASSWORD` | Supabase password | `your-password` |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJ...` |
| `CUSTOM_DOMAIN` | Custom domain for CORS | `api.yourdomain.com` |

### Environment File Template

Create a `.env` file for local development:

```bash
# .env
FLASK_ENV=development
SESSION_SECRET=verocta-local-development-secret-key-2024
HOST=127.0.0.1
PORT=5000

# OpenAI API (Optional - for AI features)
OPENAI_API_KEY=your-openai-api-key-here

# Supabase Database (Optional - for data persistence)
SUPABASE_URL=your-supabase-url-here
SUPABASE_PASSWORD=your-supabase-password-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here

# Custom Domain (Optional)
CUSTOM_DOMAIN=your-domain.com

# Security
JWT_SECRET_KEY=verocta-jwt-secret-key-2024

# Production Settings
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# Logging
LOG_LEVEL=INFO
LOG_FILE=verocta.log
```

## 🔒 Security Considerations

### 1. Environment Variables
- Never commit sensitive data to version control
- Use platform-specific secret management
- Rotate secrets regularly

### 2. HTTPS Configuration
- Always use HTTPS in production
- Configure SSL certificates
- Use secure headers

### 3. Database Security
- Use connection pooling
- Enable SSL for database connections
- Implement proper access controls

### 4. API Security
- Implement rate limiting
- Use CORS properly
- Validate all inputs
- Monitor for suspicious activity

## 📊 Monitoring and Logging

### Health Checks
The API provides health check endpoints:

```bash
# Basic health check
curl https://your-api-url.com/api/health

# Response
{
  "status": "healthy",
  "message": "VeroctaAI API is running",
  "version": "2.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Logging Configuration
```python
# In app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('verocta.log')
    ]
)
```

### Monitoring Tools
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Performance monitoring**: New Relic, DataDog
- **Error tracking**: Sentry, Rollbar
- **Log aggregation**: LogDNA, Papertrail

## 🚀 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement session storage (Redis)
- Database connection pooling
- Stateless application design

### Vertical Scaling
- Increase memory/CPU resources
- Optimize database queries
- Implement caching strategies
- Use CDN for static assets

### Performance Optimization
- Enable gzip compression
- Implement response caching
- Optimize database indexes
- Use async processing for heavy tasks

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python -m pytest tests/
      
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

## 🆘 Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Check Python version
python --version

# Verify dependencies
pip install -r requirements.txt

# Check for syntax errors
python -m py_compile app.py
```

#### 2. Runtime Errors
```bash
# Check logs
tail -f verocta.log

# Verify environment variables
echo $SESSION_SECRET

# Test health endpoint
curl http://localhost:5000/api/health
```

#### 3. Database Connection Issues
```bash
# Test database connection
python -c "from database import db_service; print(db_service.connected)"

# Check environment variables
echo $SUPABASE_URL
echo $SUPABASE_PASSWORD
```

### Debug Mode
Enable debug mode for development:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

## 📞 Support

- **Documentation**: [API Docs](API_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/veroctaai/issues)
- **Email**: support@verocta.ai

---

**Happy Deploying! 🚀**
