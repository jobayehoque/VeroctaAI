import json
import os
import logging
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY environment variable not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def load_prompt_template():
    """Load the GPT prompt template"""
    try:
        with open('prompts/insight_prompt_v2.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback prompt if file doesn't exist
        return """
        You are a financial advisor analyzing business expense data. 
        Based on the transaction data provided, generate exactly 3 actionable suggestions 
        to reduce unnecessary expenses or optimize spending.
        
        Each suggestion should have:
        - A priority level: "High", "Medium", or "Low"
        - Specific, actionable text (not vague summaries)
        - Business-aware language appropriate for a financial platform
        
        Return your response as JSON in this exact format:
        {
            "suggestions": [
                {"priority": "High", "text": "Specific actionable suggestion"},
                {"priority": "Medium", "text": "Specific actionable suggestion"},
                {"priority": "Low", "text": "Specific actionable suggestion"}
            ]
        }
        
        Focus on identifying patterns, unusual expenses, potential savings opportunities, 
        and vendor optimization based on the actual data provided.
        """

def format_transactions_for_gpt(transactions):
    """Enhanced format transaction data for GPT analysis with detailed insights"""
    if not transactions:
        return "No transaction data available."
    
    # Create comprehensive statistics
    total_amount = sum(t['amount'] for t in transactions)
    avg_amount = total_amount / len(transactions)
    
    # Enhanced breakdowns
    categories = {}
    vendors = {}
    vendor_frequency = {}
    monthly_patterns = {}
    
    for transaction in transactions:
        category = transaction.get('category', 'Uncategorized')
        vendor = transaction.get('vendor', 'Unknown')
        amount = transaction.get('amount', 0)
        date = transaction.get('date')
        
        # Category and vendor tracking
        categories[category] = categories.get(category, 0) + amount
        vendors[vendor] = vendors.get(vendor, 0) + amount
        vendor_frequency[vendor] = vendor_frequency.get(vendor, 0) + 1
        
        # Monthly pattern analysis
        if date:
            month_key = date.strftime('%Y-%m') if hasattr(date, 'strftime') else str(date)[:7]
            monthly_patterns[month_key] = monthly_patterns.get(month_key, 0) + amount
    
    # Sort by amount and identify patterns
    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
    top_vendors = sorted(vendors.items(), key=lambda x: x[1], reverse=True)[:15]
    frequent_vendors = sorted(vendor_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Identify recurring subscriptions (vendors with regular amounts)
    likely_subscriptions = []
    for vendor, total_spent in top_vendors[:10]:
        frequency = vendor_frequency.get(vendor, 0)
        if frequency >= 2:  # Appears multiple times
            avg_per_transaction = total_spent / frequency
            likely_subscriptions.append((vendor, total_spent, frequency, avg_per_transaction))
    
    # Format enhanced data for GPT
    formatted_data = f"""
    ENHANCED FINANCIAL DATA ANALYSIS REQUEST
    
    Executive Summary:
    - Total Transactions: {len(transactions):,}
    - Total Amount: ${total_amount:,.2f}
    - Average Transaction: ${avg_amount:,.2f}
    - Unique Vendors: {len(vendors)}
    - Unique Categories: {len(categories)}
    
    Top Spending Categories (with optimization potential):
    """
    
    for category, amount in top_categories:
        percentage = (amount / total_amount) * 100
        transaction_count = sum(1 for t in transactions if t.get('category') == category)
        avg_per_category = amount / transaction_count if transaction_count > 0 else 0
        formatted_data += f"- {category}: ${amount:,.2f} ({percentage:.1f}%) | {transaction_count} transactions | Avg: ${avg_per_category:,.2f}\n"
    
    formatted_data += "\nTop Vendors by Spend (consolidation opportunities):\n"
    for vendor, amount in top_vendors:
        percentage = (amount / total_amount) * 100
        frequency = vendor_frequency.get(vendor, 0)
        formatted_data += f"- {vendor}: ${amount:,.2f} ({percentage:.1f}%) | {frequency} transactions\n"
    
    # Add subscription analysis
    if likely_subscriptions:
        formatted_data += "\nLikely Recurring Subscriptions/Services:\n"
        for vendor, total, freq, avg in likely_subscriptions:
            formatted_data += f"- {vendor}: ${avg:,.2f}/transaction × {freq} times = ${total:,.2f} total\n"
    
    # Add outlier analysis
    high_value_threshold = avg_amount * 3  # Transactions 3x above average
    outliers = [t for t in transactions if t.get('amount', 0) > high_value_threshold]
    if outliers:
        formatted_data += f"\nHigh-Value Outliers (>${high_value_threshold:,.2f}+):\n"
        for transaction in sorted(outliers, key=lambda x: x.get('amount', 0), reverse=True)[:5]:
            formatted_data += f"- {transaction.get('vendor', 'Unknown')}: ${transaction.get('amount', 0):,.2f} ({transaction.get('category', 'Uncategorized')})\n"
    
    # Monthly spending patterns
    if len(monthly_patterns) > 1:
        formatted_data += "\nMonthly Spending Patterns:\n"
        for month, amount in sorted(monthly_patterns.items())[-6:]:  # Last 6 months
            formatted_data += f"- {month}: ${amount:,.2f}\n"
    
    return formatted_data

def generate_financial_insights(transactions):
    """Generate AI-powered financial insights using GPT-4o"""
    if not openai_client:
        logging.error("OpenAI client not initialized - API key missing")
        return [
            {"priority": "High", "text": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."},
            {"priority": "Medium", "text": "Unable to generate AI insights without API access."},
            {"priority": "Low", "text": "Please check your API configuration and try again."}
        ]
    
    try:
        prompt_template = load_prompt_template()
        transaction_data = format_transactions_for_gpt(transactions)
        
        full_prompt = f"{prompt_template}\n\nTRANSACTION DATA:\n{transaction_data}"
        
        logging.info("Sending request to OpenAI GPT-4o...")
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert financial advisor specializing in business expense optimization. Provide specific, actionable insights based on real transaction data."
                },
                {
                    "role": "user", 
                    "content": full_prompt
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("Empty response from OpenAI")
        result = json.loads(content)
        suggestions = result.get('suggestions', [])
        
        # Validate suggestions format
        validated_suggestions = []
        priorities = ['High', 'Medium', 'Low']
        
        for i, suggestion in enumerate(suggestions):
            if isinstance(suggestion, dict) and 'priority' in suggestion and 'text' in suggestion:
                # Ensure priority is valid
                if suggestion['priority'] not in priorities:
                    suggestion['priority'] = priorities[i % 3]
                validated_suggestions.append(suggestion)
        
        # Ensure we have exactly 3 suggestions
        while len(validated_suggestions) < 3:
            priority = priorities[len(validated_suggestions)]
            validated_suggestions.append({
                "priority": priority,
                "text": f"Review spending patterns in your transaction data for optimization opportunities."
            })
        
        validated_suggestions = validated_suggestions[:3]  # Limit to 3
        
        logging.info(f"Generated {len(validated_suggestions)} financial insights")
        return validated_suggestions
        
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse GPT response as JSON: {str(e)}")
        return [
            {"priority": "High", "text": "AI analysis temporarily unavailable due to response format issue."},
            {"priority": "Medium", "text": "Please try uploading your CSV file again."},
            {"priority": "Low", "text": "Contact support if the issue persists."}
        ]
        
    except Exception as e:
        logging.error(f"Error generating financial insights: {str(e)}")
        return [
            {"priority": "High", "text": f"AI analysis error: {str(e)[:100]}..."},
            {"priority": "Medium", "text": "Please verify your data format and try again."},
            {"priority": "Low", "text": "Consider checking your internet connection and API limits."}
        ]

def test_openai_connection():
    """Test OpenAI API connection"""
    if not openai_client:
        return False, "OpenAI API key not configured"
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )
        return True, "OpenAI connection successful"
    except Exception as e:
        return False, f"OpenAI connection failed: {str(e)}"
