"""
Authentication utilities for JWT token management
"""

import jwt
from flask import current_app
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models import User

def generate_jwt_token(user_id):
    """
    Generate a JWT token for a user
    
    Args:
        user_id: The user's unique ID
    
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    return token


def verify_jwt_token(token):
    """
    Verify a JWT token and extract user_id
    
    Args:
        token: JWT token string
    
    Returns:
        user_id if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
        return None


def token_required(f):
    """
    Decorator to require JWT token for protected routes
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': 'Success'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        # Check for token in Authorization header
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'message': 'Authorization token is missing'}), 401
        
        # Verify token
        user_id = verify_jwt_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        # Get user from database
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({'message': 'User not found'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function


def extract_token_from_request():
    """
    Extract JWT token from request Authorization header
    
    Returns:
        token string or None
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == 'Bearer':
            return parts[1]
    return None


def get_user_id_from_token(token):
    """
    Get user_id from a token without the decorator
    
    Args:
        token: JWT token string
    
    Returns:
        user_id or None
    """
    return verify_jwt_token(token)