
#!/usr/bin/env python3
"""
Automatically create Supabase tables for VeroctaAI
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def create_tables():
    """Create all required tables in Supabase"""
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        return False
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Note: These SQL commands need to be run in Supabase SQL Editor
        # as the Python client doesn't have DDL permissions
        
        print("\n📋 Please run these SQL commands in your Supabase SQL Editor:")
        print("🔗 Go to: https://peddjxzwicclrqbnooiz.supabase.co/project/peddjxzwicclrqbnooiz/sql")
        
        print("\n-- Enable UUID extension --")
        print("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        
        print("\n-- Create Users Table --")
        print("""
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
""")
        
        print("\n-- Create Reports Table --")
        print("""
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
""")
        
        print("\n-- Create Insights Table --")
        print("""
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
""")
        
        print("\n-- Create Subscriptions Table --")
        print("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR,
    stripe_subscription_id VARCHAR,
    plan_name VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'active',
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
""")
        
        print("\n-- Create Payments Table --")
        print("""
CREATE TABLE IF NOT EXISTS payments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
    stripe_payment_intent_id VARCHAR,
    amount INTEGER NOT NULL,
    currency VARCHAR DEFAULT 'usd',
    status VARCHAR DEFAULT 'pending',
    payment_method VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
""")
        
        print("\n-- Create Email Logs Table --")
        print("""
CREATE TABLE IF NOT EXISTS email_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    email_type VARCHAR NOT NULL,
    recipient_email VARCHAR NOT NULL,
    subject VARCHAR,
    status VARCHAR DEFAULT 'sent',
    sent_at TIMESTAMP DEFAULT NOW(),
    error_message TEXT
);
""")
        
        print("\n-- Enable Row Level Security (RLS) --")
        print("""
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE insights ENABLE ROW LEVEL SECURITY;
""")
        
        print("\n-- Create RLS Policies --")
        print("""
-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);

-- Reports policies
CREATE POLICY "Users can view own reports" ON reports FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own reports" ON reports FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own reports" ON reports FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own reports" ON reports FOR DELETE USING (auth.uid() = user_id);

-- Insights policies
CREATE POLICY "Users can view own insights" ON insights FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own insights" ON insights FOR INSERT WITH CHECK (auth.uid() = user_id);
""")
        
        print("\n✅ Copy and paste these SQL commands into your Supabase SQL Editor to create the tables.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    create_tables()
