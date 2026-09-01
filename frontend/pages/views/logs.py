import streamlit as st
from services import mock_data

def render():
    # Advanced Cyber Theme & Professional Table CSS Injection with Shine Effect
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Page Header Layout with Proper Spacing */
        .history-title-container {
            margin-bottom: 24px;
            padding-left: 2px;
        }
        .history-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }

        /* Shine Sweep Effect for DataFrame Container */
        @keyframes shine-sweep {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(100%); }
            100% { transform: translateX(100%); }
        }

        /* Streamlit DataFrame Custom Cyber Styling & Effects */
        div[data-testid="stDataFrame"] {
            background: linear-gradient(145deg, #1A2332 0%, #121927 100%) !important;
            border: 1px solid #263346 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
        }

        div[data-testid="stDataFrame"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 40%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.12), transparent);
            animation: shine-sweep 3s infinite ease-in-out;
            pointer-events: none;
        }

        div[data-testid="stDataFrame"]:hover {
            border-color: #38BDF8 !important;
            box-shadow: 0 12px 40px rgba(2, 132, 199, 0.25) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header Section (Subtitle Removed)
    st.markdown("""
        <div class="history-title-container">
            <div class="history-title"><i class="bi bi-clock-history" style="color: #38BDF8;"></i> Detection History & System Logs</div>
        </div>
    """, unsafe_allow_html=True)

    # Fetch History Data
    df = mock_data.generate_mock_recent_predictions()

    # Safe check to drop time/timestamp columns if they exist in the dataframe
    time_columns = ['time', 'timestamp', 'date', 'Timestamp', 'Time', 'DATE']
    for col in time_columns:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Render Cleaned Dataframe with Enhanced Styling
    st.dataframe(df, use_container_width=True)