"""
Analysis API Endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.analysis import AnalysisService
from core.file_processing import FileProcessingService
from utils.validators import validate_file_upload

analysis_bp = Blueprint('analysis', __name__)
analysis_service = AnalysisService()
file_service = FileProcessingService()

@analysis_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """Upload CSV file for analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        validation_error = validate_file_upload(file)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Get column mapping if provided
        mapping = request.form.get('mapping')
        if mapping:
            try:
                import json
                mapping = json.loads(mapping)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid mapping format'}), 400
        
        # Process file
        transactions = file_service.process_csv_file(file, mapping)
        if not transactions:
            return jsonify({'error': 'No valid transactions found in the CSV file'}), 400
        
        # Validate minimum transaction count
        if len(transactions) < 3:
            return jsonify({
                'error': f'Insufficient data for analysis. Found {len(transactions)} transactions, minimum 3 required.'
            }), 400
        
        # Perform analysis
        analysis_result = analysis_service.analyze_transactions(transactions)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'filename': file.filename,
            'transaction_count': len(transactions)
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@analysis_bp.route('/spend-score', methods=['GET'])
@jwt_required()
def get_spend_score():
    """Get SpendScore analysis"""
    try:
        # This would typically get the latest analysis for the user
        # For now, return a sample response
        return jsonify({
            'spend_score': 85,
            'score_breakdown': {
                'frequency_score': 80,
                'category_diversity': 75,
                'budget_adherence': 90,
                'redundancy_detection': 85,
                'spike_detection': 80,
                'waste_ratio': 90
            },
            'tier_info': {
                'color': 'Amber',
                'tier': 'Good',
                'green_reward_eligible': False,
                'description': 'Good financial habits with room for improvement'
            },
            'transaction_summary': {
                'total_transactions': 150,
                'total_amount': 45000.00,
                'median_amount': 250.00,
                'mean_amount': 300.00,
                'unique_categories': 8,
                'unique_vendors': 25
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
