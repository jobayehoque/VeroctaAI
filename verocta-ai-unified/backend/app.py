import os
import logging
from flask import Flask, send_from_directory, send_file
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
    # Load from project root
    env_path = os.path.join(os.path.dirname(os.path.dirname(basedir)), '.env')
    load_dotenv(env_path)
    # Also try loading from current directory
    load_dotenv()
    logging.info("Environment variables loaded from .env file")
except ImportError:
    logging.warning("python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    logging.error(f"Error loading .env file: {e}")
frontend_build_dir = os.path.join(os.path.dirname(basedir), 'frontend', 'dist')

# Create the Flask app
app = Flask(__name__,
            static_folder=frontend_build_dir,
            static_url_path='',
            template_folder=os.path.join(basedir, 'templates'))
app.secret_key = os.environ.get("SESSION_SECRET")
if not app.secret_key:
    raise ValueError("SESSION_SECRET environment variable is required")

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
from auth import init_auth
jwt = init_auth(app)

# Import routes after app creation to avoid circular imports
from routes import *

if __name__ == '__main__':
    # Production configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Always use 0.0.0.0 for Replit compatibility
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
        print('Command: gunicorn --bind 0.0.0.0:{} --workers 4 backend.app:app'.format(port))
    else:
        app.run(host=host, port=port, debug=debug)