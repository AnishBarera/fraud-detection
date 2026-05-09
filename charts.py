import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Standard fintech dark theme colors
BACKGROUND_COLOR = "#0e1117"
PAPER_COLOR = "#0e1117"
FONT_COLOR = "#FAFAFA"
SAFE_COLOR = "#00C853" # Green
FRAUD_COLOR = "#D50000" # Red
ACCENT_COLOR = "#2962FF" # Blue

def create_fraud_pie_chart(safe_count: int, fraud_count: int) -> go.Figure:
    """
    Creates a donut chart comparing safe vs fraudulent transactions.
    """
    labels = ['Safe', 'Fraud']
    values = [safe_count, fraud_count]
    colors = [SAFE_COLOR, FRAUD_COLOR]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    
    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='value', 
        textfont_size=16,
        marker=dict(colors=colors, line=dict(color=BACKGROUND_COLOR, width=2))
    )
    
    fig.update_layout(
        title="Transaction Breakdown",
        title_font_size=20,
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color=FONT_COLOR),
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig

def create_trend_line_chart(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """
    Creates a line chart showing the trend of fraud incidents over time.
    """
    fig = px.line(
        df, 
        x=x_col, 
        y=y_col, 
        markers=True,
        title="Fraud Alerts Over Time"
    )
    
    fig.update_traces(
        line=dict(color=FRAUD_COLOR, width=3),
        marker=dict(size=8, color=FRAUD_COLOR, symbol='circle')
    )
    
    fig.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color=FONT_COLOR),
        xaxis=dict(showgrid=False, title="Time"),
        yaxis=dict(showgrid=True, gridcolor="#333333", title="Incidents"),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

def create_activity_bar_chart(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """
    Creates a bar chart showing overall transaction activity.
    """
    fig = px.bar(
        df, 
        x=x_col, 
        y=y_col,
        title="Transaction Volume by Hour"
    )
    
    fig.update_traces(
        marker_color=ACCENT_COLOR,
        marker_line_color=BACKGROUND_COLOR,
        marker_line_width=1.5,
        opacity=0.8
    )
    
    fig.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color=FONT_COLOR),
        xaxis=dict(showgrid=False, title="Hour of Day"),
        yaxis=dict(showgrid=True, gridcolor="#333333", title="Transactions"),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig
