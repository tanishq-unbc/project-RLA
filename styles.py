"""Enhanced UI styles with Deep Space Glassmorphism theme"""

# ============================================================================
# CYBER-VOID COLOR PALETTE
# ============================================================================
COLORS = {
    # Primary - The Void
    'void_deep': '#0b0d17',
    'void_navy': '#151b2e',
    
    # Secondary - Glass Panels
    'glass_base': 'rgba(20, 30, 50, 0.6)',
    'glass_border': 'rgba(0, 243, 255, 0.15)',
    'glass_highlight': 'rgba(255, 255, 255, 0.05)',
    
    # Accent - The Signal
    'cyan': '#00f3ff',
    'cyan_glow': 'rgba(0, 243, 255, 0.3)',
    'amber': '#ffcc00',
    'amber_glow': 'rgba(255, 204, 0, 0.3)',
    'crimson': '#ff2a6d',
    'crimson_glow': 'rgba(255, 42, 109, 0.3)',
    
    # Data/Text
    'text_primary': '#e8f0ff',
    'text_secondary': '#8a9bb5',
    'text_dim': '#4a5568',
    'text_mono': '#b4c7e7',
}

# ============================================================================
# ENHANCED GLASSMORPHISM PANEL
# ============================================================================
GLASS = {
    'position': 'absolute',
    'backgroundColor': COLORS['glass_base'],
    'backdropFilter': 'blur(20px) saturate(180%)',
    'WebkitBackdropFilter': 'blur(20px) saturate(180%)',
    'border': f"1px solid {COLORS['glass_border']}",
    'borderRadius': '12px',
    'padding': '20px',
    'boxShadow': f"0 8px 32px 0 rgba(0, 0, 0, 0.6), inset 0 1px 0 0 {COLORS['glass_highlight']}",
    'color': COLORS['text_primary'],
    'zIndex': 10,
    'fontFamily': "'Inter', 'Segoe UI', system-ui, sans-serif",
}

# ============================================================================
# FUI CORNER BRACKETS (Decorative elements)
# ============================================================================
BRACKET_STYLE = {
    'position': 'relative',
    '::before': {
        'content': '""',
        'position': 'absolute',
        'top': 0,
        'left': 0,
        'width': '15px',
        'height': '15px',
        'borderTop': f"2px solid {COLORS['cyan']}",
        'borderLeft': f"2px solid {COLORS['cyan']}",
    },
    '::after': {
        'content': '""',
        'position': 'absolute',
        'bottom': 0,
        'right': 0,
        'width': '15px',
        'height': '15px',
        'borderBottom': f"2px solid {COLORS['cyan']}",
        'borderRight': f"2px solid {COLORS['cyan']}",
    }
}

# ============================================================================
# BUTTON STYLES - FUI DESIGN
# ============================================================================
BUTTON_PRIMARY = {
    'width': '100%',
    'padding': '12px 20px',
    'backgroundColor': COLORS['cyan'],
    'color': COLORS['void_deep'],
    'border': 'none',
    'borderRadius': '6px',
    'cursor': 'pointer',
    'fontWeight': '600',
    'fontSize': '13px',
    'letterSpacing': '0.5px',
    'textTransform': 'uppercase',
    'fontFamily': "'Rajdhani', 'Inter', sans-serif",
    'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    'boxShadow': f"0 0 20px {COLORS['cyan_glow']}, 0 4px 12px rgba(0, 0, 0, 0.4)",
}

BUTTON_SECONDARY = {
    **BUTTON_PRIMARY,
    'backgroundColor': COLORS['amber'],
    'boxShadow': f"0 0 20px {COLORS['amber_glow']}, 0 4px 12px rgba(0, 0, 0, 0.4)",
}

BUTTON_DANGER = {
    **BUTTON_PRIMARY,
    'backgroundColor': COLORS['crimson'],
    'color': '#fff',
    'boxShadow': f"0 0 20px {COLORS['crimson_glow']}, 0 4px 12px rgba(0, 0, 0, 0.4)",
}

BUTTON_GHOST = {
    'backgroundColor': 'transparent',
    'color': COLORS['cyan'],
    'border': f"1px solid {COLORS['cyan']}",
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '18px',
    'width': '30px',
    'height': '30px',
    'padding': '0',
    'transition': 'all 0.2s ease',
    'fontWeight': 'bold',
    'fontFamily': 'monospace',
}

# ============================================================================
# INPUT FIELD STYLES - TERMINAL AESTHETIC
# ============================================================================
INPUT_FIELD = {
    'width': '100%',
    'padding': '10px 12px',
    'backgroundColor': 'rgba(11, 13, 23, 0.8)',
    'color': COLORS['text_mono'],
    'border': f"1px solid {COLORS['glass_border']}",
    'borderRadius': '6px',
    'fontSize': '13px',
    'fontFamily': "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
    'outline': 'none',
    'transition': 'all 0.2s ease',
}

# ============================================================================
# DROPDOWN STYLES
# ============================================================================
DROPDOWN_STYLE = {
    'backgroundColor': 'rgba(11, 13, 23, 0.9)',
    'border': f"1px solid {COLORS['glass_border']}",
    'borderRadius': '6px',
    'color': COLORS['text_primary'],
    'fontFamily': "'Inter', sans-serif",
    'fontSize': '13px',
}

# ============================================================================
# HEADER/SECTION TITLE STYLES - MISSION CONTROL TYPOGRAPHY
# ============================================================================
HEADER_STYLE = {
    'color': COLORS['cyan'],
    'fontWeight': '700',
    'fontSize': '16px',
    'letterSpacing': '2px',
    'textTransform': 'uppercase',
    'fontFamily': "'Rajdhani', 'Montserrat', sans-serif",
    'textShadow': f"0 0 10px {COLORS['cyan_glow']}",
}

SUBHEADER_STYLE = {
    'color': COLORS['text_secondary'],
    'fontSize': '11px',
    'letterSpacing': '1px',
    'textTransform': 'uppercase',
    'fontFamily': "'Inter', sans-serif",
    'marginBottom': '8px',
}

# ============================================================================
# DATA DISPLAY - MONOSPACED TECHNICAL TEXT
# ============================================================================
DATA_VALUE_STYLE = {
    'color': COLORS['text_mono'],
    'fontFamily': "'JetBrains Mono', 'Fira Code', monospace",
    'fontSize': '13px',
    'letterSpacing': '0.5px',
}

DATA_LABEL_STYLE = {
    'color': COLORS['text_dim'],
    'fontSize': '11px',
    'fontFamily': "'Inter', sans-serif",
}

# ============================================================================
# DIVIDER/SEPARATOR STYLES
# ============================================================================
DIVIDER_STYLE = {
    'borderColor': COLORS['glass_border'],
    'margin': '15px 0',
    'opacity': 0.6,
}

# ============================================================================
# PULSE ANIMATION KEYFRAMES (for satellite markers)
# ============================================================================
PULSE_ANIMATION = """
@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(0, 243, 255, 0.7);
    }
    50% {
        box-shadow: 0 0 0 10px rgba(0, 243, 255, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(0, 243, 255, 0);
    }
}
"""

# ============================================================================
# GLITCH EFFECT (for loading states)
# ============================================================================
GLITCH_ANIMATION = """
@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}
"""

# ============================================================================
# SCANNING ANIMATION (for radar/loading)
# ============================================================================
SCAN_ANIMATION = """
@keyframes scan {
    0% { transform: translateY(-100%); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(100%); opacity: 0; }
}
"""

# ============================================================================
# BACKGROUND GRADIENT - THE VOID
# ============================================================================
VOID_BACKGROUND = {
    'background': f"radial-gradient(ellipse at center, {COLORS['void_navy']} 0%, {COLORS['void_deep']} 100%)",
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'width': '100%',
    'height': '100%',
    'zIndex': -1,
}

# ============================================================================
# HOVER EFFECTS
# ============================================================================
HOVER_GLOW = {
    'transition': 'all 0.3s ease',
    ':hover': {
        'boxShadow': f"0 0 30px {COLORS['cyan_glow']}",
        'borderColor': COLORS['cyan'],
    }
}

# ============================================================================
# CHART/GRAPH STYLING
# ============================================================================
CHART_LAYOUT = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'family': "'JetBrains Mono', monospace",
        'color': COLORS['text_secondary'],
        'size': 11,
    },
    'margin': {'l': 40, 'r': 20, 't': 30, 'b': 40},
    'xaxis': {
        'gridcolor': COLORS['glass_border'],
        'zerolinecolor': COLORS['glass_border'],
        'showgrid': False,
    },
    'yaxis': {
        'gridcolor': COLORS['glass_border'],
        'zerolinecolor': COLORS['glass_border'],
        'showgrid': True,
        'gridwidth': 0.5,
    },
}

# ============================================================================
# EXPORT ALL
# ============================================================================
__all__ = [
    'COLORS',
    'GLASS',
    'BUTTON_PRIMARY',
    'BUTTON_SECONDARY',
    'BUTTON_DANGER',
    'BUTTON_GHOST',
    'INPUT_FIELD',
    'DROPDOWN_STYLE',
    'HEADER_STYLE',
    'SUBHEADER_STYLE',
    'DATA_VALUE_STYLE',
    'DATA_LABEL_STYLE',
    'DIVIDER_STYLE',
    'VOID_BACKGROUND',
    'CHART_LAYOUT',
]