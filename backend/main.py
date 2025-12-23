import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from backend.routes import predict, auth
from backend.database import create_tables, create_default_admin

app = FastAPI(
    title="Supplier Performance Predictor",
    description="AI-powered supplier reliability prediction and risk management",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "service": "Supplier Performance Predictor",
        "version": "1.0.0"
    }

# Initialize database
create_tables()
create_default_admin()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-this-in-production")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include routers
app.include_router(auth.router)  # Auth routes (includes root)
app.include_router(predict.router, prefix="/api")
