import streamlit as st

def render_header(title: str):
    st.markdown(
        f"""
        <div style="margin-top: 0px; margin-bottom: 24px; padding-top: 2px;">
            <h2 style="
                margin: 0; 
                font-weight: 700; 
                font-size: 2rem; 
                color: #F9FAFB; 
                line-height: 1.1;
            ">Welcome IDS Controller!</h2>
            <p style="
                color: #9CA3AF; 
                margin-top: 6px; 
                margin-bottom: 0px; 
                font-size: 0.95rem;
            ">{title}</p>
        </div>
        """,
        unsafe_allow_html=True
    )