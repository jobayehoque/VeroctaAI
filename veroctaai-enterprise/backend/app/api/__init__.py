"""
API Package - Enterprise Level Organization
"""

from .auth import auth_bp
from .analysis import analysis_bp
from .reports import reports_bp
from .system import system_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'analysis_bp', 'reports_bp', 'system_bp', 'admin_bp']
