"""
Configuration management for VeroctaAI Backend API
Environment-based configuration with secure defaults
"""

import os
from typing import Optional, List, Union
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    APP_NAME: str = "VeroctaAI Backend API"
    APP_VERSION: str = "3.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES: int = 2592000  # 30 days
    
    # Database
    DATABASE_URL: Optional[str] = None
    DB_ECHO: bool = False
    
    # Supabase (optional)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_PASSWORD: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # File Upload
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER: str = "uploads"
    OUTPUTS_FOLDER: str = "outputs"
    
    # CORS  
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Redis (for background tasks)
    REDIS_URL: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "1000 per hour"
    
    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def build_db_url(cls, v, info):
        if v:
            return v
        
        # Build from Supabase if available
        data = info.data if hasattr(info, 'data') else {}
        supabase_url = data.get('SUPABASE_URL')
        supabase_password = data.get('SUPABASE_PASSWORD')
        
        if supabase_url and supabase_password:
            import urllib.parse
            parsed_url = urllib.parse.urlparse(supabase_url)
            if parsed_url.netloc:
                host = f"db.{parsed_url.netloc}"
                return f"postgresql://postgres:{supabase_password}@{host}:5432/postgres"
        
        # Default to SQLite for development if no database configured
        return "sqlite:///instance/dev.db"
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DevelopmentSettings(Settings):
    """Development environment settings"""
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DB_ECHO: bool = True


class ProductionSettings(Settings):
    """Production environment settings"""
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    DB_ECHO: bool = False
    RATE_LIMIT_DEFAULT: str = "500 per hour"


class TestingSettings(Settings):
    """Testing environment settings"""
    ENVIRONMENT: str = "testing"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///:memory:"


@lru_cache()
def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()