"""
VeroctaAI Backend Application
AI-Powered Financial Intelligence Platform
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import logging
import secrets

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configure logging
    configure_logging(app)
    
    # Load configuration
    configure_app(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app

def configure_logging(app):
    """Configure application logging"""
    log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('verocta.log') if os.environ.get('FLASK_ENV') == 'production' else logging.NullHandler()
        ]
    )

def configure_app(app):
    """Configure Flask application"""
    # Secret key configuration
    session_secret = os.environ.get("SESSION_SECRET")
    if not session_secret:
        session_secret = secrets.token_hex(32)
        logging.warning("SESSION_SECRET not found, using generated fallback secret")
    
    app.secret_key = session_secret
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', session_secret)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire for now
    
    # Upload configuration
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Database configuration
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('outputs', exist_ok=True)

def init_extensions(app):
    """Initialize Flask extensions"""
    # CORS configuration
    allowed_origins = [
        "http://localhost:5000", 
        "http://127.0.0.1:5000",
        "http://localhost:3000",
        "https://veroctaai.onrender.com",
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.netlify.app"
    ]
    
    custom_domain = os.environ.get("CUSTOM_DOMAIN")
    if custom_domain:
        allowed_origins.extend([f"https://{custom_domain}", f"http://{custom_domain}"])
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"]
        }
    })
    
    # JWT configuration
    jwt = JWTManager(app)
    
    return jwt

def register_blueprints(app):
    """Register application blueprints"""
    from app.api import auth_bp, analysis_bp, reports_bp, system_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(system_bp, url_prefix='/api')

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Production configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = not is_production
    
    print('🚀 Starting VeroctaAI API Service...')
    print(f'📍 URL: http://{host}:{port}')
    print('📊 Platform: AI-Powered Financial Intelligence & Analytics API')
    print(f'🔧 Environment: {"Production" if is_production else "Development"}')
    print('🌐 Service Type: Backend API Only')
    
    # Check OpenAI API key
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print('🤖 AI: GPT-4o Integration Ready ✅')
    else:
        print('⚠️  WARNING: OPENAI_API_KEY not set! AI features will not work.')
    
    # Check database connection
    if app.config.get("DATABASE_URL"):
        print('🗄️  Database: Supabase PostgreSQL Ready ✅')
    else:
        print('🗄️  Database: In-memory storage (no persistence)')
    
    print('📁 CSV Support: QuickBooks, Wave, Revolut, Xero')
    print('✅ Server starting...')
    
    app.run(host=host, port=port, debug=debug)
