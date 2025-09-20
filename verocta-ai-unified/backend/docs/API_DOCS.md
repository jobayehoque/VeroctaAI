# 🚀 VeroctaAI Financial Intelligence Platform - Complete API Documentation

## 📖 Overview
The VeroctaAI Financial Intelligence Platform provides comprehensive REST API for financial data analysis, SpendScore calculation, and intelligent insights generation with enhanced company branding support.

## 🔗 Base URLs
```
Development: http://127.0.0.1:5001
Web Interface: http://127.0.0.1:5001
API Endpoints: http://127.0.0.1:5001/api/
```

## 🔑 Authentication
Currently using development mode. For production deployment, implement API key or JWT authentication.

```http
Authorization: Bearer <your-api-token>
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API service is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Verocta Financial Insight Platform is running",
  "version": "2.0.0"
}
```

### 2. Upload & Analyze CSV
**POST** `/upload`

Upload a CSV file and trigger comprehensive financial analysis.

**Parameters:**
- `file` (required): CSV file (multipart/form-data)
- Max file size: 16MB
- Supported formats: QuickBooks, Wave, Revolut, Xero, Generic CSV

**Response:**
```json
{
  "success": true,
  "filename": "transactions.csv",
  "spend_score": 85,
  "tier_info": {
    "color": "Amber",
    "tier": "Good",
    "green_reward_eligible": false,
    "description": "Good financial habits with room for improvement"
  },
  "score_breakdown": {
    "frequency_score": 78.5,
    "category_diversity": 92.0,
    "budget_adherence": 85.3,
    "redundancy_detection": 95.0,
    "spike_detection": 72.1,
    "waste_ratio": 88.7,
    "final_score": 85
  },
  "transaction_summary": {
    "total_transactions": 150,
    "total_amount": 25750.50,
    "median_amount": 125.00,
    "mean_amount": 171.67,
    "unique_categories": 12,
    "unique_vendors": 45
  },
  "ai_insights": [
    "Consider consolidating software subscriptions to reduce redundant costs",
    "Dining expenses represent 23% of spending - budget optimization opportunity"
  ],
  "analysis_timestamp": "2025-08-06T14:30:00Z"
}
```

### 3. Get SpendScore Metrics
**GET** `/spend-score`

Retrieve the latest SpendScore analysis results.

**Response:**
```json
{
  "spend_score": 85,
  "tier_info": {
    "color": "Amber",
    "tier": "Good",
    "green_reward_eligible": false,
    "description": "Good financial habits with room for improvement"
  },
  "score_breakdown": {
    "frequency_score": 78.5,
    "category_diversity": 92.0,
    "budget_adherence": 85.3,
    "redundancy_detection": 95.0,
    "spike_detection": 72.1,
    "waste_ratio": 88.7,
    "final_score": 85
  },
  "enhanced_metrics": {
    "total_transactions": 150,
    "total_amount": 25750.50,
    "median_amount": 125.00,
    "unique_categories": 12,
    "unique_vendors": 45
  },
  "green_reward_eligible": false,
  "last_updated": "2025-08-06T14:30:00Z"
}
```

### 4. Download PDF Report
**GET** `/report`

Download the latest generated PDF financial analysis report.

**Response:** PDF file download
- Content-Type: `application/pdf`
- Filename: `verocta_financial_report.pdf`

### 5. Verify Clone Integrity
**GET** `/verify-clone`

Check the integrity of the project clone and detect any deviations.

**Response:**
```json
{
  "status": "clean",
  "message": "All files match baseline - clone integrity verified",
  "files_checked": 45,
  "files_matched": 45,
  "files_modified": 0,
  "files_missing": 0,
  "total_deviations": 0,
  "timestamp": "2025-08-06T14:30:00Z"
}
```

### 6. API Documentation
**GET** `/docs`

Get this API documentation in JSON format.

## SpendScore Metrics

### Traffic Light System
- **Green (90-100)**: Excellent financial management
  - Reward eligible: 15% discount on premium features
- **Amber (70-89)**: Good financial habits with optimization opportunities
- **Red (0-69)**: Significant improvement needed

### Scoring Components
1. **Frequency Score (15%)**: Transaction frequency patterns
2. **Category Diversity (10%)**: Number of spending categories
3. **Budget Adherence (20%)**: Consistency with spending patterns
4. **Redundancy Detection (15%)**: Duplicate or redundant transactions
5. **Spike Detection (20%)**: Unusual large transactions
6. **Waste Ratio (20%)**: Spending on non-essential categories

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid file type. Only CSV files are allowed."
}
```

### 404 Not Found
```json
{
  "error": "No analysis data available. Please upload a CSV file first."
}
```

### 500 Internal Server Error
```json
{
  "error": "Analysis failed: [detailed error message]"
}
```

## CSV File Format

### Required Columns (flexible naming)
- **Date**: transaction date (YYYY-MM-DD or MM/DD/YYYY)
- **Amount**: transaction amount (numeric)
- **Description/Vendor**: transaction description
- **Category**: spending category (optional)

### Supported CSV Formats
- QuickBooks exports
- Wave Accounting exports
- Revolut transaction exports
- Xero transaction exports
- Generic transaction CSV files

### Example CSV Structure
```csv
Date,Amount,Description,Category
2025-01-15,125.50,Grocery Store,Food
2025-01-16,89.99,Software Subscription,Technology
2025-01-17,450.00,Office Rent,Business
```

## Rate Limiting
- Development: No limits
- Production: 100 requests per hour per IP

## Postman Collection
Import the following URL into Postman to get started:
```
http://localhost:5001/api/docs
```

## Example Usage

### cURL Examples

**Upload CSV:**
```bash
curl -X POST http://localhost:5001/api/upload \
  -F "file=@transactions.csv"
```

**Get SpendScore:**
```bash
curl -X GET http://localhost:5001/api/spend-score
```

**Download Report:**
```bash
curl -X GET http://localhost:5001/api/report \
  -o financial_report.pdf
```

### Python Example
```python
import requests

# Upload CSV
with open('transactions.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:5001/api/upload',
        files={'file': f}
    )
    
analysis = response.json()
spend_score = analysis['spend_score']
print(f"SpendScore: {spend_score}")

# Get detailed metrics
metrics = requests.get('http://localhost:5001/api/spend-score').json()
print(f"Tier: {metrics['tier_info']['tier']}")
```

### JavaScript Example
```javascript
// Upload CSV
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('SpendScore:', data.spend_score);
    console.log('Tier:', data.tier_info.tier);
});
```

## Support

For technical support or integration questions:
- Email: support@verocta.ai
- GitHub Issues: [Project Repository]
- Documentation: http://localhost:5001/api/docs
