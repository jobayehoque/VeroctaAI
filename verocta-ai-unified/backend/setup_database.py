
#!/usr/bin/env python3
"""
Database setup script for VeroctaAI Supabase integration
Run this script to create the necessary tables in your Supabase database
"""

import os
import logging
from supabase import create_client, Client

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def setup_database():
    """Create tables in Supabase database"""
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials. Please check your .env file.")
        return False
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Note: In Supabase, you typically create tables through the dashboard
        # or SQL editor, not through the Python client. This script serves as
        # documentation of the required schema.
        
        print("""
📋 Please create the following tables in your Supabase dashboard:

1. USERS TABLE:
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'user',
    company VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

2. REPORTS TABLE:
CREATE TABLE IF NOT EXISTS reports (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    company VARCHAR,
    spend_score INTEGER,
    data JSONB,
    insights JSONB,
    analysis JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR DEFAULT 'completed'
);

3. INSIGHTS TABLE:
CREATE TABLE IF NOT EXISTS insights (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    report_id UUID REFERENCES reports(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ai_insights JSONB,
    recommendations JSONB,
    waste_percentage DECIMAL(5,2),
    duplicate_expenses INTEGER DEFAULT 0,
    spending_spikes INTEGER DEFAULT 0,
    savings_opportunities INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

To create these tables:
1. Go to your Supabase dashboard: https://peddjxzwicclrqbnooiz.supabase.co
2. Navigate to the SQL Editor
3. Copy and paste each CREATE TABLE statement above
4. Run each statement one by one

✅ Database schema ready for VeroctaAI!
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
