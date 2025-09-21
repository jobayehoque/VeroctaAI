import os
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
import logging # Assuming logging is used elsewhere for error reporting

try:
    # Attempt to import the database service, assuming it handles Supabase connection
    from database import db_service
except ImportError:
    db_service = None
    logging.warning("Database service not found. Supabase integration may not be available.")

# Simple in-memory user store (replace with database in production)
# Pre-computed password hashes for consistent authentication
admin_password_hash = b'$2b$12$ZKOiYm4737YUelAqY2xLD.lx7PI8oTUFKZjjfZlmEK3Tzx.q0ZCpm'  # admin123
demo_password_hash = b'$2b$12$z2zF.Wlh3rF.rSqkaw2Bn.7rG/EbXsuChM/xSdneDmQlVDV6YqtSu'   # demo123

users_db = {
    "admin@verocta.ai": {
        "id": 1,
        "email": "admin@verocta.ai",
        "password": admin_password_hash,
        "role": "admin",
        "created_at": datetime.now(),
        "company": "VeroctaAI",
        "is_active": True
    },
    "demo@verocta.ai": {
        "id": 2,
        "email": "demo@verocta.ai",
        "password": demo_password_hash,
        "role": "user",
        "created_at": datetime.now(),
        "company": "VeroctaAI Demo",
        "is_active": True
    },
    "demo@demo.com": {
        "id": 3,
        "email": "demo@demo.com",
        "password": bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()),
        "role": "user",
        "created_at": datetime.now(),
        "company": "Demo Company",
        "is_active": True
    }
}

def init_auth(app):
    """Initialize JWT authentication"""
    # Use environment variables for JWT secret key
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'your-fallback-secret-key' # Ensure a default or env var is set
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    jwt = JWTManager(app)
    return jwt

def validate_user(email, password):
    """Validate user credentials"""
    # Try database first (Supabase)
    if db_service and db_service.connected:
        db_user = db_service.get_user_by_email(email)
        if db_user and db_user.get('password_hash'): # Assuming password_hash is stored in Supabase
            # Ensure password comparison is done correctly, handling potential type differences
            if bcrypt.checkpw(password.encode('utf-8'), db_user['password_hash'].encode('utf-8')):
                return {
                    'id': db_user['id'],
                    'email': db_user['email'],
                    'role': db_user.get('role', 'user'), # Use .get for safety
                    'company': db_user.get('company', 'Default Company'), # Use .get for safety
                    'created_at': db_user.get('created_at', datetime.now()), # Use .get for safety
                    'is_active': db_user.get('is_active', True) # Use .get for safety
                }

    # Fallback to in-memory storage if database is not connected or user not found
    user = users_db.get(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None

def create_user(email, password, company=None, role="user"):
    """Create new user account"""
    # Check if user already exists in memory or database
    if email in users_db:
        return None
    if db_service and db_service.connected:
        if db_service.get_user_by_email(email):
            return None

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # For in-memory storage, we need an integer ID
    user_id = max([user['id'] for user in users_db.values()]) + 1 if users_db else 1

    user_data = {
        "id": user_id,  # Will be overwritten with UUID from database if successful
        "email": email,
        "password_hash": hashed_password.decode('utf-8'),
        "role": role,
        "created_at": datetime.now(),
        "company": company or "Default Company",
        "is_active": True
    }

    # Add to database first, then fallback to in-memory if db fails
    if db_service and db_service.connected:
        try:
            created_user = db_service.create_user(email, hashed_password.decode('utf-8'), company, role)
            if created_user:
                # Update user_data with actual DB ID if different
                user_data['id'] = created_user['id']
                return user_data
        except Exception as e:
            logging.error(f"Failed to create user in database: {e}")
            # Proceed to add to in-memory if DB creation fails
            pass

    # Add to in-memory storage as a fallback or if db is not connected
    users_db[email] = user_data
    return user_data


def get_user_by_email(email):
    """Get user by email"""
    # Try database first
    if db_service and db_service.connected:
        db_user = db_service.get_user_by_email(email)
        if db_user:
            return {
                'id': db_user['id'],
                'email': db_user['email'],
                'role': db_user.get('role', 'user'),
                'company': db_user.get('company', 'Default Company'),
                'created_at': db_user.get('created_at', datetime.now()),
                'is_active': db_user.get('is_active', True)
            }

    # Fallback to in-memory storage
    user = users_db.get(email)
    if user:
        return {
            'id': user['id'],
            'email': user['email'],
            'role': user.get('role', 'user'),
            'company': user.get('company', 'Default Company'),
            'created_at': user.get('created_at', datetime.now()),
            'is_active': user.get('is_active', True)
        }
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    # Try database first
    if db_service and db_service.connected:
        db_user = db_service.get_user_by_id(user_id) # Assuming this method exists
        if db_user:
            return {
                'id': db_user['id'],
                'email': db_user['email'],
                'role': db_user.get('role', 'user'),
                'company': db_user.get('company', 'Default Company'),
                'created_at': db_user.get('created_at', datetime.now()),
                'is_active': db_user.get('is_active', True)
            }

    # Fallback to in-memory storage
    for user in users_db.values():
        if user['id'] == user_id:
            return user
    return None

def require_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_email = get_jwt_identity()
        user = get_user_by_email(current_user_email)

        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user from JWT token"""
    try:
        email = get_jwt_identity()
        if not email:
            logging.warning("No email found in JWT token")
            return None

        # Try database first
        if db_service and db_service.connected:
            try:
                db_user = db_service.get_user_by_email(email)
                if db_user:
                    logging.debug(f"Found user in database: {email}")
                    return db_user
            except Exception as db_error:
                logging.error(f"Database user lookup failed: {str(db_error)}")

        # Fallback to in-memory
        for user in users_db.values():
            if user['email'] == email:
                logging.debug(f"Found user in memory: {email}")
                return user

        logging.warning(f"User not found: {email}")
        return None
    except Exception as e:
        logging.error(f"Error getting current user: {str(e)}")
        return None

# Placeholder for PDF download functionality.
# This would typically involve generating a PDF from data and returning it as a response.
# For example, using libraries like WeasyPrint or ReportLab.

# Assuming 'report_data' is a structure that can be converted to PDF
# and 'db_service' has a method to fetch reports or data for reports.

# Example structure for a report:
# report_data = {
#     "title": "Monthly Sales Report",
#     "date": "2023-10-27",
#     "data": [
#         {"item": "Product A", "quantity": 100, "price": 10.50},
#         {"item": "Product B", "quantity": 150, "price": 5.25}
#     ]
# }

# def generate_pdf_report(report_id):
#     """
#     Fetches report data and generates a PDF.
#     This is a placeholder and needs actual PDF generation logic.
#     """
#     if not db_service or not db_service.connected:
#         logging.error("Database service not connected for PDF generation.")
#         return jsonify({'error': 'Database not available'}), 500

#     try:
#         # Fetch report data from the database
#         report_data = db_service.get_report_data(report_id)
#         if not report_data:
#             return jsonify({'error': 'Report not found'}), 404

#         # --- PDF Generation Logic ---
#         # This is where you would use a library like WeasyPrint or ReportLab
#         # Example with WeasyPrint (requires installation: pip install WeasyPrint)
#         # from weasyprint import HTML
#         #
#         # html_content = f"""
#         # <html>
#         # <head><title>{report_data.get('title', 'Report')}</title></head>
#         # <body>
#         #   <h1>{report_data.get('title', 'Report')}</h1>
#         #   <p>Date: {report_data.get('date', 'N/A')}</p>
#         #   <table>
#         #     <thead><tr><th>Item</th><th>Quantity</th><th>Price</th></tr></thead>
#         #     <tbody>
#         #       {''.join([f"<tr><td>{row['item']}</td><td>{row['quantity']}</td><td>{row['price']:.2f}</td></tr>" for row in report_data.get('data', [])])}
#         #     </tbody>
#         #   </table>
#         # </body>
#         # </html>
#         # """
#         # pdf_bytes = HTML(string=html_content).write_pdf()

#         # Placeholder response if PDF generation is not implemented
#         logging.info(f"PDF generation for report {report_id} would happen here.")
#         return jsonify({'message': f'PDF generation for report {report_id} would be implemented here.'}), 200
#         # return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment; filename="report_{report_id}.pdf"'})

#     except Exception as e:
#         logging.error(f"Error generating PDF report {report_id}: {str(e)}")
#         return jsonify({'error': 'Failed to generate PDF report'}), 500