# LangSmith Integration Guide

## 🎯 What is LangSmith?

LangSmith is an advanced observability platform for LLM applications that provides:
- **Real-time monitoring** of AI model calls
- **Performance analytics** (latency, tokens, costs)
- **Debug traces** for failed predictions
- **Prompt optimization** tools
- **Production monitoring** with alerts

## 🚀 Setup Instructions

### 1. Create LangSmith Account
1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up for a free account
3. Create a new project: "supplier-performance-predictor"
4. Navigate to Settings → API Keys
5. Generate a new API key

### 2. Install Dependencies
```bash
pip install langsmith langchain-openai
```

### 3. Configure Environment Variables
Add to your `.env` file:
```bash
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGSMITH_PROJECT_NAME=supplier-performance-predictor
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

### 4. Restart Your Application
```bash
# Stop the server
pkill -f uvicorn

# Start with LangSmith enabled
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

## 📊 What You'll Monitor

### Individual Supplier Predictions
- **Input**: Supplier data (reliability score, delivery rate, etc.)
- **Output**: AI reliability assessment and confidence
- **Metrics**: Response time, tokens used, cost per prediction
- **Context**: User ID, supplier category, region

### Batch Predictions
- **Success Rate**: Percentage of successful predictions
- **Performance**: Average prediction time per supplier
- **Errors**: Failed predictions with full context
- **User Activity**: Which users are most active

### Dashboard Analytics
- **Load Times**: How fast dashboards load for users
- **Data Volume**: Number of suppliers per user
- **Usage Patterns**: Peak usage times and features

## 🔍 LangSmith Dashboard Features

### Traces View
See every AI interaction:
```
Supplier Prediction Trace
├── Input: TechCorp Industries (Region: North America)
├── AI Model: Azure OpenAI GPT-4
├── Output: Low reliability (Score: 15.0)
├── Execution Time: 1.2s
├── Tokens Used: 450
└── Cost: $0.014
```

### Analytics Dashboard
Track performance over time:
- **Prediction Volume**: 156 predictions today
- **Success Rate**: 94.2% successful
- **Average Latency**: 1.2s per prediction
- **Daily Cost**: $2.34 in AI calls
- **Error Rate**: 5.8% failures

### Debug Tools
When predictions fail:
```
Error Trace: prediction_failed
├── Supplier: Elite Manufacturing (ID: SUP005)
├── Error: Azure OpenAI timeout
├── Context: User 1, Batch upload
├── Timestamp: 2025-09-12 14:30:15
└── Stack Trace: [Full error details]
```

## 📈 Business Insights

### Cost Optimization
- Track which supplier types are most expensive to analyze
- Identify optimal batch sizes for efficiency
- Monitor daily/monthly AI spending

### User Behavior
- See which users upload the most suppliers
- Identify popular dashboard features
- Track user retention and engagement

### System Performance
- Monitor API response times
- Track error patterns and root causes
- Identify performance bottlenecks

## 🚨 Alerts and Monitoring

### Set up alerts for:
- **High Error Rate**: >10% failures in 1 hour
- **Slow Performance**: >3s average response time
- **Cost Spikes**: Daily spending >$50
- **System Issues**: Azure OpenAI downtime

## 🛠️ Advanced Features

### Custom Metrics
```python
# Track custom business metrics
tracer.trace_custom_metric(
    metric_name="high_risk_suppliers_detected",
    value=15,
    user_id=user_id,
    context={"region": "Asia", "category": "Electronics"}
)
```

### A/B Testing
Test different AI prompts:
```python
# Version A: Current prompt
result_a = predict_with_prompt_v1(supplier_data)

# Version B: New prompt
result_b = predict_with_prompt_v2(supplier_data)

# Compare performance in LangSmith
```

### Real-time Dashboards
Build custom dashboards for:
- Executive KPI tracking
- Operations monitoring
- Cost management
- User analytics

## 📋 Getting Started Checklist

- [ ] Create LangSmith account
- [ ] Add API key to `.env` file
- [ ] Install dependencies
- [ ] Restart application
- [ ] Upload test suppliers
- [ ] Check LangSmith dashboard
- [ ] Set up alerts
- [ ] Review analytics

## 🎯 Expected Benefits

### For Developers
- **Faster debugging** of AI prediction issues
- **Performance optimization** insights
- **Cost tracking** for Azure OpenAI usage
- **User behavior** understanding

### For Business
- **Reliability monitoring** of supplier predictions
- **Cost control** for AI operations
- **User engagement** analytics
- **System uptime** tracking

### For Users
- **Better predictions** through optimized prompts
- **Faster responses** through performance tuning
- **Higher reliability** through error monitoring
- **Enhanced features** based on usage data

## 📞 Support

- **LangSmith Docs**: [docs.smith.langchain.com](https://docs.smith.langchain.com)
- **Community**: LangChain Discord
- **Support**: support@langchain.dev

Start monitoring your AI supplier predictions today! 🚀
