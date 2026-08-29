import streamlit as st
from components.status import render_status_widget

def render():
    # Advanced Cyber Theme & Interactive Card Effects CSS Injection
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Page Header with Glowing Neon Text Accent */
        .analytics-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }
        .analytics-subtitle {
            font-size: 0.92rem;
            color: #38BDF8;
            margin-bottom: 24px;
            font-weight: 500;
        }

        /* Custom Hover & Glow Effects for Streamlit Metric/Status Boxes */
        div[data-testid="stMetric"], div.stMetric {
            background: linear-gradient(145deg, #1A2332 0%, #121927 100%) !important;
            border: 1px solid #263346 !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
        }

        /* Hover Glow and Elevation Effect */
        div[data-testid="stMetric"]:hover, div.stMetric:hover {
            border-color: #38BDF8 !important;
            box-shadow: 0 12px 32px rgba(2, 132, 199, 0.3), inset 0 0 12px rgba(56, 189, 248, 0.15) !important;
            transform: translateY(-4px) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header Section
    st.markdown('<div class="analytics-title"><i class="bi bi-graph-up-arrow" style="color: #38BDF8;"></i> Model Performance & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="analytics-subtitle"><i class="bi bi-cpu"></i> Machine Learning Metrics, Precision Logs & Validation Suite</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    # Render Status Widget directly without any extra wrapper to avoid blank gaps
    render_status_widget()