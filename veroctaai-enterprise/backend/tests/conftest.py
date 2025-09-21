"""
Pytest Configuration and Fixtures
"""

import pytest
import os
import tempfile
from app import create_app
from config.testing import TestingConfig

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers for testing"""
    # Register test user
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123',
        'company': 'Test Company'
    })
    
    if response.status_code == 201:
        data = response.get_json()
        token = data['token']
        return {'Authorization': f'Bearer {token}'}
    
    return {}

@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing"""
    return """Date,Description,Amount,Category,Vendor
2024-01-01,Office Supplies,150.00,Office,Office Depot
2024-01-02,Software License,299.00,Software,Adobe
2024-01-03,Marketing Campaign,500.00,Marketing,Google Ads
2024-01-04,Travel Expense,250.00,Travel,Uber
2024-01-05,Equipment Purchase,1200.00,Equipment,Apple Store"""

@pytest.fixture
def sample_transactions():
    """Sample transaction data for testing"""
    return [
        {
            'date': '2024-01-01',
            'description': 'Office Supplies',
            'amount': 150.00,
            'category': 'Office',
            'vendor': 'Office Depot'
        },
        {
            'date': '2024-01-02',
            'description': 'Software License',
            'amount': 299.00,
            'category': 'Software',
            'vendor': 'Adobe'
        },
        {
            'date': '2024-01-03',
            'description': 'Marketing Campaign',
            'amount': 500.00,
            'category': 'Marketing',
            'vendor': 'Google Ads'
        }
    ]

@pytest.fixture
def temp_upload_dir():
    """Temporary upload directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        'suggestions': [
            {'priority': 'High', 'text': 'Optimize subscription management'},
            {'priority': 'Medium', 'text': 'Implement automated categorization'},
            {'priority': 'Low', 'text': 'Set up budget alerts'}
        ]
    }
