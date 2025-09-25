"""
Report model for financial analysis reports
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from ..core.database import db


class Report(db.Model):
    """Financial analysis report model"""
    
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # SpendScore data
    spend_score = db.Column(db.Float, nullable=True)
    score_tier = db.Column(db.String(20), nullable=True)  # Green, Amber, Red
    metrics = db.Column(JSON, nullable=True)  # Detailed metrics breakdown
    
    # Financial data
    total_transactions = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Float, default=0.0)
    date_range_start = db.Column(db.Date, nullable=True)
    date_range_end = db.Column(db.Date, nullable=True)
    
    # File information
    original_filename = db.Column(db.String(255), nullable=True)
    file_format = db.Column(db.String(50), nullable=True)  # QuickBooks, Wave, etc.
    
    # Report generation
    pdf_path = db.Column(db.String(500), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    company_logo_path = db.Column(db.String(500), nullable=True)
    
    # AI insights
    ai_insights = db.Column(JSON, nullable=True)
    
    # Status
    status = db.Column(db.String(20), default='processing')  # processing, completed, failed
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='report', lazy='dynamic', cascade='all, delete-orphan')
    insights = db.relationship('Insight', backref='report', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert report to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'spend_score': self.spend_score,
            'score_tier': self.score_tier,
            'metrics': self.metrics,
            'total_transactions': self.total_transactions,
            'total_amount': self.total_amount,
            'date_range_start': self.date_range_start.isoformat() if self.date_range_start else None,
            'date_range_end': self.date_range_end.isoformat() if self.date_range_end else None,
            'original_filename': self.original_filename,
            'file_format': self.file_format,
            'company_name': self.company_name,
            'ai_insights': self.ai_insights,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Report {self.id}: {self.title}>'