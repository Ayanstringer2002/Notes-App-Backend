"""
Utility functions for the notes service
"""

from werkzeug.security import generate_password_hash, check_password_hash
import re

def hash_password(password):
    """
    Hash a password using werkzeug security
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(password, password_hash):
    """
    Verify a plain text password against a hash
    
    Args:
        password: Plain text password
        password_hash: Hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    return check_password_hash(password_hash, password)


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    
    Args:
        password: Password string to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 6:
        return False, 'Password must be at least 6 characters long'
    if len(password) > 255:
        return False, 'Password must not exceed 255 characters'
    return True, None


def validate_note_data(data):
    """
    Validate note creation/update data
    
    Args:
        data: Dictionary with 'title' and 'content' keys
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, 'Request body is required'
    
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not title:
        return False, 'Title is required and cannot be empty'
    
    if len(title) > 255:
        return False, 'Title must not exceed 255 characters'
    
    if not content:
        return False, 'Content is required and cannot be empty'
    
    if len(content) > 10000:
        return False, 'Content must not exceed 10000 characters'
    
    return True, None


def sanitize_note_data(data):
    """
    Sanitize note data by stripping whitespace
    
    Args:
        data: Dictionary with note data
    
    Returns:
        Sanitized dictionary
    """
    return {
        'title': data.get('title', '').strip(),
        'content': data.get('content', '').strip()
    }