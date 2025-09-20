
import os
import logging
from database import db_service, supabase
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_database_connection():
    """Verify database connection and setup"""
    logger.info("🔍 Verifying database connection...")
    
    if not db_service.connected:
        logger.warning("⚠️ Database not connected - using in-memory storage")
        return False
    
    try:
        # Test basic connection
        response = supabase.table('users').select('count').limit(1).execute()
        logger.info("✅ Database connection verified")
        
        # Check if tables exist and have expected structure
        tables_to_check = ['users', 'reports', 'insights']
        
        for table in tables_to_check:
            try:
                response = supabase.table(table).select('*').limit(1).execute()
                logger.info(f"✅ Table '{table}' exists and accessible")
            except Exception as e:
                logger.error(f"❌ Table '{table}' issue: {str(e)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False

def create_test_data():
    """Create test data for demonstration"""
    if not db_service.connected:
        logger.warning("⚠️ Skipping test data creation - database not connected")
        return
    
    try:
        # Create test user
        test_user = db_service.create_user(
            email="demo@verocta.ai",
            password_hash="$2b$12$dummy.hash.for.demo.purposes.only",
            company="VeroctaAI Demo",
            role="user"
        )
        
        if test_user:
            logger.info("✅ Test user created")
            
            # Create sample report
            sample_data = {
                'transactions': 250,
                'total_amount': 45000.00,
                'categories': 8,
                'filename': 'demo_financial_data.csv',
                'top_categories': ['Software & SaaS', 'Office Supplies', 'Marketing'],
                'upload_timestamp': datetime.now().isoformat()
            }
            
            sample_insights = {
                'waste_percentage': 12.4,
                'duplicate_expenses': 15,
                'spending_spikes': 3,
                'savings_opportunities': 6,
                'recommendations': [
                    'Review subscription services for duplicates',
                    'Implement automated expense categorization',
                    'Set up budget alerts for key categories'
                ]
            }
            
            sample_report = db_service.create_report(
                user_id=test_user['id'],
                title="Sample Financial Analysis",
                company="VeroctaAI Demo",
                data=sample_data,
                spend_score=78,
                insights=sample_insights
            )
            
            if sample_report:
                logger.info("✅ Sample report created")
            else:
                logger.warning("⚠️ Failed to create sample report")
        else:
            logger.warning("⚠️ Failed to create test user")
            
    except Exception as e:
        logger.error(f"❌ Error creating test data: {str(e)}")

def main():
    """Main verification function"""
    logger.info("🚀 Starting database verification...")
    
    # Check environment variables
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    if supabase_url and supabase_key:
        logger.info("✅ Database credentials found")
    else:
        logger.warning("⚠️ Database credentials missing - using in-memory storage")
    
    # Verify connection
    db_connected = verify_database_connection()
    
    if db_connected:
        logger.info("✅ Database verification complete")
        
        # Optionally create test data
        create_choice = input("\n🤔 Create sample test data? (y/N): ")
        if create_choice.lower() == 'y':
            create_test_data()
    else:
        logger.info("⚠️ Database verification failed - application will use in-memory storage")
    
    logger.info("\n✅ Verification complete!")

if __name__ == "__main__":
    main()
