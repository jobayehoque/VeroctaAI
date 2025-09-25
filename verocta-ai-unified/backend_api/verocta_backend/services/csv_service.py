"""
CSV Processing Service
Handles CSV file parsing and transaction extraction
"""

import pandas as pd
from datetime import datetime
from typing import List, Optional
from flask import current_app

from ..models import Transaction
from ..core.database import db


class CSVProcessorService:
    """Service for processing CSV files"""
    
    def __init__(self):
        self.supported_formats = {
            'quickbooks': self._parse_quickbooks,
            'wave': self._parse_wave,
            'revolut': self._parse_revolut,
            'xero': self._parse_xero,
            'generic': self._parse_generic
        }
    
    def process_file(self, file_path: str, report_id: int, file_format: str = 'generic') -> List[Transaction]:
        """
        Process CSV file and create transaction records
        """
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            current_app.logger.info(f"Processing CSV with {len(df)} rows, format: {file_format}")
            
            # Get parser function
            parser = self.supported_formats.get(file_format, self._parse_generic)
            
            # Parse transactions
            transactions = parser(df, report_id)
            
            # Save to database
            for transaction in transactions:
                db.session.add(transaction)
            
            db.session.commit()
            current_app.logger.info(f"Created {len(transactions)} transactions")
            
            return transactions
            
        except Exception as e:
            current_app.logger.error(f"CSV processing error: {str(e)}")
            db.session.rollback()
            raise
    
    def _parse_quickbooks(self, df: pd.DataFrame, report_id: int) -> List[Transaction]:
        """Parse QuickBooks CSV format"""
        transactions = []
        
        # Expected columns: Date, Description, Amount
        required_cols = ['Date', 'Description', 'Amount']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"QuickBooks CSV must have columns: {required_cols}")
        
        for _, row in df.iterrows():
            try:
                transaction = Transaction(
                    report_id=report_id,
                    transaction_date=pd.to_datetime(row['Date']).date(),
                    description=str(row['Description']).strip(),
                    amount=float(row['Amount']),
                    original_description=str(row['Description']).strip(),
                    category=row.get('Category', None),
                    merchant=row.get('Vendor', None)
                )
                transactions.append(transaction)
            except Exception as e:
                current_app.logger.warning(f"Skipping row due to error: {str(e)}")
                continue
        
        return transactions
    
    def _parse_wave(self, df: pd.DataFrame, report_id: int) -> List[Transaction]:
        """Parse Wave Accounting CSV format"""
        transactions = []
        
        # Expected columns: Date, Description, Amount
        required_cols = ['Date', 'Description', 'Amount']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Wave CSV must have columns: {required_cols}")
        
        for _, row in df.iterrows():
            try:
                transaction = Transaction(
                    report_id=report_id,
                    transaction_date=pd.to_datetime(row['Date']).date(),
                    description=str(row['Description']).strip(),
                    amount=float(row['Amount']),
                    original_description=str(row['Description']).strip(),
                    category=row.get('Category', None)
                )
                transactions.append(transaction)
            except Exception as e:
                current_app.logger.warning(f"Skipping row due to error: {str(e)}")
                continue
        
        return transactions
    
    def _parse_revolut(self, df: pd.DataFrame, report_id: int) -> List[Transaction]:
        """Parse Revolut CSV format"""
        transactions = []
        
        # Expected columns: Started Date, Description, Amount
        required_cols = ['Started Date', 'Description', 'Amount']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Revolut CSV must have columns: {required_cols}")
        
        for _, row in df.iterrows():
            try:
                transaction = Transaction(
                    report_id=report_id,
                    transaction_date=pd.to_datetime(row['Started Date']).date(),
                    description=str(row['Description']).strip(),
                    amount=float(row['Amount']),
                    original_description=str(row['Description']).strip(),
                    category=row.get('Category', None),
                    reference_number=row.get('Reference', None)
                )
                transactions.append(transaction)
            except Exception as e:
                current_app.logger.warning(f"Skipping row due to error: {str(e)}")
                continue
        
        return transactions
    
    def _parse_xero(self, df: pd.DataFrame, report_id: int) -> List[Transaction]:
        """Parse Xero CSV format"""
        transactions = []
        
        # Expected columns: Date, Description, Amount
        required_cols = ['Date', 'Description', 'Amount']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Xero CSV must have columns: {required_cols}")
        
        for _, row in df.iterrows():
            try:
                transaction = Transaction(
                    report_id=report_id,
                    transaction_date=pd.to_datetime(row['Date']).date(),
                    description=str(row['Description']).strip(),
                    amount=float(row['Amount']),
                    original_description=str(row['Description']).strip(),
                    category=row.get('Account', None),
                    reference_number=row.get('Reference', None)
                )
                transactions.append(transaction)
            except Exception as e:
                current_app.logger.warning(f"Skipping row due to error: {str(e)}")
                continue
        
        return transactions
    
    def _parse_generic(self, df: pd.DataFrame, report_id: int) -> List[Transaction]:
        """Parse generic CSV format"""
        transactions = []
        
        # Try different common column names
        date_cols = ['date', 'Date', 'DATE', 'transaction_date', 'Transaction Date']
        desc_cols = ['description', 'Description', 'DESCRIPTION', 'desc', 'Desc']
        amount_cols = ['amount', 'Amount', 'AMOUNT', 'value', 'Value', 'total', 'Total']
        
        # Find the actual column names
        date_col = next((col for col in date_cols if col in df.columns), None)
        desc_col = next((col for col in desc_cols if col in df.columns), None)
        amount_col = next((col for col in amount_cols if col in df.columns), None)
        
        if not all([date_col, desc_col, amount_col]):
            raise ValueError(f"Generic CSV must have date, description, and amount columns. Found: {list(df.columns)}")
        
        for _, row in df.iterrows():
            try:
                # Skip empty rows
                if pd.isna(row[date_col]) or pd.isna(row[desc_col]) or pd.isna(row[amount_col]):
                    continue
                
                transaction = Transaction(
                    report_id=report_id,
                    transaction_date=pd.to_datetime(row[date_col]).date(),
                    description=str(row[desc_col]).strip(),
                    amount=float(row[amount_col]),
                    original_description=str(row[desc_col]).strip(),
                    category=row.get('category', row.get('Category', None))
                )
                transactions.append(transaction)
            except Exception as e:
                current_app.logger.warning(f"Skipping row due to error: {str(e)}")
                continue
        
        return transactions