from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    company = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    reason = Column(Text, nullable=False)
    role = Column(String(20), default='user')  # 'user' or 'admin'
    is_active = Column(Boolean, default=False)  # Requires admin approval
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    approved_by = Column(Integer, nullable=True)  # Admin who approved
    approved_at = Column(DateTime, nullable=True)

class SystemSettings(Base):
    __tablename__ = 'system_settings'
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(50), unique=True, nullable=False)
    setting_value = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)  # Admin who updated

class PredictionHistory(Base):
    __tablename__ = 'prediction_history'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    supplier_id = Column(String(50), nullable=True)
    supplier_name = Column(String(100), nullable=True)
    prediction_type = Column(String(20), nullable=False)  # 'single', 'batch', 'flag', 'recommend'
    input_data = Column(Text, nullable=True)  # JSON string of input data
    result_data = Column(Text, nullable=True)  # JSON string of results
    reliability_score = Column(String(20), nullable=True)
    confidence = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./supplier_predictor.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create default admin user if not exists
def create_default_admin():
    import hashlib
    
    def simple_hash_password(password):
        """Simple password hashing for Python 3.9 compatibility"""
        return hashlib.sha256((password + "salt").encode()).hexdigest()
    
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == 'admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@supplierpredictor.com',
                first_name='System',
                last_name='Administrator',
                password_hash=simple_hash_password('admin123'),  # Change this in production!
                company='System',
                job_title='Administrator',
                reason='System default admin account',
                role='admin',
                is_active=True,
                is_approved=True,
                approved_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (admin/admin123)")
    finally:
        db.close()
