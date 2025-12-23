# 🚀 Supplier Performance Predictor AI System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-orange.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![LangSmith](https://img.shields.io/badge/LangSmith-Observability-purple.svg)](https://smith.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade AI-powered supply chain intelligence system that predicts supplier reliability, identifies high-risk orders, and recommends alternate vendors using Azure OpenAI GPT-4 with comprehensive observability.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 Overview

### Problem Statement

Supply chain disruptions cost businesses millions annually. Traditional supplier evaluation methods are reactive and lack predictive capabilities. This system provides:

- **Proactive Risk Assessment** - Predict supplier reliability before issues occur
- **Real-time Order Flagging** - Automatically identify high-risk orders  
- **Smart Vendor Recommendations** - AI-powered alternative supplier suggestions
- **Data-Driven Insights** - Comprehensive analytics for decision-making
- **Complete Observability** - Monitor AI performance, costs, and reliability with LangSmith

### Key Capabilities

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Predictions** | Azure OpenAI GPT-4 for supplier reliability analysis |
| 📊 **Real-time Dashboard** | Interactive analytics with performance trends |
| 🔒 **Enterprise Security** | Multi-tenant architecture with role-based access |
| 📈 **Advanced Analytics** | Risk distribution, trend forecasting, and KPIs |
| 🔍 **Observability** | LangSmith integration for AI monitoring |
| 🚀 **Batch Processing** | Analyze multiple suppliers simultaneously |

---

## ✨ Features

### 🤖 AI & Machine Learning

- **Azure OpenAI Integration** - GPT-4 powered intelligent analysis
- **Vector Embeddings** - FAISS-powered similarity search for recommendations
- **Semantic Kernel** - Advanced AI orchestration framework
- **Batch Processing** - Handle multiple suppliers efficiently
- **LangSmith Observability** - Real-time AI monitoring, tracing, and cost tracking

### 📊 Dashboard & Analytics

- **Interactive Visualizations** - Real-time charts and graphs
- **KPI Monitoring** - Track key performance indicators
- **Risk Analysis** - Supplier risk distribution and trends
- **Export Capabilities** - PDF reports and data exports
- **Responsive Design** - Mobile-friendly interface

### 🔒 Security & Access Control

- **Multi-Tenant Architecture** - Complete data isolation between users
- **Role-Based Access** - User and Admin roles with granular permissions
- **Session Authentication** - Secure session management
- **Approval Workflow** - Admin approval for new registrations
- **Audit Trails** - Complete activity logging

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Web Browser    │────▶│  FastAPI Backend │────▶│  Azure OpenAI   │
│  (Dashboard)    │◀────│  (Python 3.9+)   │◀────│  (GPT-4)        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │      │
                               │      │
                               ▼      ▼
                        ┌───────────┐ ┌──────────────┐
                        │PostgreSQL │ │  LangSmith   │
                        │ Database  │ │ Observability│
                        └───────────┘ └──────────────┘
```

### Technology Stack

**Backend**
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- PostgreSQL/SQLite - Data storage
- Pandas - Data processing

**AI & ML**
- Azure OpenAI - GPT-4 integration
- Semantic Kernel - AI orchestration
- FAISS - Vector similarity search
- LangSmith - AI observability

**Frontend**
- HTML5/CSS3/JavaScript
- Jinja2 Templates
- Chart.js - Data visualization
- Bootstrap - Responsive UI

**Infrastructure**
- Docker - Containerization
- Render - Cloud deployment
- PostgreSQL - Production database

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** installed
- **Azure OpenAI API** key ([Get one here](https://azure.microsoft.com/en-us/products/ai-services/openai-service))
- **LangSmith API** key (optional, [Sign up here](https://smith.langchain.com/))
- **Git** installed

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis.git
   cd Supplier_Performance_Predictor_Analysis
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

   Required variables:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   
   # Optional - for AI observability
   LANGSMITH_API_KEY=your_langsmith_key
   LANGSMITH_PROJECT=supplier-performance-predictor
   ```

5. **Initialize Database**
   ```bash
   python3 -c "from backend.database import create_tables, create_default_admin; create_tables(); create_default_admin()"
   ```

### Running Locally

```bash
# Start the server
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Access the application
# - Web Interface: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Default Login: admin / admin123
```

---

## 🌐 Deployment

### Deploy to Render (Recommended)

1. **Create a Render Account** at [render.com](https://render.com)

2. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `supplier-performance-db`
   - Plan: Free
   - Copy the "Internal Database URL"

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Runtime: Docker
   - Plan: Free

4. **Configure Environment Variables**
   ```
   DATABASE_URL = <your-postgres-internal-url>
   AZURE_OPENAI_API_KEY = <your-azure-key>
   AZURE_OPENAI_ENDPOINT = <your-azure-endpoint>
   AZURE_OPENAI_DEPLOYMENT_NAME = gpt-4.1
   AZURE_OPENAI_API_VERSION = 2024-12-01-preview
   LANGSMITH_API_KEY = <your-langsmith-key>
   LANGSMITH_PROJECT = supplier-performance-predictor
   SECRET_KEY = <random-secret-key>
   ```

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Access your app at: `https://your-app.onrender.com`

### Deploy with Docker

```bash
# Build the image
docker build -t supplier-predictor .

# Run the container
docker run -d \
  -p 8000:8001 \
  -e AZURE_OPENAI_API_KEY="your-key" \
  -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
  supplier-predictor

# Access at http://localhost:8000
```

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | User authentication |
| `POST` | `/register` | New user registration |
| `GET` | `/logout` | User logout |

### Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict_supplier_reliability` | Batch supplier prediction |
| `POST` | `/api/single_predict` | Single supplier analysis |
| `POST` | `/api/flag_orders` | Identify high-risk orders |
| `POST` | `/api/recommend_vendors` | Get vendor recommendations |

### Dashboard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/dashboard/stats` | User dashboard statistics |
| `GET` | `/api/dashboard/history` | Prediction history |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/admin/stats` | System statistics |
| `GET` | `/api/admin/pending-users` | Pending approvals |
| `POST` | `/api/admin/approve-user/{id}` | Approve user |
| `GET` | `/api/admin/system-settings` | Get settings |
| `POST` | `/api/admin/system-settings` | Update settings |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/predict_supplier_reliability" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@suppliers.csv"
```

**Interactive API Documentation:** Visit `/docs` when server is running

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Yes | Azure OpenAI API key | - |
| `AZURE_OPENAI_ENDPOINT` | Yes | Azure OpenAI endpoint URL | - |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Yes | GPT-4 deployment name | `gpt-4.1` |
| `AZURE_OPENAI_API_VERSION` | Yes | API version | `2024-12-01-preview` |
| `DATABASE_URL` | No | PostgreSQL connection string | `sqlite:///./supplier_predictor.db` |
| `LANGSMITH_API_KEY` | No | LangSmith API key for observability | - |
| `LANGSMITH_PROJECT` | No | LangSmith project name | `supplier-performance-predictor` |
| `SECRET_KEY` | No | Session secret key | Auto-generated |
| `DEFAULT_ADMIN_USERNAME` | No | Admin username | `admin` |
| `DEFAULT_ADMIN_PASSWORD` | No | Admin password | `admin123` |

### System Settings (Admin Panel)

- **Auto Approval** - Automatically approve new user registrations
- **Max Predictions Per User** - Set prediction limits
- **Email Notifications** - Enable/disable alerts
- **Maintenance Mode** - System-wide maintenance toggle

---

## 📖 Usage Guide

### 1. User Registration

1. Visit the application URL
2. Click "Register" on the login page
3. Fill in your details:
   - Username, email, name
   - Company and job title
   - Reason for access
4. Wait for admin approval (or auto-approval if enabled)

### 2. Upload Supplier Data

**CSV Format Required:**
```csv
supplier_id,supplier_name,reliability_score,past_delivery_rate,on_time_percentage,category,region,risk_level
SUP001,TechCorp,0.95,0.98,98,Electronics,Asia,Low
SUP002,ManufactureCo,0.87,0.92,92,Manufacturing,Europe,Medium
```

**Upload Steps:**
1. Navigate to "Predict" page
2. Click "Choose File"
3. Select your CSV file
4. Click "Upload and Predict"

### 3. View Predictions

The AI analyzes each supplier and provides:
- **Reliability Score** (High/Medium/Low)
- **Confidence Level** (0-100%)
- **Risk Factors** identified
- **Improvement Suggestions**
- **Future Trend** prediction

### 4. Dashboard Analytics

Access real-time insights:
- Total suppliers analyzed
- Average reliability scores
- Risk distribution charts
- Prediction history
- Performance trends

### 5. Admin Functions

**Admin Panel Features:**
- Approve pending user registrations
- View system statistics
- Manage user accounts
- Configure system settings
- Monitor prediction activity

---

## 🐛 Troubleshooting

### Common Issues

#### Azure OpenAI Connection Errors

**Symptoms:** "Connection error" or "deployment issue" in logs

**Solutions:**
1. Verify your API key is correct
2. Check endpoint URL format: `https://your-resource.openai.azure.com/`
3. Ensure deployment name matches your Azure deployment
4. Verify API version compatibility

```bash
# Test your Azure OpenAI connection
python3 -c "from backend.services.azure_openai_client import get_azure_openai_client; client, deployment = get_azure_openai_client(); print('✅ Connection successful!')"
```

#### Database Connection Issues

**Symptoms:** "readonly database" or "database locked" errors

**Solutions:**
- Ensure proper file permissions for SQLite
- Use PostgreSQL for production deployments
- Check DATABASE_URL environment variable

#### Port Already in Use

**Symptoms:** "Address already in use" error

**Solution:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python3 -m uvicorn backend.main:app --port 8001
```

#### Import Errors / Missing Dependencies

**Solution:**
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### Debug Mode

Enable detailed logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python3 -m uvicorn backend.main:app --log-level debug
```

### Get Help

- 📚 Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions
- 🏗️ See [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture details
- 🐛 [Open an issue](https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis/issues) for bug reports
- 📧 Contact: See repository for contact information

---

## 📁 Project Structure

```
supplier-performance-predictor/
├── backend/
│   ├── main.py                     # FastAPI application entry point
│   ├── database.py                 # Database models and setup
│   ├── routes/
│   │   ├── auth.py                 # Authentication routes
│   │   └── predict.py              # Prediction endpoints
│   └── services/
│       ├── azure_ai_service.py     # Azure OpenAI integration
│       ├── azure_openai_client.py  # OpenAI client wrapper
│       ├── supplier.py             # Supplier analysis logic
│       ├── order.py                # Order processing
│       ├── vendor.py               # Vendor recommendations
│       └── faiss_db.py             # Vector database
├── frontend/
│   ├── static/                     # CSS, JS, images
│   └── templates/                  # HTML templates
│       ├── login.html
│       ├── dashboard.html
│       ├── admin.html
│       └── ...
├── data/
│   ├── suppliers.csv               # Sample supplier data
│   ├── orders.csv                  # Sample order data
│   └── vendors.csv                 # Sample vendor data
├── observability/
│   └── langsmith_hook.py           # LangSmith integration
├── Dockerfile                      # Container configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── DEPLOYMENT_GUIDE.md             # Deployment instructions
├── ARCHITECTURE.md                 # System architecture
└── README.md                       # This file
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Azure OpenAI** for GPT-4 integration
- **LangSmith** for AI observability
- **FastAPI** for the excellent web framework
- **Render** for deployment platform

---

## 📞 Support

- 📖 **Documentation:** Check the `/docs` endpoint
- 🐛 **Bug Reports:** [Open an issue](https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis/issues)
- 💬 **Questions:** See repository discussions
- 📧 **Email:** Contact repository owner

---

<div align="center">

**Built with ❤️ for supply chain optimization**

[Report Bug](https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis/issues) · [Request Feature](https://github.com/adityakr1108/Supplier_Performance_Predictor_Analysis/issues)

</div>
