import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import Azure AI Service
from backend.services.azure_ai_service import AzureAIService

# Page configuration
st.set_page_config(
    page_title="Supplier Performance Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-high { border-left-color: #ff4b4b; }
    .risk-medium { border-left-color: #ffa500; }
    .risk-low { border-left-color: #00cc00; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏭 Supplier Performance Predictor</h1>', unsafe_allow_html=True)

# Initialize Azure AI Service
@st.cache_resource
def get_ai_service():
    return AzureAIService()

ai_service = get_ai_service()

# Sidebar
st.sidebar.header("📁 Data Upload")
st.sidebar.markdown("Upload your CSV files to analyze supplier performance")

# Sample data info
with st.sidebar.expander("📋 Sample Data Format"):
    st.markdown("""
    **Suppliers CSV:**
    - supplier_id, reliability_score, past_delivery_rate, on_time_percentage
    
    **Orders CSV:**
    - order_id, supplier_id, expected_delivery_date, historical_risk_flags
    
    **Vendors CSV:**
    - supplier_id, category, region, average_lead_time
    """)

# File uploaders
suppliers_file = st.sidebar.file_uploader("📊 Suppliers CSV", type=["csv"], key="suppliers")
orders_file = st.sidebar.file_uploader("📦 Orders CSV", type=["csv"], key="orders")
vendors_file = st.sidebar.file_uploader("🏢 Vendors CSV", type=["csv"], key="vendors")

# Load sample data button
if st.sidebar.button("📋 Load Sample Data"):
    st.session_state.use_sample_data = True
    st.session_state.suppliers_path = "data/suppliers.csv"
    st.session_state.orders_path = "data/orders.csv"
    st.session_state.vendors_path = "data/vendors.csv"
    st.rerun()

# Check if we're using sample data
use_sample_data = getattr(st.session_state, 'use_sample_data', False)

# Main content area
if suppliers_file or orders_file or vendors_file or use_sample_data:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Reliability Prediction", "⚠️ Risk Analysis", "💡 Recommendations"])
    
    with tab1:
        st.header("📊 Dashboard Overview")
        
        # Load data
        try:
            if use_sample_data:
                suppliers_df = pd.read_csv(st.session_state.suppliers_path)
                orders_df = pd.read_csv(st.session_state.orders_path) 
                vendors_df = pd.read_csv(st.session_state.vendors_path)
            else:
                suppliers_df = pd.read_csv(suppliers_file) if suppliers_file else None
                orders_df = pd.read_csv(orders_file) if orders_file else None
                vendors_df = pd.read_csv(vendors_file) if vendors_file else None
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            if suppliers_df is not None:
                with col1:
                    st.metric("Total Suppliers", len(suppliers_df))
                with col2:
                    avg_reliability = suppliers_df['reliability_score'].mean()
                    st.metric("Avg Reliability", f"{avg_reliability:.2f}")
            
            if orders_df is not None:
                with col3:
                    st.metric("Total Orders", len(orders_df))
                with col4:
                    high_risk_orders = len(orders_df[orders_df['historical_risk_flags'] > 1])
                    st.metric("High Risk Orders", high_risk_orders)
            
            # Visualizations
            if suppliers_df is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Supplier Reliability Distribution")
                    fig = px.histogram(
                        suppliers_df, 
                        x='reliability_score',
                        title="Supplier Reliability Scores",
                        color_discrete_sequence=['#1f77b4']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("On-Time Performance")
                    fig = px.scatter(
                        suppliers_df,
                        x='past_delivery_rate',
                        y='on_time_percentage',
                        size='reliability_score',
                        hover_data=['supplier_id'],
                        title="Delivery Rate vs On-Time Performance"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    
    with tab2:
        st.header("🔍 AI-Powered Reliability Prediction")
        
        if suppliers_file or use_sample_data:
            if st.button("🚀 Predict Supplier Reliability", type="primary"):
                with st.spinner("🤖 Analyzing suppliers with Azure OpenAI..."):
                    try:
                        if use_sample_data:
                            df = pd.read_csv(st.session_state.suppliers_path)
                        else:
                            df = pd.read_csv(suppliers_file)
                        
                        st.info("🔗 **Using Azure OpenAI for Real-Time AI Analysis**")
                        
                        # Use Azure OpenAI for each supplier
                        predictions = []
                        progress_bar = st.progress(0)
                        
                        for idx, (_, row) in enumerate(df.iterrows()):
                            # Real Azure OpenAI analysis
                            ai_result = ai_service.predict_supplier_reliability(row.to_dict())
                            
                            predictions.append({
                                "supplier_id": row['supplier_id'],
                                "reliability": ai_result.get("reliability", "Unknown"),
                                "confidence": ai_result.get("confidence", 0.5),
                                "reasoning": ai_result.get("reasoning", "AI analysis"),
                                "improvements": ai_result.get("improvements", []),
                                "future_trend": ai_result.get("future_trend", "stable"),
                                "risk_factors": ai_result.get("risk_factors", []),
                                "reliability_score": row['reliability_score'],
                                "past_delivery_rate": row['past_delivery_rate'],
                                "on_time_percentage": row['on_time_percentage']
                            })
                            
                            # Update progress
                            progress_bar.progress((idx + 1) / len(df))
                        
                        pred_df = pd.DataFrame(predictions)
                        
                        st.success(f"✅ **Azure OpenAI Analysis Complete!** Analyzed {len(predictions)} suppliers")
                        
                        # Display results with AI insights
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.subheader("🤖 AI Prediction Results")
                            
                            # Enhanced display with AI insights
                            for _, pred in pred_df.iterrows():
                                with st.expander(f"📊 {pred['supplier_id']} - {pred['reliability']} Reliability (Confidence: {pred['confidence']:.1%})"):
                                    col_a, col_b = st.columns(2)
                                    
                                    with col_a:
                                        st.write(f"**🎯 AI Assessment:** {pred['reliability']}")
                                        st.write(f"**🔍 Confidence:** {pred['confidence']:.1%}")
                                        st.write(f"**📈 Future Trend:** {pred['future_trend']}")
                                        st.write(f"**⚡ On-Time:** {pred['on_time_percentage']}%")
                                    
                                    with col_b:
                                        st.write("**💡 AI Reasoning:**")
                                        st.write(pred['reasoning'])
                                        
                                        if pred['improvements']:
                                            st.write("**🔧 AI Suggestions:**")
                                            for improvement in pred['improvements']:
                                                st.write(f"• {improvement}")
                                        
                                        if pred['risk_factors']:
                                            st.write("**⚠️ Risk Factors:**")
                                            for risk in pred['risk_factors']:
                                                st.write(f"• {risk}")
                        
                        with col2:
                            st.subheader("📊 AI Analysis Summary")
                            
                            # Reliability distribution
                            reliability_counts = pred_df['reliability'].value_counts()
                            fig = px.pie(
                                values=reliability_counts.values,
                                names=reliability_counts.index,
                                title="AI Reliability Classification",
                                color_discrete_map={
                                    'High': '#28a745',
                                    'Medium': '#ffc107',
                                    'Low': '#dc3545'
                                }
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Confidence distribution
                            st.subheader("🎯 AI Confidence Scores")
                            fig2 = px.histogram(
                                pred_df, 
                                x='confidence',
                                title="AI Prediction Confidence",
                                nbins=10
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                            
                            # Future trends
                            st.subheader("📈 Future Trends")
                            trend_counts = pred_df['future_trend'].value_counts()
                            st.bar_chart(trend_counts)
                            
                    except Exception as e:
                        st.error(f"❌ **Azure OpenAI Error:** {str(e)}")
                        st.info("🔧 Please check your Azure OpenAI credentials in the .env file")
        else:
            st.info("📁 Please upload a suppliers CSV file or load sample data to begin AI analysis.")
    
    with tab3:
        st.header("⚠️ AI-Powered Risk Analysis")
        
        if orders_file or use_sample_data:
            if st.button("🔍 Analyze Order Risks with AI", type="primary"):
                with st.spinner("🤖 Analyzing risks with Azure OpenAI..."):
                    try:
                        if use_sample_data:
                            df = pd.read_csv(st.session_state.orders_path)
                        else:
                            df = pd.read_csv(orders_file)
                        
                        st.info("🔗 **Using Azure OpenAI for Advanced Risk Assessment**")
                        
                        # Use Azure OpenAI for risk analysis
                        high_risk_orders = []
                        progress_bar = st.progress(0)
                        
                        for idx, (_, row) in enumerate(df.iterrows()):
                            # Real Azure OpenAI risk analysis
                            risk_result = ai_service.analyze_order_risk(row.to_dict())
                            
                            # Only include high-risk orders
                            if risk_result.get("risk_level", "Low") in ["High", "Medium"]:
                                high_risk_orders.append({
                                    "order_id": row['order_id'],
                                    "supplier_id": row['supplier_id'],
                                    "expected_delivery_date": row['expected_delivery_date'],
                                    "historical_risk_flags": row['historical_risk_flags'],
                                    "ai_risk_level": risk_result.get("risk_level", "Unknown"),
                                    "ai_risk_score": risk_result.get("risk_score", 0.5),
                                    "primary_risks": risk_result.get("primary_risks", []),
                                    "mitigation_strategies": risk_result.get("mitigation_strategies", []),
                                    "monitoring_points": risk_result.get("monitoring_points", []),
                                    "alternative_actions": risk_result.get("alternative_actions", [])
                                })
                            
                            # Update progress
                            progress_bar.progress((idx + 1) / len(df))
                        
                        if high_risk_orders:
                            st.warning(f"🚨 **Azure OpenAI Identified {len(high_risk_orders)} High-Risk Orders**")
                            
                            # Enhanced risk display with AI insights
                            for order in high_risk_orders:
                                risk_color = "🔴" if order['ai_risk_level'] == "High" else "🟡"
                                
                                with st.expander(f"{risk_color} Order {order['order_id']} - AI Risk: {order['ai_risk_level']} ({order['ai_risk_score']:.1%})"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.write(f"**📦 Order:** {order['order_id']}")
                                        st.write(f"**🏭 Supplier:** {order['supplier_id']}")
                                        st.write(f"**📅 Delivery Date:** {order['expected_delivery_date']}")
                                        st.write(f"**🚩 Historical Flags:** {order['historical_risk_flags']}")
                                        st.write(f"**🤖 AI Risk Level:** {order['ai_risk_level']}")
                                        st.write(f"**📊 AI Risk Score:** {order['ai_risk_score']:.1%}")
                                    
                                    with col2:
                                        if order['primary_risks']:
                                            st.write("**⚠️ AI-Identified Primary Risks:**")
                                            for risk in order['primary_risks']:
                                                st.write(f"• {risk}")
                                        
                                        if order['mitigation_strategies']:
                                            st.write("**🛡️ AI Mitigation Strategies:**")
                                            for strategy in order['mitigation_strategies']:
                                                st.write(f"• {strategy}")
                                    
                                    # Additional AI insights in expandable sections
                                    if order['monitoring_points']:
                                        with st.expander("👁️ AI Monitoring Recommendations"):
                                            for point in order['monitoring_points']:
                                                st.write(f"• {point}")
                                    
                                    if order['alternative_actions']:
                                        with st.expander("🔄 AI Alternative Actions"):
                                            for action in order['alternative_actions']:
                                                st.write(f"• {action}")
                            
                            # Risk summary chart
                            st.subheader("📊 AI Risk Analysis Summary")
                            risk_df = pd.DataFrame(high_risk_orders)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                fig = px.histogram(
                                    risk_df, 
                                    x='ai_risk_score',
                                    title="AI Risk Score Distribution",
                                    nbins=10,
                                    color_discrete_sequence=['#ff4b4b']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                risk_level_counts = risk_df['ai_risk_level'].value_counts()
                                fig2 = px.pie(
                                    values=risk_level_counts.values,
                                    names=risk_level_counts.index,
                                    title="AI Risk Level Distribution",
                                    color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107'}
                                )
                                st.plotly_chart(fig2, use_container_width=True)
                        
                        else:
                            st.success("✅ **Azure OpenAI Analysis:** No high-risk orders identified!")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ **Azure OpenAI Error:** {str(e)}")
                        st.info("🔧 Please check your Azure OpenAI credentials and try again")
        else:
            st.info("📁 Please upload an orders CSV file or load sample data to begin AI risk analysis.")
    
    with tab4:
        st.header("💡 AI-Powered Vendor Recommendations")
        
        if vendors_file or use_sample_data:
            if st.button("🔍 Get AI Vendor Recommendations", type="primary"):
                with st.spinner("🤖 Analyzing vendors with Azure OpenAI..."):
                    try:
                        if use_sample_data:
                            df = pd.read_csv(st.session_state.vendors_path)
                        else:
                            df = pd.read_csv(vendors_file)
                        
                        st.info("🔗 **Using Azure OpenAI for Strategic Vendor Analysis**")
                        
                        # Use Azure OpenAI for vendor recommendations
                        all_recommendations = []
                        progress_bar = st.progress(0)
                        
                        # Analyze each vendor for alternatives
                        for idx, (_, current_vendor) in enumerate(df.iterrows()):
                            # Get AI recommendations for this vendor
                            ai_result = ai_service.recommend_alternatives(current_vendor, df)
                            
                            if ai_result.get("recommendations"):
                                all_recommendations.append({
                                    "original_supplier": current_vendor['supplier_id'],
                                    "category": current_vendor['category'],
                                    "region": current_vendor['region'],
                                    "current_lead_time": current_vendor['average_lead_time'],
                                    "ai_recommendations": ai_result.get("recommendations", []),
                                    "sourcing_strategy": ai_result.get("sourcing_strategy", ""),
                                    "risk_mitigation": ai_result.get("risk_mitigation", "")
                                })
                            
                            # Update progress
                            progress_bar.progress((idx + 1) / len(df))
                        
                        if all_recommendations:
                            st.success(f"🎯 **Azure OpenAI Found Strategic Recommendations for {len(all_recommendations)} Vendors**")
                            
                            # Display AI-powered recommendations
                            for rec in all_recommendations:
                                with st.expander(f"🏭 AI Strategy for {rec['original_supplier']} ({rec['category']})"):
                                    col1, col2 = st.columns([1, 2])
                                    
                                    with col1:
                                        st.write(f"**📍 Current Vendor:** {rec['original_supplier']}")
                                        st.write(f"**🏷️ Category:** {rec['category']}")
                                        st.write(f"**🌍 Region:** {rec['region']}")
                                        st.write(f"**⏱️ Current Lead Time:** {rec['current_lead_time']} days")
                                        st.write(f"**🎯 AI Strategy:** {rec['sourcing_strategy'].title()}")
                                    
                                    with col2:
                                        st.write("**🤖 AI-Recommended Alternatives:**")
                                        
                                        for alt in rec['ai_recommendations']:
                                            with st.container():
                                                st.write(f"**🌟 {alt['supplier_id']}** (AI Score: {alt.get('score', 0):.2f})")
                                                
                                                if alt.get('advantages'):
                                                    st.write("**✅ AI-Identified Advantages:**")
                                                    for adv in alt['advantages']:
                                                        st.write(f"   • {adv}")
                                                
                                                if alt.get('considerations'):
                                                    st.write("**🤔 AI Considerations:**")
                                                    for cons in alt['considerations']:
                                                        st.write(f"   • {cons}")
                                                
                                                if alt.get('implementation_steps'):
                                                    st.write("**📋 AI Implementation Steps:**")
                                                    for step in alt['implementation_steps']:
                                                        st.write(f"   • {step}")
                                                
                                                st.write("---")
                                    
                                    # AI Risk Mitigation Strategy
                                    if rec['risk_mitigation']:
                                        st.write("**🛡️ AI Risk Mitigation Strategy:**")
                                        st.info(rec['risk_mitigation'])
                            
                            # AI Recommendations Summary
                            st.subheader("📊 AI Sourcing Strategy Summary")
                            
                            # Count strategies
                            strategies = [r['sourcing_strategy'] for r in all_recommendations]
                            strategy_counts = pd.Series(strategies).value_counts()
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                fig = px.pie(
                                    values=strategy_counts.values,
                                    names=strategy_counts.index,
                                    title="AI Sourcing Strategies",
                                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Count total alternatives suggested
                                total_alternatives = sum(len(r['ai_recommendations']) for r in all_recommendations)
                                avg_score = sum(
                                    alt.get('score', 0) 
                                    for r in all_recommendations 
                                    for alt in r['ai_recommendations']
                                ) / max(total_alternatives, 1)
                                
                                st.metric("Total AI Alternatives", total_alternatives)
                                st.metric("Average AI Score", f"{avg_score:.2f}")
                                st.metric("Vendors Analyzed", len(all_recommendations))
                        
                        else:
                            st.info("🤖 **Azure OpenAI Analysis:** Current vendor portfolio is optimally configured!")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ **Azure OpenAI Error:** {str(e)}")
                        st.info("🔧 Please check your Azure OpenAI credentials and try again")
        else:
            st.info("📁 Please upload a vendors CSV file or load sample data to get AI recommendations.")

else:
    # Welcome screen
    st.markdown("""
    ## 🎯 Welcome to Supplier Performance Predictor
    
    This AI-powered dashboard helps you:
    
    ### 🔍 **Predict Supplier Reliability**
    - Upload supplier data and get AI-powered reliability predictions
    - View confidence scores and reasoning for each prediction
    - Visualize supplier performance metrics
    
    ### ⚠️ **Identify High-Risk Orders**
    - Automatically flag orders with potential delivery issues
    - Get detailed risk analysis with contributing factors
    - Proactive risk management for your supply chain
    
    ### 💡 **Get Vendor Recommendations**
    - Find alternative suppliers based on performance metrics
    - Compare lead times, categories, and regions
    - Reduce supply chain dependencies and risks
    
    ### 🚀 **Get Started**
    1. Upload your CSV files using the sidebar
    2. Or click "Load Sample Data" to try with demo data
    3. Navigate through the tabs to explore different features
    
    ---
    *Powered by Azure OpenAI, FAISS, and LangSmith*
    """)

# Footer
st.markdown("---")
st.markdown("*🔬 Built for Hackathon - Supplier Performance Predictor v1.0*")
