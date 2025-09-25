# 🚀 VeroctaAI - AI-Powered Financial Intelligence Platform

[![API Version](https://img.shields.io/badge/API-v2.0.0-blue.svg)](https://veroctaai.onrender.com/api/docs)
[![Python](https://img.shields.io/badge/Python-3.13-green.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-red.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform your financial data into actionable insights with AI-powered analysis**

VeroctaAI is a comprehensive financial intelligence platform that analyzes business expenses, generates SpendScores, and provides AI-powered recommendations for cost optimization. Built with a clean, professional architecture for easy deployment and integration.

## 🏗️ Project Structure

```
veroctaai-clean/
├── backend/                    # Backend API service
│   ├── app/                   # Flask application
│   │   ├── api/              # API blueprints
│   │   ├── models/           # Data models
│   │   └── middleware/        # Custom middleware
│   ├── core/                 # Core business logic
│   │   ├── auth/             # Authentication service
│   │   ├── analysis/         # Financial analysis
│   │   └── file_processing/  # CSV processing
│   ├── services/             # External services
│   │   ├── database/         # Database service
│   │   ├── ai/               # AI integration
│   │   └── spend_score/      # SpendScore engine
│   ├── utils/                # Utilities
│   │   ├── validators/       # Input validation
│   │   ├── helpers/          # Helper functions
│   │   └── constants/        # Application constants
│   ├── config/               # Configuration files
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/                 # Frontend application (optional)
├── deployment/              # Deployment configurations
│   ├── Dockerfile           # Docker configuration
│   ├── docker-compose.yml   # Docker Compose setup
│   └── render.yaml          # Render.com deployment
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

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
   cd veroctaai-clean
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user profile

### Analysis & Processing
- `POST /api/upload` - Upload CSV file for analysis
- `GET /api/spend-score` - Generate SpendScore analysis
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

## 🐳 Docker Deployment

### Build and Run
```bash
# Build Docker image
docker build -f deployment/Dockerfile -t veroctaai-api .

# Run container
docker run -p 5000:5000 \
  -e SESSION_SECRET=your-secret \
  -e OPENAI_API_KEY=your-key \
  veroctaai-api
```

### Docker Compose
```bash
# Run with Docker Compose
docker-compose -f deployment/docker-compose.yml up -d
```

## 🌐 Platform Deployment

### Render.com
1. Connect your GitHub repository
2. Use the provided `deployment/render.yaml`
3. Set environment variables in Render dashboard
4. Deploy automatically

### Heroku
```bash
# Create Heroku app
heroku create veroctaai-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SESSION_SECRET=your-secret

# Deploy
git push heroku main
```

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
```

## 🧪 Testing

### Health Check
```bash
curl https://veroctaai.onrender.com/api/health
```

### API Documentation
Visit: `https://veroctaai.onrender.com/api/docs`

## 📚 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[Frontend Integration](docs/FRONTEND_INTEGRATION_GUIDE.md)** - Integration guide
- **[Architecture Documentation](docs/ARCHITECTURE_DOCUMENTATION.md)** - System architecture

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
