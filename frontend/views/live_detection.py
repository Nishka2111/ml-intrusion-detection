import streamlit as st
import time

def render():
    # Modern Dark Cyber Theme CSS Injection + Bootstrap Icons & Pulse Animation
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Page Header */
        .monitor-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .monitor-subtitle {
            font-size: 0.92rem;
            color: #38BDF8;
            margin-bottom: 24px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Status Badge Styling */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .status-active {
            background-color: rgba(16, 185, 129, 0.15);
            border: 1px solid #10B981;
            color: #10B981;
        }
        .status-stopped {
            background-color: rgba(239, 68, 68, 0.15);
            border: 1px solid #EF4444;
            color: #EF4444;
        }

        /* Pulsing Dot Effect for Active State */
        @keyframes pulse-glow {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 10px #10B981; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .pulse-dot {
            width: 10px;
            height: 10px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            animation: pulse-glow 1.5s infinite;
        }
        .stop-dot {
            width: 10px;
            height: 10px;
            background-color: #EF4444;
            border-radius: 50%;
            display: inline-block;
        }

        /* Custom Streamlit Metrics Overrides */
        div[data-testid="stMetric"] {
            background-color: #1A2332;
            border: 1px solid #263346;
            padding: 16px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #38BDF8;
            transform: translateY(-2px);
        }
        div[data-testid="stMetric"] label {
            color: #94A3B8 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-weight: 800 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header with Icons (Emoji Replaced)
    st.markdown('<div class="monitor-title"><i class="bi bi-activity" style="color: #38BDF8;"></i> Live Traffic Detection Monitor</div>', unsafe_allow_html=True)
    st.markdown('<div class="monitor-subtitle"><i class="bi bi-shield-check" style="color: #38BDF8;"></i> Real-time Stream Inspector & Threat Mitigation Feed</div>', unsafe_allow_html=True)

    if "monitoring" not in st.session_state:
        st.session_state["monitoring"] = False

    # Control Panel Layout without unwanted background box container
    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        if st.button("Start Monitoring", use_container_width=True, type="primary"):
            st.session_state["monitoring"] = True
            st.rerun()

    with c2:
        if st.button("Stop Monitoring", use_container_width=True):
            st.session_state["monitoring"] = False
            st.rerun()

    with c3:
        if st.session_state["monitoring"]:
            st.markdown('<div style="text-align: right; padding-top: 4px;"><span class="status-badge status-active"><span class="pulse-dot"></span> Active (Listening...)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right; padding-top: 4px;"><span class="status-badge status-stopped"><span class="stop-dot"></span> Stopped</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Metrics Display Grid
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Packets / Sec", value="1,420" if st.session_state["monitoring"] else "0")
    with m2:
        st.metric(label="Active Connections", value="312" if st.session_state["monitoring"] else "0")
    with m3:
        st.metric(label="Threats Intercepted", value="14" if st.session_state["monitoring"] else "0")