#!/bin/bash

# Supplier Performance Predictor AI System - Setup Script
# This script helps you set up the system quickly

echo "🚀 Setting up Supplier Performance Predictor AI System..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d" " -f2 | cut -d"." -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "📝 Please edit .env file with your Azure OpenAI and LangSmith credentials"
else
    echo "✅ Environment file already exists"
fi

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from backend.database import create_tables, create_default_admin; create_tables(); create_default_admin()"

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database"
    exit 1
fi

echo "✅ Database initialized successfully"

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    mkdir data
    echo "📁 Created data directory"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials:"
echo "   - AZURE_OPENAI_API_KEY"
echo "   - AZURE_OPENAI_ENDPOINT"
echo "   - AZURE_OPENAI_DEPLOYMENT_NAME"
echo "   - LANGSMITH_API_KEY (optional)"
echo ""
echo "2. Start the server:"
echo "   python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001"
echo ""
echo "3. Access the application:"
echo "   - Web Interface: http://localhost:8001"
echo "   - Admin Login: admin / admin123"
echo "   - API Docs: http://localhost:8001/docs"
echo ""
echo "4. Upload your supplier data in CSV format"
echo ""
echo "📖 Read the README.md for detailed usage instructions"
echo "🔍 Monitor AI performance at https://smith.langchain.com (if LangSmith configured)"
echo ""
echo "Happy predicting! 🎯"
