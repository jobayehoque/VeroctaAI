"""
VeroctaAI Backend API - Main Application Entry Point
Modern Flask-based financial intelligence platform API
"""

import os
from verocta_backend.core.app_factory import create_app
from verocta_backend.core.config import get_settings


# Create Flask application
app = create_app()


if __name__ == '__main__':
    settings = get_settings()
    
    print('🚀 Starting VeroctaAI Backend API...')
    print(f'📍 URL: http://{settings.HOST}:{settings.PORT}')
    print('📊 Platform: AI-Powered Financial Intelligence API')
    print(f'🔧 Environment: {settings.ENVIRONMENT.title()}')
    print(f'🗄️  Database: {"Connected" if settings.DATABASE_URL else "In-memory storage"}')
    
    # Check OpenAI API key
    if settings.OPENAI_API_KEY:
        print('🤖 AI: OpenAI Integration Ready ✅')
    else:
        print('⚠️  AI: OpenAI API key not set (AI features disabled)')
    
    print('📡 API Endpoints:')
    print('   GET  /health - Health check')
    print('   GET  /api/v1 - API information')
    print('   POST /api/v1/auth/login - User authentication')
    print('   POST /api/v1/uploads/csv - CSV file upload and analysis')
    print('   GET  /api/v1/reports - Financial reports')
    print('   GET  /api/v1/analytics/spend-score/<id> - SpendScore analysis')
    print('✅ Server starting...')
    
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )