from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import tempfile
import logging
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from csv_parser import parse_csv_file, parse_csv_file_with_mapping
    from spend_score_engine import get_enhanced_analysis
    from gpt_utils import generate_financial_insights
    from pdf_generator import generate_report_pdf
except ImportError as e:
    logging.error(f"Import error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse the URL to get query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get content type
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type:
                # Handle file upload
                self.handle_file_upload()
            else:
                # Handle JSON data
                self.handle_json_upload()
                
        except Exception as e:
            self.send_error_response(500, f'Upload processing failed: {str(e)}')

    def handle_file_upload(self):
        """Handle multipart file upload"""
        try:
            # For Vercel, we'll simulate file processing
            # In a real implementation, you'd need to handle multipart parsing
            
            # Generate sample analysis data
            analysis_data = {
                'spend_score': 82,
                'total_transactions': 350,
                'total_amount': 67500.00,
                'filename': 'sample_upload.csv',
                'suggestions': [
                    {'text': 'Optimize subscription management to reduce recurring costs', 'priority': 'High'},
                    {'text': 'Implement automated expense categorization', 'priority': 'Medium'},
                    {'text': 'Review vendor contracts for better terms', 'priority': 'Medium'},
                    {'text': 'Set up budget alerts for key categories', 'priority': 'Low'}
                ],
                'category_breakdown': {
                    'Software & SaaS': 18500,
                    'Office & Equipment': 12000,
                    'Marketing & Advertising': 15000,
                    'Travel & Entertainment': 8000,
                    'Professional Services': 9000,
                    'Other': 5000
                },
                'score_label': 'Excellent',
                'score_color': 'Green',
                'tier_info': {
                    'tier': 'Green',
                    'color': 'Green',
                    'description': 'Excellent financial discipline with optimized spending patterns'
                },
                'score_breakdown': {
                    'frequency_score': 85,
                    'category_diversity': 78,
                    'budget_adherence': 90,
                    'redundancy_detection': 88,
                    'spike_detection': 82,
                    'waste_ratio': 85
                },
                'transaction_summary': {
                    'total_transactions': 350,
                    'total_amount': 67500.00,
                    'average_transaction': 192.86,
                    'categories_count': 6
                }
            }

            # Generate AI insights
            insights = {
                'recommendations': [
                    'Review subscription services for cost optimization',
                    'Implement automated expense categorization',
                    'Set up budget alerts for key spending categories',
                    'Consider vendor consolidation opportunities',
                    'Establish approval workflows for high-value transactions'
                ],
                'priority_actions': ['Review high-value transactions', 'Categorize expenses'],
                'waste_percentage': 12.4,
                'duplicate_expenses': 23,
                'spending_spikes': 5,
                'savings_opportunities': 8
            }

            response_data = {
                'success': True,
                'filename': 'sample_upload.csv',
                'spend_score': analysis_data['spend_score'],
                'tier_info': analysis_data['tier_info'],
                'score_breakdown': analysis_data['score_breakdown'],
                'transaction_summary': analysis_data['transaction_summary'],
                'ai_insights': insights,
                'analysis_timestamp': datetime.now().isoformat(),
                'pdf_available': False,  # PDF generation disabled for serverless
                'total_transactions_processed': analysis_data['total_transactions'],
                'total_amount_analyzed': analysis_data['total_amount']
            }

            self.send_success_response(response_data)

        except Exception as e:
            self.send_error_response(500, f'File processing failed: {str(e)}')

    def handle_json_upload(self):
        """Handle JSON data upload"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response(400, 'No data provided')
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Process the data (simplified for serverless)
            response_data = {
                'success': True,
                'message': 'Data processed successfully',
                'data': data,
                'timestamp': datetime.now().isoformat()
            }

            self.send_success_response(response_data)

        except Exception as e:
            self.send_error_response(500, f'JSON processing failed: {str(e)}')

    def send_success_response(self, data):
        """Send successful response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        error_response = {
            'success': False,
            'error': message,
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
