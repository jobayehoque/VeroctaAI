# 🚀 VeroctaAI - AI-Powered Financial Intelligence API

[![API Version](https://img.shields.io/badge/API-v2.0.0-blue.svg)](https://veroctaai.onrender.com/api/docs)
[![Python](https://img.shields.io/badge/Python-3.13-green.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-red.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform your financial data into actionable insights with AI-powered analysis**

VeroctaAI is a comprehensive financial intelligence platform that analyzes business expenses, generates SpendScores, and provides AI-powered recommendations for cost optimization. Built as a robust backend API service, it's designed for seamless integration with any frontend application.

## 🌟 Key Features

### 🎯 **Core Capabilities**
- **SpendScore Engine**: Advanced 6-metric scoring system (0-100 scale)
- **AI-Powered Analysis**: GPT-4o integration for intelligent insights
- **Multi-Format Support**: QuickBooks, Wave, Revolut, Xero, and generic CSV
- **Professional Reporting**: PDF generation with company branding
- **User Management**: JWT-based authentication with role management
- **Real-time Processing**: Instant analysis and recommendations

### 📊 **Financial Analysis**
- **Traffic Light System**: Green (90-100), Amber (70-89), Red (0-69)
- **Category Analysis**: Essential vs. low-value spending detection
- **Vendor Optimization**: Consolidation opportunities identification
- **Pattern Recognition**: Subscription and recurring expense analysis
- **Outlier Detection**: Unusual spending pattern identification

### 🔐 **Security & Authentication**
- **JWT Authentication**: Secure token-based access
- **Password Hashing**: bcrypt encryption
- **Role-Based Access**: Admin and user permissions
- **CORS Support**: Cross-origin request handling
- **Input Validation**: Comprehensive data sanitization

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- OpenAI API key (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/veroctaai.git
   cd veroctaai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user profile

### Analysis & Processing
- `POST /api/upload` - Upload CSV file for analysis
- `POST /api/spend-score` - Generate SpendScore analysis
- `GET /api/reports` - List user reports
- `GET /api/reports/{id}/pdf` - Download PDF report

### System
- `GET /api/health` - Health check
- `GET /api/docs` - API documentation
- `GET /api/verify-clone` - System integrity check

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SESSION_SECRET` | Flask session secret | Yes | Auto-generated |
| `OPENAI_API_KEY` | OpenAI API key for AI features | No | - |
| `SUPABASE_URL` | Supabase database URL | No | In-memory storage |
| `SUPABASE_PASSWORD` | Supabase password | No | - |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | No | - |
| `FLASK_ENV` | Flask environment | No | development |

### Supported File Formats

| Format | Description | Sample Columns |
|--------|-------------|----------------|
| **QuickBooks** | QuickBooks CSV export | Date, Description, Amount, Category |
| **Wave** | Wave Accounting CSV | Transaction Date, Description, Amount |
| **Revolut** | Revolut Business CSV | Started Date, Description, Amount |
| **Xero** | Xero CSV export | Date, Description, Amount |
| **Generic** | Custom CSV format | Auto-detected columns |

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   External      │
│   (Any Client)  │◄──►│   (Flask)       │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Data Storage   │
                       │   (Supabase/    │
                       │    In-Memory)   │
                       └─────────────────┘
```

### Core Modules

- **`app.py`** - Main Flask application and routing
- **`routes.py`** - API endpoint definitions
- **`auth.py`** - Authentication and user management
- **`spend_score_engine.py`** - Financial analysis engine
- **`gpt_utils.py`** - AI-powered insights generation
- **`csv_parser.py`** - File parsing and data processing
- **`pdf_generator.py`** - Report generation
- **`database.py`** - Database operations

## 📊 SpendScore Algorithm

The SpendScore uses 6 weighted metrics to evaluate financial health:

| Metric | Weight | Description |
|--------|--------|-------------|
| **Frequency Score** | 15% | Transaction frequency patterns |
| **Category Diversity** | 10% | Number of spending categories |
| **Budget Adherence** | 20% | Spending vs. benchmarks |
| **Redundancy Detection** | 15% | Duplicate/redundant expenses |
| **Spike Detection** | 20% | Unusual spending patterns |
| **Waste Ratio** | 20% | Essential vs. non-essential spending |

## 🔌 Frontend Integration

### React/Vue/Angular Integration

```javascript
// Set API base URL
const API_BASE_URL = 'https://veroctaai.onrender.com/api';

// Example: Upload CSV file
const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return response.json();
};

// Example: Get SpendScore
const getSpendScore = async () => {
  const response = await fetch(`${API_BASE_URL}/spend-score`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};
```

### Environment Configuration

```bash
# Frontend .env file
VITE_API_URL=https://veroctaai.onrender.com/api
VITE_APP_NAME=VeroctaAI
VITE_APP_VERSION=2.0.0
```

## 🚀 Deployment

### Render.com Deployment

1. **Connect your GitHub repository**
2. **Configure environment variables**
3. **Deploy automatically**

The service will be available at: `https://veroctaai.onrender.com`

### Docker Deployment

```bash
# Build Docker image
docker build -t veroctaai-api .

# Run container
docker run -p 5000:5000 \
  -e SESSION_SECRET=your-secret \
  -e OPENAI_API_KEY=your-key \
  veroctaai-api
```

## 📈 Usage Examples

### 1. Upload and Analyze CSV

```bash
curl -X POST https://veroctaai.onrender.com/api/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@expenses.csv"
```

### 2. Get SpendScore Analysis

```bash
curl -X GET https://veroctaai.onrender.com/api/spend-score \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Download PDF Report

```bash
curl -X GET https://veroctaai.onrender.com/api/reports/123/pdf \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o report.pdf
```

## 🧪 Testing

### Health Check

```bash
curl https://veroctaai.onrender.com/api/health
```

### API Documentation

Visit: `https://veroctaai.onrender.com/api/docs`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Docs](https://veroctaai.onrender.com/api/docs)
- **Issues**: [GitHub Issues](https://github.com/your-username/veroctaai/issues)
- **Email**: support@verocta.ai

## 🎯 Roadmap

- [ ] API key authentication
- [ ] Webhook support
- [ ] Advanced analytics dashboard
- [ ] Multi-currency support
- [ ] Real-time notifications
- [ ] Mobile SDK

---

**Built with ❤️ by the VeroctaAI Team**

*Transforming financial data into actionable business intelligence*