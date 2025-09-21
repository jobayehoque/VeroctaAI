#!/bin/bash

# VeroctaAI Enterprise Setup Script
# This script sets up the complete enterprise development environment

echo "🏢 Setting up VeroctaAI Enterprise Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_status "Python version: $PYTHON_VERSION"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found. Skipping frontend setup."
    NODE_AVAILABLE=false
else
    NODE_VERSION=$(node --version)
    print_status "Node.js version: $NODE_VERSION"
    NODE_AVAILABLE=true
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_warning "Docker not found. Skipping Docker setup."
    DOCKER_AVAILABLE=false
else
    DOCKER_VERSION=$(docker --version)
    print_status "Docker version: $DOCKER_VERSION"
    DOCKER_AVAILABLE=true
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads outputs logs tests/unit tests/integration tests/e2e

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# VeroctaAI Enterprise Environment Configuration
FLASK_ENV=development
SECRET_KEY=verocta-enterprise-development-secret-key-2024
JWT_SECRET_KEY=verocta-enterprise-jwt-secret-key-2024
HOST=127.0.0.1
PORT=5000

# OpenAI API (Optional - for AI features)
# OPENAI_API_KEY=your-openai-api-key-here

# Supabase Database (Optional - for data persistence)
# SUPABASE_URL=your-supabase-url-here
# SUPABASE_PASSWORD=your-supabase-password-here
# SUPABASE_ANON_KEY=your-supabase-anon-key-here

# Redis (Optional - for caching)
# REDIS_URL=redis://localhost:6379/0

# Custom Domain (Optional)
# CUSTOM_DOMAIN=your-domain.com

# Security
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax

# Production Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/verocta.log

# Monitoring (Optional)
# SENTRY_DSN=your-sentry-dsn-here

# Email (Optional)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password

# Payment (Optional)
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_...

# Storage (Optional)
# STORAGE_TYPE=local
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_S3_BUCKET=your-bucket
EOF
    print_success ".env file created. Please edit it with your configuration."
fi

cd ..

# Setup frontend if Node.js is available
if [ "$NODE_AVAILABLE" = true ]; then
    print_status "Setting up frontend..."
    cd frontend
    
    # Check if package.json exists
    if [ -f package.json ]; then
        print_status "Installing frontend dependencies..."
        npm install
        
        # Create .env file for frontend
        if [ ! -f .env ]; then
            print_status "Creating frontend .env file..."
            cat > .env << EOF
# Frontend Environment Variables
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=VeroctaAI Enterprise
VITE_APP_VERSION=2.0.0
VITE_ENVIRONMENT=development
EOF
            print_success "Frontend .env file created."
        fi
    else
        print_warning "Frontend package.json not found. Skipping frontend setup."
    fi
    
    cd ..
else
    print_warning "Node.js not available. Skipping frontend setup."
fi

# Setup Docker if available
if [ "$DOCKER_AVAILABLE" = true ]; then
    print_status "Setting up Docker configuration..."
    cd deployment/docker
    
    # Create .env file for Docker
    if [ ! -f .env ]; then
        print_status "Creating Docker .env file..."
        cat > .env << EOF
# Docker Environment Variables
SECRET_KEY=verocta-docker-secret-key-2024
JWT_SECRET_KEY=verocta-docker-jwt-secret-key-2024
OPENAI_API_KEY=your-openai-api-key-here
SUPABASE_URL=your-supabase-url-here
SUPABASE_PASSWORD=your-supabase-password-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here
CUSTOM_DOMAIN=your-domain.com
REDIS_URL=redis://redis:6379/0
POSTGRES_DB=verocta
POSTGRES_USER=verocta
POSTGRES_PASSWORD=verocta_password
EOF
        print_success "Docker .env file created."
    fi
    
    cd ../..
else
    print_warning "Docker not available. Skipping Docker setup."
fi

# Create additional directories
print_status "Creating additional directories..."
mkdir -p docs/api docs/deployment docs/integration docs/architecture docs/user-guide docs/developer-guide
mkdir -p monitoring/logging monitoring/metrics monitoring/alerts
mkdir -p assets/logos assets/images assets/templates
mkdir -p configs/environments configs/secrets configs/templates

# Set up pre-commit hooks
print_status "Setting up pre-commit hooks..."
cd backend
if [ -f requirements.txt ] && grep -q "pre-commit" requirements.txt; then
    pip install pre-commit
    pre-commit install
    print_success "Pre-commit hooks installed."
else
    print_warning "Pre-commit not found in requirements. Skipping pre-commit setup."
fi
cd ..

# Run initial tests
print_status "Running initial tests..."
cd backend
if command -v pytest &> /dev/null; then
    pytest tests/unit/ -v --tb=short
    print_success "Initial tests completed."
else
    print_warning "pytest not found. Skipping tests."
fi
cd ..

echo ""
print_success "🎉 Enterprise setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Run the backend: cd backend && python main.py"
echo "3. (Optional) Run the frontend: cd frontend && npm run dev"
echo "4. (Optional) Run with Docker: cd deployment/docker && docker-compose up -d"
echo ""
echo "🔗 Services will be available at:"
echo "   Backend API: http://localhost:5000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:5000/api/docs"
echo "   Health Check: http://localhost:5000/api/health"
echo ""
echo "📚 Documentation:"
echo "   Main README: ./README.md"
echo "   Enterprise Summary: ./ENTERPRISE_RESTRUCTURE_SUMMARY.md"
echo "   API Docs: ./docs/api/"
echo "   Deployment: ./docs/deployment/"
echo ""
echo "🧪 Testing:"
echo "   Unit Tests: cd backend && pytest tests/unit/"
echo "   Integration Tests: cd backend && pytest tests/integration/"
echo "   E2E Tests: cd backend && pytest tests/e2e/"
echo ""
echo "🚀 Happy coding with VeroctaAI Enterprise! 🚀"
