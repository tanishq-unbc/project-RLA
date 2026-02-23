"""API client for fetching launch and satellite data"""
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import lru_cache
from datetime import datetime, timedelta
from config.settings import Config
from skyfield.api import load, EarthSatellite
from skyfield.api import wgs84

logging.basicConfig(level=logging.WARNING)
# Suppress urllib3 connection warnings
logging.getLogger('urllib3').setLevel(logging.ERROR)

# Cache for satellite positions (stores for 10 minutes)
_satellite_cache = {'data': None, 'timestamp': None}
CACHE_DURATION = timedelta(minutes=10)

class API:
    """API client for external data sources"""
    
    @staticmethod
    def get_session():
        """Create requests session with retry logic"""
        s = requests.Session()
        retry = Retry(total=2, backoff_factor=0.3)  # Reduced retries
        s.mount("http://", HTTPAdapter(max_retries=retry))
        s.mount("https://", HTTPAdapter(max_retries=retry))
        return s
    
    @classmethod
    def fetch(cls, upcoming=False):
        """Fetch launch data from API"""
        try:
            url = Config.UPCOMING_API if upcoming else Config.API
            return cls.get_session().get(url, timeout=5).json().get('results', [])
        except:
            return []
    
    @classmethod
    @lru_cache(maxsize=1)
    def geo(cls):
        """Fetch and cache GeoJSON data"""
        try:
            return cls.get_session().get(Config.GEOJSON, timeout=3).json()
        except:
            return {'features': []}
    
    @classmethod
    def fetch_tle(cls, norad_id):
        """Fetch TLE data for a satellite from CelesTrak"""
        try:
            url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
            response = cls.get_session().get(url, timeout=2)  # Shorter timeout
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                if len(lines) >= 3:
                    return lines[0], lines[1], lines[2]
        except Exception as e:
            logging.debug(f"TLE fetch failed for {norad_id}: {e}")
        return None
    
    @classmethod
    def calculate_satellite_position(cls, name, sat_data):
        """Calculate current satellite position using TLE data"""
        try:
            # Try to fetch TLE
            tle_data = cls.fetch_tle(sat_data['norad'])
            
            if tle_data:
                # Use Skyfield to calculate position
                ts = load.timescale()
                satellite = EarthSatellite(tle_data[1], tle_data[2], tle_data[0], ts)
                
                # Get current time
                t = ts.now()
                
                # Calculate position
                geocentric = satellite.at(t)
                subpoint = wgs84.subpoint(geocentric)
                
                # Get latitude, longitude, altitude
                lat = subpoint.latitude.degrees
                lon = subpoint.longitude.degrees
                alt = subpoint.elevation.km
                
                logging.debug(f"✓ Live position for {name}")  # Changed to debug
                
                return {
                    'name': name,
                    'latitude': lat,
                    'longitude': lon,
                    'altitude': alt,
                    'inclination': sat_data['inc'],
                    'type': sat_data['type'],
                    'live': True
                }
        except Exception as e:
            logging.debug(f"Position calculation failed for {name}: {e}")
        
        # Fallback to static data
        return {
            'name': name,
            'latitude': sat_data.get('lat', 0),
            'longitude': sat_data.get('lon', 0),
            'altitude': sat_data['alt'],
            'inclination': sat_data['inc'],
            'type': sat_data['type'],
            'live': False
        }
    
    @classmethod
    def get_satellites(cls):
        """Get satellite data with live positions (CACHED for 10 minutes)"""
        global _satellite_cache
        
        # Check if cache is valid
        now = datetime.now()
        if (_satellite_cache['data'] is not None and 
            _satellite_cache['timestamp'] is not None and 
            now - _satellite_cache['timestamp'] < CACHE_DURATION):
            logging.debug(f"✓ Using cached satellite positions ({(now - _satellite_cache['timestamp']).seconds}s old)")  # Changed to debug
            return _satellite_cache['data']
        
        # Cache expired or empty, fetch new data
        logging.debug("🔄 Fetching fresh satellite positions...")  # Changed to debug
        satellites = []
        for name, data in Config.SATELLITES.items():
            sat_info = cls.calculate_satellite_position(name, data)
            satellites.append(sat_info)
        
        live_count = sum(1 for s in satellites if s.get('live', False))
        logging.debug(f"✓ Loaded {len(satellites)} satellites ({live_count} with live positions)")  # Changed to debug
        
        # Update cache
        _satellite_cache['data'] = satellites
        _satellite_cache['timestamp'] = now
        
        return satellites