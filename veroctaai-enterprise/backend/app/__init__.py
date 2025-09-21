"""
VeroctaAI Enterprise Backend Application
AI-Powered Financial Intelligence Platform
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import logging
import secrets
from datetime import timedelta

def create_app(config_name=None):
    """Application factory pattern with environment-based configuration"""
    app = Flask(__name__)
    
    # Load configuration
    configure_app(app, config_name)
    
    # Configure logging
    configure_logging(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def configure_app(app, config_name=None):
    """Configure Flask application based on environment"""
    # Determine configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    
    # Load environment-specific configuration
    if config_name == 'production':
        app.config.from_object('config.production.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.testing.TestingConfig')
    else:
        app.config.from_object('config.development.DevelopmentConfig')
    
    # Override with environment variables
    app.config.update({
        'SECRET_KEY': os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32),
        'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=24),
        'UPLOAD_FOLDER': os.environ.get('UPLOAD_FOLDER', 'uploads'),
        'MAX_CONTENT_LENGTH': int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)),
        'DATABASE_URL': os.environ.get('DATABASE_URL'),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY'),
        'SUPABASE_URL': os.environ.get('SUPABASE_URL'),
        'SUPABASE_PASSWORD': os.environ.get('SUPABASE_PASSWORD'),
        'SUPABASE_ANON_KEY': os.environ.get('SUPABASE_ANON_KEY'),
    })
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

def configure_logging(app):
    """Configure application logging"""
    log_level = logging.INFO if app.config.get('FLASK_ENV') == 'production' else logging.DEBUG
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler (production only)
    handlers = [console_handler]
    if app.config.get('FLASK_ENV') == 'production':
        file_handler = logging.FileHandler('logs/verocta.log')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=log_level,
        handlers=handlers
    )

def init_extensions(app):
    """Initialize Flask extensions"""
    # CORS configuration
    allowed_origins = app.config.get('CORS_ORIGINS', [
        "http://localhost:3000",
        "http://localhost:5000",
        "https://veroctaai.onrender.com",
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.netlify.app"
    ])
    
    custom_domain = os.environ.get("CUSTOM_DOMAIN")
    if custom_domain:
        allowed_origins.extend([f"https://{custom_domain}", f"http://{custom_domain}"])
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True
        }
    })
    
    # JWT configuration
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token is required'}, 401
    
    return jwt

def register_blueprints(app):
    """Register application blueprints"""
    from app.api.auth import auth_bp
    from app.api.analysis import analysis_bp
    from app.api.reports import reports_bp
    from app.api.system import system_bp
    from app.api.admin import admin_bp
    
    # API blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Root route
    @app.route('/')
    def index():
        return {
            'message': 'VeroctaAI Enterprise API',
            'version': '2.0.0',
            'status': 'running',
            'docs': '/api/docs',
            'health': '/api/health'
        }

def register_error_handlers(app):
    """Register error handlers"""
    from utils.exceptions import APIException
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        return {'error': error.message, 'code': error.code}, error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return {'error': 'Resource not found', 'code': 'NOT_FOUND'}, 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        return {'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}, 500

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
