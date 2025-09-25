"""
Google Sheets Integration Service for VeroctaAI
Handles Google Sheets API integration for data import/export
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False
    logging.warning("Google APIs not installed. Install with: pip install google-api-python-client google-auth-oauthlib")

class GoogleSheetsService:
    """Google Sheets service for data integration"""
    
    def __init__(self):
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')
        self.client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
        
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        self.service = None
        self.enabled = GOOGLE_APIS_AVAILABLE and bool(self.client_id and self.client_secret)
        
        if not self.enabled:
            logging.warning("Google Sheets integration not configured - using demo mode")
    
    def get_auth_url(self, state: str = None) -> str:
        """Get Google OAuth authorization URL"""
        if not self.enabled:
            return "https://demo.google.com/auth?state=demo"
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state
            )
            
            return auth_url
        except Exception as e:
            logging.error(f"Error generating auth URL: {str(e)}")
            return ""
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Exchange authorization code for access token"""
        if not self.enabled:
            return self._demo_token()
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            flow.fetch_token(code=code)
            
            return {
                'access_token': flow.credentials.token,
                'refresh_token': flow.credentials.refresh_token,
                'expires_at': flow.credentials.expiry.isoformat() if flow.credentials.expiry else None
            }
        except Exception as e:
            logging.error(f"Error exchanging code for token: {str(e)}")
            return None
    
    def initialize_service(self, credentials: Dict) -> bool:
        """Initialize Google Sheets service with credentials"""
        if not self.enabled:
            self.service = "demo_service"
            return True
        
        try:
            creds = Credentials.from_authorized_user_info(credentials, self.scopes)
            self.service = build('sheets', 'v4', credentials=creds)
            return True
        except Exception as e:
            logging.error(f"Error initializing service: {str(e)}")
            return False
    
    def get_spreadsheet_data(self, spreadsheet_id: str, range_name: str = None) -> Optional[List[List]]:
        """Get data from Google Spreadsheet"""
        if not self.service or self.service == "demo_service":
            return self._demo_spreadsheet_data()
        
        try:
            if not range_name:
                range_name = 'Sheet1!A:Z'
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
        except HttpError as e:
            logging.error(f"Error getting spreadsheet data: {str(e)}")
            return None
    
    def write_to_spreadsheet(self, spreadsheet_id: str, range_name: str, values: List[List]) -> bool:
        """Write data to Google Spreadsheet"""
        if not self.service or self.service == "demo_service":
            logging.info(f"Demo: Writing {len(values)} rows to spreadsheet")
            return True
        
        try:
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return result.get('updatedCells', 0) > 0
        except HttpError as e:
            logging.error(f"Error writing to spreadsheet: {str(e)}")
            return False
    
    def create_spreadsheet(self, title: str) -> Optional[Dict]:
        """Create new Google Spreadsheet"""
        if not self.service or self.service == "demo_service":
            return self._demo_spreadsheet(title)
        
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [{
                    'properties': {
                        'title': 'Financial Data'
                    }
                }]
            }
            
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            return result
        except HttpError as e:
            logging.error(f"Error creating spreadsheet: {str(e)}")
            return None
    
    def get_user_spreadsheets(self) -> List[Dict]:
        """Get list of user's spreadsheets"""
        if not self.service or self.service == "demo_service":
            return self._demo_user_spreadsheets()
        
        try:
            # This would require Drive API integration
            # For now, return demo data
            return self._demo_user_spreadsheets()
        except Exception as e:
            logging.error(f"Error getting user spreadsheets: {str(e)}")
            return []
    
    def export_financial_data(self, spreadsheet_id: str, financial_data: Dict) -> bool:
        """Export financial analysis data to Google Sheets"""
        if not self.service or self.service == "demo_service":
            logging.info("Demo: Exporting financial data to Google Sheets")
            return True
        
        try:
            # Prepare data for export
            export_data = self._prepare_export_data(financial_data)
            
            # Write to spreadsheet
            return self.write_to_spreadsheet(
                spreadsheet_id, 
                'Financial Analysis!A1', 
                export_data
            )
        except Exception as e:
            logging.error(f"Error exporting financial data: {str(e)}")
            return False
    
    def import_financial_data(self, spreadsheet_id: str, range_name: str = None) -> Optional[pd.DataFrame]:
        """Import financial data from Google Sheets as DataFrame"""
        if not self.service or self.service == "demo_service":
            return self._demo_financial_dataframe()
        
        try:
            data = self.get_spreadsheet_data(spreadsheet_id, range_name)
            if not data:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
        except Exception as e:
            logging.error(f"Error importing financial data: {str(e)}")
            return None
    
    def _prepare_export_data(self, financial_data: Dict) -> List[List]:
        """Prepare financial data for Google Sheets export"""
        export_data = [
            ['Financial Analysis Report', ''],
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            [''],
            ['SpendScore', financial_data.get('spend_score', 0)],
            ['Total Amount', financial_data.get('total_amount', 0)],
            ['Transaction Count', financial_data.get('transaction_count', 0)],
            [''],
            ['Category Breakdown', 'Amount'],
        ]
        
        # Add category data
        categories = financial_data.get('categories', {})
        for category, amount in categories.items():
            export_data.append([category, amount])
        
        return export_data
    
    def _demo_token(self) -> Dict:
        """Demo token for testing"""
        return {
            'access_token': 'demo_access_token',
            'refresh_token': 'demo_refresh_token',
            'expires_at': (datetime.now().timestamp() + 3600)
        }
    
    def _demo_spreadsheet_data(self) -> List[List]:
        """Demo spreadsheet data for testing"""
        return [
            ['Date', 'Description', 'Amount', 'Category'],
            ['2024-01-01', 'Office Supplies', '150.00', 'Office'],
            ['2024-01-02', 'Software License', '99.00', 'Software'],
            ['2024-01-03', 'Marketing Campaign', '500.00', 'Marketing']
        ]
    
    def _demo_spreadsheet(self, title: str) -> Dict:
        """Demo spreadsheet for testing"""
        return {
            'spreadsheetId': f'demo_spreadsheet_{int(datetime.now().timestamp())}',
            'properties': {'title': title},
            'spreadsheetUrl': f'https://docs.google.com/spreadsheets/d/demo_spreadsheet_{int(datetime.now().timestamp())}'
        }
    
    def _demo_user_spreadsheets(self) -> List[Dict]:
        """Demo user spreadsheets for testing"""
        return [
            {
                'id': 'demo_sheet_1',
                'name': 'Financial Data 2024',
                'createdTime': '2024-01-01T00:00:00Z',
                'modifiedTime': '2024-01-15T10:30:00Z'
            },
            {
                'id': 'demo_sheet_2',
                'name': 'Expense Tracking',
                'createdTime': '2024-01-10T00:00:00Z',
                'modifiedTime': '2024-01-20T15:45:00Z'
            }
        ]
    
    def _demo_financial_dataframe(self) -> pd.DataFrame:
        """Demo financial DataFrame for testing"""
        data = {
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Description': ['Office Supplies', 'Software License', 'Marketing Campaign'],
            'Amount': [150.00, 99.00, 500.00],
            'Category': ['Office', 'Software', 'Marketing']
        }
        return pd.DataFrame(data)

# Global Google Sheets service instance
google_sheets_service = GoogleSheetsService()
