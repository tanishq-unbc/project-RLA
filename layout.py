"""Main dashboard layout - Deep Space Mission Control"""

from dash import dcc, html
from ui.styles import (
    GLASS,
    COLORS,
    BUTTON_PRIMARY,
    BUTTON_SECONDARY,
    BUTTON_GHOST,
    DROPDOWN_STYLE,
    HEADER_STYLE,
    SUBHEADER_STYLE,
    DATA_VALUE_STYLE,
    DATA_LABEL_STYLE,
    DIVIDER_STYLE,
)

def create_layout(db, stats, orbits):
    """Create the main Dash layout with Deep Space theme and Dual Panels"""
    return html.Div(
        style={
            "backgroundColor": "#000000",
            "height": "100vh",
            "width": "100vw",
            "overflow": "hidden",
            "position": "relative",
            "fontFamily": "'Inter', 'Segoe UI', system-ui, sans-serif",
        },
        children=[
            # Storage for satellite data - used by callbacks
            dcc.Store(id="satellite-store", data=[]),

            # --- CENTRAL MAP CONTAINER ---
            # This Div receives the Plotly Graph from map_callbacks.py
            html.Div(
                id="globe-viz",
                style={
                    "height": "100vh",
                    "width": "100vw",
                    "position": "absolute",
                    "top": 0,
                    "left": 0,
                    "zIndex": 0,
                    "background": "#000000",
                },
            ),

            # ============================================================================
            # SATELLITE FILTER PANEL - Top Left
            # ============================================================================
            html.Div(
                id="satellite-panel",
                style={**GLASS, "top": "20px", "left": "20px", "width": "300px", "zIndex": 10},
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "marginBottom": "15px",
                        },
                        children=[
                            html.Div("🛰️ SATELLITE FILTERS", style={**HEADER_STYLE}),
                        ],
                    ),
                    html.Hr(style={**DIVIDER_STYLE}),
                    html.Div(
                        id="satellite-content",
                        children=[
                            html.Label("MISSION CLASSIFICATION", style={**SUBHEADER_STYLE}),
                            dcc.Checklist(
                                id="satellite-types",
                                options=[
                                    {"label": " 🏛️ SPACE STATIONS", "value": "Station"},
                                    {"label": " 🔭 TELESCOPES", "value": "Science"},
                                    {"label": " 🛰️ NAVIGATION", "value": "Navigation"},
                                    {"label": " 📡 COMMUNICATIONS", "value": "Communication"},
                                    {"label": " 🌍 EARTH OBSERVATION", "value": "Earth Observation"},
                                    {"label": " 🌦️ WEATHER SYSTEMS", "value": "Weather"},
                                ],
                                value=["Station", "Science", "Navigation"],
                                style={
                                    "color": COLORS["text_primary"],
                                    "fontSize": "12px",
                                },
                                labelStyle={"display": "block", "marginBottom": "12px", "cursor": "pointer"},
                            ),
                        ],
                    ),
                ],
            ),

            # ============================================================================
            # MISSION CONTROL PANEL - Top Right
            # ============================================================================
            html.Div(
                id="control-panel",
                style={**GLASS, "top": "20px", "right": "20px", "width": "320px", "zIndex": 10},
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "marginBottom": "15px",
                        },
                        children=[
                            html.Div("🚀 MISSION CONTROL", style={**HEADER_STYLE}),
                        ],
                    ),
                    html.Hr(style={**DIVIDER_STYLE}),
                    html.Div(
                        id="control-content",
                        children=[
                            html.Label("AGENCY UPLINK", style={**SUBHEADER_STYLE}),
                            dcc.Dropdown(
                                id="agency",
                                options=[
                                    {"label": " ALL AGENCIES", "value": "All"},
                                    {"label": " SPACEX", "value": "SpaceX"},
                                    {"label": " NASA", "value": "NASA"},
                                    {"label": " ROSCOSMOS", "value": "Russia"},
                                    {"label": " CNSA", "value": "China"},
                                ],
                                value="All",
                                clearable=False,
                                style={**DROPDOWN_STYLE, "marginBottom": "18px"},
                            ),
                            
                            # Mission Stats Display
                            html.Div([
                                html.Div([
                                    html.Span("TOTAL ASSETS", style=DATA_LABEL_STYLE),
                                    html.Span(f"{stats['total']:,}", style=DATA_VALUE_STYLE),
                                ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "10px"}),
                                html.Div([
                                    html.Span("UPCOMING", style=DATA_LABEL_STYLE),
                                    html.Span(f"{stats['upcoming']:,}", style={**DATA_VALUE_STYLE, "color": COLORS["amber"]}),
                                ], style={"display": "flex", "justifyContent": "space-between"}),
                            ], style={"padding": "10px", "backgroundColor": "rgba(0,0,0,0.2)", "borderRadius": "5px"}),

                            html.Button("⟳ REFRESH UPLINK", id="refresh", n_clicks=0, 
                                        style={**BUTTON_PRIMARY, "marginTop": "20px", "width": "100%"}),
                        ],
                    ),
                ],
            ),
        ],
    )