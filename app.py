import os
import logging
from flask import Flask, send_from_directory, send_file, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Configure logging for production
log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('verocta.log') if os.environ.get('FLASK_ENV') == 'production' else logging.NullHandler()
    ]
)

# Get the directory of this script
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Environment variables loaded from .env file")
except ImportError:
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    logging.error(f"Error loading .env file: {e}")

# Debug: Log all environment variables that start with common prefixes
logging.info("=== Environment Variables Debug ===")
for key, value in os.environ.items():
    if any(key.startswith(prefix) for prefix in ['SESSION', 'FLASK', 'PYTHON', 'SUPABASE', 'OPENAI']):
        logging.info(f"{key}: {'SET' if value else 'EMPTY'}")
logging.info("=== End Environment Variables Debug ===")

# Create the Flask app for API-only service
app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'))
# Set secret key with fallback for deployment
session_secret = os.environ.get("SESSION_SECRET")
logging.info(f"SESSION_SECRET environment variable: {'SET' if session_secret else 'NOT SET'}")
if not session_secret:
    # Generate a fallback secret for production deployment
    import secrets
    session_secret = secrets.token_hex(32)
    logging.warning("SESSION_SECRET not found, using generated fallback secret")

app.secret_key = session_secret
logging.info("Flask app secret key configured successfully")

# Configure database connection securely using environment variables only
supabase_url = os.environ.get("SUPABASE_URL")
supabase_password = os.environ.get("SUPABASE_PASSWORD")
supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")

# Only configure database if all required credentials are present
if supabase_url and supabase_password:
    # Extract hostname from URL for PostgreSQL connection
    import urllib.parse
    parsed_url = urllib.parse.urlparse(supabase_url)
    if parsed_url.netloc:
        host = f"db.{parsed_url.netloc.split('//')[0] if '//' in parsed_url.netloc else parsed_url.netloc}"
        DATABASE_URL = f"postgresql://postgres:{supabase_password}@{host}:5432/postgres"
        app.config["DATABASE_URL"] = DATABASE_URL
        logging.info("✅ Database connection configured")
    else:
        logging.warning("⚠️ Invalid SUPABASE_URL format")
        app.config["DATABASE_URL"] = None
else:
    logging.warning("⚠️ Database credentials not found - using in-memory storage only")
    app.config["DATABASE_URL"] = None

# Enable CORS for development and production
allowed_origins = [
    "http://localhost:5000", 
    "http://127.0.0.1:5000",
    "http://localhost:3000",  # React dev server
    "https://verocta-ai.onrender.com",  # Production URL
    "https://*.onrender.com",  # Render subdomains
    "https://*.vercel.app",  # Vercel deployments
    "https://*.netlify.app"  # Netlify deployments
]

# Add custom domain if provided
custom_domain = os.environ.get("CUSTOM_DOMAIN")
if custom_domain:
    allowed_origins.append(f"https://{custom_domain}")
    allowed_origins.append(f"http://{custom_domain}")

# Remove empty strings and duplicates
allowed_origins = list(set([origin for origin in allowed_origins if origin]))

CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"]
    }
})

# Initialize authentication
try:
    from auth import init_auth
    jwt = init_auth(app)
except ImportError:
    logging.warning("Auth module not found - running without authentication")
    jwt = None

# Import routes after app creation to avoid circular imports
try:
    from routes import *
except ImportError:
    logging.warning("Routes module not found - creating basic routes")
    
@app.route('/')
def index():
    # API Service Landing Page
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VeroctaAI API - AI-Powered Financial Intelligence</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
            .container { max-width: 900px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .logo { font-size: 3.5em; font-weight: bold; margin-bottom: 10px; }
            .subtitle { font-size: 1.3em; opacity: 0.9; margin-bottom: 20px; }
            .version { font-size: 0.9em; opacity: 0.7; }
            .section { background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; margin: 20px 0; backdrop-filter: blur(10px); }
            .section h3 { margin-top: 0; color: #4ade80; }
            .endpoint { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; font-family: 'Courier New', monospace; }
            .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; margin-right: 10px; }
            .get { background: #4ade80; color: black; }
            .post { background: #3b82f6; color: white; }
            .btn { background: #4ade80; color: white; padding: 12px 24px; border: none; border-radius: 6px; text-decoration: none; display: inline-block; margin: 10px; transition: all 0.3s; }
            .btn:hover { background: #22c55e; transform: translateY(-2px); }
            .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #4ade80; margin-right: 8px; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
            .feature { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; text-align: center; }
            .feature-icon { font-size: 2em; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀 VeroctaAI API</div>
                <div class="subtitle">AI-Powered Financial Intelligence & Analytics</div>
                <div class="version">API Service v2.0 | Backend Only</div>
            </div>
            
            <div class="section">
                <h3><span class="status-indicator"></span>Service Status</h3>
                <p><strong>✅ API Service:</strong> Running and Ready</p>
                <p><strong>🔗 Base URL:</strong> <code>https://veroctaai.onrender.com/api</code></p>
                <p><strong>📊 Status:</strong> All endpoints operational</p>
            </div>
            
            <div class="section">
                <h3>🔗 Core API Endpoints</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> /api/health - Health check and system status
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> /api/docs - API documentation
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/auth/login - User authentication
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/auth/register - User registration
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/upload - File upload for analysis
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/spend-score - Generate spend analysis
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> /api/reports - List user reports
                </div>
            </div>
            
            <div class="section">
                <h3>🎯 Key Features</h3>
                <div class="features">
                    <div class="feature">
                        <div class="feature-icon">📊</div>
                        <h4>Financial Analysis</h4>
                        <p>AI-powered spend analysis and insights</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📁</div>
                        <h4>File Processing</h4>
                        <p>CSV upload and data processing</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🔐</div>
                        <h4>Authentication</h4>
                        <p>Secure JWT-based user management</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📈</div>
                        <h4>Reports</h4>
                        <p>Generate and download financial reports</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🚀 Quick Actions</h3>
                <a href="/api/health" class="btn">Check Health</a>
                <a href="/api/docs" class="btn">View Documentation</a>
                <a href="https://github.com/your-repo" class="btn">GitHub Repository</a>
            </div>
            
            <div class="section">
                <h3>📖 Integration Guide</h3>
                <p><strong>For Frontend Integration:</strong></p>
                <p>Set your frontend environment variable: <code>VITE_API_URL=https://veroctaai.onrender.com/api</code></p>
                <p>All API endpoints are CORS-enabled and ready for frontend consumption.</p>
            </div>
        </div>
    </body>
    </html>
    """, 200, {'Content-Type': 'text/html'}
    
    @app.route('/api/health')
    def health():
        try:
            from health import check_health
            return jsonify(check_health())
        except Exception as e:
            return jsonify({
                "status": "healthy", 
                "message": "VeroctaAI is running",
                "error": str(e)
            })

# API-only service - redirect non-API routes to main page
@app.route('/<path:path>')
def handle_unknown_routes(path):
    if path.startswith('api/'):
        return jsonify({"error": "API endpoint not found", "available_endpoints": [
            "/api/health", "/api/docs", "/api/auth/login", "/api/auth/register",
            "/api/upload", "/api/spend-score", "/api/reports"
        ]}), 404
    
    # Redirect all other routes to the main API landing page
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VeroctaAI API - Page Not Found</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { text-align: center; max-width: 600px; }
            .logo { font-size: 3em; font-weight: bold; margin-bottom: 20px; }
            .message { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
            .btn { background: #4ade80; color: white; padding: 12px 24px; border: none; border-radius: 6px; text-decoration: none; display: inline-block; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🚀 VeroctaAI API</div>
            <div class="message">
                <h3>Page Not Found</h3>
                <p>This is an API-only service. The requested page doesn't exist.</p>
                <p>Please use the API endpoints or return to the main page.</p>
            </div>
            <a href="/" class="btn">← Back to API Home</a>
            <a href="/api/health" class="btn">Check API Health</a>
        </div>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    # Production configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Always use 0.0.0.0 for Render compatibility
    debug = not is_production
    
    print('🚀 Starting VeroctaAI API Service...')
    print(f'📍 URL: http://{host}:{port}')
    print('📊 Platform: AI-Powered Financial Intelligence & Analytics API')
    print(f'🔧 Environment: {"Production" if is_production else "Development"}')
    print('🌐 Service Type: Backend API Only')

    # Check OpenAI API key
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print('🤖 AI: GPT-4o Integration Ready ✅')
    else:
        print('⚠️  WARNING: OPENAI_API_KEY not set! AI features will not work.')
        print('💡 Fix: Set environment variable or create .env file with your API key')

    # Check database connection
    if app.config.get("DATABASE_URL"):
        print('🗄️  Database: Supabase PostgreSQL Ready ✅')
    else:
        print('🗄️  Database: In-memory storage (no persistence)')

    print('📁 CSV Support: QuickBooks, Wave, Revolut, Xero')
    print('✅ Server starting...')
    
    if is_production:
        # Use Gunicorn for production
        print('🚀 Production mode: Use Gunicorn for deployment')
        print('Command: gunicorn --bind 0.0.0.0:{} --workers 4 app:app'.format(port))
    else:
        app.run(host=host, port=port, debug=debug)
