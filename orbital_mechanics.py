"""
ASTRO MISSION CONTROL - ORBITAL MECHANICS ENHANCEMENT
Concept Document for Flight Path & Telemetry Visualization
"""

# ============================================================================
# 1. COLOR-CODED ALTITUDE VISUALIZATION
# ============================================================================

ALTITUDE_GRADIENT = {
    # Atmospheric Layers (for launches)
    'troposphere': (0, 12),        # Blue (#0066ff)
    'stratosphere': (12, 50),      # Cyan (#00f3ff)
    'mesosphere': (50, 85),        # Purple (#9d4edd)
    'thermosphere': (85, 600),     # Orange (#ff6b35)
    'exosphere': (600, 10000),     # Red (#ff0054)
    
    # Orbital Regimes (for satellites)
    'leo': (160, 2000),            # Bright Cyan (#00f3ff)
    'meo': (2000, 35786),          # Amber (#ffcc00)
    'geo': (35786, 35786),         # Crimson (#ff2a6d)
}

# ============================================================================
# 2. LIVE TELEMETRY PANEL STRUCTURE
# ============================================================================

TELEMETRY_DISPLAY = {
    'mission_clock': {
        'T+': 'Time since launch',
        'countdown': 'Next burn/event',
        'ground_station': 'Current ground contact',
    },
    
    'orbital_elements': {
        'apogee': 'Highest point (km)',
        'perigee': 'Lowest point (km)',
        'inclination': 'Orbital tilt (°)',
        'period': 'Time per orbit (min)',
        'velocity': 'Current speed (km/s)',
        'altitude': 'Height above surface (km)',
    },
    
    'real_time_data': {
        'lat': 'Current latitude',
        'lon': 'Current longitude',
        'next_pass': 'When overhead',
        'ground_track': 'Path over Earth',
    }
}

# ============================================================================
# 3. SATELLITE ID CARD (HOVER POPUP)
# ============================================================================

SATELLITE_CARD_TEMPLATE = """
┌─────────────────────────────────┐
│ 🛰️ {satellite_name}             │
├─────────────────────────────────┤
│ ALT: {altitude:,} km            │
│ VEL: {velocity:.2f} km/s        │
│ INC: {inclination}°             │
│ APO: {apogee:,} km              │
│ PER: {perigee:,} km             │
├─────────────────────────────────┤
│ NEXT PASS: {next_pass}          │
│ DURATION: {pass_duration} min   │
└─────────────────────────────────┘
"""

# ============================================================================
# 4. WIREFRAME TERRAIN OVERLAY
# ============================================================================

TERRAIN_CONFIG = {
    'earth': {
        'show_mountains': True,
        'show_oceans': True,
        'wireframe_color': 'rgba(255, 255, 255, 0.1)',
        'grid_resolution': 100,
    },
    
    'moon': {
        'show_craters': True,
        'wireframe_color': 'rgba(0, 243, 255, 0.2)',
    },
    
    'mars': {
        'show_olympus_mons': True,
        'show_valles_marineris': True,
        'wireframe_color': 'rgba(255, 102, 0, 0.3)',
    }
}

# ============================================================================
# 5. MISSION CLOCK DISPLAY (NIXIE TUBE AESTHETIC)
# ============================================================================

MISSION_CLOCK_SEGMENTS = [
    {'label': 'T+ HOURS', 'format': '{:03d}', 'color': '#00f3ff'},
    {'label': 'T+ MINS', 'format': '{:02d}', 'color': '#00f3ff'},
    {'label': 'T+ SECS', 'format': '{:02d}', 'color': '#00f3ff'},
    {'separator': ':', 'glow': True},
    {'label': 'NEXT BURN', 'format': '-{:03d}', 'color': '#ffcc00'},
]

# ============================================================================
# 6. UI LAYOUT ZONES
# ============================================================================

UI_ZONES = {
    'left_panel': {
        'satellite_selector': 'Checkbox list with type filters',
        'mission_clock': 'Segmented digital display',
        'quick_stats': 'Total sats, active missions',
    },
    
    'center_globe': {
        'earth_3d': 'Rotating globe with wireframe',
        'orbital_paths': 'Color-coded by altitude',
        'ground_tracks': 'Satellite footprints',
        'launch_trajectories': 'Rocket ascent paths',
    },
    
    'right_panel': {
        'mission_control': 'Agency/orbit/search filters',
        'telemetry_live': 'Real-time selected satellite data',
        'pass_predictions': 'When satellites are overhead',
    },
    
    'bottom_panel': {
        'mission_intel': 'Chat/log interface',
        'event_timeline': 'Upcoming burns, passes, launches',
    }
}

# ============================================================================
# 7. AESTHETIC PRINCIPLES (CYBERPUNK/AVIATION)
# ============================================================================

DESIGN_RULES = {
    'negative_space': 'Large margins, breathable layout',
    'typography': {
        'headers': 'Rajdhani/Montserrat - UPPERCASE, wide tracking',
        'data': 'JetBrains Mono - monospace for precision',
        'body': 'Inter - clean sans-serif',
    },
    
    'color_hierarchy': {
        'primary_action': '#00f3ff (cyan) - active satellites',
        'secondary_action': '#ffcc00 (amber) - warnings/future',
        'danger': '#ff2a6d (crimson) - errors/critical',
        'neutral': '#8a9bb5 (grey) - inactive/labels',
    },
    
    'transparency': {
        'popup_cards': 'rgba(20, 30, 50, 0.9) - see-through',
        'panels': 'backdrop-blur(20px) - glassmorphism',
    }
}

# ============================================================================
# 8. TECH STACK RECOMMENDATIONS
# ============================================================================

IMPLEMENTATION_STACK = {
    'frontend': {
        'current': 'Dash (Python) - Good for MVP',
        'upgrade_path': 'React + Three.js - For production',
    },
    
    '3d_engine': {
        'option_1': 'Plotly (current) - Easy integration',
        'option_2': 'Three.js - More control, better performance',
        'option_3': 'CesiumJS - Industry standard aerospace',
    },
    
    'data_sources': {
        'satellites': 'Space-Track.org TLE data (current)',
        'real_time': 'Skyfield for position calculation (current)',
        'flights': 'OpenSky Network (optional expansion)',
        'weather': 'NOAA satellites',
    },
    
    'hardware_integration': {
        'macro_pad': 'Arduino + Python serial communication',
        'rotary_encoder': 'Control globe rotation',
        'led_display': 'Mission clock on physical hardware',
    }
}

# ============================================================================
# 9. FEATURE ROADMAP
# ============================================================================

FEATURE_PRIORITY = {
    'phase_1_immediate': [
        '✓ Color-coded orbital paths by altitude',
        '✓ Hover popup with telemetry (satellite ID card)',
        '✓ Mission clock display (T+ time)',
        '✓ Enhanced glassmorphism panels',
    ],
    
    'phase_2_enhancement': [
        '⚡ Real-time telemetry updates (live velocity)',
        '⚡ Pass prediction (when satellite overhead)',
        '⚡ Atmospheric layer visualization',
        '⚡ Ground track footprints',
    ],
    
    'phase_3_advanced': [
        '🚀 Launch trajectory simulation',
        '🚀 Maneuver planning (delta-V calculator)',
        '🚀 Communication windows',
        '🚀 Hardware integration (physical controls)',
    ]
}

# ============================================================================
# 10. SAMPLE CODE STRUCTURE
# ============================================================================

"""
visualization/
├── orbital_mechanics.py    # Altitude-based color gradient paths
├── telemetry_panel.py      # Live data display components
├── mission_clock.py        # T+ timer with Nixie aesthetic
└── satellite_card.py       # Hover popup ID cards

ui/
├── telemetry_layout.py     # Right panel with real-time data
└── mission_clock_widget.py # Segmented digital display

utils/
├── orbit_calculations.py   # Apogee, perigee, velocity
├── pass_predictor.py       # When satellite is overhead
└── atmospheric_layers.py   # Altitude -> layer mapping
"""

# ============================================================================
# NOTES
# ============================================================================

"""
This concept document outlines the enhancement from a simple "dot on a map"
to a full-featured orbital mechanics visualization with live telemetry.

Key Inspirations:
- Flightradar24 aesthetic (neon altitude lines)
- NASA mission control dashboards
- Cyberpunk UI design (transparency, glow effects)
- Aviation instrumentation (precision data display)

Implementation Priority:
1. Get basic orbital paths with color gradients working
2. Add telemetry hover cards
3. Build mission clock display
4. Enhance with real-time updates
"""