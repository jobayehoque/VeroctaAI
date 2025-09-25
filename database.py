import os
import logging
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")

if supabase_url and supabase_key:
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        # Test the connection
        test_response = supabase.table('users').select('count').limit(1).execute()
        logging.info("✅ Supabase connection established and tested successfully")
    except Exception as e:
        logging.warning(f"⚠️ Supabase connection failed: {str(e)} - using fallback storage")
        supabase = None
else:
    supabase = None
    logging.warning("⚠️ Supabase credentials not found - using fallback storage")

class DatabaseService:
    """Database service for VeroctaAI using Supabase"""
    
    def __init__(self):
        self.connected = supabase is not None
        
    def create_tables_if_not_exist(self):
        """Create tables if they don't exist"""
        if not self.connected:
            logging.warning("Database not connected - skipping table creation")
            return
            
        try:
            # Create users table
            users_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                email VARCHAR UNIQUE NOT NULL,
                password_hash VARCHAR NOT NULL,
                role VARCHAR DEFAULT 'user',
                company VARCHAR,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                is_active BOOLEAN DEFAULT TRUE
            );
            """
            
            # Create reports table
            reports_sql = """
            CREATE TABLE IF NOT EXISTS reports (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR NOT NULL,
                company VARCHAR,
                spend_score INTEGER,
                data JSONB,
                insights JSONB,
                analysis JSONB,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                status VARCHAR DEFAULT 'completed'
            );
            """
            
            # Create insights table
            insights_sql = """
            CREATE TABLE IF NOT EXISTS insights (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                report_id UUID REFERENCES reports(id) ON DELETE CASCADE,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                ai_insights JSONB,
                recommendations JSONB,
                waste_percentage DECIMAL(5,2),
                duplicate_expenses INTEGER DEFAULT 0,
                spending_spikes INTEGER DEFAULT 0,
                savings_opportunities INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            
            # Note: These would be executed via Supabase dashboard or migration tool
            logging.info("Database schema ready")
            
        except Exception as e:
            logging.error(f"Error creating tables: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email from database"""
        if not self.connected:
            return None
            
        try:
            response = supabase.table('users').select('*').eq('email', email).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching user: {str(e)}")
            return None
    
    def create_user(self, email: str, password_hash: str, company: str = None, role: str = "user") -> Optional[Dict]:
        """Create new user in database"""
        if not self.connected:
            return None
            
        try:
            user_data = {
                'email': email,
                'password_hash': password_hash,
                'company': company or 'Default Company',
                'role': role,
                'is_active': True
            }
            
            response = supabase.table('users').insert(user_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            return None
    
    def create_report(self, user_id: str, title: str, company: str, data: Dict, 
                     spend_score: int = None, insights: Dict = None, analysis: Dict = None) -> Optional[Dict]:
        """Create new report in database"""
        if not self.connected:
            return None
            
        try:
            report_data = {
                'user_id': user_id,
                'title': title,
                'company': company,
                'spend_score': spend_score,
                'data': data,
                'insights': insights or {},
                'analysis': analysis or {},
                'status': 'completed'
            }
            
            response = supabase.table('reports').insert(report_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error creating report: {str(e)}")
            return None
    
    def get_user_reports(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user reports from database"""
        if not self.connected:
            return []
            
        try:
            response = supabase.table('reports').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logging.error(f"Error fetching reports: {str(e)}")
            return []
    
    def get_report_by_id(self, report_id: str, user_id: str = None) -> Optional[Dict]:
        """Get specific report by ID"""
        if not self.connected:
            return None
            
        try:
            query = supabase.table('reports').select('*').eq('id', report_id)
            if user_id:
                query = query.eq('user_id', user_id)
            
            response = query.execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching report: {str(e)}")
            return None
    
    def save_insights(self, report_id: str, user_id: str, ai_insights: Dict, 
                     recommendations: List[str], metrics: Dict) -> Optional[Dict]:
        """Save AI insights to database"""
        if not self.connected:
            return None
            
        try:
            insight_data = {
                'report_id': report_id,
                'user_id': user_id,
                'ai_insights': ai_insights,
                'recommendations': recommendations,
                'waste_percentage': metrics.get('waste_percentage', 0),
                'duplicate_expenses': metrics.get('duplicate_expenses', 0),
                'spending_spikes': metrics.get('spending_spikes', 0),
                'savings_opportunities': metrics.get('savings_opportunities', 0)
            }
            
            response = supabase.table('insights').insert(insight_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error saving insights: {str(e)}")
            return None
    
    def get_next_user_id(self) -> int:
        """Get next available user ID"""
        if not self.connected:
            return 1
            
        try:
            # Get the count of users to determine next ID
            response = supabase.table('users').select('id').execute()
            if response.data:
                return len(response.data) + 1
            return 1
        except Exception as e:
            logging.error(f"Error getting next user ID: {str(e)}")
            return 1
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID from database"""
        if not self.connected:
            return None
            
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching user by ID: {str(e)}")
            return None

    def delete_report(self, report_id: str, user_id: str) -> bool:
        """Delete a report by ID for a specific user"""
        if not self.connected:
            return False
            
        try:
            # Check if report exists and belongs to user
            response = supabase.table('reports').select('*').eq('id', report_id).eq('user_id', user_id).execute()
            if not response.data:
                return False
                
            # Delete the report
            delete_response = supabase.table('reports').delete().eq('id', report_id).eq('user_id', user_id).execute()
            return len(delete_response.data) > 0
            
        except Exception as e:
            logging.error(f"Error deleting report: {str(e)}")
            return False

    def get_dashboard_stats(self, user_id: str) -> Dict:
        """Get dashboard statistics for user"""
        if not self.connected:
            return {
                'total_reports': 0,
                'avg_spend_score': 0,
                'total_savings': 0,
                'avg_waste_percentage': 0
            }
            
        try:
            # Get reports count and average spend score
            reports_response = supabase.table('reports').select('spend_score, data').eq('user_id', user_id).execute()
            reports = reports_response.data or []
            
            total_reports = len(reports)
            avg_spend_score = sum(r.get('spend_score', 0) for r in reports) / max(total_reports, 1)
            
            # Calculate total savings (estimate 15% of total amount)
            total_amount = sum(r.get('data', {}).get('total_amount', 0) for r in reports)
            total_savings = total_amount * 0.15
            
            # Get insights for waste percentage
            insights_response = supabase.table('insights').select('waste_percentage').eq('user_id', user_id).execute()
            insights = insights_response.data or []
            avg_waste_percentage = sum(i.get('waste_percentage', 0) for i in insights) / max(len(insights), 1)
            
            return {
                'total_reports': total_reports,
                'avg_spend_score': int(avg_spend_score),
                'total_savings': int(total_savings),
                'avg_waste_percentage': round(avg_waste_percentage, 1)
            }
            
        except Exception as e:
            logging.error(f"Error fetching dashboard stats: {str(e)}")
            return {
                'total_reports': 0,
                'avg_spend_score': 0,
                'total_savings': 0,
                'avg_waste_percentage': 0
            }

# Global database service instance
db_service = DatabaseService()