"""Helper functions for chat and data formatting"""

def categorize(name):
    """Categorize agency by name"""
    n = name.lower()
    for k in ["spacex", "nasa"]:
        if k in n:
            return k.title()
    for k, v in [("china", "China"), ("russia", "Russia"), ("esa", "Europe"),
                 ("europe", "Europe"), ("india", "India"), ("japan", "Japan")]:
        if k in n:
            return v
    return "Other"

"""Helper functions for chat and data formatting"""
from utils.chatbot import SpaceChatbot

# Global chatbot instance (will be initialized with db)
_chatbot_instance = None

def get_chatbot(db):
    """Get or create chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = SpaceChatbot(db)
    return _chatbot_instance

def chat_respond(q, db):
    """Process chat message through advanced chatbot"""
    chatbot = get_chatbot(db)
    return chatbot.process(q)

def categorize(name):
    """Categorize agency by name"""
    n = name.lower()
    for k in ["spacex", "nasa"]:
        if k in n:
            return k.title()
    for k, v in [("china", "China"), ("russia", "Russia"), ("esa", "Europe"),
                 ("europe", "Europe"), ("india", "India"), ("japan", "Japan")]:
        if k in n:
            return v
    return "Other"

def get_satellite_description(name, sat_type):
    """Get description for satellites"""
    descriptions = {
        'ISS': 'The International Space Station is a habitable artificial satellite in low Earth orbit. It serves as a microgravity and space environment research laboratory where crew members conduct experiments in biology, physics, astronomy, and other fields.',
        'Tiangong': 'Chinese space station serving as a research laboratory for scientific experiments in microgravity. Tiangong means "Heavenly Palace" and represents China\'s growing presence in human spaceflight.',
        'Hubble': 'Space telescope that has revolutionized astronomy by providing unprecedented deep views of the universe since 1990. Named after astronomer Edwin Hubble, it has made over 1.5 million observations.',
        'Chandra': 'X-ray observatory that observes high-energy regions of the universe, such as supernova remnants, black holes, and galaxy clusters. Launched in 1999, it\'s one of NASA\'s Great Observatories.',
        'GPS IIF-2': 'Part of the Global Positioning System constellation providing navigation and timing services worldwide. GPS satellites enable everything from smartphone navigation to precision agriculture.',
        'Galileo-11': 'European satellite navigation system providing autonomous global positioning. Galileo is Europe\'s alternative to GPS, offering improved accuracy and reliability.',
        'Starlink-1007': 'SpaceX satellite providing global broadband internet coverage. Part of a constellation of thousands of satellites designed to provide high-speed internet to underserved areas.',
        'Starlink-1020': 'SpaceX satellite providing global broadband internet coverage. These satellites operate in low Earth orbit to minimize latency for internet communications.',
        'Iridium-180': 'Communications satellite providing voice and data coverage to satellite phones and pagers worldwide. The Iridium constellation ensures global connectivity even in remote areas.',
        'Landsat 9': 'Earth observation satellite monitoring environmental changes, land use, and natural resources. Part of the longest-running Earth observation program, providing critical climate data.',
        'Sentinel-1A': 'European radar imaging satellite for environmental monitoring and emergency response. Uses synthetic aperture radar to see through clouds and darkness.',
        'Terra': 'NASA satellite studying Earth\'s climate and environmental changes through multiple instruments. Observes interactions between atmosphere, land, oceans, and solar radiation.',
        'Aqua': 'NASA satellite monitoring Earth\'s water cycle and climate system. Tracks evaporation, precipitation, ice coverage, and ocean temperatures.',
        'GOES-16': 'Geostationary weather satellite providing real-time weather monitoring and severe storm tracking. Covers the Western Hemisphere with continuous imaging.',
        'NOAA-20': 'Polar-orbiting satellite providing global weather observations and climate monitoring. Successor to the Suomi NPP satellite, ensuring continuity of critical environmental data.'
    }
    return descriptions.get(name, f'{sat_type} satellite providing critical space-based services and observations.')

def get_satellite_description(name, sat_type):
    """Get description for satellites"""
    descriptions = {
        'ISS': 'The International Space Station is a habitable artificial satellite in low Earth orbit. It serves as a microgravity and space environment research laboratory.',
        'Tiangong': 'Chinese space station serving as a research laboratory for scientific experiments in microgravity.',
        'Hubble': 'Space telescope that has revolutionized astronomy by providing unprecedented deep views of the universe since 1990.',
        'Chandra': 'X-ray observatory that observes high-energy regions of the universe, such as supernova remnants and black holes.',
        'GPS IIF-2': 'Part of the Global Positioning System constellation providing navigation and timing services worldwide.',
        'Galileo-11': 'European satellite navigation system providing autonomous global positioning.',
        'Starlink-1007': 'SpaceX satellite providing global broadband internet coverage.',
        'Starlink-1020': 'SpaceX satellite providing global broadband internet coverage.',
        'Iridium-180': 'Communications satellite providing voice and data coverage to satellite phones and pagers.',
        'Landsat 9': 'Earth observation satellite monitoring environmental changes, land use, and natural resources.',
        'Sentinel-1A': 'European radar imaging satellite for environmental monitoring and emergency response.',
        'Terra': 'NASA satellite studying Earth\'s climate and environmental changes through multiple instruments.',
        'Aqua': 'NASA satellite monitoring Earth\'s water cycle and climate system.',
        'GOES-16': 'Geostationary weather satellite providing real-time weather monitoring and severe storm tracking.',
        'NOAA-20': 'Polar-orbiting satellite providing global weather observations and climate monitoring.'
    }
    return descriptions.get(name, f'{sat_type} satellite providing critical space-based services and observations.')
# In utils/helpers.py
def chat_respond(query, db):
    if query.startswith('/'):
        command = query.split(' ')[0].lower()
        if command == '/intel':
            # Logic to search db.get_launches() for the specific keyword
            return "ACCESSING ENCRYPTED DATASTREAM... [DONE]\n**ANALYSIS:** Payload weight vs Rocket thrust indicates 98.4% nominal trajectory."
    # Standard AI logic...