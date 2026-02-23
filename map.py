import plotly.graph_objects as go
import pandas as pd
import math
from datetime import datetime, timezone
from sgp4.api import Satrec, WGS72
from sgp4.conveniences import jday

def get_current_position(line1, line2, time_offset_min=0):
    """
    Calculates Lat/Lon from TLE. 
    Added 'time_offset_min' to project future positions for launch lines.
    """
    try:
        satellite = Satrec.twoline2rv(line1, line2)
        # Apply the time offset for trajectory projection
        now = datetime.now(timezone.utc) + pd.Timedelta(minutes=time_offset_min)
        jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second)
        
        e, r, v = satellite.sgp4(jd, fr)
        if e != 0: return None, None 

        x, y, z = r
        r_mag = math.sqrt(x**2 + y**2 + z**2)
        
        lat = math.degrees(math.asin(z / r_mag))
        
        t_diff = (now - datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)).total_seconds()
        gmst_deg = (280.46061837 + 360.98564736629 * (t_diff / 86400.0)) % 360
        ra = math.degrees(math.atan2(y, x))
        lon = (ra - gmst_deg) % 360
        if lon > 180: lon -= 360
        
        return lat, lon
    except Exception:
        return None, None

def gen_map(db, selected_agency='All', selected_orbit='All', search_query='', selected_types=None):
    """3D Satellite Map with TLE Propagation and Launch Lines."""
    geo_layout = dict(
    projection_type='orthographic',
    showland=True,
    landcolor='#090909',        # Near-black land
    showocean=True,
    oceancolor='#000000',       # Pure black ocean
    showcountries=True,
    countrycolor='#1e293b',     # Dark blue-gray borders
    showcoastlines=True,
    coastlinecolor='#00f3ff',   # Neon cyan glow at edges
    coastlinewidth=0.5,
    bgcolor='#000000',          # Space background
    showlakes=False,            # Hide lakes to reduce clutter
    projection_scale=1.1        # Slightly zoom for focus
)

    try:
        df = db.get_data()
        if df is None or df.empty:
            return go.Figure().update_layout(geo=geo_layout, paper_bgcolor='#000000')

        # 1. Calculate Current Positions
        lats, lons = [], []
        if 'TLE_LINE1' in df.columns and 'TLE_LINE2' in df.columns:
            for index, row in df.iterrows():
                lat, lon = get_current_position(row['TLE_LINE1'], row['TLE_LINE2'])
                lats.append(lat)
                lons.append(lon)
            
            df['calc_lat'] = lats
            df['calc_lon'] = lons
            df = df.dropna(subset=['calc_lat', 'calc_lon'])
        else:
            return go.Figure().update_layout(geo=geo_layout, paper_bgcolor='#000000')

        # [Filtering logic remains the same...]
        # (Assuming your filters for agency, orbit, etc., stay here)
        name_col = next((c for c in df.columns if 'name' in c.lower()), df.columns[0])

        # 2. Initialize Figure
        fig = go.Figure()

        # 3. ADD LAUNCH LINES (Ground Tracks)
        # We'll plot paths for the first 15 satellites to maintain performance
        for index, row in df.head(3).iterrows():
            path_lats, path_lons = [], []
            # Calculate 20 points for the next 90 minutes
            for minutes in range(0, 91, 5): 
                p_lat, p_lon = get_current_position(row['TLE_LINE1'], row['TLE_LINE2'], time_offset_min=minutes)
                if p_lat is not None:
                    path_lats.append(p_lat)
                    path_lons.append(p_lon)
            
            # Add the line trace
            fig.add_trace(go.Scattergeo(
                lon=path_lons,
                lat=path_lats,
                mode='lines',
                line=dict(width=1.5, color='#00f3ff'),
                opacity=0.3, # Faded "vector" look
                hoverinfo='none'
            ))

        # 4. ADD SATELLITE MARKERS (The glowing nodes)
# Inside gen_map, find the name column dynamically


# ADD SATELLITE MARKERS
            fig.add_trace(go.Scattergeo(
                lon = df['calc_lon'],
                lat = df['calc_lat'],
                hovertext = df[name_col], # This ensures the name pops up
            hoverinfo = 'text',       # Tells Plotly to only show the text we provided
            mode = 'markers',
            marker = dict(
                size = 8,
                color = '#00f3ff', 
                symbol = 'circle',
                line = dict(width=1, color='white')
                )
            ))

        fig.update_layout(
            geo=geo_layout,
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        return fig

    except Exception as e:
        print(f"CRITICAL ERROR in gen_map: {e}")
        return go.Figure().update_layout(geo=geo_layout, paper_bgcolor='#000000')