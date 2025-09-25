"""
Global error handlers for the application
Provides consistent error responses across all endpoints
"""

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)


def init_error_handlers(app: Flask):
    """Initialize global error handlers"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors"""
        logger.warning(f"Validation error: {e.messages}")
        return jsonify({
            'error': 'Validation failed',
            'message': 'Invalid request data',
            'details': e.messages
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(e):
        """Handle database errors"""
        logger.error(f"Database error: {str(e)}")
        return jsonify({
            'error': 'Database error',
            'message': 'An error occurred while processing your request'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        """Handle HTTP exceptions"""
        logger.warning(f"HTTP error {e.code}: {e.description}")
        return jsonify({
            'error': e.name,
            'message': e.description,
            'status_code': e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        """Handle generic exceptions"""
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.before_request
    def log_request_info():
        """Log request information"""
        logger.info(f"{request.method} {request.url}")
    
    @app.after_request
    def log_response_info(response):
        """Log response information"""
        logger.info(f"Response: {response.status_code}")
        return response