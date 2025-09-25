"""
Reports API Endpoints
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.auth import AuthService
from services.pdf_generator import PDFGeneratorService
import os
import random
from datetime import datetime

reports_bp = Blueprint('reports', __name__)
auth_service = AuthService()
pdf_service = PDFGeneratorService()

@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    """Get all reports for the current user"""
    try:
        email = get_jwt_identity()
        user = auth_service.get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Sample reports data
        reports = [
            {
                'id': 1,
                'title': 'Q1 2024 Financial Analysis',
                'spend_score': 85,
                'total_amount': 45000.00,
                'total_transactions': 150,
                'created_at': '2024-01-15T10:30:00Z',
                'filename': 'q1_2024_analysis.csv'
            },
            {
                'id': 2,
                'title': 'Monthly Expense Review',
                'spend_score': 92,
                'total_amount': 32000.00,
                'total_transactions': 89,
                'created_at': '2024-01-10T14:20:00Z',
                'filename': 'monthly_review.csv'
            }
        ]
        
        return jsonify({'reports': reports})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('', methods=['POST'])
@jwt_required()
def create_report():
    """Create a new report"""
    try:
        email = get_jwt_identity()
        user = auth_service.get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        title = data.get('title', f'Sample Report {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        # Generate sample report data
        spend_score = random.randint(60, 95)
        report = {
            'id': random.randint(1000, 9999),
            'title': title,
            'spend_score': spend_score,
            'total_amount': random.randint(25000, 150000),
            'total_transactions': random.randint(100, 800),
            'created_at': datetime.now().isoformat(),
            'filename': f'{title.lower().replace(" ", "_")}.csv'
        }
        
        return jsonify({'report': report}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>/pdf', methods=['GET'])
@jwt_required()
def download_report_pdf(report_id):
    """Download PDF report"""
    try:
        email = get_jwt_identity()
        user = auth_service.get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if PDF exists
        pdf_path = os.path.join('outputs', f'report_{report_id}.pdf')
        
        if not os.path.exists(pdf_path):
            # Generate sample PDF
            sample_data = {
                'spend_score': 82,
                'total_transactions': 350,
                'total_amount': 67500.00,
                'filename': 'Sample Financial Analysis',
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
                'score_color': 'Green'
            }
            
            pdf_path = pdf_service.generate_report_pdf(
                sample_data,
                transactions=[],
                company_name=user.get('company', 'VeroctaAI Demo')
            )
        
        return send_file(pdf_path, as_attachment=True, download_name=f'report_{report_id}.pdf')
        
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500
