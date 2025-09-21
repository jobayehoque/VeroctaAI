#!/bin/bash

# VeroctaAI Setup Script
# This script sets up the development environment

echo "🚀 Setting up VeroctaAI Development Environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads outputs logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << EOF
# VeroctaAI Environment Configuration
FLASK_ENV=development
SESSION_SECRET=verocta-local-development-secret-key-2024
HOST=127.0.0.1
PORT=5000

# OpenAI API (Optional - for AI features)
# OPENAI_API_KEY=your-openai-api-key-here

# Supabase Database (Optional - for data persistence)
# SUPABASE_URL=your-supabase-url-here
# SUPABASE_PASSWORD=your-supabase-password-here
# SUPABASE_ANON_KEY=your-supabase-anon-key-here

# Custom Domain (Optional)
# CUSTOM_DOMAIN=your-domain.com

# Security
JWT_SECRET_KEY=verocta-jwt-secret-key-2024

# Production Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# Logging
LOG_LEVEL=INFO
LOG_FILE=verocta.log
EOF
    echo "✅ .env file created. Please edit it with your configuration."
fi

cd ..

# Setup frontend if Node.js is available
if command -v node &> /dev/null; then
    echo "📦 Setting up frontend..."
    cd frontend
    
    # Check if package.json exists
    if [ -f package.json ]; then
        echo "📥 Installing frontend dependencies..."
        npm install
        
        # Create .env file for frontend
        if [ ! -f .env ]; then
            echo "⚙️ Creating frontend .env file..."
            cat > .env << EOF
# Frontend Environment Variables
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=2.0.0
EOF
            echo "✅ Frontend .env file created."
        fi
    else
        echo "⚠️ Frontend package.json not found. Skipping frontend setup."
    fi
    
    cd ..
else
    echo "⚠️ Node.js not found. Skipping frontend setup."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Run the backend: cd backend && python main.py"
echo "3. (Optional) Run the frontend: cd frontend && npm run dev"
echo ""
echo "🔗 API will be available at: http://localhost:5000"
echo "📚 Documentation: ./docs/README.md"
echo ""
echo "Happy coding! 🚀"
