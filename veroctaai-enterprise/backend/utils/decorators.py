"""
Utility Decorators
"""

import functools
import logging
from flask import request, jsonify
from typing import Callable, Any

def validate_json(func: Callable) -> Callable:
    """Decorator to validate JSON request data"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        if not request.get_json():
            return jsonify({'error': 'Request body must contain valid JSON'}), 400
        
        return func(*args, **kwargs)
    return wrapper

def handle_errors(func: Callable) -> Callable:
    """Decorator to handle common errors"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"ValueError in {func.__name__}: {e}")
            return jsonify({'error': 'Invalid input data'}), 400
        except KeyError as e:
            logging.error(f"KeyError in {func.__name__}: {e}")
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            logging.error(f"Unexpected error in {func.__name__}: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper

def log_request(func: Callable) -> Callable:
    """Decorator to log API requests"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"API Request: {request.method} {request.path} from {request.remote_addr}")
        response = func(*args, **kwargs)
        logging.info(f"API Response: {response[1] if isinstance(response, tuple) else 200}")
        return response
    return wrapper

def rate_limit(limit: int = 100, per: int = 3600):
    """Decorator for rate limiting (simplified version)"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, you'd use Redis or similar
            # For now, this is a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_permissions(permissions: list):
    """Decorator to require specific permissions"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, you'd check user permissions
            # For now, this is a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_response(timeout: int = 300):
    """Decorator to cache response (simplified version)"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, you'd use Redis or similar
            # For now, this is a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator
