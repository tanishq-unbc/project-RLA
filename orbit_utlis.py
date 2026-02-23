"""Advanced orbit visualization utilities - Gradient fading and effects"""
import numpy as np
from ui.styles import COLORS

def create_fading_gradient(num_points, start_color, end_color, start_opacity=0.1, end_opacity=1.0):
    """
    Create a gradient color array that fades from transparent to opaque.
    Used for the "comet tail" past trajectory effect.
    
    Args:
        num_points: Number of points in the trajectory
        start_color: RGB color at the oldest point (hex)
        end_color: RGB color at the current position (hex)
        start_opacity: Opacity at tail end (0.0 - 1.0)
        end_opacity: Opacity at current position (0.0 - 1.0)
    
    Returns:
        List of RGBA color strings
    """
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    # Create gradient
    colors = []
    for i in range(num_points):
        # Linear interpolation
        t = i / max(num_points - 1, 1)
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        opacity = start_opacity + (end_opacity - start_opacity) * t
        
        colors.append(f'rgba({r},{g},{b},{opacity})')
    
    return colors


def create_dash_pattern_future():
    """
    Create dash pattern for future predicted orbit.
    Returns Plotly-compatible dash style.
    """
    return 'dot'  # Options: 'solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot'


def calculate_orbit_color_by_altitude(altitude_km):
    """
    Assign orbit color based on altitude:
    - LEO (< 2000 km): Cyan
    - MEO (2000-35786 km): Amber
    - GEO (> 35786 km): Crimson
    """
    if altitude_km < 2000:
        return COLORS['cyan']
    elif altitude_km < 35786:
        return COLORS['amber']
    else:
        return COLORS['crimson']


def create_pulse_marker_trace(lon, lat, name, color=COLORS['cyan']):
    """
    Create a pulsing marker trace for live satellites.
    Uses animation frames to create the pulse effect.
    """
    import plotly.graph_objects as go
    
    # Create multiple concentric circles with decreasing opacity
    traces = []
    
    for i, size in enumerate([15, 20, 25]):
        opacity = 0.8 - (i * 0.3)
        traces.append(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                opacity=opacity,
                symbol='circle',
                line=dict(width=0)
            ),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Main marker
    traces.append(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        mode='markers+text',
        marker=dict(
            size=12,
            color=color,
            symbol='diamond',
            line=dict(width=2, color='white')
        ),
        text=f"🛰️ {name}",
        textposition='top center',
        textfont=dict(
            size=9,
            color=color,
            family="'JetBrains Mono', monospace"
        ),
        showlegend=False
    ))
    
    return traces


def create_drop_line_trace(lon, lat, altitude_km):
    """
    Create a vertical "drop line" from satellite to ground.
    This provides depth perception for 3D orbits.
    
    Note: This is simplified for 2D map - for true 3D, use Scatter3d
    """
    import plotly.graph_objects as go
    
    # For 2D maps, we'll just create a subtle line to the ground marker
    return go.Scattergeo(
        lon=[lon, lon],
        lat=[lat, lat],
        mode='lines',
        line=dict(
            width=1,
            color=COLORS['glass_border'],
            dash='dot'
        ),
        opacity=0.3,
        hoverinfo='skip',
        showlegend=False
    )


def adaptive_orbit_sampling(total_duration_minutes, zoom_level=1.0):
    """
    Dynamically adjust orbit sampling based on zoom level.
    
    Args:
        total_duration_minutes: Total time span to plot
        zoom_level: Current map zoom (1.0 = global view, higher = zoomed in)
    
    Returns:
        sample_interval_seconds: Seconds between calculated points
    """
    # Base interval for global view
    base_interval = 45  # seconds
    
    # Increase resolution when zoomed in
    if zoom_level > 2.0:
        return base_interval // 2  # 22.5 seconds
    elif zoom_level > 4.0:
        return base_interval // 4  # 11.25 seconds
    else:
        return base_interval


def batch_orbit_data(satellites, max_batch_size=50):
    """
    Split satellites into batches to prevent overwhelming the renderer.
    For apps with 100+ satellites, render in chunks.
    """
    batches = []
    for i in range(0, len(satellites), max_batch_size):
        batches.append(satellites[i:i + max_batch_size])
    return batches


# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def estimate_trace_count(num_satellites, use_single_trace=True):
    """
    Estimate number of traces that will be created.
    
    Without optimization: 3 traces per satellite (past, future, marker)
    With single-trace: 1 trace for all orbits + 1 for markers = 2 total
    """
    if use_single_trace:
        return 2  # One combined orbit trace + one combined marker trace
    else:
        return num_satellites * 3  # Individual traces per satellite


def print_performance_stats(num_satellites, num_points_per_orbit):
    """Debug helper to estimate rendering complexity"""
    total_points = num_satellites * num_points_per_orbit
    
    print(f"""
    ═══════════════════════════════════════════
    🚀 ORBIT RENDERING PERFORMANCE STATS
    ═══════════════════════════════════════════
    Satellites: {num_satellites}
    Points per orbit: {num_points_per_orbit}
    Total geometry points: {total_points:,}
    
    Single-trace mode: ✓ ENABLED
    Estimated traces: {estimate_trace_count(num_satellites, True)}
    
    Without optimization: {estimate_trace_count(num_satellites, False)} traces
    Performance gain: {estimate_trace_count(num_satellites, False) / estimate_trace_count(num_satellites, True):.1f}x
    ═══════════════════════════════════════════
    """)