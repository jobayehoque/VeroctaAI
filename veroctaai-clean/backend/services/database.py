"""
Database Service
"""

import os
import logging
from typing import Dict, Optional, List

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("Supabase library not installed. Database features will not work.")

class DatabaseService:
    """Database service for Supabase integration"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.connected = False
        
        if SUPABASE_AVAILABLE:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        try:
            supabase_url = os.environ.get('SUPABASE_URL')
            supabase_key = os.environ.get('SUPABASE_ANON_KEY')
            
            if supabase_url and supabase_key:
                self.client = create_client(supabase_url, supabase_key)
                self.connected = True
                logging.info("Supabase client initialized successfully")
            else:
                logging.warning("Supabase credentials not found")
                
        except Exception as e:
            logging.error(f"Failed to initialize Supabase client: {e}")
            self.connected = False
    
    def create_user(self, email: str, password_hash: str, company: str = None, role: str = "user") -> Optional[Dict]:
        """Create a new user in the database"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table('users').insert({
                'email': email,
                'password_hash': password_hash,
                'company': company or 'Default Company',
                'role': role,
                'is_active': True
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logging.error(f"Database user creation failed: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email from database"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logging.error(f"Database user lookup failed: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID from database"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logging.error(f"Database user lookup failed: {e}")
            return None
    
    def create_report(self, user_id: int, title: str, spend_score: int, total_amount: float, 
                     total_transactions: int, filename: str) -> Optional[Dict]:
        """Create a new report in the database"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table('reports').insert({
                'user_id': user_id,
                'title': title,
                'spend_score': spend_score,
                'total_amount': total_amount,
                'total_transactions': total_transactions,
                'filename': filename
            }).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logging.error(f"Database report creation failed: {e}")
            return None
    
    def get_reports_by_user(self, user_id: int) -> List[Dict]:
        """Get all reports for a user"""
        if not self.connected:
            return []
        
        try:
            result = self.client.table('reports').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            return result.data or []
            
        except Exception as e:
            logging.error(f"Database reports lookup failed: {e}")
            return []
    
    def get_report_by_id(self, report_id: int) -> Optional[Dict]:
        """Get report by ID"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table('reports').select('*').eq('id', report_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logging.error(f"Database report lookup failed: {e}")
            return None
    
    def delete_report(self, report_id: int) -> bool:
        """Delete a report"""
        if not self.connected:
            return False
        
        try:
            result = self.client.table('reports').delete().eq('id', report_id).execute()
            return True
            
        except Exception as e:
            logging.error(f"Database report deletion failed: {e}")
            return False
