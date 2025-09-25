"""
Transaction model for financial transaction data
"""

from datetime import datetime, date
from ..core.database import db


class Transaction(db.Model):
    """Individual financial transaction model"""
    
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    
    # Transaction details
    transaction_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    subcategory = db.Column(db.String(100), nullable=True)
    
    # Classification
    transaction_type = db.Column(db.String(20), nullable=True)  # debit, credit, transfer
    is_recurring = db.Column(db.Boolean, default=False)
    is_essential = db.Column(db.Boolean, default=True)
    
    # Original data
    original_description = db.Column(db.String(500), nullable=True)
    merchant = db.Column(db.String(255), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'report_id': self.report_id,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'subcategory': self.subcategory,
            'transaction_type': self.transaction_type,
            'is_recurring': self.is_recurring,
            'is_essential': self.is_essential,
            'original_description': self.original_description,
            'merchant': self.merchant,
            'reference_number': self.reference_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def is_debit(self):
        """Check if transaction is a debit (negative amount)"""
        return self.amount < 0
    
    @property
    def is_credit(self):
        """Check if transaction is a credit (positive amount)"""
        return self.amount > 0
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.description} ({self.amount})>'