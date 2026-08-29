import streamlit as st

def render_status_widget(accuracy="96.8%", precision="95.4%", recall="94.9%", f1="95.1%"):
    # Inject CSS for Shadow Cards & Custom Metrics
    st.markdown("""
        <style>
        /* Individual Metric Box Styling with Shadow */
        div[data-testid="stMetric"] {
            background-color: #111827 !important;
            border: 1px solid #1F2937 !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.25) !important;
        }

        /* Metric Label Color */
        div[data-testid="stMetricLabel"] {
            color: #9CA3AF !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }

        /* Metric Value Color */
        div[data-testid="stMetricValue"] {
            color: #F9FAFB !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("##### **Model Performance**")

    # Metrics Grid Layout
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Accuracy", accuracy, "+2.1%")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        st.metric("Recall", recall, "+1.6%")
        
    with c2:
        st.metric("Precision", precision, "+1.8%")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        st.metric("F1 Score", f1, "+1.7%")