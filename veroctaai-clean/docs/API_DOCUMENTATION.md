# 📡 VeroctaAI API Documentation

## Overview

The VeroctaAI API provides comprehensive financial analysis capabilities through a RESTful interface. This documentation covers all available endpoints, request/response formats, and integration examples.

**Base URL**: `https://veroctaai.onrender.com/api`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

1. **Register a new user**:
   ```http
   POST /api/auth/register
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "securepassword",
     "company": "Your Company"
   }
   ```

2. **Login with existing credentials**:
   ```http
   POST /api/auth/login
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "securepassword"
   }
   ```

**Response**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "company": "Your Company",
    "role": "user"
  }
}
```

## Endpoints

### 🔐 Authentication Endpoints

#### POST /api/auth/register
Register a new user account.

**Request Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)",
  "company": "string (optional)"
}
```

**Response**:
```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "email": "string",
    "company": "string",
    "role": "string"
  }
}
```

#### POST /api/auth/login
Authenticate user and get access token.

**Request Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response**:
```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "email": "string",
    "company": "string",
    "role": "string"
  }
}
```

#### GET /api/auth/me
Get current user profile.

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "user": {
    "id": "integer",
    "email": "string",
    "company": "string",
    "role": "string",
    "created_at": "datetime"
  }
}
```

### 📊 Analysis Endpoints

#### POST /api/upload
Upload CSV file for financial analysis.

**Headers**: `Authorization: Bearer <token>`

**Request**: `multipart/form-data`
- `file`: CSV file (required)
- `mapping`: JSON string with column mapping (optional)

**Example Column Mapping**:
```json
{
  "date": "Transaction Date",
  "description": "Description",
  "amount": "Amount",
  "category": "Category",
  "vendor": "Payee"
}
```

**Response**:
```json
{
  "success": true,
  "analysis": {
    "spend_score": 85,
    "total_transactions": 150,
    "total_amount": 45000.00,
    "categories": {
      "Software & SaaS": 12000,
      "Office Supplies": 8000,
      "Marketing": 15000,
      "Travel": 5000,
      "Other": 5000
    },
    "insights": [
      {
        "priority": "High",
        "text": "Review subscription services for cost optimization"
      },
      {
        "priority": "Medium", 
        "text": "Implement automated expense categorization"
      },
      {
        "priority": "Low",
        "text": "Set up budget alerts for key categories"
      }
    ],
    "score_tier": {
      "color": "Amber",
      "tier": "Good",
      "description": "Good financial habits with room for improvement"
    }
  },
  "filename": "expenses_2024.csv"
}
```

#### POST /api/spend-score
Generate detailed SpendScore analysis.

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "transactions": [
    {
      "date": "2024-01-15",
      "description": "Office supplies",
      "amount": 150.00,
      "category": "Office",
      "vendor": "Office Depot"
    }
  ]
}
```

**Response**:
```json
{
  "spend_score": 85,
  "score_breakdown": {
    "frequency_score": 80,
    "category_diversity": 75,
    "budget_adherence": 90,
    "redundancy_detection": 85,
    "spike_detection": 80,
    "waste_ratio": 90
  },
  "tier_info": {
    "color": "Amber",
    "tier": "Good",
    "green_reward_eligible": false,
    "description": "Good financial habits with room for improvement"
  },
  "transaction_summary": {
    "total_transactions": 150,
    "total_amount": 45000.00,
    "median_amount": 250.00,
    "mean_amount": 300.00,
    "unique_categories": 8,
    "unique_vendors": 25
  }
}
```

### 📄 Report Endpoints

#### GET /api/reports
List all reports for the current user.

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "reports": [
    {
      "id": 1,
      "title": "Q1 2024 Financial Analysis",
      "spend_score": 85,
      "total_amount": 45000.00,
      "total_transactions": 150,
      "created_at": "2024-01-15T10:30:00Z",
      "filename": "q1_2024_analysis.csv"
    }
  ]
}
```

#### GET /api/reports/{id}/pdf
Download PDF report.

**Headers**: `Authorization: Bearer <token>`

**Response**: PDF file download

#### POST /api/reports
Create a new report.

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "string (optional)"
}
```

**Response**:
```json
{
  "report": {
    "id": 1,
    "title": "Q1 2024 Financial Analysis",
    "spend_score": 85,
    "total_amount": 45000.00,
    "total_transactions": 150,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 🔧 System Endpoints

#### GET /api/health
Check API health and system status.

**Response**:
```json
{
  "status": "healthy",
  "message": "VeroctaAI API is running",
  "version": "2.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "connected",
    "openai": "available",
    "pdf_generator": "ready"
  }
}
```

#### GET /api/docs
Get API documentation.

**Response**:
```json
{
  "title": "VeroctaAI Financial Analysis API",
  "version": "2.0.0",
  "description": "AI-powered financial intelligence and SpendScore analysis platform",
  "base_url": "https://veroctaai.onrender.com/api/",
  "endpoints": {
    "POST /upload": {
      "description": "Upload CSV and trigger analysis",
      "parameters": {
        "file": "CSV file (multipart/form-data)"
      },
      "response": "Analysis results with SpendScore and insights"
    }
  }
}
```

#### GET /api/verify-clone
Verify system integrity and clone status.

**Response**:
```json
{
  "status": "verified",
  "message": "System integrity verified",
  "checks": {
    "database": "ok",
    "files": "ok",
    "dependencies": "ok"
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "error": "Error message",
  "details": "Additional error details",
  "code": "ERROR_CODE"
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `AUTH_REQUIRED` | Authentication required | 401 |
| `INVALID_TOKEN` | Invalid or expired token | 401 |
| `INVALID_FILE` | Invalid file format | 400 |
| `INSUFFICIENT_DATA` | Not enough data for analysis | 400 |
| `ANALYSIS_FAILED` | Analysis calculation failed | 500 |
| `FILE_TOO_LARGE` | File exceeds size limit | 413 |

### Example Error Responses

**Authentication Required**:
```json
{
  "error": "Authentication required",
  "details": "Please provide a valid JWT token",
  "code": "AUTH_REQUIRED"
}
```

**Invalid File Format**:
```json
{
  "error": "Invalid file format",
  "details": "Only CSV files are supported",
  "code": "INVALID_FILE"
}
```

## Rate Limiting

- **Upload**: 10 requests per minute
- **Analysis**: 20 requests per minute
- **Reports**: 30 requests per minute
- **Health/Docs**: 100 requests per minute

## Supported File Formats

### QuickBooks CSV
```csv
Date,Description,Amount,Category
2024-01-15,Office supplies,150.00,Office
2024-01-16,Software subscription,99.00,Software
```

### Wave Accounting CSV
```csv
Transaction Date,Description,Amount
2024-01-15,Office supplies,150.00
2024-01-16,Software subscription,99.00
```

### Revolut Business CSV
```csv
Started Date,Description,Amount
2024-01-15,Office supplies,150.00
2024-01-16,Software subscription,99.00
```

### Generic CSV
The API automatically detects common column names:
- Date columns: `date`, `transaction_date`, `started_date`
- Description columns: `description`, `memo`, `details`
- Amount columns: `amount`, `value`, `total`
- Category columns: `category`, `type`, `classification`
- Vendor columns: `vendor`, `payee`, `merchant`

## Integration Examples

### JavaScript/Node.js

```javascript
class VeroctaAI {
  constructor(apiKey, baseUrl = 'https://veroctaai.onrender.com/api') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  async uploadFile(file, mapping = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (mapping) {
      formData.append('mapping', JSON.stringify(mapping));
    }

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: formData
    });

    return response.json();
  }

  async getSpendScore() {
    const response = await fetch(`${this.baseUrl}/spend-score`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`
      }
    });

    return response.json();
  }

  async downloadReport(reportId) {
    const response = await fetch(`${this.baseUrl}/reports/${reportId}/pdf`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`
      }
    });

    return response.blob();
  }
}

// Usage
const client = new VeroctaAI('your-jwt-token');
const analysis = await client.uploadFile(csvFile);
```

### Python

```python
import requests
import json

class VeroctaAI:
    def __init__(self, api_key, base_url='https://veroctaai.onrender.com/api'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {api_key}'}

    def upload_file(self, file_path, mapping=None):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'mapping': json.dumps(mapping)} if mapping else {}
            
            response = requests.post(
                f'{self.base_url}/upload',
                headers=self.headers,
                files=files,
                data=data
            )
            
        return response.json()

    def get_spend_score(self):
        response = requests.get(
            f'{self.base_url}/spend-score',
            headers=self.headers
        )
        return response.json()

    def download_report(self, report_id):
        response = requests.get(
            f'{self.base_url}/reports/{report_id}/pdf',
            headers=self.headers
        )
        return response.content

# Usage
client = VeroctaAI('your-jwt-token')
analysis = client.upload_file('expenses.csv')
```

### cURL Examples

**Upload CSV**:
```bash
curl -X POST https://veroctaai.onrender.com/api/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@expenses.csv"
```

**Get SpendScore**:
```bash
curl -X GET https://veroctaai.onrender.com/api/spend-score \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Download PDF Report**:
```bash
curl -X GET https://veroctaai.onrender.com/api/reports/123/pdf \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o report.pdf
```

## Webhooks (Coming Soon)

Webhook support will be available in v2.1 for real-time notifications:

- `analysis.completed` - When analysis is finished
- `report.generated` - When PDF report is ready
- `score.threshold` - When SpendScore crosses thresholds

## Changelog

### v2.0.0 (Current)
- Complete API rewrite
- JWT authentication
- Enhanced SpendScore algorithm
- GPT-4o integration
- Multi-format CSV support
- PDF report generation

### v1.0.0
- Initial release
- Basic CSV analysis
- Simple scoring system

---

For more information, visit the [main documentation](README.md) or contact support at support@verocta.ai.
