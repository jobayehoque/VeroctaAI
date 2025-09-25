"""
Insight model for AI-generated financial insights
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from ..core.database import db


class Insight(db.Model):
    """AI-generated financial insights model"""
    
    __tablename__ = 'insights'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    
    # Insight content
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    insight_type = db.Column(db.String(50), nullable=False)  # spending_pattern, recommendation, alert, etc.
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    
    # Categories
    category = db.Column(db.String(100), nullable=True)  # spending_behavior, budgeting, savings, etc.
    tags = db.Column(JSON, nullable=True)  # Array of tags
    
    # AI metadata
    confidence_score = db.Column(db.Float, nullable=True)  # 0.0 to 1.0
    ai_model = db.Column(db.String(100), nullable=True)  # GPT-4, etc.
    prompt_version = db.Column(db.String(50), nullable=True)
    
    # Status
    is_actionable = db.Column(db.Boolean, default=True)
    is_dismissed = db.Column(db.Boolean, default=False)
    user_feedback = db.Column(db.String(20), nullable=True)  # helpful, not_helpful, irrelevant
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert insight to dictionary"""
        return {
            'id': self.id,
            'report_id': self.report_id,
            'title': self.title,
            'content': self.content,
            'insight_type': self.insight_type,
            'priority': self.priority,
            'category': self.category,
            'tags': self.tags,
            'confidence_score': self.confidence_score,
            'ai_model': self.ai_model,
            'prompt_version': self.prompt_version,
            'is_actionable': self.is_actionable,
            'is_dismissed': self.is_dismissed,
            'user_feedback': self.user_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Insight {self.id}: {self.title}>'