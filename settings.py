"""Configuration and constants for Astro Mission Control"""

class Config:
    """Application configuration"""
    LAUNCH_DB = ":memory:"
    API = "https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=100"
    UPCOMING_API = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=20"
    GEOJSON = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    R = 6371  # Earth radius in km
    SCALE = 4  # Visual scale for orbits
    
    # Major satellites with accurate orbital data
    # Major satellites with accurate orbital data
    SATELLITES = {
        # Space Stations
        'ISS': {'norad': 25544, 'alt': 420, 'inc': 51.6, 'type': 'Space Station', 'lat': 0, 'lon': 0},
        'Tiangong': {'norad': 48274, 'alt': 390, 'inc': 41.5, 'type': 'Space Station', 'lat': 30, 'lon': 110},
        # Telescopes
        'Hubble': {'norad': 20580, 'alt': 540, 'inc': 28.5, 'type': 'Telescope', 'lat': 20, 'lon': -80},
        'Chandra': {'norad': 25867, 'alt': 133000, 'inc': 64.0, 'type': 'Telescope', 'lat': 40, 'lon': 50},
        # Navigation
        'GPS IIF-2': {'norad': 37753, 'alt': 20200, 'inc': 55.0, 'type': 'Navigation', 'lat': 45, 'lon': 0},
        'Galileo-11': {'norad': 41174, 'alt': 23222, 'inc': 56.0, 'type': 'Navigation', 'lat': 50, 'lon': 30},
        # Communication
        'Starlink-1007': {'norad': 44713, 'alt': 550, 'inc': 53.0, 'type': 'Communication', 'lat': 53, 'lon': -120},
        'Starlink-1020': {'norad': 44714, 'alt': 550, 'inc': 53.0, 'type': 'Communication', 'lat': 53, 'lon': 120},
        'Iridium-180': {'norad': 43926, 'alt': 780, 'inc': 86.4, 'type': 'Communication', 'lat': 70, 'lon': 0},
        # Earth Observation
        'Landsat 9': {'norad': 49260, 'alt': 705, 'inc': 98.2, 'type': 'Earth Observation', 'lat': -30, 'lon': -100},
        'Sentinel-1A': {'norad': 39634, 'alt': 693, 'inc': 98.2, 'type': 'Earth Observation', 'lat': -40, 'lon': 10},
        'Terra': {'norad': 25994, 'alt': 705, 'inc': 98.2, 'type': 'Earth Observation', 'lat': -50, 'lon': 150},
        'Aqua': {'norad': 27424, 'alt': 705, 'inc': 98.2, 'type': 'Earth Observation', 'lat': -35, 'lon': -150},
        # Weather
        'GOES-16': {'norad': 41866, 'alt': 35786, 'inc': 0.1, 'type': 'Weather', 'lat': 0, 'lon': -75},
        'NOAA-20': {'norad': 43013, 'alt': 824, 'inc': 98.7, 'type': 'Weather', 'lat': 60, 'lon': -90},
    }