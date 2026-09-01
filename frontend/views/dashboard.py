import streamlit as st
from services import api_client
from components.header import render_header
from components.cards import render_kpi_card
from components.charts import render_donut_chart, render_traffic_line_chart
from components.tables import render_predictions_table
from components.status import render_status_widget

def render():
    # CSS to force equal height on bottom row containers
    st.markdown("""
    <style>
        /* Bottom Row Columns Stretch to Equal Height */
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTable"]),
        div[data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
        }
        
        div[data-testid="column"] {
            display: flex;
            flex-direction: column;
        }
        
        div[data-testid="column"] > div {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        div[data-testid="column"] [data-testid="stElementContainer"] {
            flex: 1;
        }

        /* Ensure st.container inside status_col takes 100% height */
        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
            height: 100% !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    </style>
    """, unsafe_allow_html=True)

    # Top Header Row (Without Time)
    col_title, col_status = st.columns([0.7, 0.3])
    
    with col_title:
        render_header("Monitor your network, detect threats, and keep your system secure.")
        
    with col_status:
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: flex-end; height: 100%; margin-top: 4px;">
                <span style="
                    background: rgba(16, 185, 129, 0.15); 
                    color: #10B981; 
                    padding: 6px 14px; 
                    border-radius: 20px; 
                    font-size: 0.85rem; 
                    font-weight: 600;
                    border: 1px solid rgba(16, 185, 129, 0.3);
                ">● System Online</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    data = api_client.get_dashboard_data()
    metrics = data["metrics"]

    # Top KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Traffic", metrics["total_traffic"], metrics["total_traffic_change"], True)
    with col2:
        render_kpi_card("Detected Threats", metrics["detected_threats"], metrics["detected_threats_change"], False)
    with col3:
        render_kpi_card("Safe Traffic", metrics["safe_traffic"], metrics["safe_traffic_change"], True)
    with col4:
        render_kpi_card("Threat Rate", metrics["threat_rate"], metrics["threat_rate_change"], True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row in Separate Box Cards
    chart_col1, chart_col2 = st.columns([1, 2])
    
    # Donut Chart Box Card
    with chart_col1:
        with st.container(border=True):
            st.markdown("<h5 style='margin-bottom: 15px;'><b>Attack Distribution</b></h5>", unsafe_allow_html=True)
            st.plotly_chart(render_donut_chart(data["attack_dist"]), use_container_width=True)
            
    # Line Chart Box Card
    with chart_col2:
        with st.container(border=True):
            st.markdown("<h5 style='margin-bottom: 15px;'><b>Network Traffic (Last 24 Hours)</b></h5>", unsafe_allow_html=True)
            st.plotly_chart(render_traffic_line_chart(data["traffic_history"]), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Table & Status Row - Bottom Alignment Fixed
    table_col, status_col = st.columns([2, 1])
    
    with table_col:
        render_predictions_table(data["recent_predictions"])
        
    with status_col:
        with st.container(border=True):
            render_status_widget()