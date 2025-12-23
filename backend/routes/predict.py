import pandas as pd
import json
import time
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Request, Depends
from sqlalchemy.orm import Session
from ..services.supplier import predict_reliability
from ..database import get_db, User, PredictionHistory
from observability.langsmith_hook import tracer

router = APIRouter(prefix="/predict_supplier_reliability", tags=["Prediction"])

def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current user from session"""
    user_id = request.session.get("user_id")
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return None

@router.post("")
async def predict_supplier(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    start_time = time.time()
    successful_predictions = 0
    failed_predictions = 0
    
    try:
        # Read the uploaded CSV
        df = pd.read_csv(file.file)
        
        # Get current user
        current_user = get_current_user(request, db)
        current_user_id = current_user.id if current_user else 0
        
        # Get predictions with individual timing
        results = []
        for index, row in df.iterrows():
            prediction_start = time.time()
            
            try:
                # Get prediction for this supplier
                supplier_predictions = predict_reliability(pd.DataFrame([row]))
                result = supplier_predictions[0] if supplier_predictions else {}
                
                # Trace individual prediction
                prediction_time = time.time() - prediction_start
                tracer.trace_supplier_prediction(
                    supplier_data=row.to_dict(),
                    prediction_result=result,
                    user_id=current_user_id,
                    execution_time=prediction_time
                )
                
                results.append(result)
                successful_predictions += 1
                
            except Exception as e:
                failed_predictions += 1
                tracer.trace_error(
                    error_type="prediction_failed",
                    error_message=str(e),
                    context={
                        "supplier_id": row.get("supplier_id"),
                        "user_id": current_user_id,
                        "row_index": index
                    }
                )
                # Add empty result for failed prediction
                results.append({"error": str(e), "reliability": "unknown"})
        
        # Save predictions to database if user is logged in
        if current_user:
            for i, result in enumerate(results):
                try:
                    # Get supplier data from the row
                    row = df.iloc[i]
                    supplier_id = str(row.get('supplier_id', f'BATCH_{i+1}'))
                    supplier_name = str(row.get('supplier_name', f'Supplier_{i+1}'))
                    
                    # Create prediction record
                    prediction_record = PredictionHistory(
                        user_id=current_user.id,
                        supplier_id=supplier_id,
                        supplier_name=supplier_name,
                        prediction_type='batch',
                        input_data=json.dumps(row.to_dict()),
                        result_data=json.dumps(result),
                        reliability_score=result.get('reliability', 'Unknown'),
                        confidence=str(result.get('confidence', 0)),
                        created_at=datetime.utcnow()
                    )
                    
                    db.add(prediction_record)
                except Exception as e:
                    print(f"Error saving prediction {i}: {e}")
                    continue
            
            try:
                db.commit()
                print(f"Saved {len(results)} predictions to database for user {current_user.username}")
            except Exception as e:
                print(f"Error committing predictions to database: {e}")
                db.rollback()
        else:
            print("No user session found - predictions not saved to database")
        
        # Trace batch results
        total_time = time.time() - start_time
        tracer.trace_batch_prediction(
            suppliers_count=len(df),
            successful_predictions=successful_predictions,
            failed_predictions=failed_predictions,
            total_execution_time=total_time,
            user_id=current_user_id
        )
        
        return {"predictions": results}
        
    except Exception as e:
        tracer.trace_error("batch_processing_failed", str(e), {"user_id": current_user_id if 'current_user_id' in locals() else 0})
        print(f"Error processing file: {e}")
        return {"error": str(e), "predictions": []}
