"""
Unit Tests for Authentication
"""

import pytest
from unittest.mock import patch, MagicMock
from core.auth import AuthService
from app.api.auth.validators import AuthValidator

class TestAuthService:
    """Test cases for AuthService"""
    
    def test_hash_password(self):
        """Test password hashing"""
        auth_service = AuthService()
        password = "testpassword123"
        hashed = auth_service.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert auth_service.verify_password(password, hashed)
    
    def test_verify_password(self):
        """Test password verification"""
        auth_service = AuthService()
        password = "testpassword123"
        hashed = auth_service.hash_password(password)
        
        assert auth_service.verify_password(password, hashed)
        assert not auth_service.verify_password("wrongpassword", hashed)
    
    def test_create_user(self):
        """Test user creation"""
        auth_service = AuthService()
        
        # Test successful user creation
        user = auth_service.create_user(
            email="test@example.com",
            password="testpassword123",
            company="Test Company"
        )
        
        assert user is not None
        assert user['email'] == "test@example.com"
        assert user['company'] == "Test Company"
        assert user['role'] == "user"
    
    def test_create_duplicate_user(self):
        """Test duplicate user creation"""
        auth_service = AuthService()
        
        # Create first user
        auth_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        # Try to create duplicate user
        user = auth_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        assert user is None
    
    def test_validate_user(self):
        """Test user validation"""
        auth_service = AuthService()
        
        # Create user first
        auth_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        # Test valid credentials
        user = auth_service.validate_user("test@example.com", "testpassword123")
        assert user is not None
        assert user['email'] == "test@example.com"
        
        # Test invalid credentials
        user = auth_service.validate_user("test@example.com", "wrongpassword")
        assert user is None

class TestAuthValidator:
    """Test cases for AuthValidator"""
    
    def test_validate_registration_valid(self):
        """Test valid registration data"""
        validator = AuthValidator()
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'company': 'Test Company'
        }
        
        result = validator.validate_registration(data)
        assert result['valid'] is True
    
    def test_validate_registration_missing_email(self):
        """Test registration with missing email"""
        validator = AuthValidator()
        data = {
            'password': 'testpassword123'
        }
        
        result = validator.validate_registration(data)
        assert result['valid'] is False
        assert 'email' in result['message'].lower()
    
    def test_validate_registration_invalid_email(self):
        """Test registration with invalid email"""
        validator = AuthValidator()
        data = {
            'email': 'invalid-email',
            'password': 'testpassword123'
        }
        
        result = validator.validate_registration(data)
        assert result['valid'] is False
        assert 'invalid' in result['message'].lower()
    
    def test_validate_registration_weak_password(self):
        """Test registration with weak password"""
        validator = AuthValidator()
        data = {
            'email': 'test@example.com',
            'password': '123'
        }
        
        result = validator.validate_registration(data)
        assert result['valid'] is False
        assert 'password' in result['message'].lower()
    
    def test_validate_login_valid(self):
        """Test valid login data"""
        validator = AuthValidator()
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        result = validator.validate_login(data)
        assert result['valid'] is True
    
    def test_validate_password_change_valid(self):
        """Test valid password change data"""
        validator = AuthValidator()
        data = {
            'current_password': 'oldpassword123',
            'new_password': 'newpassword123'
        }
        
        result = validator.validate_password_change(data)
        assert result['valid'] is True
    
    def test_validate_password_change_same_passwords(self):
        """Test password change with same passwords"""
        validator = AuthValidator()
        data = {
            'current_password': 'password123',
            'new_password': 'password123'
        }
        
        result = validator.validate_password_change(data)
        assert result['valid'] is False
        assert 'different' in result['message'].lower()
