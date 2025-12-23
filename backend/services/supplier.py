import os
import pandas as pd
from datetime import datetime
from ..services.azure_ai_service import AzureAIService
from dotenv import load_dotenv
import json

load_dotenv()

def predict_reliability(df: pd.DataFrame):
    """
    Predict supplier reliability using Azure OpenAI
    """
    ai_service = AzureAIService()
    results = []
    
    for _, row in df.iterrows():
        # Create a comprehensive prompt for reliability prediction
        prompt = f"""
        Analyze this supplier's reliability based on historical performance data:
        
        Supplier Details:
        - Supplier ID: {row.get('supplier_id', 'Unknown')}
        - Supplier Name: {row.get('supplier_name', 'Unknown')}
        - On-Time Percentage: {row.get('on_time_percentage', 0)}%
        - Quality Score: {row.get('quality_score', 0)}/10
        - Reliability Score: {row.get('reliability_score', 0)}
        - Total Orders: {row.get('total_orders', 0)}
        - Defect Rate: {row.get('defect_rate', 0)}%
        - Geographic Region: {row.get('region', 'Unknown')}
        - Years Active: {row.get('years_active', 0)}
        - Contract Compliance: {row.get('contract_compliance', 0)}%
        
        Based on these metrics, predict the supplier's future reliability.
        Consider factors like consistency, quality trends, and operational history.
        
        Provide a JSON response with:
        - reliability: "High", "Medium", or "Low"
        - confidence: 0.0 to 1.0
        - predicted_score: 0.0 to 1.0
        - reasoning: detailed explanation
        - risk_factors: list of potential risks
        - improvements: suggested improvements
        - future_trend: "improving", "stable", or "declining"
        """
        
        try:
            # Use the AI service to get prediction
            ai_response = ai_service._call_azure_openai(prompt, max_tokens=800)
            
            # Try to parse JSON response
            try:
                prediction_data = json.loads(ai_response)
            except json.JSONDecodeError:
                # Fallback to basic analysis if JSON parsing fails
                prediction_data = analyze_supplier_basic(row)
            
            # Add supplier ID to the result
            prediction_data['supplier_id'] = row.get('supplier_id', 'Unknown')
            prediction_data['supplier_name'] = row.get('supplier_name', 'Unknown')
            
            results.append(prediction_data)
            
        except Exception as e:
            # Fallback analysis in case of API failure
            print(f"Error predicting reliability for supplier {row.get('supplier_id')}: {str(e)}")
            fallback_result = analyze_supplier_basic(row)
            fallback_result['supplier_id'] = row.get('supplier_id', 'Unknown')
            fallback_result['supplier_name'] = row.get('supplier_name', 'Unknown')
            results.append(fallback_result)
    
    return results

def analyze_supplier_basic(row):
    """
    Basic fallback analysis for supplier reliability
    """
    on_time_pct = float(row.get('on_time_percentage', 0))
    quality_score = float(row.get('quality_score', 0))
    reliability_score = float(row.get('reliability_score', 0))
    defect_rate = float(row.get('defect_rate', 0))
    
    # Calculate composite score
    composite_score = (
        (on_time_pct / 100) * 0.3 +
        (quality_score / 10) * 0.25 +
        reliability_score * 0.25 +
        (max(0, 100 - defect_rate) / 100) * 0.2
    )
    
    # Determine reliability category
    if composite_score >= 0.8:
        reliability = "High"
        confidence = 0.85
        trend = "stable"
    elif composite_score >= 0.6:
        reliability = "Medium"
        confidence = 0.75
        trend = "improving" if on_time_pct > 80 else "stable"
    else:
        reliability = "Low"
        confidence = 0.80
        trend = "declining"
    
    # Identify risk factors
    risk_factors = []
    if on_time_pct < 80:
        risk_factors.append("Poor on-time delivery performance")
    if quality_score < 7:
        risk_factors.append("Below average quality scores")
    if defect_rate > 5:
        risk_factors.append("High defect rate")
    if reliability_score < 0.7:
        risk_factors.append("Low historical reliability")
    
    # Suggest improvements
    improvements = []
    if on_time_pct < 90:
        improvements.append("Improve delivery scheduling and logistics")
    if quality_score < 8:
        improvements.append("Enhance quality control processes")
    if defect_rate > 2:
        improvements.append("Implement defect reduction programs")
    
    if not improvements:
        improvements = ["Maintain current performance levels"]
    
    return {
        "reliability": reliability,
        "confidence": confidence,
        "predicted_score": composite_score,
        "reasoning": f"Based on {on_time_pct}% on-time delivery, {quality_score}/10 quality score, and {defect_rate}% defect rate, supplier shows {reliability.lower()} reliability.",
        "risk_factors": risk_factors if risk_factors else ["Minimal risk factors identified"],
        "improvements": improvements,
        "future_trend": trend
    }
