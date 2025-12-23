# LangSmith observability and tracing for Supplier Performance Predictor
import os
import time
import json
from typing import Dict, Any, Optional
from langsmith import Client
from langsmith.run_helpers import traceable
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupplierPredictorTracer:
    def __init__(self):
        self.api_key = os.getenv("LANGSMITH_API_KEY")
        self.project_name = os.getenv("LANGSMITH_PROJECT_NAME", "supplier-performance-predictor")
        self.client = None
        
        if self.api_key:
            try:
                self.client = Client(api_key=self.api_key)
                logger.info("LangSmith client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LangSmith: {e}")
        else:
            logger.warning("LANGSMITH_API_KEY not found. Tracing disabled.")
    
    @traceable(project_name="supplier-performance-predictor")
    def trace_supplier_prediction(self, 
                                supplier_data: Dict[str, Any], 
                                prediction_result: Dict[str, Any],
                                user_id: int,
                                execution_time: float) -> Dict[str, Any]:
        """
        Trace a supplier reliability prediction with detailed context
        """
        if not self.client:
            return prediction_result
            
        try:
            # Create run context
            run_context = {
                "inputs": {
                    "supplier_id": supplier_data.get("supplier_id"),
                    "supplier_name": supplier_data.get("supplier_name"),
                    "reliability_score": supplier_data.get("reliability_score"),
                    "delivery_rate": supplier_data.get("past_delivery_rate"),
                    "on_time_percentage": supplier_data.get("on_time_percentage"),
                    "category": supplier_data.get("category"),
                    "region": supplier_data.get("region"),
                    "user_id": user_id
                },
                "outputs": {
                    "ai_reliability_assessment": prediction_result.get("reliability"),
                    "predicted_score": prediction_result.get("score"),
                    "confidence_level": prediction_result.get("confidence"),
                    "trend_prediction": prediction_result.get("trend"),
                    "reasoning": prediction_result.get("reasoning", "")
                },
                "metadata": {
                    "execution_time_ms": execution_time * 1000,
                    "model_used": "azure-openai-gpt-4",
                    "prediction_type": "supplier_reliability",
                    "timestamp": time.time()
                }
            }
            
            logger.info(f"Traced prediction for supplier {supplier_data.get('supplier_id')}")
            return prediction_result
            
        except Exception as e:
            logger.error(f"LangSmith tracing failed: {e}")
            return prediction_result
    
    @traceable(project_name="supplier-performance-predictor")  
    def trace_batch_prediction(self,
                             suppliers_count: int,
                             successful_predictions: int,
                             failed_predictions: int,
                             total_execution_time: float,
                             user_id: int) -> Dict[str, Any]:
        """
        Trace batch predictions for analytics
        """
        if not self.client:
            return {}
            
        try:
            batch_metrics = {
                "inputs": {
                    "total_suppliers": suppliers_count,
                    "user_id": user_id,
                    "batch_type": "csv_upload"
                },
                "outputs": {
                    "successful_predictions": successful_predictions,
                    "failed_predictions": failed_predictions,
                    "success_rate": (successful_predictions / suppliers_count) * 100 if suppliers_count > 0 else 0,
                    "avg_prediction_time": total_execution_time / suppliers_count if suppliers_count > 0 else 0
                },
                "metadata": {
                    "total_execution_time_ms": total_execution_time * 1000,
                    "timestamp": time.time()
                }
            }
            
            logger.info(f"Traced batch prediction: {successful_predictions}/{suppliers_count} successful")
            return batch_metrics
            
        except Exception as e:
            logger.error(f"Batch tracing failed: {e}")
            return {}

    def trace_error(self, error_type: str, error_message: str, context: Dict[str, Any]):
        """
        Trace errors for debugging
        """
        if not self.client:
            return
            
        try:
            error_context = {
                "error_type": error_type,
                "error_message": str(error_message),
                "context": context,
                "timestamp": time.time()
            }
            logger.error(f"Traced error: {error_type} - {error_message}")
            
        except Exception as e:
            logger.error(f"Error tracing failed: {e}")

    @traceable(project_name="supplier-performance-predictor")
    def trace_azure_openai_call(self, 
                               prompt: str,
                               response: str,
                               tokens_used: int,
                               execution_time: float,
                               user_id: int) -> Dict[str, Any]:
        """
        Trace Azure OpenAI API calls
        """
        if not self.client:
            return {}
            
        try:
            ai_call_context = {
                "inputs": {
                    "prompt": prompt[:500] + "..." if len(prompt) > 500 else prompt,
                    "user_id": user_id,
                    "model": "azure-openai-gpt-4"
                },
                "outputs": {
                    "response": response[:1000] + "..." if len(response) > 1000 else response,
                    "tokens_used": tokens_used,
                    "estimated_cost": tokens_used * 0.00003  # Rough estimate
                },
                "metadata": {
                    "execution_time_ms": execution_time * 1000,
                    "timestamp": time.time(),
                    "api_provider": "azure_openai"
                }
            }
            
            logger.info(f"Traced Azure OpenAI call: {tokens_used} tokens, {execution_time:.2f}s")
            return ai_call_context
            
        except Exception as e:
            logger.error(f"Azure OpenAI tracing failed: {e}")
            return {}

    @traceable(project_name="supplier-performance-predictor")
    def trace_dashboard_access(self, 
                             user_id: int,
                             total_suppliers: int,
                             load_time: float) -> Dict[str, Any]:
        """
        Trace dashboard access for analytics
        """
        if not self.client:
            return {}
            
        try:
            dashboard_context = {
                "inputs": {
                    "user_id": user_id,
                    "action": "dashboard_access"
                },
                "outputs": {
                    "total_suppliers_loaded": total_suppliers,
                    "load_time_ms": load_time * 1000
                },
                "metadata": {
                    "timestamp": time.time(),
                    "feature": "dashboard"
                }
            }
            
            logger.info(f"Traced dashboard access for user {user_id}: {total_suppliers} suppliers")
            return dashboard_context
            
        except Exception as e:
            logger.error(f"Dashboard tracing failed: {e}")
            return {}

# Global tracer instance
tracer = SupplierPredictorTracer()

def trace_request(request):
    """Legacy function for backward compatibility"""
    if not tracer.client:
        return
    try:
        logger.info(f"HTTP Request: {request.method} {request.url}")
    except Exception as e:
        logger.error(f"Request tracing failed: {e}")
