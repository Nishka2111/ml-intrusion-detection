import streamlit as st
from services import api_client

def render():
    # Advanced Cyber Theme & Professional Alert Icons CSS Injection
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Page Header Layout with Proper Spacing */
        .alerts-title-container {
            margin-bottom: 24px;
            padding-left: 2px;
        }
        .alerts-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 20px rgba(239, 68, 68, 0.25);
        }

        /* Unique Pulsing Cyber Border for Threat/Alert Management */
        @keyframes alert-pulse {
            0% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.4); }
            50% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.45); border-color: rgba(239, 68, 68, 0.8); }
            100% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.4); }
        }

        /* Streamlit DataFrame Custom Threat Styling & Animation */
        div[data-testid="stDataFrame"] {
            background: linear-gradient(145deg, #1A1A24 0%, #12121A 100%) !important;
            border: 1px solid #EF4444 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            animation: alert-pulse 3s infinite ease-in-out !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stDataFrame"]:hover {
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.5) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header Section with Professional SOC Icons
    st.markdown("""
        <div class="alerts-title-container">
            <div class="alerts-title"><i class="bi bi-shield-shaded" style="color: #EF4444;"></i> Security Alerts & Threat Management</div>
        </div>
    """, unsafe_allow_html=True)

    # Fetch Alerts and Clean up any accidental time/timestamp columns if present
    alerts_df = api_client.get_alerts()
    
    # Safe check to drop time columns if they exist in the dataframe
    time_columns = ['time', 'timestamp', 'date', 'Timestamp', 'Time', 'DATE']
    for col in time_columns:
        if col in alerts_df.columns:
            alerts_df = alerts_df.drop(columns=[col])

    # Render Cleaned Alerts Dataframe
    st.dataframe(alerts_df, use_container_width=True)