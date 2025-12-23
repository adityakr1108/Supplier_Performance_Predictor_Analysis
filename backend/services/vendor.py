import os
import pandas as pd
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

def recommend_alternate_vendors(df: pd.DataFrame):
    client = get_azure_client()
    recommendations = []
    
    # Group by category and region for better recommendations
    for _, row in df.iterrows():
        # Find similar vendors in same category/region
        candidates = df[
            (df['category'] == row['category']) & 
            (df['region'] == row['region']) & 
            (df['supplier_id'] != row['supplier_id'])
        ].copy()
        
        if candidates.empty:
            # Try same category, different region
            candidates = df[
                (df['category'] == row['category']) & 
                (df['supplier_id'] != row['supplier_id'])
            ].copy()
        
        if not candidates.empty:
            # Create prompt for AI recommendation
            vendor_data = candidates.to_dict('records')
            prompt = f"""
            Current vendor: {row['supplier_id']} in {row['category']} category, {row['region']} region
            Lead time: {row['average_lead_time']} days
            
            Alternative vendors:
            {json.dumps(vendor_data, indent=2)}
            
            Recommend the top 2 alternative vendors considering:
            1. Shorter lead times
            2. Same or compatible category
            3. Regional preferences
            4. Overall reliability
            
            Return JSON: {{"recommendations": [
                {{"supplier_id": "SUP001", "score": 0.95, "reason": "Best lead time"}},
                {{"supplier_id": "SUP002", "score": 0.85, "reason": "Same region"}}
            ]}}
            """
            
            try:
                response = client.chat.completions.create(
                    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=300,
                    temperature=0.2
                )
                
                ai_response = response.choices[0].message.content.strip()
                try:
                    ai_recommendations = json.loads(ai_response)
                    recommended_vendors = ai_recommendations.get("recommendations", [])
                except:
                    # Fallback: sort by lead time
                    candidates_sorted = candidates.sort_values('average_lead_time')
                    recommended_vendors = [
                        {
                            "supplier_id": candidates_sorted.iloc[0]['supplier_id'],
                            "score": 0.8,
                            "reason": "Shortest lead time"
                        }
                    ]
                
                recommendations.append({
                    "original_supplier": row['supplier_id'],
                    "category": row['category'],
                    "region": row['region'],
                    "current_lead_time": row['average_lead_time'],
                    "alternatives": recommended_vendors
                })
                
            except Exception as e:
                # Simple fallback recommendation
                best_candidate = candidates.sort_values('average_lead_time').iloc[0]
                recommendations.append({
                    "original_supplier": row['supplier_id'],
                    "category": row['category'],
                    "region": row['region'],
                    "current_lead_time": row['average_lead_time'],
                    "alternatives": [{
                        "supplier_id": best_candidate['supplier_id'],
                        "score": 0.7,
                        "reason": f"Better lead time ({best_candidate['average_lead_time']} days)"
                    }]
                })
    
    return recommendations
