import sqlite3
import pandas as pd
import os

class DB:
    """Database manager for both Launch data (SQLite) and Satellite data (CSV)"""
    
    def __init__(self, path="launches.db"):
        # 1. SETUP SQLITE (For Launches)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_sqlite()

        # 2. SETUP CSV (For Satellites)
        # We assume satellites.csv is in the same folder as this script, or one level up
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.csv_path = os.path.join(base_path, 'satellites.csv') 
        self.satellite_df = None
        self._load_csv_data()

    def _init_sqlite(self):
        """Initialize SQLite tables for launches"""
        self.conn.execute("""CREATE TABLE IF NOT EXISTS launches (
            id TEXT PRIMARY KEY, name TEXT, orbit TEXT, 
            agency_id INT, pad_id INT, date TEXT, status TEXT, rocket TEXT, 
            desc TEXT, img TEXT, vid TEXT, upcoming INT)""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS agencies (
            id INT PRIMARY KEY, name TEXT, type TEXT, country TEXT)""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS pads (
            id INT PRIMARY KEY, name TEXT, lat REAL, lon REAL, loc TEXT, cnt INT)""")
        self.conn.commit()

    def _load_csv_data(self):
        """Load Satellite CSV data into a Pandas DataFrame"""
        try:
            if os.path.exists(self.csv_path):
                self.satellite_df = pd.read_csv(self.csv_path)
            else:
                # If file missing, create empty structure to prevent crashes
                print(f"WARNING: Satellite CSV not found at {self.csv_path}")
                self.satellite_df = pd.DataFrame(columns=[
                    'Name of Satellite, Alternate Names', 'Owner', 
                    'Purpose', 'Class of Orbit', 'TLE_LINE1', 'TLE_LINE2'
                ])
        except Exception as e:
            print(f"Error loading satellite CSV: {e}")
            self.satellite_df = pd.DataFrame()

    # =========================================================================
    # SATELLITE METHODS (Used by 3D Map)
    # =========================================================================
    
    def get_data(self):
        """
        Returns the Satellite DataFrame.
        called by: visualization/map.py
        """
        if self.satellite_df is None or self.satellite_df.empty:
            self._load_csv_data()
        return self.satellite_df.copy()

    # =========================================================================
    # LAUNCH METHODS (Used by Launch Dashboard)
    # =========================================================================

    def insert(self, data, upcoming=False):
        """Insert launch data into database"""
        for l in data:
            try:
                a = l.get('launch_service_provider', {})
                p = l.get('pad', {})
                m = l.get('mission', {})
                r = l.get('rocket', {})
                
                self.conn.execute("INSERT OR IGNORE INTO agencies VALUES (?, ?, ?, ?)",
                    (a.get('id'), a.get('name', 'Unk'), a.get('type', 'Unk'), a.get('country_code', 'UN')))
                
                self.conn.execute("""INSERT OR REPLACE INTO pads VALUES (?, ?, ?, ?, ?, 
                    COALESCE((SELECT cnt FROM pads WHERE id = ?) + 1, 1))""",
                    (p.get('id'), p.get('name', 'Unk'), p.get('latitude', 0), p.get('longitude', 0),
                     p.get('location', {}).get('name', 'Unk'), p.get('id')))
                
                orbit = m.get('orbit', {}).get('abbrev', 'LEO') if m else 'LEO'
                
                self.conn.execute("""INSERT OR REPLACE INTO launches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (l.get('id'), l.get('name', 'Unk'), orbit, a.get('id'), p.get('id'), l.get('net', 'Unk'),
                     l.get('status', {}).get('name', 'Unk'), r.get('configuration', {}).get('name', 'Unk'),
                     m.get('description', 'No desc') if m else 'No desc', l.get('image', ''),
                     l.get('vidURLs', [{}])[0].get('url', '') if l.get('vidURLs') else '', 1 if upcoming else 0))
            except:
                pass
        self.conn.commit()
    
    def get_launches(self, search=None, orbit=None, upcoming=False):
        """Retrieve launches with optional filtering"""
        q = """SELECT l.id, l.name, a.name, p.name, l.orbit, p.lat, p.lon, l.date, l.status, l.rocket, l.desc, l.img, l.vid
            FROM launches l JOIN agencies a ON l.agency_id = a.id JOIN pads p ON l.pad_id = p.id WHERE 1=1"""
        params = []
        if upcoming:
            q += " AND l.upcoming = 1"
        if orbit and orbit != "All":
            q += " AND l.orbit = ?"
            params.append(orbit)
        if search:
            q += " AND (l.name LIKE ? OR l.rocket LIKE ? OR a.name LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s])
        return self.conn.execute(q, params).fetchall()
    
    def get_launch_by_id(self, lid):
        """Get specific launch details"""
        return self.conn.execute("""SELECT l.*, a.name, p.name, p.loc 
            FROM launches l JOIN agencies a ON l.agency_id = a.id
            JOIN pads p ON l.pad_id = p.id WHERE l.id = ?""", (lid,)).fetchone()
    
    def stats(self):
        """Get launch statistics"""
        try:
            total = self.conn.execute("SELECT COUNT(*) FROM launches WHERE upcoming = 0").fetchone()[0]
            upcoming = self.conn.execute("SELECT COUNT(*) FROM launches WHERE upcoming = 1").fetchone()[0]
            agencies = self.conn.execute("SELECT COUNT(DISTINCT agency_id) FROM launches").fetchone()[0]
            orbits = dict(self.conn.execute("SELECT orbit, COUNT(*) FROM launches WHERE upcoming = 0 GROUP BY orbit").fetchall())
            agency_stats = self.conn.execute("""SELECT a.name, COUNT(*) as t, 
                SUM(CASE WHEN l.status LIKE '%Success%' THEN 1 ELSE 0 END) as s
                FROM launches l JOIN agencies a ON l.agency_id = a.id WHERE l.upcoming = 0 
                GROUP BY a.name ORDER BY t DESC LIMIT 8""").fetchall()
            return {
                'total': total,
                'upcoming': upcoming,
                'agencies': agencies,
                'orbits': orbits,
                'agency_stats': agency_stats
            }
        except:
             return {'total': 0, 'upcoming': 0, 'agencies': 0, 'orbits': {}, 'agency_stats': []}
        

