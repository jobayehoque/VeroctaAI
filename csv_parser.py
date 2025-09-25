import pandas as pd
import logging
from datetime import datetime
import re

# Enhanced header mapping for different CSV formats from various platforms
HEADER_MAPPINGS = {
    'vendor': [
        'merchant', 'payee', 'supplier', 'description', 'counterparty', 'recipient',
        'name', 'vendor name', 'business name', 'company', 'paid to', 'beneficiary',
        'transaction description', 'reference', 'details'
    ],
    'amount': [
        'transaction value', 'total', 'cost', 'debit', 'credit', 'sum', 'value',
        'paid out', 'paid in', 'amount usd', 'amount gbp', 'amount eur',
        'transaction amount', 'net amount', 'gross amount', 'payment amount'
    ],
    'date': [
        'txn date', 'transaction date', 'posted', 'posting date', 'completed date', 'created date',
        'date', 'completion date', 'processing date', 'value date', 'booking date',
        'settlement date', 'effective date'
    ],
    'category': [
        'type', 'classification', 'expense type', 'account', 'reference',
        'category', 'class', 'transaction type', 'expense category', 'account type',
        'business category', 'expense class'
    ],
    'description': [
        'details', 'memo', 'notes', 'comment', 'reference', 'memo description',
        'transaction details', 'payment details', 'additional info', 'remarks'
    ]
}

def normalize_header(header):
    """Normalize header name to lowercase and remove special characters"""
    return re.sub(r'[^\w\s]', '', header.lower().strip())

def find_matching_column(df_columns, target_field):
    """Find the best matching column for a target field with enhanced matching"""
    normalized_columns = {normalize_header(col): col for col in df_columns}
    
    # First try exact match
    if target_field in normalized_columns:
        return normalized_columns[target_field]
    
    # Then try synonym matching with priority scoring
    best_match = None
    best_score = 0
    
    if target_field in HEADER_MAPPINGS:
        for i, synonym in enumerate(HEADER_MAPPINGS[target_field]):
            normalized_synonym = normalize_header(synonym)
            if normalized_synonym in normalized_columns:
                # Earlier synonyms in the list have higher priority
                score = len(HEADER_MAPPINGS[target_field]) - i
                if score > best_score:
                    best_score = score
                    best_match = normalized_columns[normalized_synonym]
    
    if best_match:
        return best_match
    
    # Enhanced partial matching with context awareness
    for col_name, original_col in normalized_columns.items():
        # Check for partial matches with context
        if target_field in col_name:
            return original_col
        if col_name in target_field:
            return original_col
        
        # Special handling for amount fields
        if target_field == 'amount':
            if any(keyword in col_name for keyword in ['usd', 'gbp', 'eur', 'dollar', 'pound', 'euro']):
                return original_col
        
        # Special handling for date fields
        if target_field == 'date':
            if any(keyword in col_name for keyword in ['time', 'when', 'on']):
                return original_col
    
    return None

def clean_amount_value(value):
    """Clean and convert amount values to float"""
    if pd.isna(value):
        return 0.0
    
    # Convert to string and clean
    str_value = str(value).strip()
    
    # Remove currency symbols and whitespace
    str_value = re.sub(r'[£$€¥₹,\s]', '', str_value)
    
    # Handle parentheses (negative values)
    if str_value.startswith('(') and str_value.endswith(')'):
        str_value = '-' + str_value[1:-1]
    
    try:
        return float(str_value)
    except (ValueError, TypeError):
        logging.warning(f"Could not convert amount value: {value}")
        return 0.0

def parse_date_value(value):
    """Parse date values with multiple format support"""
    if pd.isna(value):
        return None
    
    str_value = str(value).strip()
    
    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%d.%m.%Y',
        '%m.%d.%Y'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(str_value, fmt).date()
        except ValueError:
            continue
    
    logging.warning(f"Could not parse date value: {value}")
    return None

def parse_csv_file(filepath):
    """Parse CSV file and return standardized transaction data"""
    try:
        logging.info(f"Starting to parse CSV file: {filepath}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                logging.info(f"Successfully read CSV with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        if df.empty:
            logging.warning("CSV file is empty")
            return []
        
        logging.info(f"CSV loaded with {len(df)} rows and columns: {list(df.columns)}")
        
        # Find matching columns
        vendor_col = find_matching_column(df.columns, 'vendor')
        amount_col = find_matching_column(df.columns, 'amount')
        date_col = find_matching_column(df.columns, 'date')
        category_col = find_matching_column(df.columns, 'category')
        description_col = find_matching_column(df.columns, 'description')
        
        logging.info(f"Column mapping - Vendor: {vendor_col}, Amount: {amount_col}, Date: {date_col}, Category: {category_col}")
        
        if not amount_col:
            raise ValueError("Could not find amount column in CSV file")
        
        transactions = []
        
        for index, row in df.iterrows():
            try:
                # Extract and clean data
                amount = clean_amount_value(row[amount_col]) if amount_col else 0.0
                
                # Skip zero or very small amounts
                if abs(amount) < 0.01:
                    continue
                
                transaction = {
                    'amount': abs(amount),  # Use absolute value for spend analysis
                    'vendor': str(row[vendor_col]).strip() if vendor_col is not None and pd.notna(row[vendor_col]) else 'Unknown Vendor',
                    'date': parse_date_value(row[date_col]) if date_col is not None else None,
                    'category': str(row[category_col]).strip() if category_col is not None and pd.notna(row[category_col]) else 'Uncategorized',
                    'description': str(row[description_col]).strip() if description_col is not None and pd.notna(row[description_col]) else ''
                }
                
                transactions.append(transaction)
                
            except Exception as e:
                logging.warning(f"Error processing row {index}: {str(e)}")
                continue
        
        logging.info(f"Successfully parsed {len(transactions)} valid transactions")
        
        if not transactions:
            logging.warning("No valid transactions found after parsing")
        
        return transactions
        
    except Exception as e:
        logging.error(f"Error parsing CSV file: {str(e)}")
        raise ValueError(f"Failed to parse CSV file: {str(e)}")

def parse_csv_file_with_mapping(filepath, mapping):
    """Parse CSV file using provided column mapping"""
    try:
        logging.info(f"Starting to parse CSV file with mapping: {filepath}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                logging.info(f"Successfully read CSV with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        if df.empty:
            logging.warning("CSV file is empty")
            return []
        
        logging.info(f"CSV loaded with {len(df)} rows and columns: {list(df.columns)}")
        
        # Use provided mapping
        amount_col = mapping.get('amount')
        vendor_col = mapping.get('vendor')
        date_col = mapping.get('date')
        category_col = mapping.get('category')
        description_col = mapping.get('description')
        
        logging.info(f"Using mapping - Amount: {amount_col}, Vendor: {vendor_col}, Date: {date_col}, Category: {category_col}")
        
        if not amount_col:
            raise ValueError("Amount column must be specified in mapping")
        
        if amount_col not in df.columns:
            raise ValueError(f"Amount column '{amount_col}' not found in CSV file")
        
        transactions = []
        
        for index, row in df.iterrows():
            try:
                # Extract and clean data using mapping
                amount = clean_amount_value(row[amount_col]) if amount_col else 0.0
                
                # Skip zero or very small amounts
                if abs(amount) < 0.01:
                    continue
                
                transaction = {
                    'amount': abs(amount),  # Use absolute value for spend analysis
                    'vendor': str(row[vendor_col]).strip() if vendor_col and vendor_col in df.columns and pd.notna(row[vendor_col]) else 'Unknown Vendor',
                    'date': parse_date_value(row[date_col]) if date_col and date_col in df.columns else None,
                    'category': str(row[category_col]).strip() if category_col and category_col in df.columns and pd.notna(row[category_col]) else 'Uncategorized',
                    'description': str(row[description_col]).strip() if description_col and description_col in df.columns and pd.notna(row[description_col]) else ''
                }
                
                transactions.append(transaction)
                
            except Exception as e:
                logging.warning(f"Error processing row {index}: {str(e)}")
                continue
        
        logging.info(f"Successfully parsed {len(transactions)} valid transactions using mapping")
        
        if not transactions:
            logging.warning("No valid transactions found after parsing with mapping")
        
        return transactions
        
    except Exception as e:
        logging.error(f"Error parsing CSV file with mapping: {str(e)}")
        raise ValueError(f"Failed to parse CSV file with mapping: {str(e)}")

def get_transaction_summary(transactions):
    """Generate summary statistics for transactions"""
    if not transactions:
        return {}
    
    total_amount = sum(t['amount'] for t in transactions)
    
    # Category breakdown
    category_totals = {}
    for transaction in transactions:
        category = transaction.get('category', 'Uncategorized')
        category_totals[category] = category_totals.get(category, 0) + transaction['amount']
    
    # Vendor breakdown (top 10)
    vendor_totals = {}
    for transaction in transactions:
        vendor = transaction.get('vendor', 'Unknown')
        vendor_totals[vendor] = vendor_totals.get(vendor, 0) + transaction['amount']
    
    top_vendors = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_transactions': len(transactions),
        'total_amount': total_amount,
        'average_amount': total_amount / len(transactions),
        'category_breakdown': category_totals,
        'top_vendors': top_vendors
    }
