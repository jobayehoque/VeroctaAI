"""
Authentication Service
"""

import bcrypt
from datetime import datetime
from typing import Dict, Optional
import logging

try:
    from services.database import DatabaseService
    db_service = DatabaseService()
except ImportError:
    db_service = None
    logging.warning("Database service not found. Using in-memory storage.")

class AuthService:
    """Authentication and user management service"""
    
    def __init__(self):
        # In-memory user storage (fallback)
        self.users_db = {
            "admin@verocta.ai": {
                "id": 1,
                "email": "admin@verocta.ai",
                "password": b'$2b$12$ZKOiYm4737YUelAqY2xLD.lx7PI8oTUFKZjjfZlmEK3Tzx.q0ZCpm',  # admin123
                "role": "admin",
                "created_at": datetime.now(),
                "company": "VeroctaAI",
                "is_active": True
            },
            "demo@verocta.ai": {
                "id": 2,
                "email": "demo@verocta.ai",
                "password": b'$2b$12$z2zF.Wlh3rF.rSqkaw2Bn.7rG/EbXsuChM/xSdneDmQlVDV6YqtSu',  # demo123
                "role": "user",
                "created_at": datetime.now(),
                "company": "VeroctaAI Demo",
                "is_active": True
            }
        }
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except Exception as e:
            logging.error(f"Password verification error: {e}")
            return False
    
    def create_user(self, email: str, password: str, company: str = None, role: str = "user") -> Optional[Dict]:
        """Create a new user"""
        try:
            # Check if user already exists
            if self.get_user_by_email(email):
                return None
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Create user data
            user_data = {
                "id": self._get_next_user_id(),
                "email": email,
                "password": hashed_password.encode('utf-8'),
                "role": role,
                "created_at": datetime.now(),
                "company": company or "Default Company",
                "is_active": True
            }
            
            # Try database first, fallback to in-memory
            if db_service and db_service.connected:
                try:
                    created_user = db_service.create_user(email, hashed_password, company, role)
                    if created_user:
                        user_data['id'] = created_user['id']
                        return user_data
                except Exception as e:
                    logging.error(f"Database user creation failed: {e}")
            
            # Fallback to in-memory storage
            self.users_db[email] = user_data
            return user_data
            
        except Exception as e:
            logging.error(f"User creation error: {e}")
            return None
    
    def validate_user(self, email: str, password: str) -> Optional[Dict]:
        """Validate user credentials"""
        try:
            # Try database first
            if db_service and db_service.connected:
                db_user = db_service.get_user_by_email(email)
                if db_user and db_user.get('password_hash'):
                    if self.verify_password(password, db_user['password_hash']):
                        return {
                            'id': db_user['id'],
                            'email': db_user['email'],
                            'role': db_user.get('role', 'user'),
                            'company': db_user.get('company', 'Default Company'),
                            'created_at': db_user.get('created_at', datetime.now()),
                            'is_active': db_user.get('is_active', True)
                        }
            
            # Fallback to in-memory storage
            user = self.users_db.get(email)
            if user and self.verify_password(password, user['password']):
                return {
                    'id': user['id'],
                    'email': user['email'],
                    'role': user['role'],
                    'company': user['company'],
                    'created_at': user['created_at'],
                    'is_active': user['is_active']
                }
            
            return None
            
        except Exception as e:
            logging.error(f"User validation error: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            # Try database first
            if db_service and db_service.connected:
                db_user = db_service.get_user_by_email(email)
                if db_user:
                    return {
                        'id': db_user['id'],
                        'email': db_user['email'],
                        'role': db_user.get('role', 'user'),
                        'company': db_user.get('company', 'Default Company'),
                        'created_at': db_user.get('created_at', datetime.now()),
                        'is_active': db_user.get('is_active', True)
                    }
            
            # Fallback to in-memory storage
            user = self.users_db.get(email)
            if user:
                return {
                    'id': user['id'],
                    'email': user['email'],
                    'role': user['role'],
                    'company': user['company'],
                    'created_at': user['created_at'],
                    'is_active': user['is_active']
                }
            
            return None
            
        except Exception as e:
            logging.error(f"User lookup error: {e}")
            return None
    
    def _get_next_user_id(self) -> int:
        """Get next available user ID"""
        if self.users_db:
            return max(user['id'] for user in self.users_db.values()) + 1
        return 1
