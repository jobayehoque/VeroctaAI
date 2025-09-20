from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from spend_score_engine import get_score_label, get_score_color
except ImportError:
    # Fallback functions if imports fail
    def get_score_label(score):
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        else:
            return "Needs Improvement"
    
    def get_score_color(score):
        if score >= 90:
            return "Green"
        elif score >= 70:
            return "Amber"
        else:
            return "Red"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Generate sample spend score data
            spend_score = 82
            
            response_data = {
                'score': spend_score,
                'status': get_score_label(spend_score),
                'color': get_score_color(spend_score),
                'recommendations': [
                    'Review subscription services for cost optimization',
                    'Implement automated expense categorization',
                    'Set up budget alerts for key spending categories',
                    'Consider vendor consolidation opportunities',
                    'Establish approval workflows for high-value transactions'
                ],
                'report_id': 'sample-report-001',
                'created_at': datetime.now().isoformat(),
                'tier_info': {
                    'tier': 'Green',
                    'color': 'Green',
                    'description': 'Excellent financial discipline with optimized spending patterns',
                    'green_reward_eligible': True
                },
                'score_breakdown': {
                    'frequency_score': 85,
                    'category_diversity': 78,
                    'budget_adherence': 90,
                    'redundancy_detection': 88,
                    'spike_detection': 82,
                    'waste_ratio': 85
                },
                'insights': {
                    'waste_percentage': 12.4,
                    'duplicate_expenses': 23,
                    'spending_spikes': 5,
                    'savings_opportunities': 8
                }
            }

            self.send_success_response(response_data)

        except Exception as e:
            self.send_error_response(500, f'Failed to get spend score: {str(e)}')

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
