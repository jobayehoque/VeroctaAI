"""
Input Validation Utilities
"""

import re
from werkzeug.utils import secure_filename
import os

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if not password or not isinstance(password, str):
        return False
    
    # Minimum 8 characters
    if len(password) < 8:
        return False
    
    return True

def validate_file_upload(file) -> str:
    """Validate uploaded file"""
    if not file or not file.filename:
        return "No file provided"
    
    # Check file extension
    allowed_extensions = {'csv'}
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return "Only CSV files are allowed"
    
    # Check file size (16MB limit)
    max_size = 16 * 1024 * 1024  # 16MB
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        return "File size must be less than 16MB"
    
    # Check filename security
    filename = secure_filename(file.filename)
    if not filename or filename != file.filename:
        return "Invalid filename"
    
    return None  # No validation errors

def validate_transaction_data(transaction: dict) -> bool:
    """Validate transaction data structure"""
    required_fields = ['amount', 'description']
    
    for field in required_fields:
        if field not in transaction:
            return False
    
    # Validate amount
    try:
        amount = float(transaction['amount'])
        if amount <= 0:
            return False
    except (ValueError, TypeError):
        return False
    
    # Validate description
    if not transaction['description'] or not isinstance(transaction['description'], str):
        return False
    
    return True

def validate_column_mapping(mapping: dict) -> bool:
    """Validate column mapping structure"""
    if not isinstance(mapping, dict):
        return False
    
    valid_fields = ['date', 'description', 'amount', 'category', 'vendor']
    
    for field, column in mapping.items():
        if field not in valid_fields:
            return False
        
        if column and not isinstance(column, str):
            return False
    
    return True
