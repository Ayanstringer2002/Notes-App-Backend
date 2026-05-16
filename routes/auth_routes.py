"""
Authentication routes: /register, /login
"""

from flask import Blueprint, request, jsonify
from database import db
from models import User
from utils import (
    hash_password, verify_password, 
    validate_email, validate_password
)
from auth import generate_jwt_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Endpoint: POST /register
    Payload: {
        "email": "string",
        "password": "string"
    }
    
    Response: 201 CREATED with success message
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'message': 'Request body is required'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate email
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        
        if not validate_email(email):
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Validate password
        if not password:
            return jsonify({'message': 'Password is required'}), 400
        
        is_valid, error = validate_password(password)
        if not is_valid:
            return jsonify({'message': error}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already registered'}), 409
        
        # Create new user
        hashed_password = hash_password(password)
        new_user = User(email=email, password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    
    Endpoint: POST /login
    Payload: {
        "email": "string",
        "password": "string"
    }
    
    Response (Success - 200): {
        "access_token": "string"
    }
    
    Response (Failure - 401): {
        "message": "Invalid email or password"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'message': 'Invalid email or password'}), 401
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user.password_hash):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Generate JWT token
        access_token = generate_jwt_token(user.id)
        
        return jsonify({'access_token': access_token}), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500