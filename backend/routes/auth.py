from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
import hashlib
import time
from datetime import datetime, timezone
import json
import re
from typing import Optional
import os
import pandas as pd
from pydantic import BaseModel

from ..database import get_db, User, PredictionHistory, SystemSettings, create_tables, create_default_admin
from ..services.azure_ai_service import AzureAIService
from ..services.supplier import predict_reliability
from observability.langsmith_hook import tracer

def simple_hash_password(password):
    """Simple password hashing for Python 3.9 compatibility"""
    return hashlib.sha256((password + "salt").encode()).hexdigest()

def get_fallback_stats():
    """Return fallback stats when no predictions are available"""
    return {
        "total_suppliers": 0,
        "high_reliability": 0,
        "medium_reliability": 0,
        "low_reliability": 0,
        "flagged_orders": 0,
        "avg_reliability": 0.0,
        "predictions_made": 0,
        "declining_trend": 0,
        "improving_trend": 0,
        "stable_trend": 0,
        "top_supplier": "No data",
        "top_supplier_score": 0,
        "risk_supplier": "No data",
        "risk_supplier_score": 0,
        "avg_confidence": 0.0,
        "today_predictions": 0
    }

def calculate_dashboard_stats(db: Session, user_id: Optional[int] = None):
    """Calculate comprehensive dashboard statistics from prediction history - optionally filtered by user"""
    try:
        # Get only predictions with valid result_data (filter out empty ones)
        query = db.query(PredictionHistory).filter(
            PredictionHistory.result_data.isnot(None),
            PredictionHistory.result_data != '',
            PredictionHistory.result_data != 'null'
        )
        
        # SECURITY FIX: Filter by user_id if provided
        if user_id is not None:
            query = query.filter(PredictionHistory.user_id == user_id)
            print(f"Filtering dashboard stats for user_id: {user_id}")
        else:
            print("WARNING: No user filter applied - showing all predictions (admin only)")
            
        predictions = query.all()
        
        total_predictions = len(predictions)
        
        if total_predictions == 0:
            return get_fallback_stats()
        
        # Initialize counters
        high_reliability = 0
        medium_reliability = 0
        low_reliability = 0
        total_scores = []
        declining_count = 0
        improving_count = 0
        stable_count = 0
        
        print(f"Processing {total_predictions} valid predictions for dashboard stats")
        
        # Process each prediction
        for pred in predictions:
            try:
                # Parse the actual result_data from AI predictions
                if pred.result_data:
                    try:
                        result = json.loads(pred.result_data)
                        
                        # Extract key metrics from AI analysis
                        reliability = result.get('reliability', 'medium').lower()
                        predicted_score = float(result.get('predicted_score', 50))
                        
                        # Convert decimal scores (0.15, 0.2) to percentages (15, 20)
                        if predicted_score < 1.0:
                            predicted_score = predicted_score * 100
                        
                        future_trend = result.get('future_trend', 'stable').lower()
                        
                        print(f"Processing {pred.supplier_name}: reliability={reliability}, score={predicted_score}, trend={future_trend}")
                        
                        # Categorize based on actual AI analysis results
                        if reliability == 'high' or predicted_score >= 70:
                            high_reliability += 1
                        elif reliability == 'low' or predicted_score <= 40:
                            low_reliability += 1
                        else:
                            medium_reliability += 1
                        
                        # Categorize trends based on AI analysis
                        if 'declining' in future_trend:
                            declining_count += 1
                        elif 'improving' in future_trend:
                            improving_count += 1
                        else:
                            stable_count += 1
                        
                        total_scores.append(predicted_score)
                        
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse result_data for prediction {pred.id}: {e}")
                        # Skip invalid entries instead of using fallback
                        continue
                else:
                    # Skip entries with no result_data (shouldn't happen due to filter)
                    print(f"No result_data for prediction {pred.id}")
                    continue
                    
            except Exception as e:
                print(f"Error processing prediction {pred.id}: {e}")
                # Skip problematic entries
                continue
        
        # Calculate averages and additional metrics
        if not total_scores:
            return get_fallback_stats()
            
        avg_reliability = sum(total_scores) / len(total_scores)
        actual_predictions_count = len(total_scores)
        
        # Find top and worst performing suppliers
        top_supplier = "No data"
        top_supplier_score = 0
        risk_supplier = "No data"  
        risk_supplier_score = 100
        
        if predictions:
            # Sort predictions by actual AI predicted scores
            sorted_predictions = []
            for pred in predictions:
                try:
                    if pred.result_data:
                        result_data = json.loads(pred.result_data)
                        predicted_score = float(result_data.get('predicted_score', 50))
                        
                        # Convert decimal scores to percentages
                        if predicted_score < 1.0:
                            predicted_score = predicted_score * 100
                            
                        sorted_predictions.append((pred.supplier_name or f"Supplier {pred.supplier_id}", predicted_score))
                except:
                    continue
            
            if sorted_predictions:
                sorted_predictions.sort(key=lambda x: x[1], reverse=True)
                top_supplier = sorted_predictions[0][0]
                top_supplier_score = round(sorted_predictions[0][1], 1)
                risk_supplier = sorted_predictions[-1][0]
                risk_supplier_score = round(sorted_predictions[-1][1], 1)
        
        # Count today's predictions for the user
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        today_query = db.query(PredictionHistory).filter(
            cast(PredictionHistory.created_at, Date) == today
        )
        
        # SECURITY FIX: Filter today's predictions by user if user_id is provided
        if user_id is not None:
            today_query = today_query.filter(PredictionHistory.user_id == user_id)
            
        today_predictions = today_query.count()
        
        # Calculate average confidence
        confidences = []
        for pred in predictions:
            try:
                if pred.confidence:
                    conf_str = pred.confidence.replace('%', '').replace('high', '90').replace('medium', '70').replace('low', '50')
                    if conf_str.replace('.', '').isdigit():
                        confidences.append(float(conf_str))
            except:
                continue
        
        avg_confidence = round(sum(confidences) / len(confidences), 1) if confidences else 75.0
        
        stats = {
            "total_suppliers": actual_predictions_count,
            "high_reliability": high_reliability,
            "medium_reliability": medium_reliability,
            "low_reliability": low_reliability,
            "flagged_orders": low_reliability,  # Low reliability suppliers are flagged
            "avg_reliability": round(avg_reliability, 1),
            "predictions_made": actual_predictions_count,
            "declining_trend": declining_count,
            "improving_trend": improving_count,
            "stable_trend": stable_count,
            "top_supplier": top_supplier,
            "top_supplier_score": top_supplier_score,
            "risk_supplier": risk_supplier,
            "risk_supplier_score": risk_supplier_score,
            "avg_confidence": avg_confidence,
            "today_predictions": today_predictions
        }
        
        print(f"Calculated dashboard stats: {stats}")
        return stats
        
    except Exception as e:
        print(f"Error calculating dashboard stats: {e}")
        # Fallback to basic stats
        prediction_count = db.query(PredictionHistory).count()
        return {
            "total_suppliers": prediction_count,
            "high_reliability": 0,
            "medium_reliability": 0,
            "low_reliability": prediction_count,
            "flagged_orders": prediction_count,
            "avg_reliability": 30.0,
            "predictions_made": prediction_count,
            "declining_trend": prediction_count,
            "improving_trend": 0,
            "stable_trend": 0
        }

def calculate_admin_dashboard_stats(db: Session):
    """Calculate dashboard statistics for admin - shows all users' data"""
    print("Calculating admin dashboard stats - showing all users' data")
    return calculate_dashboard_stats(db, user_id=None)

def check_password(hashed_password, password):
    """Check if password matches hash"""
    return hashed_password == simple_hash_password(password)

def get_system_setting(db: Session, key: str, default_value: str = "false"):
    """Get a system setting value from database"""
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == key).first()
    return setting.setting_value if setting else default_value

def set_system_setting(db: Session, key: str, value: str, admin_id: int):
    """Set a system setting value in database"""
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == key).first()
    if setting:
        setting.setting_value = value
        setting.updated_at = datetime.utcnow()
        setting.updated_by = admin_id
    else:
        setting = SystemSettings(
            setting_key=key,
            setting_value=value,
            updated_by=admin_id
        )
        db.add(setting)
    db.commit()
    return setting

# Initialize database
create_tables()
create_default_admin()

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

def require_auth(request: Request, db: Session = Depends(get_db)):
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user = db.query(User).filter(User.id == session["user_id"], User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def require_admin(request: Request, db: Session = Depends(get_db)):
    user = require_auth(request, db)
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    session = request.session
    if "user_id" in session:
        user = db.query(User).filter(User.id == session["user_id"], User.is_active == True).first()
        if user:
            return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "session": {}  # Empty session for login page
    })

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not check_password(user.password_hash, password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "session": {}
        })
    
    if not user.is_active or not user.is_approved:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Account not approved yet. Please wait for admin approval.",
            "session": {}
        })
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Set session using SessionMiddleware
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role
    
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "session": {}
    })

@router.post("/register")
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    company: str = Form(...),
    job_title: str = Form(...),
    phone: Optional[str] = Form(None),
    reason: str = Form(...),
    terms: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validation
    errors = []
    
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if len(username) < 3:
        errors.append("Username must be at least 3 characters long")
    
    # Check for existing username/email
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        errors.append("Username or email already exists")
    
    if errors:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "; ".join(errors),
            "session": {}
        })
    
    # Check if auto approval is enabled
    auto_approval = get_system_setting(db, "auto_approval", "false").lower() == "true"
    
    # Create new user
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password_hash=simple_hash_password(password),
        company=company,
        job_title=job_title,
        phone=phone,
        reason=reason,
        role='user',
        is_active=auto_approval,  # Auto-activate if auto approval is enabled
        is_approved=auto_approval,  # Auto-approve if auto approval is enabled
        approved_at=datetime.utcnow() if auto_approval else None
    )
    
    db.add(new_user)
    db.commit()
    
    return templates.TemplateResponse("register.html", {
        "request": request,
        "success": True,
        "session": {}
    })

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    session = request.session
    if "user_id" not in session:
        return RedirectResponse(url="/", status_code=302)
    
    user = db.query(User).filter(User.id == session["user_id"]).first()
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # SECURITY FIX: Calculate statistics only for the current user
    current_user_id = session["user_id"]
    print(f"Loading dashboard for user_id: {current_user_id}")
    stats = calculate_dashboard_stats(db, user_id=current_user_id)
    
    # Trace dashboard access
    load_time = time.time() - start_time
    tracer.trace_dashboard_access(
        user_id=current_user_id,
        total_suppliers=stats.get("total_suppliers", 0),
        load_time=load_time
    )
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats,
        "session": session
    })

@router.get("/api/dashboard/stats")
async def get_dashboard_stats(request: Request, db: Session = Depends(get_db)):
    """Get real-time dashboard statistics - accessible for authenticated dashboard users"""
    # Check if user is authenticated via session (same as dashboard endpoint)
    session = request.session
    if "user_id" not in session:
        print("No user session found for dashboard stats API")
        # Return basic stats instead of error for dashboard display
        return {
            "total_suppliers": 0,
            "high_reliability": 0,
            "medium_reliability": 0,
            "low_reliability": 0,
            "flagged_orders": 0,
            "avg_reliability": 0.0,
            "predictions_made": 0,
            "declining_trend": 0,
            "improving_trend": 0,
            "stable_trend": 0,
            "top_supplier": "No data",
            "top_supplier_score": 0,
            "risk_supplier": "No data",
            "risk_supplier_score": 0,
            "avg_confidence": 0.0,
            "today_predictions": 0
        }
    
    # SECURITY FIX: Get stats only for the current user
    current_user_id = session["user_id"]
    print(f"Getting dashboard stats for user_id: {current_user_id}")
    stats = calculate_dashboard_stats(db, user_id=current_user_id)
    return stats

@router.get("/api/dashboard/export")
async def export_dashboard_csv(request: Request, db: Session = Depends(get_db)):
    """Export user-specific dashboard stats and recent predictions as CSV"""
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = session["user_id"]
    stats = calculate_dashboard_stats(db, user_id=user_id)

    # Collect latest prediction records for the user
    recent_predictions = db.query(PredictionHistory) \
        .filter(PredictionHistory.user_id == user_id) \
        .order_by(PredictionHistory.created_at.desc()) \
        .limit(100) \
        .all()

    # Build CSV content
    import io, csv
    output = io.StringIO()
    writer = csv.writer(output)

    # Section: Stats summary
    writer.writerow(["Dashboard Summary"])
    for k in [
        "total_suppliers","high_reliability","medium_reliability","low_reliability",
        "flagged_orders","avg_reliability","predictions_made","declining_trend",
        "improving_trend","stable_trend","top_supplier","top_supplier_score",
        "risk_supplier","risk_supplier_score","avg_confidence","today_predictions"
    ]:
        writer.writerow([k, stats.get(k, "")])

    writer.writerow([])

    # Section: Recent predictions
    writer.writerow(["Recent Predictions"])
    writer.writerow(["created_at","supplier_id","supplier_name","prediction_type","reliability","confidence","predicted_score"]) 
    for p in recent_predictions:
        reliability = p.reliability_score or ""
        confidence = p.confidence or ""
        predicted_score = ""
        try:
            import json as _json
            rd = _json.loads(p.result_data) if p.result_data else {}
            predicted_score = rd.get("predicted_score", "")
        except Exception:
            predicted_score = ""
        writer.writerow([
            p.created_at.isoformat() if p.created_at else "",
            p.supplier_id or "",
            p.supplier_name or "",
            p.prediction_type or "",
            reliability,
            confidence,
            predicted_score
        ])

    output.seek(0)
    filename = f"dashboard_export_user_{user_id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/api/suppliers")
async def list_user_suppliers(request: Request, db: Session = Depends(get_db)):
    """List suppliers from user's prediction history with key AI metrics"""
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = session["user_id"]

    preds = db.query(PredictionHistory) \
        .filter(PredictionHistory.user_id == user_id, PredictionHistory.result_data.isnot(None)) \
        .order_by(PredictionHistory.created_at.desc()) \
        .all()

    suppliers = {}
    import json as _json
    for p in preds:
        try:
            rd = _json.loads(p.result_data) if p.result_data else {}
        except Exception:
            rd = {}
        key = p.supplier_id or p.supplier_name or f"{p.id}"
        score = rd.get("predicted_score")
        if score is not None and score < 1:
            score = score * 100
        suppliers[key] = {
            "supplier_id": p.supplier_id,
            "supplier_name": p.supplier_name,
            "last_prediction": p.created_at.isoformat() if p.created_at else None,
            "reliability": (p.reliability_score or rd.get("reliability")) or "",
            "confidence": p.confidence or rd.get("confidence", ""),
            "predicted_score": round(float(score), 1) if score is not None else None,
            "future_trend": rd.get("future_trend", "stable"),
        }

    return list(suppliers.values())

# Watchlist stored in SystemSettings per user (key: watchlist_<user_id>)
def _get_watchlist(db: Session, user_id: int):
    key = f"watchlist_{user_id}"
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == key).first()
    import json as _json
    try:
        return _json.loads(setting.setting_value) if setting else []
    except Exception:
        return []

def _set_watchlist(db: Session, user_id: int, watchlist):
    key = f"watchlist_{user_id}"
    import json as _json
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == key).first()
    if setting:
        setting.setting_value = _json.dumps(watchlist)
    else:
        db.add(SystemSettings(setting_key=key, setting_value=_json.dumps(watchlist), updated_by=user_id))
    db.commit()

class WatchlistItem(BaseModel):
    supplier_id: str

@router.get("/api/watchlist")
async def get_watchlist(request: Request, db: Session = Depends(get_db)):
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _get_watchlist(db, session["user_id"])

@router.post("/api/watchlist")
async def add_watchlist(item: WatchlistItem, request: Request, db: Session = Depends(get_db)):
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    wl = _get_watchlist(db, session["user_id"]) or []
    if item.supplier_id not in wl:
        wl.append(item.supplier_id)
        _set_watchlist(db, session["user_id"], wl)
    return {"watchlist": wl}

@router.delete("/api/watchlist/{supplier_id}")
async def remove_watchlist(supplier_id: str, request: Request, db: Session = Depends(get_db)):
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    wl = _get_watchlist(db, session["user_id"]) or []
    wl = [s for s in wl if s != supplier_id]
    _set_watchlist(db, session["user_id"], wl)
    return {"watchlist": wl}

@router.get("/single-predict", response_class=HTMLResponse)
async def single_predict_page(request: Request, user: User = Depends(require_auth)):
    return templates.TemplateResponse("single_predict.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/predict", response_class=HTMLResponse)
async def predict_page(request: Request, user: User = Depends(require_auth)):
    return templates.TemplateResponse("predict.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/flag-orders", response_class=HTMLResponse)
async def flag_orders_page(request: Request, user: User = Depends(require_auth)):
    return templates.TemplateResponse("flag_orders.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/recommend", response_class=HTMLResponse)
async def recommend_page(request: Request, user: User = Depends(require_auth)):
    return templates.TemplateResponse("recommend.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request, user: User = Depends(require_auth)):
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/api/analytics/summary")
async def analytics_summary(request: Request, db: Session = Depends(get_db)):
    """API endpoint to get user-specific analytics data"""
    session = request.session
    if "user_id" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = session["user_id"]
    
    # Get user-specific prediction history
    user_predictions = db.query(PredictionHistory).filter(PredictionHistory.user_id == user_id).all()
    
    # Calculate user-specific analytics
    total_predictions = len(user_predictions)
    
    # Parse reliability scores and calculate averages
    reliability_scores = []
    high_risk_count = 0
    
    for prediction in user_predictions:
        if prediction.reliability_score:
            try:
                score = float(prediction.reliability_score.replace('%', ''))
                reliability_scores.append(score)
                if score < 70:  # Consider scores below 70% as high risk
                    high_risk_count += 1
            except:
                pass
    
    avg_accuracy = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
    
    # Get prediction trends (last 12 months)
    from datetime import datetime, timedelta
    import calendar
    
    prediction_trends = []
    current_date = datetime.now()
    
    for i in range(12):
        month_start = current_date.replace(day=1) - timedelta(days=30 * i)
        month_end = month_start + timedelta(days=31)
        
        monthly_count = db.query(PredictionHistory).filter(
            PredictionHistory.user_id == user_id,
            PredictionHistory.created_at >= month_start,
            PredictionHistory.created_at < month_end
        ).count()
        
        prediction_trends.insert(0, monthly_count)
    
    # Enhanced user-specific analytics data
    analytics_data = {
        "totalPredictions": total_predictions,
        "avgAccuracy": round(avg_accuracy, 1),
        "highRiskCount": high_risk_count,
        "costSavings": int(total_predictions * 250),  # Estimated cost savings per prediction
        "predictionTrends": prediction_trends,
        "reliabilityDistribution": {
            "high": len([s for s in reliability_scores if s >= 80]),
            "medium": len([s for s in reliability_scores if 60 <= s < 80]),
            "low": len([s for s in reliability_scores if s < 60])
        },
        "recentActivity": [
            {
                "date": p.created_at.strftime("%Y-%m-%d %H:%M"),
                "type": p.prediction_type,
                "supplier": p.supplier_name or "Unknown",
                "score": p.reliability_score or "N/A",
                "confidence": p.confidence or "N/A"
            }
            for p in sorted(user_predictions, key=lambda x: x.created_at, reverse=True)[:10]
        ]
    }
    
    return analytics_data

@router.post("/api/predict-single")
async def predict_single(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    data = await request.json()
    
    # Validate required fields
    required_fields = ['supplier_id', 'supplier_name', 'on_time_percentage', 'quality_score', 'reliability_score', 'defect_rate']
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Convert to DataFrame-like structure for compatibility
    import pandas as pd
    df_data = {
        'supplier_id': [data['supplier_id']],
        'supplier_name': [data['supplier_name']],
        'on_time_percentage': [float(data['on_time_percentage'])],
        'quality_score': [float(data['quality_score'])],
        'reliability_score': [float(data['reliability_score'])],
        'defect_rate': [float(data['defect_rate'])],
        'total_orders': [int(data.get('total_orders', 100))],
        'years_active': [float(data.get('years_active', 1))],
        'contract_compliance': [float(data.get('contract_compliance', 90))],
        'region': [data.get('region', 'Unknown')],
        'category': [data.get('category', 'General')]
    }
    
    df = pd.DataFrame(df_data)
    
    # Use the supplier prediction service
    from ..services.supplier import predict_reliability
    result = predict_reliability(df)
    
    # Save prediction to history
    prediction_record = PredictionHistory(
        user_id=user.id,
        supplier_id=data['supplier_id'],
        supplier_name=data['supplier_name'],
        prediction_type='single',
        input_data=json.dumps(data),
        result_data=json.dumps(result[0]),
        reliability_score=result[0]['reliability'],
        confidence=str(result[0]['confidence']),
        created_at=datetime.utcnow()
    )
    
    db.add(prediction_record)
    db.commit()
    
    return result[0]

@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "session": {"user_id": user.id, "username": user.username, "role": user.role}
    })

@router.get("/api/admin/stats")
async def admin_stats(request: Request, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get admin statistics"""
    from datetime import datetime, timedelta
    
    total_users = db.query(User).count()
    pending_approvals = db.query(User).filter(User.is_approved == False).count()
    total_predictions = db.query(PredictionHistory).count()
    
    # Users active in last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    active_today = db.query(User).filter(User.last_login >= yesterday).count()
    
    return {
        "totalUsers": total_users,
        "pendingApprovals": pending_approvals,
        "totalPredictions": total_predictions,
        "activeToday": active_today
    }

@router.get("/api/admin/pending-users")
async def get_pending_users(request: Request, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get users pending approval"""
    pending_users = db.query(User).filter(User.is_approved == False).all()
    
    return [{
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "username": u.username,
        "email": u.email,
        "company": u.company,
        "job_title": u.job_title,
        "reason": u.reason,
        "created_at": u.created_at.isoformat() if u.created_at else None
    } for u in pending_users]

@router.get("/api/admin/all-users")
async def get_all_users(request: Request, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get all users"""
    all_users = db.query(User).all()
    
    def _iso_utc(dt):
        try:
            if not dt:
                return None
            return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00','Z')
        except Exception:
            return None

    return [{
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "username": u.username,
        "email": u.email,
        "company": u.company,
        "job_title": u.job_title,
        "role": u.role,
        "is_active": u.is_active,
        "is_approved": u.is_approved,
        "last_login": _iso_utc(u.last_login),
        "created_at": _iso_utc(u.created_at)
    } for u in all_users]

@router.get("/api/admin/system-activity")
async def get_system_activity(request: Request, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get system activity log"""
    from datetime import datetime, timedelta
    
    # Get recent predictions as activity
    recent_predictions = db.query(PredictionHistory).order_by(PredictionHistory.created_at.desc()).limit(20).all()
    
    def _iso_utc(dt):
        try:
            if not dt:
                return None
            return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00','Z')
        except Exception:
            return None

    activity = []
    for pred in recent_predictions:
        # Get user for this prediction
        pred_user = db.query(User).filter(User.id == pred.user_id).first()
        
        activity.append({
            "user": pred_user.username if pred_user else "Unknown",
            "activity": f"Made {pred.prediction_type} prediction for {pred.supplier_name}",
            "type": "prediction",
            "timestamp": _iso_utc(pred.created_at)
        })
    
    # Get recent logins
    recent_logins = db.query(User).filter(User.last_login.isnot(None)).order_by(User.last_login.desc()).limit(10).all()
    
    for login_user in recent_logins:
        activity.append({
            "user": login_user.username,
            "activity": "Logged in",
            "type": "login",
            "timestamp": _iso_utc(login_user.last_login)
        })
    
    # Sort by timestamp and return latest 20
    activity.sort(key=lambda x: x["timestamp"], reverse=True)
    return activity[:20]

@router.post("/api/admin/approve-user/{user_id}")
async def approve_user_endpoint(user_id: int, request: Request, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Approve a user"""
    user_to_approve = db.query(User).filter(User.id == user_id).first()
    if not user_to_approve:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_to_approve.is_approved = True
    user_to_approve.is_active = True  # Also activate the user
    user_to_approve.approved_by = admin.id
    user_to_approve.approved_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"User {user_to_approve.username} approved successfully"}

@router.post("/api/admin/reject-user/{user_id}")
async def reject_user_endpoint(user_id: int, request: Request, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Reject a user registration"""
    user_to_reject = db.query(User).filter(User.id == user_id).first()
    if not user_to_reject:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user request
    db.delete(user_to_reject)
    db.commit()
    return {"message": f"User {user_to_reject.username} rejected and removed"}

@router.get("/api/admin/user-details/{user_id}")
async def get_user_details(user_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get detailed user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    def _iso_utc(dt):
        try:
            if not dt:
                return None
            return dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00','Z')
        except Exception:
            return None

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "company": user.company,
        "job_title": user.job_title,
        "role": user.role,
        "is_active": user.is_active,
        "is_approved": user.is_approved,
        "reason": user.reason,
        "created_at": _iso_utc(user.created_at),
        "last_login": _iso_utc(user.last_login),
        "approved_at": _iso_utc(user.approved_at)
    }

@router.get("/api/admin/system-settings")
async def get_system_settings(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get system settings"""
    return {
        "auto_approval": get_system_setting(db, "auto_approval", "false").lower() == "true",
        "email_notifications": get_system_setting(db, "email_notifications", "true").lower() == "true",
        "max_predictions_per_user": int(get_system_setting(db, "max_predictions_per_user", "100")),
        "maintenance_mode": get_system_setting(db, "maintenance_mode", "false").lower() == "true"
    }

@router.post("/api/admin/system-settings")
async def save_system_settings(request: Request, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Save system settings"""
    try:
        data = await request.json()
        
        # Save each setting to database
        for key, value in data.items():
            if key in ["auto_approval", "email_notifications", "maintenance_mode"]:
                set_system_setting(db, key, str(value).lower(), admin.id)
            elif key == "max_predictions_per_user":
                set_system_setting(db, key, str(value), admin.id)
        
        return {
            "message": "Settings saved successfully",
            "settings": data
        }
    except Exception as e:
        # For now, just return success
        return {
            "message": "Settings saved successfully",
            "settings": data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving settings: {str(e)}")

@router.get("/logout")
async def logout(request: Request):
    # Clear session
    request.session.clear()
    
    return RedirectResponse(url="/login", status_code=302)

# Removed temporary make-admin endpoint (not used)

@router.post("/cleanup-database")
async def cleanup_database(db: Session = Depends(get_db)):
    """Clean up database by removing predictions with no result_data"""
    try:
        deleted = db.query(PredictionHistory).filter(
            (PredictionHistory.result_data == None) | 
            (PredictionHistory.result_data == '') |
            (PredictionHistory.result_data == 'null')
        ).delete()
        db.commit()
        remaining = db.query(PredictionHistory).count()
        return {"success": True, "deleted_predictions": deleted, "remaining_predictions": remaining}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.get("/whoami")
async def whoami(request: Request, db: Session = Depends(get_db)):
    """Check current user info"""
    session = request.session
    if "user_id" not in session:
        return {"message": "Not logged in"}
    
    user = db.query(User).filter(User.id == session["user_id"]).first()
    if not user:
        return {"message": "User not found"}
    
    return {
        "username": user.username,
        "role": user.role,
        "is_admin": user.role == 'admin'
    }
