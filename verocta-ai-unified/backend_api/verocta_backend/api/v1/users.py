"""
Users API endpoints
User management and profile operations
"""

from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError

from . import api_v1_bp
from ...models import User
from ...core.database import db


class UpdateProfileSchema(Schema):
    """Profile update validation"""
    first_name = fields.String(required=False, allow_none=True)
    last_name = fields.String(required=False, allow_none=True)
    email = fields.Email(required=False)


class ChangePasswordSchema(Schema):
    """Password change validation"""
    current_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=lambda x: len(x) >= 6)


@api_v1_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile'}), 500


@api_v1_bp.route('/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user profile
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate request data
        schema = UpdateProfileSchema()
        data = schema.load(request.json or {})
        
        # Check if email is being changed and is unique
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'Email already in use'}), 409
        
        # Update fields
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500


@api_v1_bp.route('/users/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate request data
        schema = ChangePasswordSchema()
        data = schema.load(request.json or {})
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Update password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': 'Failed to change password'}), 500


@api_v1_bp.route('/users/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    Delete user account and all associated data
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete user (cascades to reports, transactions, insights)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Delete account error: {str(e)}")
        return jsonify({'error': 'Failed to delete account'}), 500


@api_v1_bp.route('/users/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """
    Get user statistics and activity summary
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user statistics
        total_reports = user.reports.count()
        completed_reports = user.reports.filter_by(status='completed').count()
        
        # Get latest activity
        latest_report = user.reports.order_by(user.reports.desc()).first()
        
        return jsonify({
            'user_id': current_user_id,
            'account_created': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'total_reports': total_reports,
            'completed_reports': completed_reports,
            'latest_report': {
                'id': latest_report.id,
                'title': latest_report.title,
                'created_at': latest_report.created_at.isoformat()
            } if latest_report else None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user stats error: {str(e)}")
        return jsonify({'error': 'Failed to get user statistics'}), 500