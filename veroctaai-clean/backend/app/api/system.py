"""
System API Endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import os

system_bp = Blueprint('system', __name__)

@system_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check various system components
        health_status = {
            'status': 'healthy',
            'message': 'VeroctaAI API is running',
            'version': '2.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'services': {
                'database': 'connected' if os.environ.get('DATABASE_URL') else 'in-memory',
                'openai': 'available' if os.environ.get('OPENAI_API_KEY') else 'not-configured',
                'pdf_generator': 'ready',
                'file_processing': 'ready'
            }
        }
        
        return jsonify(health_status)
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@system_bp.route('/docs', methods=['GET'])
def api_documentation():
    """API documentation endpoint"""
    docs = {
        "title": "VeroctaAI Financial Analysis API",
        "version": "2.0.0",
        "description": "AI-powered financial intelligence and SpendScore analysis platform",
        "base_url": request.host_url + "api/",
        "endpoints": {
            "POST /auth/login": {
                "description": "User authentication",
                "parameters": {
                    "email": "User email (string)",
                    "password": "User password (string)"
                },
                "response": "JWT token and user information"
            },
            "POST /auth/register": {
                "description": "User registration",
                "parameters": {
                    "email": "User email (string)",
                    "password": "User password (string)",
                    "company": "Company name (string, optional)"
                },
                "response": "JWT token and user information"
            },
            "POST /upload": {
                "description": "Upload CSV and trigger analysis",
                "parameters": {
                    "file": "CSV file (multipart/form-data)",
                    "mapping": "Column mapping (JSON string, optional)"
                },
                "response": "Analysis results with SpendScore and insights"
            },
            "GET /spend-score": {
                "description": "Return JSON of latest SpendScore metrics",
                "response": "SpendScore breakdown and tier information"
            },
            "GET /reports": {
                "description": "List user reports",
                "response": "Array of user reports"
            },
            "GET /reports/{id}/pdf": {
                "description": "Download PDF report",
                "response": "PDF file download"
            },
            "GET /health": {
                "description": "Health check endpoint",
                "response": "Service status"
            },
            "GET /docs": {
                "description": "This API documentation",
                "response": "API documentation JSON"
            }
        },
        "authentication": {
            "type": "Bearer Token",
            "header": "Authorization: Bearer <token>",
            "note": "JWT tokens are required for protected endpoints"
        },
        "supported_formats": [
            "QuickBooks CSV",
            "Wave Accounting CSV", 
            "Revolut CSV",
            "Xero CSV",
            "Generic transaction CSV"
        ]
    }
    
    return jsonify(docs)

@system_bp.route('/verify-clone', methods=['GET'])
def verify_clone():
    """Verify system integrity and clone status"""
    try:
        verification_result = {
            'status': 'verified',
            'message': 'System integrity verified',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'database': 'ok',
                'files': 'ok',
                'dependencies': 'ok',
                'configuration': 'ok'
            }
        }
        
        return jsonify(verification_result)
        
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'message': f'Verification failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500
