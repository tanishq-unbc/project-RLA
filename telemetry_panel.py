"""Live Telemetry Panel - Mission Clock & Orbital Data Display"""
from dash import html, dcc
from ui.styles import COLORS, HEADER_STYLE, DATA_VALUE_STYLE, DATA_LABEL_STYLE
from datetime import datetime, timedelta

def create_mission_clock_segment(value, label, color=COLORS['cyan']):
    """Create a single Nixie-tube style segment"""
    return html.Div(
        style={
            'display': 'inline-block',
            'margin': '0 8px',
            'textAlign': 'center',
        },
        children=[
            # Value (large, glowing)
            html.Div(
                value,
                style={
                    'fontSize': '48px',
                    'fontFamily': "'JetBrains Mono', monospace",
                    'color': color,
                    'fontWeight': '700',
                    'letterSpacing': '4px',
                    'textShadow': f"0 0 20px {color}, 0 0 40px {color}",
                    'backgroundColor': 'rgba(0, 0, 0, 0.8)',
                    'padding': '15px 20px',
                    'borderRadius': '8px',
                    'border': f"2px solid {color}",
                    'minWidth': '120px',
                }
            ),
            # Label (small, beneath)
            html.Div(
                label,
                style={
                    'fontSize': '10px',
                    'fontFamily': "'Rajdhani', sans-serif",
                    'color': COLORS['text_dim'],
                    'letterSpacing': '2px',
                    'marginTop': '8px',
                    'textTransform': 'uppercase',
                }
            )
        ]
    )


def create_mission_clock():
    """Create full mission clock display (T+ time since launch)"""
    return html.Div(
        style={
            'padding': '20px',
            'backgroundColor': 'rgba(0, 0, 0, 0.5)',
            'borderRadius': '12px',
            'border': f"1px solid {COLORS['glass_border']}",
            'marginBottom': '20px',
        },
        children=[
            html.Div("⏱️ MISSION CLOCK", style={**HEADER_STYLE, 'marginBottom': '20px'}),
            
            html.Div(
                id='mission-clock-display',
                style={'textAlign': 'center'},
                children=[
                    create_mission_clock_segment('000', 'HOURS', COLORS['cyan']),
                    html.Span(':', style={'fontSize': '48px', 'color': COLORS['cyan'], 'margin': '0 5px'}),
                    create_mission_clock_segment('00', 'MINUTES', COLORS['cyan']),
                    html.Span(':', style={'fontSize': '48px', 'color': COLORS['cyan'], 'margin': '0 5px'}),
                    create_mission_clock_segment('00', 'SECONDS', COLORS['cyan']),
                ]
            ),
            
            # Countdown to next event
            html.Div(
                style={'marginTop': '20px', 'textAlign': 'center'},
                children=[
                    html.Div("NEXT EVENT", style={'fontSize': '10px', 'color': COLORS['text_dim'], 'marginBottom': '10px'}),
                    create_mission_clock_segment('-045', 'MINS TO BURN', COLORS['amber']),
                ]
            )
        ]
    )


def create_telemetry_row(label, value, unit='', color=COLORS['cyan']):
    """Create a single telemetry data row"""
    return html.Div(
        style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '12px 0',
            'borderBottom': f"1px solid {COLORS['glass_border']}",
        },
        children=[
            html.Span(label, style={**DATA_LABEL_STYLE, 'fontSize': '11px'}),
            html.Div(
                style={'display': 'flex', 'alignItems': 'baseline'},
                children=[
                    html.Span(
                        value,
                        style={
                            **DATA_VALUE_STYLE,
                            'color': color,
                            'fontSize': '18px',
                            'fontWeight': '600',
                        }
                    ),
                    html.Span(
                        f" {unit}" if unit else "",
                        style={
                            'fontSize': '12px',
                            'color': COLORS['text_dim'],
                            'marginLeft': '5px',
                        }
                    )
                ]
            )
        ]
    )


def create_satellite_telemetry_panel(satellite_data=None):
    """Create live telemetry panel for selected satellite"""
    
    # Default placeholder data
    if not satellite_data:
        satellite_data = {
            'name': 'No Satellite Selected',
            'altitude': '---',
            'velocity': '---',
            'apogee': '---',
            'perigee': '---',
            'inclination': '---',
            'period': '---',
            'latitude': '---',
            'longitude': '---',
        }
    
    return html.Div(
        id='telemetry-panel',
        style={
            'padding': '20px',
            'backgroundColor': 'rgba(0, 0, 0, 0.5)',
            'borderRadius': '12px',
            'border': f"1px solid {COLORS['glass_border']}",
        },
        children=[
            html.Div("📡 LIVE TELEMETRY", style={**HEADER_STYLE, 'marginBottom': '15px'}),
            
            html.Div(
                id='selected-satellite-name',
                children=satellite_data['name'],
                style={
                    'fontSize': '16px',
                    'color': COLORS['text_primary'],
                    'fontWeight': '600',
                    'marginBottom': '20px',
                    'fontFamily': "'JetBrains Mono', monospace",
                }
            ),
            
            # Orbital Elements
            html.Div("ORBITAL ELEMENTS", style={'fontSize': '10px', 'color': COLORS['text_dim'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
            
            create_telemetry_row('ALTITUDE', f"{satellite_data['altitude']}", 'km', COLORS['cyan']),
            create_telemetry_row('VELOCITY', f"{satellite_data['velocity']}", 'km/s', COLORS['cyan']),
            create_telemetry_row('APOGEE', f"{satellite_data['apogee']}", 'km', COLORS['amber']),
            create_telemetry_row('PERIGEE', f"{satellite_data['perigee']}", 'km', COLORS['amber']),
            create_telemetry_row('INCLINATION', f"{satellite_data['inclination']}", '°', COLORS['cyan']),
            create_telemetry_row('PERIOD', f"{satellite_data['period']}", 'min', COLORS['cyan']),
            
            # Current Position
            html.Div("CURRENT POSITION", style={'fontSize': '10px', 'color': COLORS['text_dim'], 'marginTop': '20px', 'marginBottom': '10px', 'letterSpacing': '1px'}),
            
            create_telemetry_row('LATITUDE', f"{satellite_data['latitude']}", '°', COLORS['cyan']),
            create_telemetry_row('LONGITUDE', f"{satellite_data['longitude']}", '°', COLORS['cyan']),
        ]
    )


def create_pass_prediction_panel():
    """Create panel showing when satellite will be overhead"""
    return html.Div(
        style={
            'padding': '20px',
            'backgroundColor': 'rgba(0, 0, 0, 0.5)',
            'borderRadius': '12px',
            'border': f"1px solid {COLORS['glass_border']}",
            'marginTop': '20px',
        },
        children=[
            html.Div("🌍 NEXT PASS", style={**HEADER_STYLE, 'marginBottom': '15px'}),
            
            html.Div(
                id='next-pass-info',
                children=[
                    create_telemetry_row('RISE TIME', '22:45:30', 'UTC', COLORS['amber']),
                    create_telemetry_row('MAX ELEVATION', '45', '°', COLORS['cyan']),
                    create_telemetry_row('SET TIME', '22:53:12', 'UTC', COLORS['amber']),
                    create_telemetry_row('DURATION', '7.7', 'min', COLORS['cyan']),
                ]
            )
        ]
    )


# Auto-update interval component
def create_telemetry_updater():
    """Create interval component for live data updates"""
    return dcc.Interval(
        id='telemetry-update-interval',
        interval=1000,  # Update every 1 second
        n_intervals=0
    )