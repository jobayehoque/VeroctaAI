# 🚀 FinDash Financial Intelligence Platform

**Professional-grade financial analysis platform with AI-powered insights and comprehensive SpendScore analytics.**

![FinDash](static/assets/images/findash-logo.png)

## ✨ Features

- **🧮 SpendScore Engine**: 6-metric weighted financial health calculation
- **🤖 AI Insights**: OpenAI GPT-4o powered recommendations
- **📊 Enhanced Visualizations**: Professional pie charts and analytics
- **🏢 Company Branding**: Logo upload and custom PDF reports
- **🔌 REST API**: Complete API suite for integration
- **📱 Responsive UI**: Modern Bootstrap 5 interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FinDashApp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the platform**
   ```
   http://127.0.0.1:5001
   ```

## 📊 Usage

### Web Interface
1. Upload your CSV financial data
2. Add company name and logo (optional)
3. Get instant SpendScore analysis
4. Download professional PDF report

### API Integration
```bash
# Upload and analyze
curl -X POST http://127.0.0.1:5001/api/upload \
  -F "file=@transactions.csv"

# Get SpendScore
curl -X GET http://127.0.0.1:5001/api/spend-score

# Download report
curl -X GET http://127.0.0.1:5001/api/report -o report.pdf
```

## 📁 Project Structure

```
VeroctaAIApp/
├── app.py                 # Main Flask application
├── routes.py              # API routes and handlers
├── csv_parser.py          # CSV processing logic
├── spend_score_engine.py  # SpendScore calculation
├── gpt_utils.py           # AI integration
├── pdf_generator.py       # Report generation
├── clone_verifier.py      # Project integrity
├── create_logo.py         # Logo creation utility
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── samples/               # Sample CSV files
├── uploads/               # Uploaded files
├── outputs/               # Generated reports
├── docs/                  # Documentation
└── requirements.txt       # Dependencies
```

## 📈 SpendScore Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| Frequency Score | 15% | Transaction frequency patterns |
| Category Diversity | 10% | Spending category distribution |
| Budget Adherence | 20% | Spending vs. expected patterns |
| Redundancy Detection | 15% | Duplicate/similar transactions |
| Spike Detection | 20% | Unusual large transactions |
| Waste Ratio | 20% | Non-essential spending analysis |

**Score Ranges:**
- 🟩 **Green (90-100)**: Excellent financial discipline
- 🟨 **Amber (70-89)**: Good management, optimization opportunities  
- 🟥 **Red (0-69)**: Significant improvement needed

## 🔌 API Documentation

Complete API documentation available at: `docs/API_DOCS.md`

### Key Endpoints
- `POST /api/upload` - Upload and analyze CSV
- `GET /api/spend-score` - Get latest analysis
- `GET /api/report` - Download PDF report
- `GET /api/verify-clone` - System health check

## 🏢 Company Branding

- Upload company logos (PNG, JPG, JPEG, SVG)
- Custom company names in reports
- Professional PDF branding
- Enhanced visual identity

## 🚢 Deployment

### Production Setup
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker Deployment
```bash
# Build image
docker build -t findash-ai .

# Run container
docker run -p 5001:5001 -e OPENAI_API_KEY=your_key findash-ai
```

See `docs/DEPLOYMENT.md` for detailed deployment instructions.

## 🧪 Testing

### Sample Data
Use provided sample files in `/samples/`:
- `quickbooks_sample.csv`
- `xero_sample.csv`

### API Testing
```bash
# Health check
curl http://127.0.0.1:5001/api/health

# Test upload
curl -X POST http://127.0.0.1:5001/api/upload \
  -F "file=@samples/quickbooks_sample.csv"
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: `/docs/`
- **API Reference**: `docs/API_DOCS.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **Enhancement Report**: `docs/FINAL_ENHANCEMENT_REPORT.md`

---

**VeroctaAI Financial Intelligence Platform v2.0.0**  
*Professional financial analysis with AI-powered insights*
