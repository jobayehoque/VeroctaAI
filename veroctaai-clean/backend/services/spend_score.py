"""
SpendScore Calculation Service
"""

import logging
import math
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from statistics import median, mean
from typing import List, Dict, Any, Tuple

class SpendScoreService:
    """Enhanced SpendScore calculation service"""
    
    # Metric weights as per requirements
    WEIGHTS = {
        'frequency_score': 15,      # How often transactions occur in certain categories
        'category_diversity': 10,   # Number of distinct categories used
        'budget_adherence': 20,     # Actual spend vs benchmark/limit
        'redundancy_detection': 15, # Repeated vendor/expense types within short timespan
        'spike_detection': 20,      # Outlier or one-time big spends
        'waste_ratio': 20          # Spending on low-value/non-essential categories
    }
    
    # Category classifications for waste detection
    ESSENTIAL_CATEGORIES = {
        'utilities', 'rent', 'mortgage', 'insurance', 'groceries', 'fuel',
        'medical', 'healthcare', 'transportation', 'education', 'childcare'
    }
    
    LOW_VALUE_CATEGORIES = {
        'entertainment', 'gaming', 'subscriptions', 'luxury', 'dining',
        'fast food', 'coffee', 'alcohol', 'tobacco', 'impulse purchases'
    }
    
    def calculate_spend_score(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive SpendScore"""
        try:
            if not transactions:
                return self._get_default_score()
            
            # Prepare data
            self._prepare_data(transactions)
            
            # Calculate individual metrics
            metrics = {
                'frequency_score': self._calculate_frequency_score(),
                'category_diversity': self._calculate_category_diversity(),
                'budget_adherence': self._calculate_budget_adherence(),
                'redundancy_detection': self._calculate_redundancy_detection(),
                'spike_detection': self._calculate_spike_detection(),
                'waste_ratio': self._calculate_waste_ratio()
            }
            
            # Calculate weighted final score
            final_score = sum(
                metrics[metric] * (self.WEIGHTS[metric] / 100)
                for metric in metrics
            )
            
            # Get tier information
            tier_info = self._get_score_tier(final_score)
            
            return {
                'final_score': round(final_score, 1),
                'score_breakdown': metrics,
                'tier_info': tier_info,
                'transaction_summary': {
                    'total_transactions': self.num_transactions,
                    'total_amount': self.total_amount,
                    'median_amount': self.median_amount,
                    'mean_amount': self.mean_amount,
                    'unique_categories': len(self.category_spending),
                    'unique_vendors': len(self.vendor_spending)
                }
            }
            
        except Exception as e:
            logging.error(f"SpendScore calculation error: {e}")
            return self._get_default_score()
    
    def _prepare_data(self, transactions: List[Dict[str, Any]]):
        """Prepare transaction data for analysis"""
        self.transactions = transactions
        self.total_amount = sum(t.get('amount', 0) for t in transactions)
        self.num_transactions = len(transactions)
        
        # Calculate basic statistics
        amounts = [t.get('amount', 0) for t in transactions if t.get('amount')]
        self.median_amount = median(amounts) if amounts else 0
        self.mean_amount = mean(amounts) if amounts else 0
        
        # Categorize spending
        self.category_spending = defaultdict(float)
        self.vendor_spending = defaultdict(float)
        self.vendor_frequency = defaultdict(int)
        
        for transaction in transactions:
            category = transaction.get('category', 'Unknown').lower()
            vendor = transaction.get('vendor', 'Unknown').lower()
            amount = transaction.get('amount', 0)
            
            self.category_spending[category] += amount
            self.vendor_spending[vendor] += amount
            self.vendor_frequency[vendor] += 1
    
    def _calculate_frequency_score(self) -> float:
        """Calculate frequency score based on transaction patterns"""
        try:
            if not self.transactions:
                return 50
            
            # Analyze transaction frequency patterns
            daily_transactions = defaultdict(int)
            for transaction in self.transactions:
                date = transaction.get('date')
                if date:
                    if isinstance(date, str):
                        date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    daily_transactions[date.date()] += 1
            
            if not daily_transactions:
                return 50
            
            # Calculate consistency score
            frequencies = list(daily_transactions.values())
            avg_frequency = mean(frequencies)
            frequency_variance = sum((f - avg_frequency) ** 2 for f in frequencies) / len(frequencies)
            
            # Lower variance = higher score
            consistency_score = max(0, 100 - (frequency_variance * 10))
            return min(100, consistency_score)
            
        except Exception:
            return 50
    
    def _calculate_category_diversity(self) -> float:
        """Calculate category diversity score"""
        try:
            if not self.category_spending:
                return 50
            
            num_categories = len(self.category_spending)
            
            # Optimal range is 5-15 categories
            if 5 <= num_categories <= 15:
                return 100
            elif num_categories < 5:
                return num_categories * 20  # 0-80 for 0-4 categories
            else:
                # Penalty for too many categories (over-fragmentation)
                return max(50, 100 - ((num_categories - 15) * 2))
                
        except Exception:
            return 50
    
    def _calculate_budget_adherence(self) -> float:
        """Calculate budget adherence score"""
        try:
            # This is a simplified version - in production, you'd compare against actual budgets
            if not self.transactions:
                return 50
            
            # Calculate monthly spending pattern
            monthly_spending = defaultdict(float)
            for transaction in self.transactions:
                date = transaction.get('date')
                if date:
                    if isinstance(date, str):
                        date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    month_key = date.strftime('%Y-%m')
                    monthly_spending[month_key] += transaction.get('amount', 0)
            
            if len(monthly_spending) < 2:
                return 75  # Default good score for insufficient data
            
            # Calculate spending consistency
            amounts = list(monthly_spending.values())
            avg_monthly = mean(amounts)
            variance = sum((amount - avg_monthly) ** 2 for amount in amounts) / len(amounts)
            
            # Lower variance = better budget adherence
            adherence_score = max(0, 100 - (variance / avg_monthly) * 50)
            return min(100, adherence_score)
            
        except Exception:
            return 50
    
    def _calculate_redundancy_detection(self) -> float:
        """Calculate redundancy detection score"""
        try:
            if not self.transactions:
                return 50
            
            redundancy_penalty = 0
            
            # Check for duplicate transactions (same vendor, similar amount, close date)
            for i, t1 in enumerate(self.transactions):
                for j, t2 in enumerate(self.transactions[i+1:], i+1):
                    if self._is_duplicate_transaction(t1, t2):
                        redundancy_penalty += 10
            
            # Check for vendor frequency (too many transactions with same vendor)
            for vendor, frequency in self.vendor_frequency.items():
                if frequency > 10:  # More than 10 transactions with same vendor
                    redundancy_penalty += 5
            
            redundancy_score = max(0, 100 - redundancy_penalty)
            return min(100, redundancy_score)
            
        except Exception:
            return 50
    
    def _calculate_spike_detection(self) -> float:
        """Calculate spike detection score"""
        try:
            if not self.transactions:
                return 50
            
            amounts = [t.get('amount', 0) for t in self.transactions if t.get('amount')]
            if not amounts:
                return 50
            
            # Calculate outliers (transactions significantly above average)
            avg_amount = mean(amounts)
            std_dev = math.sqrt(sum((amount - avg_amount) ** 2 for amount in amounts) / len(amounts))
            
            spike_count = 0
            for amount in amounts:
                if amount > avg_amount + (2 * std_dev):  # 2 standard deviations above mean
                    spike_count += 1
            
            # Fewer spikes = higher score
            spike_ratio = spike_count / len(amounts)
            spike_score = max(0, 100 - (spike_ratio * 200))
            return min(100, spike_score)
            
        except Exception:
            return 50
    
    def _calculate_waste_ratio(self) -> float:
        """Calculate waste ratio score"""
        try:
            if not self.category_spending:
                return 50
            
            essential_spending = 0
            low_value_spending = 0
            total_spending = sum(self.category_spending.values())
            
            for category, amount in self.category_spending.items():
                if category in self.ESSENTIAL_CATEGORIES:
                    essential_spending += amount
                elif category in self.LOW_VALUE_CATEGORIES:
                    low_value_spending += amount
            
            if total_spending == 0:
                return 50
            
            # Calculate waste ratio
            waste_ratio = low_value_spending / total_spending
            essential_ratio = essential_spending / total_spending
            
            # Higher essential ratio and lower waste ratio = higher score
            waste_score = (essential_ratio * 100) - (waste_ratio * 50)
            return max(0, min(100, waste_score))
            
        except Exception:
            return 50
    
    def _is_duplicate_transaction(self, t1: Dict, t2: Dict) -> bool:
        """Check if two transactions are duplicates"""
        try:
            # Same vendor
            if t1.get('vendor', '').lower() != t2.get('vendor', '').lower():
                return False
            
            # Similar amount (within 5%)
            amount1 = t1.get('amount', 0)
            amount2 = t2.get('amount', 0)
            if abs(amount1 - amount2) / max(amount1, amount2) > 0.05:
                return False
            
            # Close dates (within 7 days)
            date1 = t1.get('date')
            date2 = t2.get('date')
            if date1 and date2:
                if isinstance(date1, str):
                    date1 = datetime.fromisoformat(date1.replace('Z', '+00:00'))
                if isinstance(date2, str):
                    date2 = datetime.fromisoformat(date2.replace('Z', '+00:00'))
                
                if abs((date1 - date2).days) > 7:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _get_score_tier(self, score: float) -> Dict[str, Any]:
        """Get traffic light tier and reward eligibility"""
        if score >= 90:
            return {
                'color': 'Green',
                'tier': 'Excellent',
                'green_reward_eligible': True,
                'description': 'Outstanding financial management!'
            }
        elif score >= 70:
            return {
                'color': 'Amber',
                'tier': 'Good',
                'green_reward_eligible': False,
                'description': 'Good financial habits with room for improvement'
            }
        else:
            return {
                'color': 'Red',
                'tier': 'Needs Improvement',
                'green_reward_eligible': False,
                'description': 'Significant opportunities for financial optimization'
            }
    
    def _get_default_score(self) -> Dict[str, Any]:
        """Get default score when calculation fails"""
        return {
            'final_score': 50.0,
            'score_breakdown': {
                'frequency_score': 50,
                'category_diversity': 50,
                'budget_adherence': 50,
                'redundancy_detection': 50,
                'spike_detection': 50,
                'waste_ratio': 50
            },
            'tier_info': {
                'color': 'Red',
                'tier': 'Needs Improvement',
                'green_reward_eligible': False,
                'description': 'Unable to calculate score - please check your data'
            },
            'transaction_summary': {
                'total_transactions': 0,
                'total_amount': 0,
                'median_amount': 0,
                'mean_amount': 0,
                'unique_categories': 0,
                'unique_vendors': 0
            }
        }
