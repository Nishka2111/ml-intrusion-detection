import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
        /* Modern Dark Enterprise Theme Base */
        :root {
            --bg-dark: #0B1120;
            --card-bg: #111827;
            --card-border: #1F2937;
            --accent-blue: #2563EB;
            --accent-cyan: #06B6D4;
            --text-primary: #F9FAFB;
            --text-secondary: #9CA3AF;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
        }

        /* App Background Overrides */
        .stApp {
            background-color: var(--bg-dark) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid var(--card-border) !important;
        }

        /* Custom Card Metric Containers */
        .kpi-card {
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .kpi-card:hover {
            border-color: #374151;
            transform: translateY(-2px);
        }
        .kpi-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }
        .kpi-value {
            font-size: 1.875rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 8px 0;
        }
        .kpi-footer {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
        }

        /* Status Pills */
        .status-pill {
            padding: 2px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            text-align: center;
        }
        .pill-high { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid #EF4444; }
        .pill-medium { background: rgba(245, 158, 11, 0.2); color: #FDE047; border: 1px solid #F59E0B; }
        .pill-low { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid #10B981; }

        /* Custom Tabs & Selectors */
        .stButton button {
            background-color: var(--accent-blue) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            background-color: #1D4ED8 !important;
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.4) !important;
        }

        /* Responsive Container Fixes */
        @media (max-width: 768px) {
            .kpi-value { font-size: 1.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)