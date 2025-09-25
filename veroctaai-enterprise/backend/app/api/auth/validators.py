"""
Authentication Validators
"""

import re
from typing import Dict, Any
from utils.validators import validate_email, validate_password

class AuthValidator:
    """Authentication input validation"""
    
    def validate_registration(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user registration data"""
        if not isinstance(data, dict):
            return {'valid': False, 'message': 'Invalid request data'}
        
        # Required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'valid': False, 'message': f'{field.title()} is required'}
        
        # Email validation
        if not validate_email(data['email']):
            return {'valid': False, 'message': 'Invalid email format'}
        
        # Password validation
        if not validate_password(data['password']):
            return {'valid': False, 'message': 'Password must be at least 8 characters long'}
        
        # Company validation (optional)
        if 'company' in data and data['company']:
            if not isinstance(data['company'], str) or len(data['company'].strip()) < 2:
                return {'valid': False, 'message': 'Company name must be at least 2 characters'}
        
        # Role validation (optional)
        if 'role' in data and data['role']:
            valid_roles = ['user', 'admin']
            if data['role'] not in valid_roles:
                return {'valid': False, 'message': f'Role must be one of: {", ".join(valid_roles)}'}
        
        return {'valid': True}
    
    def validate_login(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user login data"""
        if not isinstance(data, dict):
            return {'valid': False, 'message': 'Invalid request data'}
        
        # Required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'valid': False, 'message': f'{field.title()} is required'}
        
        # Email validation
        if not validate_email(data['email']):
            return {'valid': False, 'message': 'Invalid email format'}
        
        # Password validation (basic check)
        if not isinstance(data['password'], str) or len(data['password']) < 1:
            return {'valid': False, 'message': 'Password is required'}
        
        return {'valid': True}
    
    def validate_password_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate password change data"""
        if not isinstance(data, dict):
            return {'valid': False, 'message': 'Invalid request data'}
        
        # Required fields
        required_fields = ['current_password', 'new_password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'valid': False, 'message': f'{field.replace("_", " ").title()} is required'}
        
        # Current password validation
        if not isinstance(data['current_password'], str) or len(data['current_password']) < 1:
            return {'valid': False, 'message': 'Current password is required'}
        
        # New password validation
        if not validate_password(data['new_password']):
            return {'valid': False, 'message': 'New password must be at least 8 characters long'}
        
        # Check if passwords are different
        if data['current_password'] == data['new_password']:
            return {'valid': False, 'message': 'New password must be different from current password'}
        
        return {'valid': True}
    
    def validate_email_format(self, email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        
        # Basic email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        if not password or not isinstance(password, str):
            return {'valid': False, 'message': 'Password is required'}
        
        if len(password) < 8:
            return {'valid': False, 'message': 'Password must be at least 8 characters long'}
        
        if len(password) > 128:
            return {'valid': False, 'message': 'Password must be less than 128 characters'}
        
        # Check for at least one letter and one number
        has_letter = re.search(r'[a-zA-Z]', password)
        has_number = re.search(r'[0-9]', password)
        
        if not has_letter:
            return {'valid': False, 'message': 'Password must contain at least one letter'}
        
        if not has_number:
            return {'valid': False, 'message': 'Password must contain at least one number'}
        
        return {'valid': True}
