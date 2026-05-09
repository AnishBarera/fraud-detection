import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Import our custom chart functions
from charts import create_fraud_pie_chart, create_trend_line_chart, create_activity_bar_chart

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR DARK FINTECH THEME ---
# Streamlit has a default dark theme, but we can enhance the metrics and layout
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Enhance metric cards */
    div[data-testid="metric-container"] {
        background-color: #1a1c23;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Make headers pop */
    h1, h2, h3 {
        color: #FAFAFA !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Style the fake alerts table */
    .dataframe {
        background-color: #1a1c23 !important;
        color: #FAFAFA !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA GENERATION ---
@st.cache_data
def load_dummy_data():
    """Generates dummy data for the dashboard."""
    # Base numbers
    total_tx = 15420
    fraud_tx = 342
    safe_tx = total_tx - fraud_tx
    
    # Trend data (last 7 days)
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    trend_data = pd.DataFrame({
        'Date': dates,
        'Fraud Incidents': [45, 38, 52, 41, 60, 48, 58]
    })
    
    # Activity data (24 hours)
    hours = [f"{i:02d}:00" for i in range(24)]
    # Create a nice curve for transaction volume
    volumes = [int(100 + 500 * np.sin(np.pi * i / 24) + np.random.normal(0, 50)) for i in range(24)]
    activity_data = pd.DataFrame({
        'Hour': hours,
        'Transactions': volumes
    })
    
    return total_tx, fraud_tx, safe_tx, trend_data, activity_data

def generate_fake_alert():
    """Generates a single fake fraud alert."""
    locations = ["New York, US", "London, UK", "Tokyo, JP", "Sydney, AU", "Berlin, DE"]
    amounts = [round(np.random.uniform(500, 5000), 2) for _ in range(5)]
    merchants = ["TechStore", "CryptoEx", "LuxuryGoods", "TravelAgency", "AutoDealer"]
    
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Card": f"**** {np.random.randint(1000, 9999)}",
        "Amount": f"${np.random.choice(amounts)}",
        "Merchant": np.random.choice(merchants),
        "Location": np.random.choice(locations),
        "Risk Score": f"{np.random.randint(85, 99)}/100"
    }

# Load data
total_tx, fraud_tx, safe_tx, trend_data, activity_data = load_dummy_data()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked--v1.png", width=60)
    st.title("Fraud Guard AI")
    st.markdown("---")
    
    # Navigation mock
    st.button("📊 Dashboard", use_container_width=True, type="primary")
    st.button("🔍 Investigate", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### System Status")
    st.success("🟢 Real-time Engine Active")
    st.info("ℹ️ Model Version: v2.4.1")

# --- MAIN DASHBOARD AREA ---
st.title("Real-Time Analytics Dashboard")
st.markdown("Monitor transaction streams and detect anomalies in real-time.")

# 1. Top Metrics Row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Transactions (24h)", value=f"{total_tx:,}", delta="12% from yesterday")
with col2:
    st.metric(label="Fraud Detected", value=f"{fraud_tx:,}", delta="5% from yesterday", delta_color="inverse")
with col3:
    st.metric(label="Safe Transactions", value=f"{safe_tx:,}", delta="12.5% from yesterday")

st.markdown("---")

# 2. Charts Row
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Transaction Distribution")
    # Using our reusable function from charts.py
    pie_chart = create_fraud_pie_chart(safe_tx, fraud_tx)
    st.plotly_chart(pie_chart, use_container_width=True)

with col_right:
    st.subheader("Fraud Trend (Last 7 Days)")
    # Using our reusable function from charts.py
    line_chart = create_trend_line_chart(trend_data, 'Date', 'Fraud Incidents')
    st.plotly_chart(line_chart, use_container_width=True)

# 3. Bottom Row: Activity and Live Alerts
col_bottom_left, col_bottom_right = st.columns([2, 1])

with col_bottom_left:
    st.subheader("Hourly Transaction Volume")
    # Using our reusable function from charts.py
    bar_chart = create_activity_bar_chart(activity_data, 'Hour', 'Transactions')
    st.plotly_chart(bar_chart, use_container_width=True)

with col_bottom_right:
    st.subheader("🚨 Live Fraud Alerts")
    st.markdown("Recent flagged transactions requiring review:")
    
    # Create a placeholder to simulate streaming data
    alerts_placeholder = st.empty()
    
    # Generate an initial list of alerts
    if 'alerts' not in st.session_state:
        st.session_state.alerts = [generate_fake_alert() for _ in range(5)]
    
    # Display the alerts in a dataframe
    alerts_df = pd.DataFrame(st.session_state.alerts)
    
    # We use Streamlit's dataframe to render the table nicely
    alerts_placeholder.dataframe(
        alerts_df,
        hide_index=True,
        use_container_width=True
    )
    
    # Add a refresh button for manual triggering of new alerts
    if st.button("Refresh Alerts"):
        # Add a new alert to the top and keep only the latest 5
        st.session_state.alerts.insert(0, generate_fake_alert())
        st.session_state.alerts = st.session_state.alerts[:5]
        alerts_df = pd.DataFrame(st.session_state.alerts)
        alerts_placeholder.dataframe(alerts_df, hide_index=True, use_container_width=True)
