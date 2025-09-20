from datetime import datetime
from typing import Dict, List, Optional, Any

# Simple in-memory data store (replace with database in production)
reports_db = {}
next_report_id = 1

class Report:
    def __init__(self, title: str, user_id: int, company: str, data: Dict[str, Any], spend_score: Optional[int] = None, insights: Optional[Dict[str, Any]] = None):
        global next_report_id
        self.id = next_report_id
        next_report_id += 1
        self.title = title
        self.user_id = user_id
        self.company = company
        self.data = data
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = 'completed'
        self.spend_score = spend_score if spend_score is not None else self._calculate_mock_score()
        self.insights = insights if insights is not None else self._generate_mock_insights()
        
    def _calculate_mock_score(self) -> int:
        """Generate a mock SpendScore for demonstration"""
        import random
        return random.randint(65, 95)
    
    def _generate_mock_insights(self) -> Dict[str, Any]:
        """Generate mock insights for demonstration"""
        import random
        return {
            'waste_percentage': round(random.uniform(5, 25), 1),
            'duplicate_expenses': random.randint(2, 12),
            'spending_spikes': random.randint(1, 8),
            'savings_opportunities': random.randint(3, 15),
            'recommendations': [
                'Consider consolidating vendor payments to reduce transaction fees',
                'Review subscription services for duplicates and unused accounts',
                'Implement approval workflows for expenses over $500',
                'Negotiate better rates with top 3 vendors'
            ][:random.randint(2, 4)]
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'company': self.company,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'spend_score': self.spend_score,
            'insights': self.insights
        }

def create_report(title: str, user_id: int, company: str, data: Dict[str, Any], spend_score: Optional[int] = None, insights: Optional[Dict[str, Any]] = None) -> Report:
    """Create a new report"""
    report = Report(title, user_id, company, data, spend_score, insights)
    reports_db[report.id] = report
    return report

def get_reports_by_user(user_id: int) -> List[Report]:
    """Get all reports for a user"""
    return [report for report in reports_db.values() if report.user_id == user_id]

def get_report_by_id(report_id: int, user_id: int) -> Optional[Report]:
    """Get a specific report by ID (with user access check)"""
    report = reports_db.get(report_id)
    if report and report.user_id == user_id:
        return report
    return None

def delete_report(report_id: int, user_id: int) -> bool:
    """Delete a report (with user access check)"""
    report = reports_db.get(report_id)
    if report and report.user_id == user_id:
        del reports_db[report_id]
        return True
    return False

# Create some sample reports for demonstration
def init_sample_data():
    """Initialize with sample data"""
    global next_report_id
    if not reports_db:  # Only create if empty
        sample_reports = [
            {
                'title': 'Q1 2025 Financial Analysis',
                'user_id': 1,
                'company': 'VeroctaAI',
                'data': {'transactions': 1250, 'total_amount': 125000, 'categories': 15}
            },
            {
                'title': 'March Expense Review',
                'user_id': 1,
                'company': 'VeroctaAI',
                'data': {'transactions': 420, 'total_amount': 45000, 'categories': 12}
            },
            {
                'title': 'Vendor Analysis Report',
                'user_id': 1,
                'company': 'VeroctaAI',
                'data': {'transactions': 890, 'total_amount': 89000, 'categories': 18}
            },
            {
                'title': 'Demo Financial Analysis',
                'user_id': 2,
                'company': 'VeroctaAI Demo',
                'data': {'transactions': 850, 'total_amount': 95000, 'categories': 14}
            },
            {
                'title': 'Demo Q2 Report',
                'user_id': 2,
                'company': 'VeroctaAI Demo',
                'data': {'transactions': 620, 'total_amount': 67000, 'categories': 16}
            }
        ]
        
        for report_data in sample_reports:
            create_report(**report_data)