"""
Production Configuration
"""

import os
from datetime import timedelta

class ProductionConfig:
    """Production environment configuration"""
    
    # Flask Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'csv'}
    
    # CORS Configuration
    CORS_ORIGINS = [
        "https://veroctaai.onrender.com",
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.netlify.app"
    ]
    
    # Add custom domain if provided
    custom_domain = os.environ.get("CUSTOM_DOMAIN")
    if custom_domain:
        CORS_ORIGINS.extend([f"https://{custom_domain}", f"http://{custom_domain}"])
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/verocta.log'
    
    # AI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o'
    OPENAI_MAX_TOKENS = 1000
    OPENAI_TEMPERATURE = 0.7
    
    # Supabase Configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_PASSWORD = os.environ.get('SUPABASE_PASSWORD')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Payment Configuration
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # Storage Configuration
    STORAGE_TYPE = os.environ.get('STORAGE_TYPE', 'local')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "1000 per hour"
    
    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Security Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance Configuration
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Monitoring Configuration
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    @staticmethod
    def init_app(app):
        """Initialize production-specific configurations"""
        # Configure Sentry for error tracking
        if ProductionConfig.SENTRY_DSN:
            try:
                import sentry_sdk
                from sentry_sdk.integrations.flask import FlaskIntegration
                sentry_sdk.init(
                    dsn=ProductionConfig.SENTRY_DSN,
                    integrations=[FlaskIntegration()],
                    traces_sample_rate=0.1
                )
            except ImportError:
                pass
