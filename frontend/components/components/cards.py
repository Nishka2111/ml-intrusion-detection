import streamlit as st

def render_kpi_card(title: str, value: str, change: str, is_positive: bool = True):
    configs = {
        "Total Traffic": {
            "title_text": "TOTAL TRAFFIC",
            "sub_text": "Connections",
            "bg": "linear-gradient(135deg, #0A192F 0%, #0D213A 100%)",
            "border": "#1E3A5F",
            "icon_bg": "#1D4ED8",
            "line_color": "#3B82F6",
            "fill_id": "blueGlow",
            "svg_icon": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>'
        },
        "Detected Threats": {
            "title_text": "DETECTED ATTACKS",
            "sub_text": "Threats Found",
            "bg": "linear-gradient(135deg, #2A0F14 0%, #1A090C 100%)",
            "border": "#4C1D24",
            "icon_bg": "#DC2626",
            "line_color": "#EF4444",
            "fill_id": "redGlow",
            "svg_icon": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
        },
        "Safe Traffic": {
            "title_text": "NORMAL TRAFFIC",
            "sub_text": "Safe Connections",
            "bg": "linear-gradient(135deg, #062319 0%, #03140E 100%)",
            "border": "#0D4732",
            "icon_bg": "#16A34A",
            "line_color": "#10B981",
            "fill_id": "greenGlow",
            "svg_icon": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>'
        },
        "Threat Rate": {
            "title_text": "THREAT RATE",
            "sub_text": "Of Total Traffic",
            "bg": "linear-gradient(135deg, #281609 0%, #170C04 100%)",
            "border": "#4A2810",
            "icon_bg": "#EA580C",
            "line_color": "#F97316",
            "fill_id": "orangeGlow",
            "svg_icon": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>'
        }
    }

    cfg = configs.get(title, configs["Total Traffic"])

    sparkline_svg = (
        f'<svg width="65" height="32" viewBox="0 0 75 38" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">'
        f'<defs>'
        f'<linearGradient id="{cfg["fill_id"]}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{cfg["line_color"]}" stop-opacity="0.45"/>'
        f'<stop offset="100%" stop-color="{cfg["line_color"]}" stop-opacity="0.0"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<path d="M2 32 C 10 22, 16 30, 23 18 C 30 6, 37 24, 46 15 C 53 8, 60 2, 73 12 L 73 36 L 2 36 Z" fill="url(#{cfg["fill_id"]})"/>'
        f'<path d="M2 32 C 10 22, 16 30, 23 18 C 30 6, 37 24, 46 15 C 53 8, 60 2, 73 12" stroke="{cfg["line_color"]}" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
        f'</svg>'
    )

    html_card = (
        f'<div style="'
        f'background: {cfg["bg"]}; '
        f'border: 1px solid {cfg["border"]}; '
        f'border-radius: 12px; '
        f'padding: 12px 14px; '
        f'box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4); '
        f'display: flex; '
        f'flex-direction: column; '
        f'justify-content: space-between; '
        f'min-height: 128px; '
        f'height: auto; '
        f'box-sizing: border-box; '
        f'overflow: hidden;">'
        
        # Top Container
        f'<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 8px;">'
        f'<div style="background-color: {cfg["icon_bg"]}; width: 38px; height: 38px; border-radius: 8px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); flex-shrink: 0;">{cfg["svg_icon"]}</div>'
        
        f'<div style="flex-grow: 1; min-width: 0; overflow: hidden;">'
        f'<div style="color: #94A3B8; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{cfg["title_text"]}</div>'
        f'<div style="color: #FFFFFF; font-size: 1.35rem; font-weight: 800; line-height: 1.1; margin: 2px 0; word-break: break-all;">{value}</div>'
        f'<div style="color: #64748B; font-size: 0.68rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{cfg["sub_text"]}</div>'
        f'</div>'
        
        f'<div style="display: flex; align-items: center; justify-content: flex-end; flex-shrink: 0;">{sparkline_svg}</div>'
        f'</div>'
        
        # Bottom Container
        f'<div style="display: flex; align-items: center; flex-wrap: wrap; font-size: 0.7rem; font-weight: 600; margin-top: 8px; gap: 4px;">'
        f'<span style="color: {cfg["line_color"]}; flex-shrink: 0;">{change}</span>'
        f'<span style="color: #64748B; font-weight: 400; flex-shrink: 0;">From Yesterday</span>'
        f'</div>'
        
        f'</div>'
    )

    st.markdown(html_card, unsafe_allow_html=True)