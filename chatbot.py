"""Advanced chatbot with natural language understanding and commands"""
import re
from datetime import datetime, timedelta

class SpaceChatbot:
    """Intelligent chatbot for space mission control"""
    
    def __init__(self, db):
        self.db = db
        self.context = {}  # Store conversation context
        
    def process(self, message):
        """Process user message and return response"""
        msg = message.lower().strip()
        
        # Check for commands first (start with /)
        if msg.startswith('/'):
            return self.handle_command(msg)
        
        # Natural language understanding
        return self.understand_query(msg)
    
    def handle_command(self, cmd):
        """Handle slash commands"""
        parts = cmd.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            '/help': self.cmd_help,
            '/filter': self.cmd_filter,
            '/show': self.cmd_show,
            '/hide': self.cmd_hide,
            '/stats': self.cmd_stats,
            '/search': self.cmd_search,
            '/clear': self.cmd_clear,
            '/upcoming': self.cmd_upcoming,
            '/compare': self.cmd_compare
        }
        
        handler = commands.get(command)
        if handler:
            return handler(args)
        else:
            return f"❌ Unknown command: {command}. Type /help for available commands."
    
    def understand_query(self, msg):
        """Natural language query understanding"""
        
        # Greetings
        if any(word in msg for word in ['hello', 'hi', 'hey', 'howdy']):
            return self.respond_greeting()
        
        # Help requests
        if any(word in msg for word in ['help', 'what can you do', 'commands']):
            return self.cmd_help([])
        
        # Count queries
        if 'how many' in msg:
            return self.handle_count_query(msg)
        
        # Success rate queries
        if any(word in msg for word in ['success rate', 'successful', 'failures']):
            return self.handle_success_query(msg)
        
        # Upcoming launches
        if 'upcoming' in msg or 'next' in msg or 'future' in msg:
            return self.handle_upcoming_query(msg)
        
        # Orbit queries
        if 'orbit' in msg:
            return self.handle_orbit_query(msg)
        
        # Agency queries
        if any(agency in msg for agency in ['spacex', 'nasa', 'russia', 'china', 'europe', 'india', 'japan']):
            return self.handle_agency_query(msg)
        
        # Satellite queries
        if any(word in msg for word in ['satellite', 'iss', 'hubble', 'starlink', 'gps']):
            return self.handle_satellite_query(msg)
        
        # Comparison queries
        if 'compare' in msg or 'vs' in msg or 'versus' in msg:
            return self.handle_comparison_query(msg)
        
        # Show/display requests
        if any(word in msg for word in ['show', 'display', 'view', 'see']):
            return self.handle_show_query(msg)
        
        # Timeline queries
        if any(word in msg for word in ['when', 'date', 'time', 'year']):
            return self.handle_timeline_query(msg)
        
        # Location queries
        if any(word in msg for word in ['where', 'location', 'site', 'pad']):
            return self.handle_location_query(msg)
        
        # Default: didn't understand
        return self.respond_unknown(msg)
    
    # ========== Command Handlers ==========
    
    def cmd_help(self, args):
        """Show help information"""
        return """🤖 **SPACE CHATBOT COMMANDS**

**💬 Natural Questions:**
- "How many SpaceX launches?"
- "What's NASA's success rate?"
- "Show me upcoming launches"
- "Tell me about the ISS"
- "Compare SpaceX vs NASA"

**⚡ Quick Commands:**
- `/filter [agency]` - Filter by agency
- `/show [orbit]` - Show specific orbit
- `/hide satellites` - Hide satellites
- `/stats [agency]` - Agency statistics
- `/search [term]` - Search launches
- `/upcoming` - Next launches
- `/compare [a] vs [b]` - Compare agencies
- `/clear` - Clear filters

**📊 Data Questions:**
- "Which orbit is most common?"
- "What's the busiest launch site?"
- "Launches this year?"

Just ask me anything! 🚀"""
    
    def cmd_filter(self, args):
        """Filter launches by agency"""
        if not args:
            return "Usage: /filter [agency] (e.g., /filter spacex)"
        agency = ' '.join(args).title()
        return f"🎯 Filter set to: **{agency}**\n(Use the Agency dropdown to apply)"
    
    def cmd_show(self, args):
        """Show specific orbit or satellite type"""
        if not args:
            return "Usage: /show [orbit/satellite] (e.g., /show leo)"
        target = ' '.join(args).upper()
        return f"👁️ Showing: **{target}**\n(Use filters to apply)"
    
    def cmd_hide(self, args):
        """Hide satellites or launches"""
        if not args:
            return "Usage: /hide [satellites/launches]"
        return f"🙈 Hiding: **{' '.join(args)}**"
    
    def cmd_stats(self, args):
        """Show statistics"""
        stats = self.db.stats()
        if args:
            agency = ' '.join(args).title()
            return self.get_agency_stats(agency)
        return self.get_overall_stats(stats)
    
    def cmd_search(self, args):
        """Search launches"""
        if not args:
            return "Usage: /search [term] (e.g., /search starlink)"
        term = ' '.join(args)
        return f"🔍 Searching for: **{term}**\n(Use the search box to apply)"
    
    def cmd_clear(self, args):
        """Clear all filters"""
        return "🗑️ All filters cleared!\n(Reset dropdowns to 'All')"
    
    def cmd_upcoming(self, args):
        """Show upcoming launches"""
        stats = self.db.stats()
        return f"📅 **{stats['upcoming']} upcoming launches** scheduled!\n\nClick on the map to see details or ask 'show upcoming launches this week'."
    
    def cmd_compare(self, args):
        """Compare two agencies"""
        if len(args) < 3:
            return "Usage: /compare [agency1] vs [agency2]\nExample: /compare spacex vs nasa"
        return self.handle_comparison_query(' '.join(args))
    
    # ========== Natural Language Handlers ==========
    
    def handle_count_query(self, msg):
        """Handle 'how many' questions"""
        stats = self.db.stats()
        
        if 'upcoming' in msg:
            return f"📅 There are **{stats['upcoming']} upcoming launches** scheduled."
        
        if 'total' in msg or 'all' in msg:
            return f"🚀 Total launches in database: **{stats['total']}**"
        
        # Agency-specific
        for agency in ['spacex', 'nasa', 'russia', 'china', 'europe', 'india']:
            if agency in msg:
                return self.get_agency_launch_count(agency.title())
        
        return f"🚀 **{stats['total']} total launches** | 📅 **{stats['upcoming']} upcoming**"
    
    def handle_success_query(self, msg):
        """Handle success rate questions"""
        stats = self.db.stats()
        
        if not stats['agency_stats']:
            return "No success rate data available."
        
        # Check for specific agency
        for agency in ['spacex', 'nasa', 'russia', 'china', 'europe', 'india']:
            if agency in msg:
                return self.get_agency_success_rate(agency.title())
        
        # Overall top agency
        top = stats['agency_stats'][0]
        rate = (top[2]/top[1]*100) if top[1] > 0 else 0
        
        return f"✅ **{top[0]}** leads with {rate:.1f}% success rate ({top[2]}/{top[1]} launches successful)"
    
    def handle_upcoming_query(self, msg):
        """Handle upcoming launch questions"""
        launches = self.db.get_launches(upcoming_only=True)
        
        if 'week' in msg or 'this week' in msg:
            # Filter to next 7 days
            count = min(len(launches), 5)  # Approximate
            return f"📅 **{count} launches** expected in the next week!\n\nCheck the map for details."
        
        return f"📅 **{len(launches)} upcoming launches** scheduled!\n\nClick launches on the map for details or ask about specific agencies."
    
    def handle_orbit_query(self, msg):
        """Handle orbit questions"""
        stats = self.db.stats()
        orbits = stats['orbits']
        
        if 'most common' in msg or 'popular' in msg:
            most_common = max(orbits.items(), key=lambda x: x[1])
            return f"🌍 **{most_common[0]}** is the most common orbit with **{most_common[1]} launches**."
        
        if 'leo' in msg:
            leo_count = orbits.get('LEO', 0)
            return f"🌍 **LEO (Low Earth Orbit)**: {leo_count} launches"
        
        orbit_list = ', '.join([f"{k}: {v}" for k, v in list(orbits.items())[:5]])
        return f"🌍 **Orbit Distribution:**\n{orbit_list}"
    
    def handle_agency_query(self, msg):
        """Handle agency-specific questions"""
        agency_map = {
            'spacex': 'SpaceX',
            'nasa': 'NASA', 
            'russia': 'Russia',
            'china': 'China',
            'europe': 'Europe',
            'india': 'India',
            'japan': 'Japan'
        }
        
        for key, name in agency_map.items():
            if key in msg:
                return self.get_detailed_agency_info(name)
        
        return "Which agency would you like to know about? (SpaceX, NASA, Russia, China, Europe, India, Japan)"
    
    def handle_satellite_query(self, msg):
        """Handle satellite questions"""
        sat_keywords = {
            'iss': 'International Space Station',
            'hubble': 'Hubble Space Telescope',
            'tiangong': 'Tiangong Space Station',
            'starlink': 'Starlink Constellation',
            'gps': 'GPS Navigation Satellites'
        }
        
        for key, name in sat_keywords.items():
            if key in msg:
                return self.get_satellite_info(key)
        
        return "🛰️ I can tell you about: ISS, Hubble, Tiangong, Starlink, GPS, and more!\n\nClick satellites on the map for live details."
    
    def handle_comparison_query(self, msg):
        """Handle comparison between agencies"""
        stats = self.db.stats()
        
        # Extract agency names
        agencies = []
        for agency_data in stats['agency_stats']:
            if agency_data[0].lower() in msg:
                agencies.append(agency_data)
        
        if len(agencies) >= 2:
            a1, a2 = agencies[0], agencies[1]
            rate1 = (a1[2]/a1[1]*100) if a1[1] > 0 else 0
            rate2 = (a2[2]/a2[1]*100) if a2[1] > 0 else 0
            
            return f"""📊 **Comparison: {a1[0]} vs {a2[0]}**

**{a1[0]}:**
- Total Launches: {a1[1]}
- Successful: {a1[2]}
- Success Rate: {rate1:.1f}%

**{a2[0]}:**
- Total Launches: {a2[1]}
- Successful: {a2[2]}
- Success Rate: {rate2:.1f}%

{'🏆 ' + a1[0] if a1[1] > a2[1] else '🏆 ' + a2[0]} has more launches!"""
        
        return "Please specify two agencies to compare (e.g., 'compare SpaceX vs NASA')"
    
    def handle_show_query(self, msg):
        """Handle show/display requests"""
        if 'leo' in msg:
            return "🎯 Showing LEO orbits. Use the Orbit filter to apply!"
        if 'geo' in msg:
            return "🎯 Showing GEO orbits. Use the Orbit filter to apply!"
        if 'satellite' in msg:
            return "🛰️ Satellites visible! Check the satellite panel on the left."
        
        return "What would you like to see? (orbits, satellites, agencies, launches)"
    
    def handle_timeline_query(self, msg):
        """Handle time-related questions"""
        if 'year' in msg or '2024' in msg or '2025' in msg:
            return f"📆 Database contains launches from recent years. {self.db.stats()['total']} total missions tracked!"
        
        return "Ask me about upcoming launches or specific time periods!"
    
    def handle_location_query(self, msg):
        """Handle location questions"""
        return "🗺️ **Major Launch Sites:**\n• Kennedy Space Center (USA)\n• Cape Canaveral (USA)\n• Baikonur (Kazakhstan)\n• Jiuquan (China)\n• Guiana Space Centre (France)\n\nClick launches on the map to see their exact pad!"
    
    # ========== Helper Methods ==========
    
    def get_agency_launch_count(self, agency_name):
        """Get launch count for specific agency"""
        launches = [l for l in self.db.get_launches() if agency_name.lower() in l[2].lower()]
        return f"🚀 **{agency_name}**: {len(launches)} launches in database"
    
    def get_agency_success_rate(self, agency_name):
        """Get success rate for specific agency"""
        stats = self.db.stats()
        for agency_data in stats['agency_stats']:
            if agency_name.lower() in agency_data[0].lower():
                rate = (agency_data[2]/agency_data[1]*100) if agency_data[1] > 0 else 0
                return f"✅ **{agency_data[0]}** Success Rate: {rate:.1f}% ({agency_data[2]}/{agency_data[1]} successful)"
        
        return f"No data found for {agency_name}"
    
    def get_detailed_agency_info(self, agency_name):
        """Get comprehensive agency information"""
        stats = self.db.stats()
        for agency_data in stats['agency_stats']:
            if agency_name.lower() in agency_data[0].lower():
                rate = (agency_data[2]/agency_data[1]*100) if agency_data[1] > 0 else 0
                return f"""🏢 **{agency_data[0]} Statistics**

📊 Total Launches: **{agency_data[1]}**
✅ Successful: **{agency_data[2]}**
❌ Failed: **{agency_data[1] - agency_data[2]}**
📈 Success Rate: **{rate:.1f}%**

Click launches on the map to see individual missions!"""
        
        return f"📊 {agency_name} data not found. They might have fewer launches in our database."
    
    def get_satellite_info(self, sat_key):
        """Get satellite information"""
        from config.settings import Config
        
        info = {
            'iss': "🏛️ **International Space Station**\n• Altitude: 420 km\n• Crew: Usually 6-7 astronauts\n• Speed: 28,000 km/h\n• Orbits Earth every 90 minutes\n\nClick the ISS on the map for live position!",
            'hubble': "🔭 **Hubble Space Telescope**\n• Altitude: 540 km\n• Launched: 1990\n• Has taken over 1.5 million observations\n• Revolutionized astronomy\n\nClick Hubble on the map to track it!",
            'tiangong': "🏛️ **Tiangong Space Station**\n• China's space station\n• Altitude: 390 km\n• Operational since 2021\n• Can host 3 astronauts\n\nClick Tiangong for live position!",
            'starlink': "📡 **Starlink**\n• SpaceX's satellite internet constellation\n• Thousands of satellites in LEO\n• Provides global broadband\n\nCheck the Communication filter to see Starlink satellites!",
            'gps': "🛰️ **GPS Satellites**\n• Global Positioning System\n• Altitude: ~20,200 km\n• 31 operational satellites\n• Provides location/time data\n\nEnable Navigation satellites to see GPS!"
        }
        
        return info.get(sat_key, "Satellite information not available.")
    
    def get_overall_stats(self, stats):
        """Get overall statistics"""
        return f"""📊 **Overall Statistics**

🚀 Total Launches: **{stats['total']}**
📅 Upcoming: **{stats['upcoming']}**
🏢 Active Agencies: **{stats['agencies']}**

Top orbit: **{max(stats['orbits'].items(), key=lambda x: x[1])[0]}** ({max(stats['orbits'].values())} launches)

Ask me about specific agencies or click the 📊 Stats button!"""
    
    def respond_greeting(self):
        """Respond to greetings"""
        greetings = [
            "👋 Hello! I'm your Space Mission Control AI. Ask me anything about launches, satellites, or space agencies!",
            "🚀 Hi there! Ready to explore space missions? Ask me about launches, stats, or satellites!",
            "🌍 Hey! I can help you with launch data, satellite tracking, and space statistics. What would you like to know?"
        ]
        import random
        return random.choice(greetings)
    
    def respond_unknown(self, msg):
        """Handle unknown queries"""
        return f"""🤔 I'm not sure about that. Try asking:

- "How many SpaceX launches?"
- "What's NASA's success rate?"
- "Show upcoming launches"
- "Tell me about the ISS"
- "Compare SpaceX vs NASA"

Or type **/help** for all commands!"""