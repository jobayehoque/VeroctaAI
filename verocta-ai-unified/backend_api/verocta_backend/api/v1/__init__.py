"""
API v1 Blueprint
RESTful API endpoints for VeroctaAI financial intelligence platform
"""

from flask import Blueprint, jsonify

# Create the v1 API blueprint
api_v1_bp = Blueprint('api_v1', __name__)

# Import all route modules to register them with the blueprint
from . import auth, analytics, reports, uploads, users

# API v1 info endpoint
@api_v1_bp.route('/')
def api_info():
    """API v1 information"""
    return jsonify({
        'name': 'VeroctaAI API',
        'version': '1.0',
        'description': 'AI-powered financial intelligence and analytics API',
        'endpoints': {
            '/auth': 'Authentication endpoints',
            '/analytics': 'Financial analytics and spend score',
            '/reports': 'Report generation and management',
            '/uploads': 'CSV file upload and processing',
            '/users': 'User management'
        }
    })

@api_v1_bp.route('/health')
def health():
    """API v1 health check"""
    return jsonify({'status': 'healthy', 'version': '1.0'})

__all__ = ['api_v1_bp']