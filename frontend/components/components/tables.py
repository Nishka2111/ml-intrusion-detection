import streamlit as st
import pandas as pd

def render_predictions_table(df: pd.DataFrame):
    rows_list = []
    
    for i, (_, row) in enumerate(df.iterrows()):
        risk_val = str(row['Risk']).upper()
        if risk_val == "HIGH":
            pill_style = "background: rgba(239, 68, 68, 0.15); color: #FCA5A5; border: 1px solid #EF4444;"
        elif risk_val == "MEDIUM":
            pill_style = "background: rgba(245, 158, 11, 0.15); color: #FDE047; border: 1px solid #F59E0B;"
        else:
            pill_style = "background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border: 1px solid #10B981;"

        # Bottom border for internal table rows
        border_bottom = "border-bottom: 1px solid #1F2937;" if i < len(df) - 1 else ""

        row_html = (
            f'<tr style="{border_bottom}">'
            f'<td style="padding: 10px 12px; color: #9CA3AF;">{row["Time"]}</td>'
            f'<td style="padding: 10px 12px; color: #FFFFFF; font-weight: 500;">{row["Source IP"]}</td>'
            f'<td style="padding: 10px 12px; color: #E2E8F0;">{row["Destination IP"]}</td>'
            f'<td style="padding: 10px 12px; color: #E2E8F0;">{row["Attack Type"]}</td>'
            f'<td style="padding: 10px 12px; color: #FFFFFF; font-weight: 600;">{row["Confidence"]}</td>'
            f'<td style="padding: 10px 12px;"><span style="display: inline-block; padding: 2px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; {pill_style}">{row["Risk"]}</span></td>'
            f'</tr>'
        )
        rows_list.append(row_html)
        
    rows_joined = "".join(rows_list)

    # Clean Single Card Wrapper (Matches Right Card Perfectly)
    full_card_html = (
        f'<div style="'
        f'background: #0B132B; '
        f'border: 1px solid #1C2541; '
        f'border-radius: 12px; '
        f'padding: 20px; '
        f'box-sizing: border-box; '
        f'width: 100%;">'
        f'<h4 style="margin: 0 0 16px 0; color: #FFFFFF; font-weight: 700; font-size: 1.1rem; font-family: sans-serif;">Recent Predictions</h4>'
        f'<div style="overflow-x: auto; background: #111827; border: 1px solid #1F2937; border-radius: 8px;">'
        f'<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; font-family: sans-serif;">'
        f'<thead>'
        f'<tr style="border-bottom: 1px solid #1F2937; background: #161F33; color: #9CA3AF;">'
        f'<th style="padding: 10px 12px; font-weight: 600;">Time</th>'
        f'<th style="padding: 10px 12px; font-weight: 600;">Source IP</th>'
        f'<th style="padding: 10px 12px; font-weight: 600;">Destination IP</th>'
        f'<th style="padding: 10px 12px; font-weight: 600;">Attack Type</th>'
        f'<th style="padding: 10px 12px; font-weight: 600;">Confidence</th>'
        f'<th style="padding: 10px 12px; font-weight: 600;">Risk</th>'
        f'</tr>'
        f'</thead>'
        f'<tbody>'
        f'{rows_joined}'
        f'</tbody>'
        f'</table>'
        f'</div>'
        f'</div>'
    )
    
    st.markdown(full_card_html, unsafe_allow_html=True)