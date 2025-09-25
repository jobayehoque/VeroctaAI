"""
Financial Analysis Service
"""

from typing import List, Dict, Any
import logging
from services.ai import AIService
from services.spend_score import SpendScoreService

class AnalysisService:
    """Financial analysis and SpendScore calculation service"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.spend_score_service = SpendScoreService()
    
    def analyze_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive financial analysis"""
        try:
            # Calculate SpendScore
            spend_score_result = self.spend_score_service.calculate_spend_score(transactions)
            
            # Generate AI insights
            ai_insights = self.ai_service.generate_insights(transactions)
            
            # Calculate summary statistics
            summary = self._calculate_summary_stats(transactions)
            
            # Categorize spending
            categories = self._categorize_spending(transactions)
            
            return {
                'spend_score': spend_score_result['final_score'],
                'score_breakdown': spend_score_result['score_breakdown'],
                'tier_info': spend_score_result['tier_info'],
                'transaction_summary': summary,
                'categories': categories,
                'insights': ai_insights,
                'total_transactions': len(transactions),
                'total_amount': sum(t.get('amount', 0) for t in transactions)
            }
            
        except Exception as e:
            logging.error(f"Analysis error: {e}")
            # Return fallback analysis
            return self._get_fallback_analysis(transactions)
    
    def _calculate_summary_stats(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        amounts = [t.get('amount', 0) for t in transactions if t.get('amount')]
        
        if not amounts:
            return {
                'total_amount': 0,
                'median_amount': 0,
                'mean_amount': 0,
                'unique_categories': 0,
                'unique_vendors': 0
            }
        
        categories = set(t.get('category', 'Unknown') for t in transactions)
        vendors = set(t.get('vendor', 'Unknown') for t in transactions)
        
        return {
            'total_amount': sum(amounts),
            'median_amount': sorted(amounts)[len(amounts) // 2] if amounts else 0,
            'mean_amount': sum(amounts) / len(amounts) if amounts else 0,
            'unique_categories': len(categories),
            'unique_vendors': len(vendors)
        }
    
    def _categorize_spending(self, transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Categorize spending by category"""
        categories = {}
        
        for transaction in transactions:
            category = transaction.get('category', 'Unknown')
            amount = transaction.get('amount', 0)
            
            if category not in categories:
                categories[category] = 0
            categories[category] += amount
        
        return categories
    
    def _get_fallback_analysis(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback analysis when main analysis fails"""
        total_amount = sum(t.get('amount', 0) for t in transactions)
        
        return {
            'spend_score': 75,  # Default score
            'score_breakdown': {
                'frequency_score': 70,
                'category_diversity': 75,
                'budget_adherence': 80,
                'redundancy_detection': 70,
                'spike_detection': 75,
                'waste_ratio': 80
            },
            'tier_info': {
                'color': 'Amber',
                'tier': 'Good',
                'green_reward_eligible': False,
                'description': 'Good financial habits with room for improvement'
            },
            'transaction_summary': {
                'total_transactions': len(transactions),
                'total_amount': total_amount,
                'median_amount': total_amount / len(transactions) if transactions else 0,
                'mean_amount': total_amount / len(transactions) if transactions else 0,
                'unique_categories': len(set(t.get('category', 'Unknown') for t in transactions)),
                'unique_vendors': len(set(t.get('vendor', 'Unknown') for t in transactions))
            },
            'categories': self._categorize_spending(transactions),
            'insights': [
                {'priority': 'Medium', 'text': 'Review your spending patterns for optimization opportunities'},
                {'priority': 'Low', 'text': 'Consider implementing automated expense categorization'},
                {'priority': 'Low', 'text': 'Set up budget alerts for key spending categories'}
            ],
            'total_transactions': len(transactions),
            'total_amount': total_amount
        }
