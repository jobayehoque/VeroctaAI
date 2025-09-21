"""
Authentication Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .controllers import AuthController
from .validators import AuthValidator
from utils.decorators import validate_json, handle_errors

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()
auth_validator = AuthValidator()

@auth_bp.route('/register', methods=['POST'])
@validate_json
@handle_errors
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    validation_result = auth_validator.validate_registration(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Create user
    result = auth_controller.register_user(
        email=data['email'],
        password=data['password'],
        company=data.get('company'),
        role=data.get('role', 'user')
    )
    
    if not result['success']:
        return jsonify({'error': result['message']}), result.get('status_code', 400)
    
    # Generate token
    token = create_access_token(identity=data['email'])
    
    return jsonify({
        'success': True,
        'token': token,
        'user': result['user']
    }), 201

@auth_bp.route('/login', methods=['POST'])
@validate_json
@handle_errors
def login():
    """Authenticate user and return token"""
    data = request.get_json()
    
    # Validate input
    validation_result = auth_validator.validate_login(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Authenticate user
    result = auth_controller.authenticate_user(
        email=data['email'],
        password=data['password']
    )
    
    if not result['success']:
        return jsonify({'error': result['message']}), result.get('status_code', 401)
    
    # Generate token
    token = create_access_token(identity=data['email'])
    
    return jsonify({
        'success': True,
        'token': token,
        'user': result['user']
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@handle_errors
def get_current_user():
    """Get current user profile"""
    email = get_jwt_identity()
    
    result = auth_controller.get_user_profile(email)
    
    if not result['success']:
        return jsonify({'error': result['message']}), result.get('status_code', 404)
    
    return jsonify({
        'success': True,
        'user': result['user']
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
@handle_errors
def refresh_token():
    """Refresh JWT token"""
    email = get_jwt_identity()
    
    # Generate new token
    token = create_access_token(identity=email)
    
    return jsonify({
        'success': True,
        'token': token
    })

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@handle_errors
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@validate_json
@handle_errors
def change_password():
    """Change user password"""
    email = get_jwt_identity()
    data = request.get_json()
    
    # Validate input
    validation_result = auth_validator.validate_password_change(data)
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    # Change password
    result = auth_controller.change_password(
        email=email,
        current_password=data['current_password'],
        new_password=data['new_password']
    )
    
    if not result['success']:
        return jsonify({'error': result['message']}), result.get('status_code', 400)
    
    return jsonify({
        'success': True,
        'message': 'Password changed successfully'
    })
