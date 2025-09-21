#!/bin/bash

# VeroctaAI Build Script for Render
# This script ensures proper build process for deployment

echo "🚀 Starting VeroctaAI build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build frontend
echo "🏗️ Building frontend..."
npm run build

# Return to root directory
cd ..

echo "✅ Build process complete!"
echo "🎯 Ready for deployment!"
