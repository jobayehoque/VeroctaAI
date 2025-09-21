"""
AI Service for GPT-4o Integration
"""

import os
import json
import logging
from typing import List, Dict, Any

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not installed. AI features will not work.")

class AIService:
    """AI-powered insights generation service"""
    
    def __init__(self):
        self.openai_client = None
        if OPENAI_AVAILABLE and os.environ.get('OPENAI_API_KEY'):
            try:
                self.openai_client = openai.OpenAI(
                    api_key=os.environ.get('OPENAI_API_KEY')
                )
                logging.info("OpenAI client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize OpenAI client: {e}")
    
    def generate_insights(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate AI-powered financial insights"""
        if not self.openai_client:
            return self._get_fallback_insights()
        
        try:
            prompt_template = self._load_prompt_template()
            transaction_data = self._format_transactions_for_gpt(transactions)
            
            full_prompt = f"{prompt_template}\n\nTRANSACTION DATA:\n{transaction_data}"
            
            logging.info("Sending request to OpenAI GPT-4o...")
            
            response = self.openai_client.chat.completions.create(
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
                    priority = suggestion['priority']
                    text = suggestion['text']
                    
                    if priority in priorities and text.strip():
                        validated_suggestions.append({
                            'priority': priority,
                            'text': text.strip()
                        })
                
                # Limit to 3 suggestions
                if len(validated_suggestions) >= 3:
                    break
            
            # Ensure we have exactly 3 suggestions
            while len(validated_suggestions) < 3:
                validated_suggestions.append({
                    'priority': 'Low',
                    'text': 'Continue monitoring your spending patterns for optimization opportunities'
                })
            
            return validated_suggestions
            
        except Exception as e:
            logging.error(f"AI insights generation failed: {e}")
            return self._get_fallback_insights()
    
    def _load_prompt_template(self) -> str:
        """Load the prompt template for GPT analysis"""
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
    
    def _format_transactions_for_gpt(self, transactions: List[Dict[str, Any]]) -> str:
        """Format transaction data for GPT analysis"""
        if not transactions:
            return "No transaction data available."
        
        # Create comprehensive statistics
        total_amount = sum(t['amount'] for t in transactions)
        avg_amount = total_amount / len(transactions)
        
        # Enhanced breakdowns
        categories = {}
        vendors = {}
        vendor_frequency = {}
        
        for transaction in transactions:
            category = transaction.get('category', 'Uncategorized')
            vendor = transaction.get('vendor', 'Unknown')
            amount = transaction.get('amount', 0)
            
            categories[category] = categories.get(category, 0) + amount
            vendors[vendor] = vendors.get(vendor, 0) + amount
            vendor_frequency[vendor] = vendor_frequency.get(vendor, 0) + 1
        
        # Sort by amount and identify patterns
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
        top_vendors = sorted(vendors.items(), key=lambda x: x[1], reverse=True)[:15]
        
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
        
        # Add outlier analysis
        high_value_threshold = avg_amount * 3  # Transactions 3x above average
        outliers = [t for t in transactions if t.get('amount', 0) > high_value_threshold]
        if outliers:
            formatted_data += f"\nHigh-Value Transactions (${high_value_threshold:,.2f}+):\n"
            for outlier in outliers[:5]:  # Show top 5 outliers
                formatted_data += f"- {outlier.get('description', 'Unknown')}: ${outlier.get('amount', 0):,.2f}\n"
        
        return formatted_data
    
    def _get_fallback_insights(self) -> List[Dict[str, str]]:
        """Get fallback insights when AI is not available"""
        return [
            {
                "priority": "High", 
                "text": "Review your spending patterns and identify opportunities for cost optimization"
            },
            {
                "priority": "Medium", 
                "text": "Consider implementing automated expense categorization for better tracking"
            },
            {
                "priority": "Low", 
                "text": "Set up budget alerts for key spending categories to maintain control"
            }
        ]
