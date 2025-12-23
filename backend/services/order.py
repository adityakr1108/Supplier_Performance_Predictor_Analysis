import os
import pandas as pd
from datetime import datetime, timedelta
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

def get_azure_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def flag_high_risk_orders(df: pd.DataFrame):
    client = get_azure_client()
    results = []
    
    for _, row in df.iterrows():
        # Calculate days until delivery
        try:
            delivery_date = datetime.strptime(row['expected_delivery_date'], '%Y-%m-%d')
            days_until_delivery = (delivery_date - datetime.now()).days
        except:
            days_until_delivery = 0
        
        # Create prompt for AI risk analysis
        prompt = f"""
        Analyze this order's risk level:
        - Order ID: {row['order_id']}
        - Supplier ID: {row['supplier_id']}
        - Expected Delivery Date: {row['expected_delivery_date']}
        - Days Until Delivery: {days_until_delivery}
        - Historical Risk Flags: {row['historical_risk_flags']}
        
        Based on these factors, determine if this is a high-risk order.
        Consider: tight delivery timeline, supplier history, past risk flags.
        
        Return JSON: {{"high_risk": true/false, "risk_score": 0.8, "risk_factors": ["factor1", "factor2"]}}
        """
        
        try:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=150,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            try:
                risk_analysis = json.loads(ai_response)
            except:
                # Fallback analysis
                high_risk = row['historical_risk_flags'] > 1 or days_until_delivery < 3
                risk_analysis = {
                    "high_risk": high_risk,
                    "risk_score": 0.7 if high_risk else 0.3,
                    "risk_factors": ["Historical issues", "Tight timeline"] if high_risk else []
                }
            
            if risk_analysis.get("high_risk", False):
                results.append({
                    "order_id": row['order_id'],
                    "supplier_id": row['supplier_id'],
                    "high_risk": True,
                    "risk_score": risk_analysis.get("risk_score", 0.5),
                    "risk_factors": risk_analysis.get("risk_factors", []),
                    "expected_delivery_date": row['expected_delivery_date'],
                    "days_until_delivery": days_until_delivery,
                    "historical_risk_flags": row['historical_risk_flags']
                })
                
        except Exception as e:
            # Fallback to rule-based flagging
            high_risk = row['historical_risk_flags'] > 1 or days_until_delivery < 3
            if high_risk:
                results.append({
                    "order_id": row['order_id'],
                    "supplier_id": row['supplier_id'],
                    "high_risk": True,
                    "risk_score": 0.7,
                    "risk_factors": ["Rule-based analysis"],
                    "expected_delivery_date": row['expected_delivery_date'],
                    "days_until_delivery": days_until_delivery,
                    "historical_risk_flags": row['historical_risk_flags']
                })
    
    return results
