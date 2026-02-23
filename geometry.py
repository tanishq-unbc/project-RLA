"""Geometric calculations for 3D visualization"""
import numpy as np
from config.settings import Config

def xyz(lat, lon, r):
    """Convert latitude/longitude to 3D Cartesian coordinates"""
    lat_r, lon_r = np.radians(lat), np.radians(lon)
    return (
        r * np.cos(lat_r) * np.cos(lon_r),
        r * np.cos(lat_r) * np.sin(lon_r),
        r * np.sin(lat_r)
    )

def orbit_h(orbit):
    """Calculate visual height based on orbit type"""
    heights = {
        'LEO': 500, 'MEO': 2000, 'GEO': 10000,
        'HEO': 8000, 'SSO': 700, 'GTO': 6000
    }
    return heights.get(orbit, 500) * Config.SCALE