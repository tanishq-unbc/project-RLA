from dash import Input, Output, clientside_callback
from datetime import datetime, timedelta

from visualization.deck_map import get_current_position

_position_cache = {}
_cache_time = None
_cache_duration = timedelta(seconds=60)


def get_cached_positions(df):
    global _position_cache, _cache_time

    now = datetime.now()
    if _cache_time is None or (now - _cache_time) > _cache_duration:
        _position_cache = {}

        for _, row in df.iterrows():
            if "TLE_LINE1" in row and "TLE_LINE2" in row:
                sat_id = str(row.get("NORAD_CAT_ID", row.get("Name of Satellite, Alternate Names", "")))
                try:
                    lat, lon, alt_km = get_current_position(row["TLE_LINE1"], row["TLE_LINE2"])
                    if lat is not None and lon is not None and alt_km is not None:
                        _position_cache[sat_id] = {"lat": lat, "lon": lon, "alt_km": alt_km}
                except Exception:
                    continue

        _cache_time = now

    return _position_cache


def register(app, db):
    # Prevent double-registration (the same callback added twice still triggers the same error) [web:2]
    if getattr(app, "_satellite_store_registered", False):
        return
    app._satellite_store_registered = True

    @app.callback(
        Output("satellite-store", "data"),
        Input("refresh", "n_clicks"),
        Input("satellite-types", "value"),
        Input("agency", "value"),
        Input("orbit", "value"),
    )
    def update_satellite_positions(n_clicks, selected_types, selected_agency, selected_orbit):
        df = db.get_data()
        if df is None or df.empty or "TLE_LINE1" not in df.columns or "TLE_LINE2" not in df.columns:
            return []

        filtered_df = df.copy()

        owner_col = next((c for c in filtered_df.columns if ("own" in c.lower() or "oper" in c.lower())), None)
        if selected_agency and selected_agency != "All" and owner_col:
            filtered_df = filtered_df[
                filtered_df[owner_col].astype(str).str.contains(selected_agency, case=False, na=False)
            ]

        orbit_col = next((c for c in filtered_df.columns if ("orb" in c.lower() or "class" in c.lower())), None)
        if selected_orbit and selected_orbit != "All" and orbit_col:
            filtered_df = filtered_df[filtered_df[orbit_col] == selected_orbit]

        type_col = next((c for c in filtered_df.columns if ("purp" in c.lower() or "purpose" in c.lower())), None)
        if selected_types and type_col:
            if isinstance(selected_types, str):
                selected_types = [selected_types]
            filtered_df = filtered_df[filtered_df[type_col].isin(selected_types)]

        MAX_SATELLITES = 300
        if len(filtered_df) > MAX_SATELLITES:
            filtered_df = filtered_df.head(MAX_SATELLITES)

        position_cache = get_cached_positions(df)

        satellites = []
        for _, row in filtered_df.iterrows():
            sat_id = str(row.get("NORAD_CAT_ID", row.get("Name of Satellite, Alternate Names", "")))

            if sat_id in position_cache:
                lat = position_cache[sat_id]["lat"]
                lon = position_cache[sat_id]["lon"]
                alt_km = position_cache[sat_id]["alt_km"]
            else:
                try:
                    lat, lon, alt_km = get_current_position(row["TLE_LINE1"], row["TLE_LINE2"])
                except Exception:
                    continue

            if lat is None or lon is None or alt_km is None:
                continue

            viz_alt = max(0.02, min((float(alt_km) / 40000.0) * 2.0, 0.5))

            sat_type = row.get(type_col, row.get("Purpose", "Unknown")) if type_col else row.get("Purpose", "Unknown")
            owner_val = row.get(owner_col, row.get("Owner", "Unknown")) if owner_col else row.get("Owner", "Unknown")

            color = "#00f3ff"
            if isinstance(sat_type, str) and "Space Station" in sat_type:
                color = "#ffcc00"
            elif isinstance(sat_type, str) and "Telescope" in sat_type:
                color = "#ff2a6d"
            elif isinstance(sat_type, str) and "Communication" in sat_type:
                color = "#00ff88"
            elif isinstance(sat_type, str) and "Navigation" in sat_type:
                color = "#8800ff"

            satellites.append(
                {
                    "name": row.get("Name of Satellite, Alternate Names", "Unknown"),
                    "owner": owner_val,
                    "lat": float(lat),
                    "lng": float(lon),
                    "alt": float(viz_alt),
                    "type": sat_type if sat_type is not None else "Unknown",
                    "color": color,
                }
            )

        return satellites

    clientside_callback(
        """
        function(data) {
            if (window.dash_clientside && window.dash_clientside.clientside) {
                window.dash_clientside.clientside.render_globe(null, data || []);
            }
            return "";
        }
        """,
        Output("globe-render-signal", "children"),
        Input("chat-store", "data"),
    )

    @app.callback(Output("satellite-count", "children"), Input("chat-store", "data"))
    def update_count(data):
        if not data:
            return "[ SEARCHING... ]"
        return f"[ TRACKING {len(data)} ASSETS ]"
from dash import Input, Output, clientside_callback
from datetime import datetime, timedelta

from visualization.deck_map import get_current_position

_position_cache = {}
_cache_time = None
_cache_duration = timedelta(seconds=60)


def get_cached_positions(df):
    global _position_cache, _cache_time

    now = datetime.now()
    if _cache_time is None or (now - _cache_time) > _cache_duration:
        _position_cache = {}

        for _, row in df.iterrows():
            if "TLE_LINE1" in row and "TLE_LINE2" in row:
                sat_id = str(row.get("NORAD_CAT_ID", row.get("Name of Satellite, Alternate Names", "")))
                try:
                    lat, lon, alt_km = get_current_position(row["TLE_LINE1"], row["TLE_LINE2"])
                    if lat is not None and lon is not None and alt_km is not None:
                        _position_cache[sat_id] = {"lat": lat, "lon": lon, "alt_km": alt_km}
                except Exception:
                    continue

        _cache_time = now

    return _position_cache


def register(app, db):
    # Prevent double-registration (the same callback added twice still triggers the same error) [web:2]
    if getattr(app, "_satellite_store_registered", False):
        return
    app._satellite_store_registered = True

    @app.callback(
        Output("chat-store", "data"),
        Input("refresh", "n_clicks"),
        Input("satellite-types", "value"),
        Input("agency", "value"),
        Input("orbit", "value"),
    )
    def update_satellite_positions(n_clicks, selected_types, selected_agency, selected_orbit):
        df = db.get_data()
        if df is None or df.empty or "TLE_LINE1" not in df.columns or "TLE_LINE2" not in df.columns:
            return []

        filtered_df = df.copy()

        owner_col = next((c for c in filtered_df.columns if ("own" in c.lower() or "oper" in c.lower())), None)
        if selected_agency and selected_agency != "All" and owner_col:
            filtered_df = filtered_df[
                filtered_df[owner_col].astype(str).str.contains(selected_agency, case=False, na=False)
            ]

        orbit_col = next((c for c in filtered_df.columns if ("orb" in c.lower() or "class" in c.lower())), None)
        if selected_orbit and selected_orbit != "All" and orbit_col:
            filtered_df = filtered_df[filtered_df[orbit_col] == selected_orbit]

        type_col = next((c for c in filtered_df.columns if ("purp" in c.lower() or "purpose" in c.lower())), None)
        if selected_types and type_col:
            if isinstance(selected_types, str):
                selected_types = [selected_types]
            filtered_df = filtered_df[filtered_df[type_col].isin(selected_types)]

        MAX_SATELLITES = 300
        if len(filtered_df) > MAX_SATELLITES:
            filtered_df = filtered_df.head(MAX_SATELLITES)

        position_cache = get_cached_positions(df)

        satellites = []
        for _, row in filtered_df.iterrows():
            sat_id = str(row.get("NORAD_CAT_ID", row.get("Name of Satellite, Alternate Names", "")))

            if sat_id in position_cache:
                lat = position_cache[sat_id]["lat"]
                lon = position_cache[sat_id]["lon"]
                alt_km = position_cache[sat_id]["alt_km"]
            else:
                try:
                    lat, lon, alt_km = get_current_position(row["TLE_LINE1"], row["TLE_LINE2"])
                except Exception:
                    continue

            if lat is None or lon is None or alt_km is None:
                continue

            viz_alt = max(0.02, min((float(alt_km) / 40000.0) * 2.0, 0.5))

            sat_type = row.get(type_col, row.get("Purpose", "Unknown")) if type_col else row.get("Purpose", "Unknown")
            owner_val = row.get(owner_col, row.get("Owner", "Unknown")) if owner_col else row.get("Owner", "Unknown")

            color = "#00f3ff"
            if isinstance(sat_type, str) and "Space Station" in sat_type:
                color = "#ffcc00"
            elif isinstance(sat_type, str) and "Telescope" in sat_type:
                color = "#ff2a6d"
            elif isinstance(sat_type, str) and "Communication" in sat_type:
                color = "#00ff88"
            elif isinstance(sat_type, str) and "Navigation" in sat_type:
                color = "#8800ff"

            satellites.append(
                {
                    "name": row.get("Name of Satellite, Alternate Names", "Unknown"),
                    "owner": owner_val,
                    "lat": float(lat),
                    "lng": float(lon),
                    "alt": float(viz_alt),
                    "type": sat_type if sat_type is not None else "Unknown",
                    "color": color,
                }
            )

        return satellites

    clientside_callback(
        """
        function(data) {
            if (window.dash_clientside && window.dash_clientside.clientside) {
                window.dash_clientside.clientside.render_globe(null, data || []);
            }
            return "";
        }
        """,
        Output("globe-render-signal", "children"),
        Input("chat-store", "data"),
    )

    @app.callback(Output("satellite-count", "children"), Input("chat-store", "data"))
    def update_count(data):
        if not data:
            return "[ SEARCHING... ]"
        return f"[ TRACKING {len(data)} ASSETS ]"