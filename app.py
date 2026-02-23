# app.py
from dash import Dash
from ui.layout import create_layout
from data.database import DB
from callbacks import register_callbacks

external_scripts = [
    "https://unpkg.com/globe.gl@2.44.0/dist/globe.gl.min.js",
]


app = Dash(__name__, external_scripts=external_scripts, suppress_callback_exceptions=True)
server = app.server

db = DB()

# Load satellite df and compute orbits safely
df = db.get_data()
if df is not None and not df.empty:
    orbit_col = next((c for c in df.columns if "orb" in c.lower() or "class" in c.lower()), None)
    orbits = sorted(df[orbit_col].dropna().astype(str).unique().tolist()) if orbit_col else []
else:
    orbits = []

# Your DB class defines stats(), not get_stats()
stats = db.stats() if hasattr(db, "stats") else {"total": 0, "upcoming": 0, "agencies": 0}

app.layout = create_layout(db, stats, orbits)

register_callbacks(app, db, stats)

if __name__ == "__main__":
    app.run(debug=True)
