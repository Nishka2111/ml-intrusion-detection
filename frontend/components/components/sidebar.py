import streamlit as st
import os
from utils.helpers import load_logo

def render_sidebar():
    # Session State Default Setup
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Dashboard"

    # Cyber Theme & Shining Sweep Animation CSS Injection
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Sidebar Outer Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0B132B 0%, #070A17 100%) !important;
            border-right: 1px solid #1C2541 !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding: 1rem 0.6rem !important;
        }

        /* Streamlit Native Buttons Custom Dark Styling */
        div[data-testid="stSidebar"] div.stButton {
            margin-bottom: 6px !important;
        }

        div[data-testid="stSidebar"] div.stButton > button {
            background-color: rgba(17, 24, 39, 0.6) !important;
            color: #94A3B8 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            padding: 8px 12px 8px 40px !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            height: 42px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            text-align: left !important;
            position: relative !important;
            width: 100% !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }

        /* Shine / Sweep Animation Effect */
        @keyframes shine-sweep {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(100%); }
            100% { transform: translateX(100%); }
        }

        div[data-testid="stSidebar"] div.stButton > button::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 50%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
            transform: translateX(-100%);
            pointer-events: none;
        }

        div[data-testid="stSidebar"] div.stButton > button:hover::after {
            animation: shine-sweep 1.2s infinite ease-in-out;
        }

        /* Inactive Hover Effect */
        div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
            background-color: rgba(30, 41, 59, 0.9) !important;
            color: #E2E8F0 !important;
            border-color: rgba(56, 189, 248, 0.4) !important;
            transform: translateX(4px) !important;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15) !important;
        }

        /* Active Button Highlight (Primary) with Neon Glow & Continuous Shine */
        div[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.35) 0%, rgba(29, 78, 216, 0.2) 100%) !important;
            color: #38BDF8 !important;
            border: 1px solid #0284C7 !important;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.3), inset 0 0 8px rgba(56, 189, 248, 0.15) !important;
            font-weight: 600 !important;
            transform: translateX(4px) !important;
        }

        div[data-testid="stSidebar"] div.stButton > button[kind="primary"]::after {
            animation: shine-sweep 2.5s infinite ease-in-out;
        }

        /* Bootstrap Icon Mapping for Sidebar Buttons */
        div[data-testid="stSidebar"] div.stButton > button::before {
            font-family: "bootstrap-icons" !important;
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.1rem;
            color: #38BDF8;
            opacity: 0.7;
            transition: all 0.2s ease !important;
            z-index: 2;
        }

        div[data-testid="stSidebar"] div.stButton > button:hover::before {
            opacity: 1;
            filter: drop-shadow(0 0 4px #60A5FA);
        }

        div[data-testid="stSidebar"] div.stButton > button[kind="primary"]::before {
            opacity: 1;
            color: #38BDF8;
            filter: drop-shadow(0 0 6px #38BDF8);
        }

        /* Specific Icon Class Bindings via Keys */
        button[key="nav_dashboard"]::before { content: "\\F375"; }
        button[key="nav_traffic_detection"]::before { content: "\\F52A"; }
        button[key="nav_live_detection"]::before { content: "\\F32A"; }
        button[key="nav_alerts"]::before { content: "\\F512"; }
        button[key="nav_history"]::before { content: "\\F293"; }
        button[key="nav_analytics"]::before { content: "\\F3EE"; }
        button[key="nav_about"]::before { content: "\\F422"; }

        /* Pulse Dot Animation */
        @keyframes pulse-cyan {
            0% { transform: scale(0.95); opacity: 0.8; }
            70% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Header Logo Banner
        logo_path = load_logo() if 'load_logo' in globals() else None
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown(
                '''
                <div style="text-align: center; margin-bottom: 6px;">
                    <h3 style="margin: 0; font-weight: 800; color: #FFFFFF; font-size: 1.15rem; letter-spacing:0.5px;">ML Intrusion Detector</h3>
                </div>
                ''',
                unsafe_allow_html=True
            )

        # Unique Subtitle Tagline
        st.markdown(
            '''
            <div style="text-align: center; margin-bottom: 16px;">
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(56, 189, 248, 0.3); padding: 4px 10px; border-radius: 20px;">
                    <span style="height: 6px; width: 6px; background-color: #38BDF8; border-radius: 50%; display: inline-block; animation: pulse-cyan 2s infinite;"></span>
                    <span style="font-size: 0.68rem; color: #7DD3FC; font-weight: 600; letter-spacing: 0.3px;">Smarter Security • Safer Networks</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

        pages = {
            "Dashboard": "nav_dashboard",
            "Traffic Detection": "nav_traffic_detection",
            "Live Detection": "nav_live_detection",
            "Alerts": "nav_alerts",
            "History": "nav_history",
            "Analytics": "nav_analytics",
            "About": "nav_about"
        }

        # Fast Native Streamlit Buttons with Custom CSS & Shine Effect
        for page_name, btn_key in pages.items():
            is_active = (st.session_state["selected_page"] == page_name)
            btn_type = "primary" if is_active else "secondary"
            
            if st.button(page_name, key=btn_key, use_container_width=True, type=btn_type):
                if st.session_state["selected_page"] != page_name:
                    st.session_state["selected_page"] = page_name
                    st.rerun()

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

        # Compact System Status Box with Glowing Border Effect
        st.markdown(
            '''
            <div style="background: linear-gradient(145deg, #111827 0%, #0D1322 100%); padding: 10px 12px; border-radius: 10px; border: 1px solid #1F2937; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <p style="margin:0; font-size:0.7rem; color:#94A3B8; font-weight: 500;">System Status</p>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
                    <span style="height: 6px; width: 6px; background-color: #10B981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10B981;"></span>
                    <span style="font-size: 0.78rem; font-weight: 600; color: #10B981;">Online <span style="color: #64748B; font-weight: 400; font-size: 0.7rem;">(v2.4.0)</span></span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )