"""
VeroctaAI SpendScore Engine - Enhanced Version
Complete logic breakdown with weighted metrics as per requirements
"""

import logging
import math
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from statistics import median, mean
from typing import List, Dict, Any, Tuple

class SpendScoreEngine:
    """Enhanced SpendScore calculation engine with detailed metrics"""
    
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
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        """Initialize with transaction data"""
        self.transactions = transactions
        self.total_amount = sum(t.get('amount', 0) for t in transactions)
        self.num_transactions = len(transactions)
        self.score_breakdown = {}
        
        # Process transaction data
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and clean transaction data for analysis"""
        try:
            # Extract amounts and ensure numeric values
            self.amounts = [float(t.get('amount', 0)) for t in self.transactions]
            
            # Calculate median instead of average (as per requirements)
            self.median_amount = median(self.amounts) if self.amounts else 0
            self.mean_amount = mean(self.amounts) if self.amounts else 0
            
            # Group by categories and vendors
            self.category_spending = defaultdict(float)
            self.vendor_spending = defaultdict(float)
            self.vendor_frequency = defaultdict(int)
            
            # Process dates
            self.transaction_dates = []
            
            for transaction in self.transactions:
                # Category grouping
                category = self._normalize_category(transaction.get('category', 'Uncategorized'))
                amount = float(transaction.get('amount', 0))
                self.category_spending[category] += amount
                
                # Vendor grouping
                vendor = transaction.get('vendor', 'Unknown')
                self.vendor_spending[vendor] += amount
                self.vendor_frequency[vendor] += 1
                
                # Date processing
                date = transaction.get('date')
                if date:
                    if isinstance(date, str):
                        try:
                            date = datetime.strptime(date, '%Y-%m-%d')
                        except:
                            try:
                                date = datetime.strptime(date, '%m/%d/%Y')
                            except:
                                continue
                    self.transaction_dates.append(date)
            
            self.transaction_dates.sort()
            
        except Exception as e:
            logging.error(f"Error preparing data: {str(e)}")
            self.amounts = [0]
            self.median_amount = 0
            self.mean_amount = 0
    
    def _normalize_category(self, category: str) -> str:
        """Normalize category names for consistent analysis"""
        if not category:
            return 'Uncategorized'
        
        category = category.lower().strip()
        
        # Map common variations to standard categories
        category_mappings = {
            'food': 'groceries',
            'gas': 'fuel',
            'petrol': 'fuel',
            'restaurant': 'dining',
            'cafe': 'coffee',
            'subscription': 'subscriptions',
            'streaming': 'subscriptions',
            'electric': 'utilities',
            'water': 'utilities',
            'internet': 'utilities',
            'phone': 'utilities'
        }
        
        for key, value in category_mappings.items():
            if key in category:
                return value
        
        return category
    
    def calculate_frequency_score(self) -> float:
        """
        Calculate frequency score (15% weight)
        Measures how often transactions occur in certain categories
        """
        try:
            if not self.category_spending:
                return 0.0
            
            # Calculate transaction frequency by category
            category_frequencies = defaultdict(int)
            for transaction in self.transactions:
                category = self._normalize_category(transaction.get('category', 'Uncategorized'))
                category_frequencies[category] += 1
            
            # Calculate frequency distribution score
            total_transactions = sum(category_frequencies.values())
            frequency_scores = []
            
            for category, frequency in category_frequencies.items():
                frequency_ratio = frequency / total_transactions
                
                # Optimal frequency range: 5-25% per category
                if 0.05 <= frequency_ratio <= 0.25:
                    frequency_scores.append(100)
                elif frequency_ratio < 0.05:
                    # Too infrequent
                    frequency_scores.append(frequency_ratio / 0.05 * 100)
                else:
                    # Too frequent (over-concentration)
                    frequency_scores.append(max(0, 100 * (1 - (frequency_ratio - 0.25) / 0.75)))
            
            score = mean(frequency_scores) if frequency_scores else 0
            self.score_breakdown['frequency_score'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating frequency score: {str(e)}")
            return 50.0
    
    def calculate_category_diversity(self) -> float:
        """
        Calculate category diversity score (10% weight)
        Number of distinct categories used
        """
        try:
            unique_categories = len(self.category_spending)
            
            # Optimal range: 5-15 categories
            if 5 <= unique_categories <= 15:
                score = 100
            elif unique_categories < 5:
                # Too few categories
                score = (unique_categories / 5) * 100
            else:
                # Too many categories (might indicate poor categorization)
                score = max(0, 100 - (unique_categories - 15) * 5)
            
            self.score_breakdown['category_diversity'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating category diversity: {str(e)}")
            return 50.0
    
    def calculate_budget_adherence(self) -> float:
        """
        Calculate budget adherence score (20% weight)
        Actual spend vs benchmark/limit based on transaction patterns
        """
        try:
            if not self.amounts:
                return 0.0
            
            # Use median as benchmark (more robust than mean)
            benchmark = self.median_amount
            
            # Calculate adherence based on variation from median
            adherence_scores = []
            for amount in self.amounts:
                if benchmark > 0:
                    deviation = abs(amount - benchmark) / benchmark
                    # Score decreases with higher deviation
                    adherence_score = max(0, 100 * (1 - min(deviation, 2) / 2))
                    adherence_scores.append(adherence_score)
            
            score = mean(adherence_scores) if adherence_scores else 50
            self.score_breakdown['budget_adherence'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating budget adherence: {str(e)}")
            return 50.0
    
    def calculate_redundancy_detection(self) -> float:
        """
        Calculate redundancy detection score (15% weight)
        Repeated vendor/expense types within short timespan
        """
        try:
            if len(self.transaction_dates) < 2:
                return 100.0  # No redundancy possible with <2 transactions
            
            # Group transactions by vendor and date
            vendor_dates = defaultdict(list)
            for i, transaction in enumerate(self.transactions):
                vendor = transaction.get('vendor', 'Unknown')
                if i < len(self.transaction_dates):
                    vendor_dates[vendor].append(self.transaction_dates[i])
            
            redundancy_penalties = []
            
            # Check for transactions with same vendor within 24 hours
            for vendor, dates in vendor_dates.items():
                if len(dates) > 1:
                    dates.sort()
                    for i in range(len(dates) - 1):
                        time_diff = (dates[i + 1] - dates[i]).total_seconds() / 3600  # hours
                        if time_diff <= 24:  # Within 24 hours
                            penalty = max(0, 100 - time_diff * 2)  # Higher penalty for closer transactions
                            redundancy_penalties.append(penalty)
            
            if redundancy_penalties:
                avg_penalty = mean(redundancy_penalties)
                score = max(0, 100 - avg_penalty)
            else:
                score = 100  # No redundancy detected
            
            self.score_breakdown['redundancy_detection'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating redundancy detection: {str(e)}")
            return 75.0
    
    def calculate_spike_detection(self) -> float:
        """
        Calculate spike detection score (20% weight)
        Outlier or one-time big spends
        """
        try:
            if not self.amounts:
                return 0.0
            
            # Calculate outliers using IQR method
            sorted_amounts = sorted(self.amounts)
            n = len(sorted_amounts)
            
            if n < 4:
                return 100.0  # Not enough data for outlier detection
            
            q1 = sorted_amounts[n // 4]
            q3 = sorted_amounts[3 * n // 4]
            iqr = q3 - q1
            
            # Define outlier threshold
            outlier_threshold = q3 + 1.5 * iqr
            
            # Count outliers and calculate their impact
            outliers = [amount for amount in self.amounts if amount > outlier_threshold]
            outlier_ratio = len(outliers) / len(self.amounts)
            
            # Calculate severity of outliers
            if outliers and self.median_amount > 0:
                max_outlier = max(outliers)
                outlier_severity = max_outlier / self.median_amount
                
                # Score decreases with more outliers and higher severity
                score = max(0, 100 * (1 - outlier_ratio) * (1 - min(outlier_severity / 10, 1)))
            else:
                score = 100
            
            self.score_breakdown['spike_detection'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating spike detection: {str(e)}")
            return 75.0
    
    def calculate_waste_ratio(self) -> float:
        """
        Calculate waste ratio score (20% weight)
        Spending on low-value/non-essential categories
        """
        try:
            if not self.category_spending:
                return 50.0
            
            total_spending = sum(self.category_spending.values())
            
            # Calculate spending on low-value categories
            low_value_spending = 0
            essential_spending = 0
            
            for category, amount in self.category_spending.items():
                category_lower = category.lower()
                
                if any(lv_cat in category_lower for lv_cat in self.LOW_VALUE_CATEGORIES):
                    low_value_spending += amount
                elif any(es_cat in category_lower for es_cat in self.ESSENTIAL_CATEGORIES):
                    essential_spending += amount
            
            # Calculate waste ratio
            if total_spending > 0:
                waste_ratio = low_value_spending / total_spending
                essential_ratio = essential_spending / total_spending
                
                # Score based on waste ratio (lower is better)
                waste_score = max(0, 100 * (1 - waste_ratio))
                
                # Bonus for high essential spending
                essential_bonus = min(20, essential_ratio * 40)
                
                score = min(100, waste_score + essential_bonus)
            else:
                score = 50
            
            self.score_breakdown['waste_ratio'] = round(score, 2)
            return score
            
        except Exception as e:
            logging.error(f"Error calculating waste ratio: {str(e)}")
            return 50.0
    
    def calculate_spend_score(self) -> float:
        """
        Calculate final weighted SpendScore (0-100)
        Normalized and rounded as per requirements
        """
        try:
            # Calculate individual metric scores
            scores = {
                'frequency_score': self.calculate_frequency_score(),
                'category_diversity': self.calculate_category_diversity(),
                'budget_adherence': self.calculate_budget_adherence(),
                'redundancy_detection': self.calculate_redundancy_detection(),
                'spike_detection': self.calculate_spike_detection(),
                'waste_ratio': self.calculate_waste_ratio()
            }
            
            # Apply weights and calculate final score
            weighted_score = 0
            total_weight = sum(self.WEIGHTS.values())
            
            for metric, score in scores.items():
                weight = self.WEIGHTS.get(metric, 0)
                weighted_score += (score * weight / 100)
            
            # Normalize to 0-100 range
            final_score = (weighted_score / total_weight) * 100
            
            # Round to nearest whole number as per requirements
            final_score = round(final_score)
            
            # Store detailed breakdown
            self.score_breakdown['final_score'] = final_score
            self.score_breakdown['individual_scores'] = scores
            
            logging.info(f"SpendScore calculation complete: {final_score}")
            logging.info(f"Score breakdown: {self.score_breakdown}")
            
            return final_score
            
        except Exception as e:
            logging.error(f"Error calculating final spend score: {str(e)}")
            return 50
    
    def get_score_tier(self, score: float) -> Dict[str, Any]:
        """
        Get traffic light tier and reward eligibility
        Red: 0-69, Amber: 70-89, Green: 90-100
        """
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
    
    def get_detailed_analysis(self) -> Dict[str, Any]:
        """Get comprehensive analysis results"""
        final_score = self.calculate_spend_score()
        tier_info = self.get_score_tier(final_score)
        
        return {
            'final_score': final_score,
            'tier_info': tier_info,
            'score_breakdown': self.score_breakdown,
            'transaction_summary': {
                'total_transactions': self.num_transactions,
                'total_amount': self.total_amount,
                'median_amount': self.median_amount,
                'mean_amount': self.mean_amount,
                'unique_categories': len(self.category_spending),
                'unique_vendors': len(self.vendor_spending)
            }
        }


def calculate_spend_score(transactions: List[Dict[str, Any]]) -> float:
    """
    Main function to calculate SpendScore using the enhanced engine
    Compatible with existing codebase
    """
    engine = SpendScoreEngine(transactions)
    return engine.calculate_spend_score()


def get_score_label(score: float) -> str:
    """Get score label based on enhanced tiers"""
    engine = SpendScoreEngine([])  # Empty engine for tier calculation
    tier_info = engine.get_score_tier(score)
    return tier_info['tier']


def get_score_color(score: float) -> str:
    """Get traffic light color for score"""
    engine = SpendScoreEngine([])  # Empty engine for tier calculation
    tier_info = engine.get_score_tier(score)
    return tier_info['color']


def get_enhanced_analysis(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get complete enhanced analysis"""
    engine = SpendScoreEngine(transactions)
    return engine.get_detailed_analysis()
