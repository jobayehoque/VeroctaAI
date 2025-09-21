"""
Authentication Controllers
"""

import logging
from typing import Dict, Any, Optional
from core.auth import AuthService
from utils.exceptions import APIException

class AuthController:
    """Authentication controller for handling auth business logic"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def register_user(self, email: str, password: str, company: str = None, role: str = "user") -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = self.auth_service.get_user_by_email(email)
            if existing_user:
                return {
                    'success': False,
                    'message': 'User already exists',
                    'status_code': 409
                }
            
            # Create user
            user = self.auth_service.create_user(email, password, company, role)
            if not user:
                return {
                    'success': False,
                    'message': 'Failed to create user',
                    'status_code': 500
                }
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'company': user['company'],
                    'role': user['role'],
                    'created_at': user['created_at'].isoformat() if user.get('created_at') else None
                }
            }
            
        except Exception as e:
            logging.error(f"User registration error: {e}")
            return {
                'success': False,
                'message': 'Registration failed',
                'status_code': 500
            }
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user credentials"""
        try:
            user = self.auth_service.validate_user(email, password)
            if not user:
                return {
                    'success': False,
                    'message': 'Invalid credentials',
                    'status_code': 401
                }
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'company': user['company'],
                    'role': user['role'],
                    'created_at': user['created_at'].isoformat() if user.get('created_at') else None
                }
            }
            
        except Exception as e:
            logging.error(f"User authentication error: {e}")
            return {
                'success': False,
                'message': 'Authentication failed',
                'status_code': 500
            }
    
    def get_user_profile(self, email: str) -> Dict[str, Any]:
        """Get user profile by email"""
        try:
            user = self.auth_service.get_user_by_email(email)
            if not user:
                return {
                    'success': False,
                    'message': 'User not found',
                    'status_code': 404
                }
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'company': user['company'],
                    'role': user['role'],
                    'created_at': user['created_at'].isoformat() if user.get('created_at') else None,
                    'is_active': user.get('is_active', True)
                }
            }
            
        except Exception as e:
            logging.error(f"Get user profile error: {e}")
            return {
                'success': False,
                'message': 'Failed to retrieve user profile',
                'status_code': 500
            }
    
    def change_password(self, email: str, current_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        try:
            # Verify current password
            user = self.auth_service.validate_user(email, current_password)
            if not user:
                return {
                    'success': False,
                    'message': 'Current password is incorrect',
                    'status_code': 400
                }
            
            # Update password
            success = self.auth_service.update_password(email, new_password)
            if not success:
                return {
                    'success': False,
                    'message': 'Failed to update password',
                    'status_code': 500
                }
            
            return {
                'success': True,
                'message': 'Password updated successfully'
            }
            
        except Exception as e:
            logging.error(f"Change password error: {e}")
            return {
                'success': False,
                'message': 'Password change failed',
                'status_code': 500
            }
