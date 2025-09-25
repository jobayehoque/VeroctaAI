"""
Testing Configuration
"""

import os
from datetime import timedelta

class TestingConfig:
    """Testing environment configuration"""
    
    # Flask Configuration
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    
    # JWT Configuration
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Database Configuration
    DATABASE_URL = 'sqlite:///:memory:'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'test_uploads'
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB for testing
    ALLOWED_EXTENSIONS = {'csv'}
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:3000"]
    
    # Logging Configuration
    LOG_LEVEL = 'WARNING'
    LOG_FILE = None  # Disable file logging in tests
    
    # AI Configuration
    OPENAI_API_KEY = 'test-openai-key'
    OPENAI_MODEL = 'gpt-4o'
    OPENAI_MAX_TOKENS = 100
    OPENAI_TEMPERATURE = 0.7
    
    # Supabase Configuration
    SUPABASE_URL = 'https://test.supabase.co'
    SUPABASE_PASSWORD = 'test-password'
    SUPABASE_ANON_KEY = 'test-anon-key'
    
    # Email Configuration
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    
    # Payment Configuration
    STRIPE_SECRET_KEY = 'sk_test_...'
    STRIPE_WEBHOOK_SECRET = 'whsec_test_...'
    
    # Storage Configuration
    STORAGE_TYPE = 'local'
    AWS_ACCESS_KEY_ID = 'test-access-key'
    AWS_SECRET_ACCESS_KEY = 'test-secret-key'
    AWS_S3_BUCKET = 'test-bucket'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = "1000 per hour"
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60
    
    # Security Configuration
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance Configuration
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Monitoring Configuration
    SENTRY_DSN = None
