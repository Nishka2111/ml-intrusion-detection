import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_donut_chart(df: pd.DataFrame):
    fig = px.pie(
        df, 
        values='Count', 
        names='Attack Type', 
        hole=0.6,
        color_discrete_sequence=['#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6', '#10B981']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F9FAFB'),
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def render_traffic_line_chart(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Total Traffic'], mode='lines', name='Total Traffic', line=dict(color='#2563EB', width=2)))
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Detected Threats'], mode='lines', name='Detected Threats', line=dict(color='#EF4444', width=2)))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F9FAFB'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#1F2937'),
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(orientation="h", y=1.1)
    )
    return fig