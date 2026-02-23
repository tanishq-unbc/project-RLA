import plotly.graph_objects as go
import numpy as np
import requests
from dash import Input, Output, dcc, html
import random

# Core Geometry
R_EARTH = 6371
GEOJSON_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

SPACEPORTS = {
    "NASA": {"lat": 28.57, "lon": -80.64, "color": "#00f3ff", "pad": "Kennedy Space Center"},
    "SpaceX": {"lat": 25.99, "lon": -97.15, "color": "#00FF00", "pad": "Starbase TX"},
    "Russia": {"lat": 45.96, "lon": 63.30, "color": "#FF9900", "pad": "Baikonur"},
    "China": {"lat": 28.24, "lon": 102.02, "color": "#FFFF00", "pad": "Xichang"},
    "India": {"lat": 13.71, "lon": 80.23, "color": "#ff5500", "pad": "Sriharikota"},
    "Europe": {"lat": 5.23, "lon": -52.76, "color": "#ff00ff", "pad": "Kourou"},
    "Default": {"lat": 10.0, "lon": -20.0, "color": "#00f3ff", "pad": "Intl. Pad"}
}

def lat_lon_to_xyz(lat, lon, radius):
    phi = np.radians(90 - lat); theta = np.radians(lon)
    return (radius * np.sin(phi) * np.cos(theta), radius * np.sin(phi) * np.sin(theta), radius * np.cos(phi))

def register(app, db):
    @app.callback(
        Output("globe-viz", "children"),
        Input("refresh", "n_clicks"),
        Input("agency", "value"),
        Input("satellite-types", "value")
    )
    def update_big_label_globe(n, selected_agency, selected_types):
        df = db.get_data() #
        if df is None or df.empty: return []

        filtered_df = df.copy()
        
        # Filtering logic
        if selected_agency and selected_agency != "All":
            filtered_df = filtered_df[filtered_df['Owner'].astype(str).str.contains(selected_agency, case=False, na=False)]
        
        if selected_types:
            pattern = '|'.join(selected_types)
            filtered_df = filtered_df[filtered_df['Purpose'].str.contains(pattern, case=False, na=False)]

        fig = go.Figure()
        
        # --- ROBUST WIREFRAME ---
        try:
            geo = requests.get(GEOJSON_URL, timeout=5).json()
            gx, gy, gz = [], [], []
            for feat in geo['features']:
                poly_list = feat['geometry']['coordinates'] if feat['geometry']['type'] == 'Polygon' else [p[0] for p in feat['geometry']['coordinates']]
                for ring in poly_list:
                    lats, lons = np.array([p[1] for p in ring]), np.array([p[0] for p in ring])
                    tx, ty, tz = lat_lon_to_xyz(lats, lons, R_EARTH * 1.01)
                    gx.extend(tx); gx.append(None); gy.extend(ty); gy.append(None); gz.extend(tz); gz.append(None)
            fig.add_trace(go.Scatter3d(x=gx, y=gy, z=gz, mode='lines', line=dict(color='#00ffcc', width=1.5), hoverinfo='skip'))
        except: pass

        # --- 300 MISSION BEAMS ---
        port_keys = list(SPACEPORTS.keys())
        for i, (_, row) in enumerate(filtered_df.head(300).iterrows()):
            name = row.get("Name of Satellite, Alternate Names", "Asset")
            owner = str(row.get("Owner", "International")).upper()
            site_key = next((k for k in SPACEPORTS if k.upper() in owner), port_keys[i % (len(port_keys)-1)])
            site = SPACEPORTS[site_key]
            
            j_lat, j_lon = site["lat"] + (np.sin(i) * 3.8), site["lon"] + (np.cos(i) * 3.8)
            h = 45000 if "GEO" in str(row.get("Class of Orbit", "")).upper() else 15000 
            
            sx, sy, sz = lat_lon_to_xyz(j_lat, j_lon, R_EARTH)
            ex, ey, ez = lat_lon_to_xyz(j_lat, j_lon, R_EARTH + h)

            # --- BIG DATA TOOLTIP FIX ---
            # We use <br> for spacing and <b> for emphasis
            hover_intel = (
                f"<span style='font-size: 14px; color: #ffffff;'><b>MISSION:</b> {name}</span><br>"
                f"<span style='font-size: 12px; color: #00f3ff;'><b>AGENCY:</b> {owner}</span><br>"
                f"<span style='font-size: 12px; color: #00f3ff;'><b>PAD:</b> {site['pad']}</span>"
            )

            fig.add_trace(go.Scatter3d(
                x=[sx, ex], y=[sy, ey], z=[sz, ez], mode='lines+markers',
                marker=dict(size=[0, 8], color=['white', 'white']), 
                line=dict(color=site["color"], width=5), 
                name=hover_intel,
                hoverinfo='name',
                # This makes the box expand to fit the text
                hoverlabel=dict(
                    bgcolor="rgba(0,0,0,0.9)",
                    bordercolor="#00f3ff",
                    font=dict(size=13, color="#00f3ff", family="Consolas"),
                    namelength=-1 # Stretches the box to full text length
                ),
                showlegend=False
            ))

        fig.update_layout(
            template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0),
            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='black',
                       camera=dict(eye=dict(x=1.6, y=1.6, z=1.6)))
        )
        return dcc.Graph(figure=fig, style={"height": "100vh", "width": "100vw"}, config={'displayModeBar': False})