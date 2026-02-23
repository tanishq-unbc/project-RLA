"""Enhanced chart generation with holographic styling"""
import plotly.graph_objects as go
from ui.styles import COLORS, CHART_LAYOUT

def chart_agency(stats):
    """Create holographic agency distribution chart"""
    if not stats or 'agency_counts' not in stats:
        return go.Figure()
    
    agencies = list(stats['agency_counts'].keys())[:8]  # Top 8
    counts = [stats['agency_counts'][a] for a in agencies]
    
    fig = go.Figure(data=[
        go.Bar(
            x=agencies,
            y=counts,
            marker=dict(
                color=COLORS['cyan'],
                line=dict(
                    color=COLORS['cyan'],
                    width=2
                ),
                opacity=0.8
            ),
            hovertemplate='<b>%{x}</b><br>Launches: %{y}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text='',
            font=dict(size=14, color=COLORS['cyan'])
        ),
        height=250,
        showlegend=False,
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=10, color=COLORS['text_secondary']),
            showgrid=False,
        ),
        yaxis=dict(
            tickfont=dict(size=10, color=COLORS['text_secondary']),
            gridcolor=COLORS['glass_border'],
            gridwidth=0.5,
        ),
        bargap=0.3,
    )
    
    return fig


def chart_orbit(stats):
    """Create holographic orbit distribution chart"""
    if not stats or 'orbit_counts' not in stats:
        return go.Figure()
    
    orbits = list(stats['orbit_counts'].keys())[:8]  # Top 8
    counts = [stats['orbit_counts'][o] for o in orbits]
    
    # Create gradient colors from cyan to amber
    colors = [COLORS['cyan'] if i % 2 == 0 else COLORS['amber'] for i in range(len(orbits))]
    
    fig = go.Figure(data=[
        go.Bar(
            y=orbits,
            x=counts,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(
                    color=colors,
                    width=2
                ),
                opacity=0.8
            ),
            hovertemplate='<b>%{y}</b><br>Missions: %{x}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text='',
            font=dict(size=14, color=COLORS['cyan'])
        ),
        height=300,
        showlegend=False,
        xaxis=dict(
            tickfont=dict(size=10, color=COLORS['text_secondary']),
            gridcolor=COLORS['glass_border'],
            gridwidth=0.5,
        ),
        yaxis=dict(
            tickfont=dict(size=10, color=COLORS['text_secondary']),
            showgrid=False,
        ),
        bargap=0.2,
    )
    
    return fig