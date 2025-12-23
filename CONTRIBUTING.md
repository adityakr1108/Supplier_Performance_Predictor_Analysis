# Contributing to Supplier Performance Predictor AI System

We welcome contributions to the Supplier Performance Predictor AI System! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Azure OpenAI API access
- Basic understanding of FastAPI, SQLAlchemy, and AI/ML concepts

### Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/your-username/supplier-performance-predictor.git
cd supplier-performance-predictor
```

2. **Create Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

4. **Set Up Environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize Database**
```bash
python3 -c "from backend.database import create_tables, create_default_admin; create_tables(); create_default_admin()"
```

6. **Run Tests**
```bash
pytest
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where possible
- Write descriptive variable and function names
- Add docstrings to functions and classes

### Project Structure
```
supplier-performance-predictor/
├── backend/
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── database.py      # Database models
│   └── main.py         # FastAPI application
├── frontend/
│   ├── templates/      # HTML templates
│   └── static/         # CSS, JS, images
├── observability/      # Monitoring and logging
├── data/              # Sample data files
└── tests/             # Test files
```

### Commit Messages
Use conventional commit messages:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` code style changes
- `refactor:` code refactoring
- `test:` test additions/changes
- `chore:` maintenance tasks

Example:
```
feat: add batch prediction endpoint
fix: resolve user authentication issue
docs: update API documentation
```

## 🛠️ Contributing Process

### 1. Create an Issue
Before starting work, create an issue to discuss:
- Bug reports
- Feature requests
- Performance improvements
- Documentation updates

### 2. Fork and Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Write clean, tested code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_predictions.py

# Run with coverage
pytest --cov=backend

# Test the application manually
python3 -m uvicorn backend.main:app --reload
```

### 5. Submit Pull Request
- Push your branch to your fork
- Create a pull request with a clear description
- Link related issues
- Ensure all checks pass

## 🧪 Testing Guidelines

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (Azure OpenAI, etc.)

### Test Structure
```python
def test_prediction_endpoint_success():
    """Test successful supplier prediction."""
    # Arrange
    supplier_data = {...}
    
    # Act
    response = client.post("/api/predict", json=supplier_data)
    
    # Assert
    assert response.status_code == 200
    assert "reliability_score" in response.json()
```

### Running Tests
```bash
# All tests
pytest

# Specific category
pytest tests/test_api.py
pytest tests/test_database.py
pytest tests/test_services.py

# With coverage
pytest --cov=backend --cov-report=html
```

## 📖 Documentation

### API Documentation
- All endpoints should have proper FastAPI documentation
- Include request/response examples
- Document error responses

### Code Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include type hints

Example:
```python
def predict_supplier_reliability(
    supplier_data: Dict[str, Any],
    user_id: int
) -> PredictionResult:
    """Predict supplier reliability using AI.
    
    Args:
        supplier_data: Dictionary containing supplier information
        user_id: ID of the user making the prediction
        
    Returns:
        PredictionResult with reliability score and analysis
        
    Raises:
        ValidationError: If supplier data is invalid
        AIServiceError: If AI service fails
    """
```

## 🔧 Areas for Contribution

### High Priority
- **Performance Optimization**: Improve response times
- **Test Coverage**: Increase test coverage
- **Error Handling**: Better error messages and recovery
- **Security**: Additional security measures

### Medium Priority
- **Feature Enhancements**: New prediction algorithms
- **UI/UX Improvements**: Better user interface
- **Documentation**: Expand user guides
- **Integration**: Add new data sources

### Low Priority
- **Code Refactoring**: Improve code structure
- **Dependencies**: Update and optimize dependencies
- **Monitoring**: Enhanced observability features

## 🐛 Bug Reports

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs
- Screenshots if applicable

## 💡 Feature Requests

For feature requests, provide:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Any relevant examples or mockups

## 🔒 Security

If you discover security vulnerabilities:
- **DO NOT** create a public issue
- Email security concerns privately
- Provide detailed information about the vulnerability
- Allow time for the issue to be addressed before disclosure

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check README.md and inline documentation
- **Code Examples**: Look at existing tests and implementations

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to the Supplier Performance Predictor AI System! 🚀
