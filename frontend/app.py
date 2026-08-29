import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="ML Intrusion Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pixel-Perfect Level Alignment & Top Space Fix
st.markdown(
    """
    <style>
        /* Deploy Button, 3-dots Menu aur Native Header hide karein */
        .stAppDeployButton, 
        #MainMenu, 
        [data-testid="stHeaderActionElements"] {
            display: none !important;
        }
        
        /* Transparent & Zero Height Header */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            z-index: 99999 !important;
            height: 0px !important;
        }

        /* Default Sidebar Nav Hide */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Sidebar Top Padding Align */
        [data-testid="stSidebarUserContent"] {
            padding-top: 1.2rem !important;
            padding-bottom: 1rem !important;
        }

        /* Main Page Top Padding Alignment with Sidebar */
        div.block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

from utils.styles import inject_global_css
from components.sidebar import render_sidebar
from views import dashboard, traffic_analyzer, live_detection, alerts, logs, analytics, about

inject_global_css()
render_sidebar()

current_page = st.session_state.get("selected_page", "Dashboard")

if current_page == "Dashboard":
    dashboard.render()
elif current_page == "Traffic Detection":
    traffic_analyzer.render()
elif current_page == "Live Detection":
    live_detection.render()
elif current_page == "Alerts":
    alerts.render()
elif current_page == "History":
    logs.render()
elif current_page == "Analytics":
    analytics.render()
elif current_page == "About":
    about.render()