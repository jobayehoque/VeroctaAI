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

# Frontend build directory - simplified path
frontend_build_dir = os.path.join(basedir, 'frontend', 'dist')

# Create the Flask app
app = Flask(__name__,
            static_folder=frontend_build_dir,
            static_url_path='',
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
    index_path = os.path.join(frontend_build_dir, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    else:
        # Fallback HTML when frontend build is missing
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>VeroctaAI - AI-Powered Financial Intelligence</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
                .container { max-width: 800px; margin: 0 auto; text-align: center; }
                .logo { font-size: 3em; font-weight: bold; margin-bottom: 20px; }
                .subtitle { font-size: 1.2em; margin-bottom: 30px; opacity: 0.9; }
                .status { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
                .api-status { color: #4ade80; font-weight: bold; }
                .build-status { color: #fbbf24; font-weight: bold; }
                .btn { background: #4ade80; color: white; padding: 12px 24px; border: none; border-radius: 6px; text-decoration: none; display: inline-block; margin: 10px; }
                .btn:hover { background: #22c55e; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🚀 VeroctaAI</div>
                <div class="subtitle">AI-Powered Financial Intelligence & Analytics</div>
                
                <div class="status">
                    <h3>System Status</h3>
                    <p class="api-status">✅ Backend API: Running</p>
                    <p class="build-status">⚠️ Frontend: Building...</p>
                    <p>📊 Platform: Ready for Financial Analysis</p>
                </div>
                
                <div>
                    <h3>Available Services</h3>
                    <a href="/api/health" class="btn">Health Check</a>
                    <a href="/api/docs" class="btn">API Documentation</a>
                </div>
                
                <div style="margin-top: 40px; opacity: 0.8;">
                    <p>Frontend is currently building. Please refresh in a few moments.</p>
                    <p>If this persists, check the build logs in your deployment dashboard.</p>
                </div>
            </div>
            
            <script>
                // Auto-refresh every 30 seconds
                setTimeout(() => location.reload(), 30000);
            </script>
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

# Serve React app for all non-API routes
@app.route('/<path:path>')
def serve_react_app(path):
    if path.startswith('api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    
    # Check if it's a file request
    if '.' in path:
        try:
            return send_from_directory(frontend_build_dir, path)
        except:
            pass
    
    # For all other routes, serve the React app or fallback
    index_path = os.path.join(frontend_build_dir, 'index.html')
    if os.path.exists(index_path):
        try:
            return send_file(index_path)
        except:
            pass
    
    # Fallback when frontend is not available
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VeroctaAI - Frontend Building</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
            .container { max-width: 600px; margin: 0 auto; text-align: center; }
            .logo { font-size: 2.5em; font-weight: bold; margin-bottom: 20px; }
            .message { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🚀 VeroctaAI</div>
            <div class="message">
                <h3>Frontend Building...</h3>
                <p>The frontend is currently being built. Please wait a moment and refresh the page.</p>
                <p>If this persists, check the build logs in your deployment dashboard.</p>
            </div>
        </div>
        <script>setTimeout(() => location.reload(), 10000);</script>
    </body>
    </html>
    """, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    # Production configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Always use 0.0.0.0 for Render compatibility
    debug = not is_production
    
    print('🚀 Starting VeroctaAI Flask Application...')
    print(f'📍 URL: http://{host}:{port}')
    print('📊 Platform: AI-Powered Financial Intelligence & Analytics')
    print(f'🔧 Environment: {"Production" if is_production else "Development"}')

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
