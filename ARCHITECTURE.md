# Supplier Performance Predictor - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          SUPPLIER PERFORMANCE PREDICTOR                         │
│                              System Architecture                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│     Users       │    │     Frontend        │    │  Nginx Proxy    │
│                 │    │                     │    │                 │
│ • Admin Panel   │◄──►│ • HTML/CSS/JS       │◄──►│ • Load Balancer │
│ • Analysts      │    │ • Jinja2 Templates  │    │ • SSL Termination│
│ • Suppliers     │    │ • Interactive UI    │    │ • Reverse Proxy │
└─────────────────┘    └─────────────────────┘    └─────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FASTAPI BACKEND                                   │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │  Authentication │  │   API Routes    │  │  Business Logic │                │
│  │                 │  │                 │  │                 │                │
│  │ • JWT Tokens    │  │ • /predict      │  │ • Auto-approval │                │
│  │ • User Sessions │  │ • /recommend    │  │ • Data Validation│                │
│  │ • Role-based    │  │ • /flag         │  │ • Multi-tenant  │                │
│  │   Access        │  │ • /admin        │  │   Isolation     │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Data Processing │ │  Database Layer │ │  AI Services    │
│                 │ │                 │ │                 │
│ • CSV Ingestion │ │ • SQLite/MySQL  │ │ • Azure OpenAI  │
│ • FAISS Vector  │ │ • User Management│ │ • GPT-4 Models  │
│ • Data Cleaning │ │ • System Settings│ │ • Embeddings    │
│ • Validation    │ │ • Audit Logs    │ │ • Vector Search │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Data Sources   │ │   Persistence   │ │ External APIs   │
│                 │ │                 │ │                 │
│ • suppliers.csv │ │ • Database Files│ │ • Azure OpenAI  │
│ • orders.csv    │ │ • Volume Mounts │ │ • LangSmith     │
│ • vendors.csv   │ │ • Backups       │ │ • Health Checks │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Component Details

### 🎯 Frontend Layer
- **Technology**: HTML5, CSS3, JavaScript, Jinja2 Templates
- **Features**: 
  - Interactive dashboard for supplier analysis
  - Admin panel for system configuration
  - Responsive design for mobile/desktop
  - Real-time status updates

### 🚀 Backend API (FastAPI)
- **Technology**: Python 3.9+, FastAPI, Uvicorn
- **Features**:
  - RESTful API with automatic documentation
  - JWT-based authentication
  - Multi-tenant data isolation
  - Auto-approval workflow
  - Comprehensive error handling

### 🤖 AI Services
- **Technology**: Azure OpenAI, FAISS, LangChain
- **Features**:
  - Supplier performance prediction
  - Risk assessment and flagging
  - Intelligent recommendations
  - Vector similarity search
  - Natural language processing

### 💾 Data Layer
- **Technology**: SQLite (dev), MySQL (prod), SQLAlchemy ORM
- **Features**:
  - User management and authentication
  - System settings persistence
  - Audit logging
  - Data validation and integrity

### 📊 Observability
- **Technology**: LangSmith, Health Checks, Logging
- **Features**:
  - AI operation tracing
  - Performance monitoring
  - Error tracking and alerting
  - Cost optimization

### 🐳 Infrastructure
- **Technology**: Docker, Docker Compose, Nginx
- **Features**:
  - Containerized deployment
  - Multi-stage builds for optimization
  - Production-ready orchestration
  - SSL termination and load balancing

## Data Flow

```
1. User Request → Nginx → FastAPI Backend
2. Authentication & Authorization Check
3. Route to Appropriate Service:
   
   For Predictions:
   User Input → Data Validation → AI Service → Azure OpenAI → Response
   
   For Admin Operations:
   Admin Request → Permission Check → Database Update → Response
   
   For File Upload:
   CSV File → Validation → Processing → FAISS Index → Storage

4. All Operations → LangSmith Tracing → Observability Dashboard
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Network Security                                             │
│    • Nginx SSL Termination                                     │
│    • Reverse Proxy Protection                                  │
│    • CORS Configuration                                        │
├─────────────────────────────────────────────────────────────────┤
│ 2. Application Security                                         │
│    • JWT Token Authentication                                  │
│    • Role-based Access Control                                 │
│    • Input Validation & Sanitization                           │
├─────────────────────────────────────────────────────────────────┤
│ 3. Data Security                                                │
│    • Multi-tenant Data Isolation                               │
│    • Encrypted Database Connections                            │
│    • Secure Environment Variables                              │
├─────────────────────────────────────────────────────────────────┤
│ 4. Container Security                                           │
│    • Non-root User Execution                                   │
│    • Minimal Base Images                                       │
│    • Security Scanning                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Patterns

### Development Deployment
```
Developer → Local Docker Container → SQLite Database
```

### Production Deployment
```
Load Balancer → Nginx → FastAPI Container → MySQL Database
                           ↓
                    External Services:
                    • Azure OpenAI
                    • LangSmith
```

### Scaling Options
```
Horizontal Scaling:
Load Balancer → Multiple FastAPI Instances → Shared Database

Vertical Scaling:
Enhanced Container Resources → Optimized Performance
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User Interface |
| **API** | FastAPI, Python 3.9+ | Backend Services |
| **Database** | SQLite/MySQL, SQLAlchemy | Data Persistence |
| **AI/ML** | Azure OpenAI, FAISS | Intelligent Features |
| **Observability** | LangSmith, Health Checks | Monitoring |
| **Infrastructure** | Docker, Docker Compose | Deployment |
| **Proxy** | Nginx | Load Balancing & SSL |
| **Security** | JWT, CORS, Validation | Protection |
