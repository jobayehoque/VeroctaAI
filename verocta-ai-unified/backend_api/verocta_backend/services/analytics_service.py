"""
Analytics Service
SpendScore calculation and financial insights generation
"""

import math
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
from flask import current_app

from ..models import Report, Transaction, Insight
from ..core.database import db


class AnalyticsService:
    """Service for financial analytics and SpendScore calculation"""
    
    def __init__(self):
        self.score_weights = {
            'frequency_score': 0.15,
            'category_diversity': 0.10,
            'budget_adherence': 0.20,
            'redundancy_detection': 0.15,
            'spike_detection': 0.20,
            'waste_ratio': 0.20
        }
    
    def generate_report(self, report_id: int) -> Dict[str, Any]:
        """
        Generate complete analytics report with SpendScore
        """
        try:
            report = Report.query.get(report_id)
            if not report:
                raise ValueError(f"Report {report_id} not found")
            
            # Get transactions
            transactions = report.transactions.all()
            if not transactions:
                raise ValueError("No transactions found for report")
            
            # Calculate SpendScore metrics
            metrics = self._calculate_spend_score_metrics(transactions)
            
            # Calculate overall SpendScore
            spend_score = self._calculate_overall_score(metrics)
            
            # Determine score tier
            score_tier = self._get_score_tier(spend_score)
            
            # Generate AI insights if OpenAI is available
            ai_insights = self._generate_ai_insights(report_id, transactions, metrics)
            
            result = {
                'spend_score': spend_score,
                'score_tier': score_tier,
                'metrics': metrics,
                'ai_insights': ai_insights
            }
            
            current_app.logger.info(f"Generated analytics for report {report_id}: SpendScore {spend_score} ({score_tier})")
            
            return result
            
        except Exception as e:
            current_app.logger.error(f"Analytics generation error: {str(e)}")
            raise
    
    def _calculate_spend_score_metrics(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """Calculate individual SpendScore metrics"""
        
        # Basic transaction analysis
        total_transactions = len(transactions)
        total_amount = sum(abs(t.amount) for t in transactions)
        debit_transactions = [t for t in transactions if t.amount < 0]
        spending_amounts = [abs(t.amount) for t in debit_transactions]
        
        # 1. Frequency Score (15%)
        frequency_score = self._calculate_frequency_score(transactions)
        
        # 2. Category Diversity (10%)
        category_diversity = self._calculate_category_diversity(transactions)
        
        # 3. Budget Adherence (20%)
        budget_adherence = self._calculate_budget_adherence(spending_amounts)
        
        # 4. Redundancy Detection (15%)
        redundancy_detection = self._calculate_redundancy_score(transactions)
        
        # 5. Spike Detection (20%)
        spike_detection = self._calculate_spike_score(spending_amounts)
        
        # 6. Waste Ratio (20%)
        waste_ratio = self._calculate_waste_ratio(transactions)
        
        return {
            'frequency_score': frequency_score,
            'category_diversity': category_diversity,
            'budget_adherence': budget_adherence,
            'redundancy_detection': redundancy_detection,
            'spike_detection': spike_detection,
            'waste_ratio': waste_ratio,
            'total_transactions': total_transactions,
            'total_spending': sum(spending_amounts),
            'average_transaction': sum(spending_amounts) / len(spending_amounts) if spending_amounts else 0
        }
    
    def _calculate_frequency_score(self, transactions: List[Transaction]) -> float:
        """Calculate frequency score based on transaction patterns"""
        if not transactions:
            return 50.0
        
        # Group transactions by day
        daily_counts = defaultdict(int)
        for t in transactions:
            daily_counts[t.transaction_date] += 1
        
        # Calculate variance in daily transaction counts
        counts = list(daily_counts.values())
        if len(counts) < 2:
            return 75.0
        
        mean_count = sum(counts) / len(counts)
        variance = sum((x - mean_count) ** 2 for x in counts) / len(counts)
        
        # Lower variance = more consistent = higher score
        consistency_score = max(0, 100 - (variance * 10))
        
        return min(100, max(0, consistency_score))
    
    def _calculate_category_diversity(self, transactions: List[Transaction]) -> float:
        """Calculate category diversity score"""
        if not transactions:
            return 50.0
        
        # Count categories
        categories = [t.category for t in transactions if t.category]
        if not categories:
            return 50.0
        
        category_counts = Counter(categories)
        num_categories = len(category_counts)
        
        # Optimal number of categories is around 8-12
        if num_categories >= 8 and num_categories <= 12:
            diversity_score = 100.0
        elif num_categories < 8:
            diversity_score = (num_categories / 8) * 80
        else:
            diversity_score = max(60, 100 - ((num_categories - 12) * 5))
        
        return min(100, max(0, diversity_score))
    
    def _calculate_budget_adherence(self, spending_amounts: List[float]) -> float:
        """Calculate budget adherence score"""
        if not spending_amounts:
            return 100.0
        
        # Estimate "budget" as median + 1.5 * IQR
        sorted_amounts = sorted(spending_amounts)
        n = len(sorted_amounts)
        
        if n < 4:
            return 80.0
        
        q1 = sorted_amounts[n // 4]
        q3 = sorted_amounts[3 * n // 4]
        median = sorted_amounts[n // 2]
        iqr = q3 - q1
        
        estimated_budget = median + 1.5 * iqr
        
        # Count transactions within budget
        within_budget = sum(1 for amount in spending_amounts if amount <= estimated_budget)
        adherence_rate = within_budget / len(spending_amounts)
        
        return adherence_rate * 100
    
    def _calculate_redundancy_score(self, transactions: List[Transaction]) -> float:
        """Calculate redundancy/duplicate detection score"""
        if not transactions:
            return 100.0
        
        # Group similar transactions
        similar_groups = defaultdict(list)
        
        for t in transactions:
            # Create a simplified description key
            key = self._simplify_description(t.description)
            similar_groups[key].append(t)
        
        # Count potential duplicates
        total_transactions = len(transactions)
        duplicate_count = 0
        
        for group in similar_groups.values():
            if len(group) > 1:
                # Check if transactions are close in time and amount
                group.sort(key=lambda x: x.transaction_date)
                for i in range(1, len(group)):
                    prev_t = group[i-1]
                    curr_t = group[i]
                    
                    # Same day and similar amount = potential duplicate
                    if (curr_t.transaction_date - prev_t.transaction_date).days <= 1:
                        if abs(curr_t.amount - prev_t.amount) < 0.01:
                            duplicate_count += 1
        
        duplicate_rate = duplicate_count / total_transactions if total_transactions > 0 else 0
        redundancy_score = max(0, 100 - (duplicate_rate * 200))  # Penalize duplicates heavily
        
        return min(100, max(0, redundancy_score))
    
    def _calculate_spike_score(self, spending_amounts: List[float]) -> float:
        """Calculate spending spike detection score"""
        if len(spending_amounts) < 3:
            return 90.0
        
        mean_amount = sum(spending_amounts) / len(spending_amounts)
        std_dev = math.sqrt(sum((x - mean_amount) ** 2 for x in spending_amounts) / len(spending_amounts))
        
        if std_dev == 0:
            return 95.0
        
        # Count transactions that are more than 2 standard deviations above mean
        spike_count = sum(1 for amount in spending_amounts if amount > mean_amount + 2 * std_dev)
        spike_rate = spike_count / len(spending_amounts)
        
        # Lower spike rate = higher score
        spike_score = max(0, 100 - (spike_rate * 300))
        
        return min(100, max(0, spike_score))
    
    def _calculate_waste_ratio(self, transactions: List[Transaction]) -> float:
        """Calculate waste/non-essential spending ratio"""
        if not transactions:
            return 80.0
        
        # Keywords that indicate non-essential spending
        waste_keywords = [
            'entertainment', 'gaming', 'subscription', 'streaming', 
            'restaurant', 'takeout', 'coffee', 'bar', 'alcohol',
            'luxury', 'premium', 'designer', 'brand'
        ]
        
        total_spending = 0
        waste_spending = 0
        
        for t in transactions:
            if t.amount < 0:  # Only count spending (negative amounts)
                amount = abs(t.amount)
                total_spending += amount
                
                description_lower = t.description.lower()
                if any(keyword in description_lower for keyword in waste_keywords):
                    waste_spending += amount
        
        if total_spending == 0:
            return 80.0
        
        waste_ratio = waste_spending / total_spending
        waste_score = max(0, 100 - (waste_ratio * 150))  # Penalize high waste ratios
        
        return min(100, max(0, waste_score))
    
    def _calculate_overall_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate weighted overall SpendScore"""
        total_score = 0.0
        
        for metric, weight in self.score_weights.items():
            if metric in metrics:
                total_score += metrics[metric] * weight
        
        return round(total_score, 1)
    
    def _get_score_tier(self, score: float) -> str:
        """Get score tier based on SpendScore value"""
        if score >= 90:
            return 'Green'
        elif score >= 70:
            return 'Amber'
        else:
            return 'Red'
    
    def _simplify_description(self, description: str) -> str:
        """Simplify transaction description for duplicate detection"""
        # Remove common transaction details
        simplified = description.lower()
        # Remove numbers, dates, and common transaction codes
        import re
        simplified = re.sub(r'\d+', '', simplified)
        simplified = re.sub(r'[^\w\s]', '', simplified)
        simplified = ' '.join(simplified.split()[:3])  # First 3 words only
        return simplified.strip()
    
    def _generate_ai_insights(self, report_id: int, transactions: List[Transaction], metrics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate AI insights using OpenAI (if available)"""
        try:
            import os
            
            openai_key = os.environ.get("OPENAI_API_KEY")
            if not openai_key:
                current_app.logger.info("OpenAI API key not available, skipping AI insights")
                return None
            
            # This would call OpenAI API - simplified for now
            # In production, this would be moved to a background task
            
            insights = {
                'summary': f"Analysis of {len(transactions)} transactions with SpendScore of {metrics.get('spend_score', 0)}",
                'recommendations': [
                    "Consider reviewing high-frequency spending categories",
                    "Monitor unusual transaction spikes",
                    "Optimize recurring subscription expenses"
                ],
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return insights
            
        except Exception as e:
            current_app.logger.error(f"AI insights generation error: {str(e)}")
            return None
    
    def get_spending_trends(self, report_id: int) -> Dict[str, Any]:
        """Get spending trends analysis"""
        report = Report.query.get(report_id)
        if not report:
            raise ValueError(f"Report {report_id} not found")
        
        transactions = report.transactions.filter(Transaction.amount < 0).all()  # Only spending
        
        # Group by date
        daily_spending = defaultdict(float)
        for t in transactions:
            daily_spending[t.transaction_date.isoformat()] += abs(t.amount)
        
        # Calculate trend
        dates = sorted(daily_spending.keys())
        amounts = [daily_spending[date] for date in dates]
        
        trend = "stable"
        if len(amounts) > 1:
            recent_avg = sum(amounts[-7:]) / min(7, len(amounts))
            overall_avg = sum(amounts) / len(amounts)
            
            if recent_avg > overall_avg * 1.2:
                trend = "increasing"
            elif recent_avg < overall_avg * 0.8:
                trend = "decreasing"
        
        return {
            'daily_spending': dict(daily_spending),
            'trend': trend,
            'total_days': len(dates),
            'average_daily_spending': sum(amounts) / len(amounts) if amounts else 0
        }
    
    def get_category_analysis(self, report_id: int) -> Dict[str, Any]:
        """Get spending by category analysis"""
        report = Report.query.get(report_id)
        if not report:
            raise ValueError(f"Report {report_id} not found")
        
        transactions = report.transactions.filter(Transaction.amount < 0).all()  # Only spending
        
        # Group by category
        category_spending = defaultdict(float)
        category_counts = defaultdict(int)
        
        for t in transactions:
            category = t.category or 'Uncategorized'
            amount = abs(t.amount)
            category_spending[category] += amount
            category_counts[category] += 1
        
        # Calculate percentages
        total_spending = sum(category_spending.values())
        
        categories = []
        for category, amount in category_spending.items():
            percentage = (amount / total_spending * 100) if total_spending > 0 else 0
            categories.append({
                'name': category,
                'amount': round(amount, 2),
                'percentage': round(percentage, 1),
                'transaction_count': category_counts[category]
            })
        
        # Sort by amount descending
        categories.sort(key=lambda x: x['amount'], reverse=True)
        
        return {
            'categories': categories,
            'total_spending': round(total_spending, 2),
            'top_category': categories[0] if categories else None
        }