"""
Reports API endpoints
Report management and PDF generation
"""

import os
from flask import jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import api_v1_bp
from ...models import User, Report
from ...core.database import db
from ...services.pdf_service import PDFGeneratorService


@api_v1_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    """
    Get all reports for current user
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get all reports for user
        reports = Report.query.filter_by(user_id=current_user_id).order_by(
            Report.created_at.desc()
        ).all()
        
        return jsonify({
            'reports': [report.to_dict() for report in reports],
            'total': len(reports)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get reports error: {str(e)}")
        return jsonify({'error': 'Failed to get reports'}), 500


@api_v1_bp.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """
    Get specific report by ID
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Include transactions if requested
        include_transactions = request.args.get('include_transactions', 'false').lower() == 'true'
        
        report_data = report.to_dict()
        
        if include_transactions and report.status == 'completed':
            transactions = report.transactions.all()
            report_data['transactions'] = [t.to_dict() for t in transactions]
        
        return jsonify({'report': report_data}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get report error: {str(e)}")
        return jsonify({'error': 'Failed to get report'}), 500


@api_v1_bp.route('/reports/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    """
    Delete specific report
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Delete PDF file if exists
        if report.pdf_path and os.path.exists(report.pdf_path):
            try:
                os.remove(report.pdf_path)
            except Exception:
                pass  # File cleanup is not critical
        
        # Delete company logo if exists
        if report.company_logo_path and os.path.exists(report.company_logo_path):
            try:
                os.remove(report.company_logo_path)
            except Exception:
                pass
        
        # Delete report (cascades to transactions and insights)
        db.session.delete(report)
        db.session.commit()
        
        return jsonify({'message': 'Report deleted successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Delete report error: {str(e)}")
        return jsonify({'error': 'Failed to delete report'}), 500


@api_v1_bp.route('/reports/<int:report_id>/pdf', methods=['GET'])
@jwt_required()
def download_pdf(report_id):
    """
    Download PDF report
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        if report.status != 'completed':
            return jsonify({'error': 'Report not completed yet'}), 400
        
        # Generate PDF if it doesn't exist
        if not report.pdf_path or not os.path.exists(report.pdf_path):
            pdf_service = PDFGeneratorService()
            pdf_path = pdf_service.generate_report_pdf(report_id)
            
            report.pdf_path = pdf_path
            db.session.commit()
        
        # Send file
        return send_file(
            report.pdf_path,
            as_attachment=True,
            download_name=f"financial_report_{report.id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f"Download PDF error: {str(e)}")
        return jsonify({'error': 'Failed to download PDF'}), 500


@api_v1_bp.route('/reports/<int:report_id>/regenerate', methods=['POST'])
@jwt_required()
def regenerate_report(report_id):
    """
    Regenerate analysis for existing report
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Update status to processing
        report.status = 'processing'
        report.error_message = None
        db.session.commit()
        
        # Regenerate analytics (this could be moved to background task)
        from ...services.analytics_service import AnalyticsService
        
        analytics_service = AnalyticsService()
        analytics_result = analytics_service.generate_report(report_id)
        
        # Update report with new results
        report.status = 'completed'
        report.completed_at = datetime.utcnow()
        report.spend_score = analytics_result.get('spend_score')
        report.score_tier = analytics_result.get('score_tier')
        report.metrics = analytics_result.get('metrics')
        
        # Clear old PDF
        if report.pdf_path and os.path.exists(report.pdf_path):
            try:
                os.remove(report.pdf_path)
                report.pdf_path = None
            except Exception:
                pass
        
        db.session.commit()
        
        return jsonify({
            'message': 'Report regenerated successfully',
            'report': report.to_dict(),
            'analytics': analytics_result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Regenerate report error: {str(e)}")
        report.status = 'failed'
        report.error_message = str(e)
        db.session.commit()
        return jsonify({'error': 'Failed to regenerate report'}), 500


@api_v1_bp.route('/reports/stats', methods=['GET'])
@jwt_required()
def get_reports_stats():
    """
    Get reports statistics for current user
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report counts by status
        from sqlalchemy import func
        
        stats = db.session.query(
            Report.status,
            func.count(Report.id)
        ).filter_by(user_id=current_user_id).group_by(Report.status).all()
        
        status_counts = {status: count for status, count in stats}
        
        return jsonify({
            'total_reports': sum(status_counts.values()),
            'completed': status_counts.get('completed', 0),
            'processing': status_counts.get('processing', 0),
            'failed': status_counts.get('failed', 0),
            'status_breakdown': status_counts
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get reports stats error: {str(e)}")
        return jsonify({'error': 'Failed to get reports statistics'}), 500