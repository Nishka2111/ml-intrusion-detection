import streamlit as st
import pandas as pd
from utils.helpers import DATASET_FEATURES, format_title
from services import api_client

def render():
    # Modern Dark Cyber Theme CSS Injection
    st.markdown("""
        <style>
        /* Headings & Subtitles */
        .page-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 4px;
        }
        .page-subtitle {
            font-size: 0.92rem;
            color: #38BDF8;
            margin-bottom: 20px;
            font-weight: 500;
        }

        /* Streamlit Tabs Custom Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 1px solid #1E293B;
            padding-bottom: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            background-color: #1A2332 !important;
            border: 1px solid #263346 !important;
            border-radius: 8px !important;
            color: #94A3B8 !important;
            font-weight: 600 !important;
            padding: 0px 20px !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(38, 189, 248, 0.15) !important;
            border: 1px solid #0284C7 !important;
            color: #38BDF8 !important;
        }

        /* Custom Form & Expanders */
        div[data-testid="stForm"] {
            background-color: #121927;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 20px;
        }

        .stExpander {
            background-color: #1A2332 !important;
            border: 1px solid #263346 !important;
            border-radius: 8px !important;
            margin-bottom: 10px !important;
        }

        /* Submit Button Styling */
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"],
        div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            height: 46px !important;
            width: 100% !important;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
            transition: all 0.2s ease-in-out !important;
        }
        div[data-testid="stForm"] button:hover {
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5) !important;
            transform: translateY(-1px);
        }

        /* Results & Metrics Box */
        .res-box {
            background-color: #1A2332;
            border: 1px solid #263346;
            border-radius: 10px;
            padding: 16px;
            text-align: center;
        }
        .res-label {
            font-size: 0.75rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .res-value {
            font-size: 1.4rem;
            font-weight: 800;
        }

        /* Status Variant Colors */
        .val-safe { color: #10B981; }
        .val-warning { color: #F59E0B; }
        .val-danger { color: #EF4444; }
        .val-info { color: #38BDF8; }
        </style>
    """, unsafe_allow_html=True)

    # Page Header
    st.markdown('<div class="page-title">Traffic Detection & 78 Feature Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">⚡ Deep Packet Flow Analysis • Real-time Classification Engine</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍   Manual Feature Entry", "📁   Batch CSV Upload"])

    # TAB 1: MANUAL FEATURE ENTRY
    with tab1:
        st.markdown("<div style='margin-bottom: 12px; color: #94A3B8; font-size: 0.9rem;'>Input network flow data vectors across 78 dimensions below:</div>", unsafe_allow_html=True)
        
        feature_values = {}
        
        with st.form("prediction_form"):
            with st.expander("🌐 Flow Information (Basic Metrics)", expanded=True):
                cols = st.columns(4)
                for idx, feat in enumerate(DATASET_FEATURES[:10]):
                    with cols[idx % 4]:
                        feature_values[feat] = st.number_input(format_title(feat), value=0.0, key=f"f_{feat}")

            with st.expander("📊 Packet & Flag Statistics"):
                cols = st.columns(4)
                for idx, feat in enumerate(DATASET_FEATURES[10:40]):
                    with cols[idx % 4]:
                        feature_values[feat] = st.number_input(format_title(feat), value=0.0, key=f"f_{feat}")

            with st.expander("🛡️ Header & Segment Metrics"):
                cols = st.columns(4)
                for idx, feat in enumerate(DATASET_FEATURES[40:60]):
                    with cols[idx % 4]:
                        feature_values[feat] = st.number_input(format_title(feat), value=0.0, key=f"f_{feat}")

            with st.expander("⚡ Bulk & Activity Timings"):
                cols = st.columns(4)
                for idx, feat in enumerate(DATASET_FEATURES[60:]):
                    with cols[idx % 4]:
                        feature_values[feat] = st.number_input(format_title(feat), value=0.0, key=f"f_{feat}")

            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Run Deep ML Analysis")

        if submit:
            result = api_client.predict_traffic(feature_values)
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            st.markdown("### **Analysis Result**")
            
            # Custom Designed Result Metrics
            res_col1, res_col2, res_col3 = st.columns(3)
            
            status_cls = "val-safe" if result["status"].lower() == "benign" else "val-danger"
            risk_cls = "val-safe" if result["risk_level"].lower() in ["low", "none"] else ("val-warning" if result["risk_level"].lower() == "medium" else "val-danger")

            with res_col1:
                st.markdown(f'''
                    <div class="res-box">
                        <div class="res-label">Detection Status</div>
                        <div class="res-value {status_cls}">{result["status"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

            with res_col2:
                st.markdown(f'''
                    <div class="res-box">
                        <div class="res-label">Confidence Score</div>
                        <div class="res-value val-info">{result["confidence"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

            with res_col3:
                st.markdown(f'''
                    <div class="res-box">
                        <div class="res-label">Risk Level</div>
                        <div class="res-value {risk_cls}">{result["risk_level"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

    # TAB 2: BATCH CSV UPLOAD
    with tab2:
        st.markdown("<div style='margin-bottom: 12px; color: #94A3B8; font-size: 0.9rem;'>Upload a `.csv` file containing multi-row network traffic feature vectors:</div>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], label_visibility="collapsed")
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'''
                        <div class="res-box">
                            <div class="res-label">Uploaded Rows</div>
                            <div class="res-value val-info">{len(df):,}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'''
                        <div class="res-box">
                            <div class="res-label">Detected Features</div>
                            <div class="res-value val-info">{len(df.columns)} / 78</div>
                        </div>
                    ''', unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                
                missing = [f for f in DATASET_FEATURES if f not in df.columns]
                if missing:
                    st.error(f"❌ Dataset Validation Failed! Missing {len(missing)} required features.")
                else:
                    st.success("✅ Dataset Validated Successfully! All 78 required features present.")
                    st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")