"""
Analytics API endpoints
SpendScore calculation and financial insights
"""

from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import api_v1_bp
from ...models import User, Report
from ...services.analytics_service import AnalyticsService


@api_v1_bp.route('/analytics/spend-score/<int:report_id>', methods=['GET'])
@jwt_required()
def get_spend_score(report_id):
    """
    Get SpendScore for specific report
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        if report.status != 'completed':
            return jsonify({
                'error': 'Report not completed',
                'status': report.status
            }), 400
        
        return jsonify({
            'report_id': report.id,
            'spend_score': report.spend_score,
            'score_tier': report.score_tier,
            'metrics': report.metrics,
            'total_transactions': report.total_transactions,
            'total_amount': report.total_amount,
            'date_range': {
                'start': report.date_range_start.isoformat() if report.date_range_start else None,
                'end': report.date_range_end.isoformat() if report.date_range_end else None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get spend score error: {str(e)}")
        return jsonify({'error': 'Failed to get spend score'}), 500


@api_v1_bp.route('/analytics/insights/<int:report_id>', methods=['GET'])
@jwt_required()
def get_insights(report_id):
    """
    Get AI insights for specific report
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Get insights
        insights = report.insights.filter_by(is_dismissed=False).all()
        
        return jsonify({
            'report_id': report.id,
            'insights': [insight.to_dict() for insight in insights],
            'ai_insights': report.ai_insights,
            'total_insights': len(insights)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get insights error: {str(e)}")
        return jsonify({'error': 'Failed to get insights'}), 500


@api_v1_bp.route('/analytics/trends/<int:report_id>', methods=['GET'])
@jwt_required()
def get_spending_trends(report_id):
    """
    Get spending trends and patterns
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Generate trends analysis
        analytics_service = AnalyticsService()
        trends = analytics_service.get_spending_trends(report_id)
        
        return jsonify({
            'report_id': report.id,
            'trends': trends
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get trends error: {str(e)}")
        return jsonify({'error': 'Failed to get spending trends'}), 500


@api_v1_bp.route('/analytics/categories/<int:report_id>', methods=['GET'])
@jwt_required()
def get_category_analysis(report_id):
    """
    Get spending by category analysis
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get report and verify ownership
        report = Report.query.filter_by(id=report_id, user_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Generate category analysis
        analytics_service = AnalyticsService()
        categories = analytics_service.get_category_analysis(report_id)
        
        return jsonify({
            'report_id': report.id,
            'categories': categories
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get category analysis error: {str(e)}")
        return jsonify({'error': 'Failed to get category analysis'}), 500


@api_v1_bp.route('/analytics/summary', methods=['GET'])
@jwt_required()
def get_user_summary():
    """
    Get user's overall financial summary across all reports
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all completed reports
        reports = Report.query.filter_by(
            user_id=current_user_id,
            status='completed'
        ).all()
        
        if not reports:
            return jsonify({
                'message': 'No completed reports found',
                'total_reports': 0,
                'reports': []
            }), 200
        
        # Calculate summary statistics
        total_transactions = sum(r.total_transactions or 0 for r in reports)
        average_spend_score = sum(r.spend_score or 0 for r in reports if r.spend_score) / len([r for r in reports if r.spend_score])
        
        # Get latest report for recent insights
        latest_report = max(reports, key=lambda x: x.created_at)
        
        return jsonify({
            'user_id': current_user_id,
            'total_reports': len(reports),
            'total_transactions': total_transactions,
            'average_spend_score': round(average_spend_score, 2) if reports else 0,
            'latest_report': latest_report.to_dict() if latest_report else None,
            'reports_summary': [
                {
                    'id': r.id,
                    'title': r.title,
                    'spend_score': r.spend_score,
                    'score_tier': r.score_tier,
                    'created_at': r.created_at.isoformat() if r.created_at else None
                } for r in reports
            ]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user summary error: {str(e)}")
        return jsonify({'error': 'Failed to get user summary'}), 500