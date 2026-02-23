from datetime import datetime, timezone
from sgp4.api import Satrec
from sgp4.conveniences import jday
import math

def get_current_position(line1, line2):
    """Calculates Lat/Lon/Alt from TLE - OPTIMIZED"""
    try:
        satellite = Satrec.twoline2rv(line1, line2)
        now = datetime.now(timezone.utc)
        jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second)
        e, r, v = satellite.sgp4(jd, fr)
        
        if e != 0: 
            return None, None, None
        
        x, y, z = r
        r_mag = math.sqrt(x*x + y*y + z*z)
        
        # Fast math
        lat = math.degrees(math.asin(z / r_mag))
        
        t_diff = (now - datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)).total_seconds()
        gmst_deg = (280.46061837 + 360.98564736629 * (t_diff / 86400.0)) % 360
        ra = math.degrees(math.atan2(y, x))
        lon = (ra - gmst_deg) % 360
        
        if lon > 180: 
            lon -= 360
            
        alt = (r_mag - 6371) * 1000  # km to meters
        
        return lat, lon, alt
        
    except:
        return None, None, None

# Remove gen_deck_map - not needed anymore