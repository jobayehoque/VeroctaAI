from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            docs = {
                "title": "VeroctaAI Financial Analysis API",
                "version": "2.0.0",
                "description": "AI-powered financial intelligence and SpendScore analysis platform - Vercel Serverless Edition",
                "platform": "Vercel Serverless Functions",
                "base_url": "https://your-app.vercel.app/api/",
                "endpoints": {
                    "GET /api/health": {
                        "description": "Health check endpoint",
                        "response": "Service status and platform information"
                    },
                    "POST /api/upload": {
                        "description": "Upload CSV and trigger analysis (simplified for serverless)",
                        "parameters": {
                            "file": "CSV file (multipart/form-data) or JSON data"
                        },
                        "response": "Analysis results with SpendScore and insights",
                        "note": "File processing simplified for serverless environment"
                    },
                    "GET /api/spend-score": {
                        "description": "Return JSON of latest SpendScore metrics",
                        "response": "SpendScore breakdown and tier information"
                    },
                    "GET /api/docs": {
                        "description": "This API documentation",
                        "response": "API documentation JSON"
                    }
                },
                "authentication": {
                    "type": "Bearer Token (Future)",
                    "header": "Authorization: Bearer <token>",
                    "note": "Authentication will be implemented in future versions"
                },
                "supported_formats": [
                    "QuickBooks CSV",
                    "Wave Accounting CSV", 
                    "Revolut CSV",
                    "Xero CSV",
                    "Generic transaction CSV"
                ],
                "limitations": {
                    "serverless": "Some features simplified for serverless environment",
                    "file_processing": "File upload processing adapted for Vercel",
                    "pdf_generation": "PDF generation disabled in serverless mode",
                    "database": "In-memory storage only (no persistence)"
                },
                "deployment": {
                    "platform": "Vercel",
                    "functions": "Serverless Python functions",
                    "frontend": "Static React build",
                    "scaling": "Automatic scaling with Vercel"
                }
            }

            self.send_success_response(docs)

        except Exception as e:
            self.send_error_response(500, f'Failed to get API docs: {str(e)}')

    def send_success_response(self, data):
        """Send successful response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

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
