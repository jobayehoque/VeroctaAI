"""
Authentication API endpoints
JWT-based authentication with refresh tokens
"""

from datetime import datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from marshmallow import Schema, fields, ValidationError

from . import api_v1_bp
from ...models import User
from ...core.database import db


class LoginSchema(Schema):
    """Login request validation"""
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=lambda x: len(x) >= 6)


class RegisterSchema(Schema):
    """Registration request validation"""
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=lambda x: len(x) >= 3)
    password = fields.String(required=True, validate=lambda x: len(x) >= 6)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)


@api_v1_bp.route('/auth/login', methods=['POST'])
def login():
    """
    User login endpoint
    Returns access and refresh tokens
    """
    try:
        # Validate request data
        schema = LoginSchema()
        data = schema.load(request.json or {})
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500


@api_v1_bp.route('/auth/register', methods=['POST'])
def register():
    """
    User registration endpoint
    Creates new user account
    """
    try:
        # Validate request data
        schema = RegisterSchema()
        data = schema.load(request.json or {})
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            username=data['username'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500


@api_v1_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Token refresh endpoint
    Returns new access token using refresh token
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 404
        
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500


@api_v1_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout endpoint
    In a production system, you would blacklist the token
    """
    return jsonify({'message': 'Logged out successfully'}), 200


@api_v1_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500