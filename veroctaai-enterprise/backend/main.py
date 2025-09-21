"""
VeroctaAI Enterprise Backend Application Entry Point
"""

import os
from app import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = not is_production
    
    print('🚀 Starting VeroctaAI Enterprise API...')
    print(f'📍 URL: http://{host}:{port}')
    print('📊 Platform: AI-Powered Financial Intelligence & Analytics')
    print(f'🔧 Environment: {"Production" if is_production else "Development"}')
    print('🌐 Service Type: Enterprise Backend API')
    
    # Check services
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print('🤖 AI: GPT-4o Integration Ready ✅')
    else:
        print('⚠️  WARNING: OPENAI_API_KEY not set! AI features will not work.')
    
    if app.config.get("DATABASE_URL"):
        print('🗄️  Database: Supabase PostgreSQL Ready ✅')
    else:
        print('🗄️  Database: In-memory storage (no persistence)')
    
    print('📁 CSV Support: QuickBooks, Wave, Revolut, Xero')
    print('✅ Server starting...')
    
    app.run(host=host, port=port, debug=debug)
