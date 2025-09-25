"""
Application factory for VeroctaAI Backend API
Creates and configures Flask application instances
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import Settings
from .database import init_db
from ..middleware.error_handlers import init_error_handlers
from ..middleware.logging import init_logging
from ..api.v1 import api_v1_bp


def create_app(settings: Settings = None) -> Flask:
    """
    Application factory function
    Creates and configures Flask application
    """
    from .config import get_settings
    
    if settings is None:
        settings = get_settings()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRES,
        SQLALCHEMY_DATABASE_URI=settings.DATABASE_URL,
        SQLALCHEMY_ECHO=settings.DB_ECHO,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=settings.MAX_CONTENT_LENGTH,
    )
    
    # Initialize extensions
    init_extensions(app, settings)
    
    # Initialize error handlers and logging
    init_error_handlers(app)
    init_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'app': settings.APP_NAME,
            'version': settings.APP_VERSION,
            'environment': settings.ENVIRONMENT
        })
    
    return app


def init_extensions(app: Flask, settings: Settings):
    """Initialize Flask extensions"""
    
    # Database
    init_db(app)
    
    # CORS
    CORS(app, 
         origins=settings.CORS_ORIGINS,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'Accept'])
    
    # JWT
    jwt = JWTManager(app)
    
    # Configure JWT callbacks
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token required'}), 401
    
    # Rate Limiting
    if settings.RATE_LIMIT_ENABLED:
        limiter = Limiter(
            key_func=get_remote_address,
            default_limits=[settings.RATE_LIMIT_DEFAULT]
        )
        limiter.init_app(app)


def register_blueprints(app: Flask):
    """Register application blueprints"""
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')


def create_celery(app: Flask):
    """Create Celery instance for background tasks"""
    try:
        from celery import Celery
        
        celery = Celery(
            app.import_name,
            backend=app.config.get('CELERY_RESULT_BACKEND'),
            broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379')
        )
        celery.conf.update(app.config)
        
        class ContextTask(celery.Task):
            """Make celery tasks work with Flask app context"""
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
        return celery
        
    except ImportError:
        # Celery not installed, return None
        return None