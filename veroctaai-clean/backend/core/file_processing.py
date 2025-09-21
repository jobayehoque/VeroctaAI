"""
File Processing Service
"""

import csv
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

class FileProcessingService:
    """CSV file processing and parsing service"""
    
    def __init__(self):
        self.supported_formats = {
            'quickbooks': ['Date', 'Description', 'Amount', 'Category'],
            'wave': ['Transaction Date', 'Description', 'Amount'],
            'revolut': ['Started Date', 'Description', 'Amount'],
            'xero': ['Date', 'Description', 'Amount', 'Account'],
            'generic': ['date', 'description', 'amount', 'category', 'vendor']
        }
    
    def process_csv_file(self, file, mapping: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Process uploaded CSV file"""
        try:
            # Save uploaded file temporarily
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            
            # Parse CSV with or without mapping
            if mapping and any(mapping.values()):
                transactions = self._parse_with_mapping(filepath, mapping)
            else:
                transactions = self._parse_with_auto_detection(filepath)
            
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return transactions
            
        except Exception as e:
            logging.error(f"File processing error: {e}")
            # Clean up on error
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            raise e
    
    def _parse_with_mapping(self, filepath: str, mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse CSV with provided column mapping"""
        transactions = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    transaction = {}
                    
                    # Map columns according to provided mapping
                    for field, column in mapping.items():
                        if column and column in row:
                            value = row[column].strip()
                            
                            if field == 'amount':
                                try:
                                    transaction[field] = float(value.replace(',', '').replace('$', ''))
                                except ValueError:
                                    continue  # Skip invalid amounts
                            elif field == 'date':
                                transaction[field] = self._parse_date(value)
                            else:
                                transaction[field] = value
                    
                    # Only add if we have essential fields
                    if 'amount' in transaction and 'description' in transaction:
                        transactions.append(transaction)
                        
        except Exception as e:
            logging.error(f"Mapping parse error: {e}")
            raise e
        
        return transactions
    
    def _parse_with_auto_detection(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse CSV with automatic column detection"""
        transactions = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                
                if not headers:
                    return transactions
                
                # Detect column mapping
                mapping = self._detect_column_mapping(headers)
                
                for row in reader:
                    transaction = {}
                    
                    for field, column in mapping.items():
                        if column and column in row:
                            value = row[column].strip()
                            
                            if field == 'amount':
                                try:
                                    transaction[field] = float(value.replace(',', '').replace('$', ''))
                                except ValueError:
                                    continue
                            elif field == 'date':
                                transaction[field] = self._parse_date(value)
                            else:
                                transaction[field] = value
                    
                    if 'amount' in transaction and 'description' in transaction:
                        transactions.append(transaction)
                        
        except Exception as e:
            logging.error(f"Auto-detection parse error: {e}")
            raise e
        
        return transactions
    
    def _detect_column_mapping(self, headers: List[str]) -> Dict[str, str]:
        """Detect column mapping from headers"""
        mapping = {}
        
        # Common date column names
        date_columns = ['date', 'transaction_date', 'started_date', 'transaction date', 'started date']
        for header in headers:
            if header.lower() in date_columns:
                mapping['date'] = header
                break
        
        # Common description column names
        desc_columns = ['description', 'memo', 'details', 'payee', 'merchant']
        for header in headers:
            if header.lower() in desc_columns:
                mapping['description'] = header
                break
        
        # Common amount column names
        amount_columns = ['amount', 'value', 'total', 'debit', 'credit']
        for header in headers:
            if header.lower() in amount_columns:
                mapping['amount'] = header
                break
        
        # Common category column names
        category_columns = ['category', 'type', 'classification', 'account']
        for header in headers:
            if header.lower() in category_columns:
                mapping['category'] = header
                break
        
        # Common vendor column names
        vendor_columns = ['vendor', 'payee', 'merchant', 'supplier']
        for header in headers:
            if header.lower() in vendor_columns:
                mapping['vendor'] = header
                break
        
        return mapping
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        # Common date formats
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M:%S'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # If no format matches, try pandas
        try:
            return pd.to_datetime(date_str)
        except:
            return None
