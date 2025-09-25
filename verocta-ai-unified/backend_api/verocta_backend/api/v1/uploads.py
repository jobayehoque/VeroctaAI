"""
File upload API endpoints
CSV file upload and processing for financial analysis
"""

import os
from datetime import datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from marshmallow import Schema, fields, ValidationError

from . import api_v1_bp
from ...models import User, Report
from ...core.database import db
from ...services.csv_service import CSVProcessorService
from ...services.analytics_service import AnalyticsService


ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadSchema(Schema):
    """Upload request validation"""
    company_name = fields.String(required=False)
    file_format = fields.String(required=False)  # quickbooks, wave, revolut, xero, generic


@api_v1_bp.route('/uploads/csv', methods=['POST'])
@jwt_required()
def upload_csv():
    """
    Upload and process CSV file
    Creates analysis report with SpendScore and insights
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400
        
        # Validate form data
        form_data = request.form.to_dict()
        schema = UploadSchema()
        data = schema.load(form_data)
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Create report record
        report = Report(
            user_id=current_user_id,
            title=f"Financial Analysis - {filename}",
            description="Automated financial analysis from uploaded CSV",
            original_filename=filename,
            file_format=data.get('file_format', 'generic'),
            company_name=data.get('company_name'),
            status='processing'
        )
        db.session.add(report)
        db.session.commit()
        
        # Process CSV file (this could be moved to background task)
        try:
            csv_service = CSVProcessorService()
            transactions = csv_service.process_file(
                file_path, 
                report.id,
                file_format=report.file_format
            )
            
            if not transactions:
                report.status = 'failed'
                report.error_message = 'No valid transactions found in CSV file'
                db.session.commit()
                return jsonify({
                    'error': 'No valid transactions found',
                    'report_id': report.id
                }), 400
            
            # Generate analytics
            analytics_service = AnalyticsService()
            analytics_result = analytics_service.generate_report(report.id)
            
            # Update report with results
            report.status = 'completed'
            report.completed_at = datetime.utcnow()
            report.spend_score = analytics_result.get('spend_score')
            report.score_tier = analytics_result.get('score_tier')
            report.metrics = analytics_result.get('metrics')
            report.total_transactions = len(transactions)
            report.total_amount = sum(t.amount for t in transactions)
            
            if transactions:
                report.date_range_start = min(t.transaction_date for t in transactions)
                report.date_range_end = max(t.transaction_date for t in transactions)
            
            db.session.commit()
            
            # Clean up uploaded file
            try:
                os.remove(file_path)
            except Exception:
                pass  # File cleanup is not critical
            
            return jsonify({
                'message': 'File processed successfully',
                'report': report.to_dict(),
                'analytics': analytics_result
            }), 201
            
        except Exception as e:
            current_app.logger.error(f"CSV processing error: {str(e)}")
            report.status = 'failed'
            report.error_message = str(e)
            db.session.commit()
            
            return jsonify({
                'error': 'Failed to process CSV file',
                'report_id': report.id,
                'details': str(e)
            }), 500
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500


@api_v1_bp.route('/uploads/formats', methods=['GET'])
def get_supported_formats():
    """
    Get list of supported CSV formats
    """
    return jsonify({
        'supported_formats': [
            {
                'id': 'quickbooks',
                'name': 'QuickBooks CSV',
                'description': 'Standard QuickBooks transaction export'
            },
            {
                'id': 'wave',
                'name': 'Wave Accounting CSV',
                'description': 'Wave accounting transaction export'
            },
            {
                'id': 'revolut',
                'name': 'Revolut CSV',
                'description': 'Revolut transaction history export'
            },
            {
                'id': 'xero',
                'name': 'Xero CSV',
                'description': 'Xero accounting transaction export'
            },
            {
                'id': 'generic',
                'name': 'Generic CSV',
                'description': 'Generic transaction CSV with date, description, amount columns'
            }
        ]
    }), 200


@api_v1_bp.route('/uploads/requirements', methods=['GET'])
def get_upload_requirements():
    """
    Get file upload requirements and limits
    """
    return jsonify({
        'max_file_size': MAX_FILE_SIZE,
        'max_file_size_mb': MAX_FILE_SIZE / (1024 * 1024),
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'required_columns': {
            'generic': ['date', 'description', 'amount'],
            'quickbooks': ['Date', 'Description', 'Amount'],
            'wave': ['Date', 'Description', 'Amount'],
            'revolut': ['Started Date', 'Description', 'Amount'],
            'xero': ['Date', 'Description', 'Amount']
        }
    }), 200