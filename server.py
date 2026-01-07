"""
Oil & Gas Plant Safety Bot - Flask Backend API
Handles AI integration and API endpoints
"""

import os
import json
from datetime import datetime
from typing import Optional, Any
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Type hints for optional google generative AI
genai: Optional[Any] = None
model: Optional[Any] = None
HAS_GENAI: bool = False

# Try to import google generative AI, but provide fallback
try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception as e:
    print(f"Note: google.generativeai not available ({type(e).__name__})")
    print("Using demo mode with example responses")
    HAS_GENAI = False
    genai = None

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS manually
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Configure Gemini API
API_KEY = os.environ.get('GENAI_API_KEY')

if HAS_GENAI and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Warning: Could not configure genai: {e}")
        HAS_GENAI = False
elif not API_KEY:
    print("Note: GENAI_API_KEY not found in .env - using demo responses")

# System prompt for safety restrictions
SYSTEM_PROMPT = """
You are an Oil and Gas Plant Safety & Operations Explainer Bot.

Your role:
- Provide ONLY educational explanations of safety concepts, procedures, and guidelines.
- Explain safety zones, emergency procedures, PPE requirements, and safety symbols.
- Clarify operational best practices for training and compliance awareness.

STRICT RULES - You MUST NOT:
- Approve, authorize, or recommend specific operational actions.
- Assess, quantify, or approve hazard risks.
- Make decisions about safety compliance or regulatory adherence.
- Replace professional safety audits, certifications, or expert consultation.
- Provide real-time operational guidance.

Always include disclaimers and recommend professional consultation.
Keep responses concise, clear, and accessible for new employees and contractors.
"""

# Initialize Gemini model
if HAS_GENAI and genai:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
    except Exception as e:
        print(f"Warning: Could not initialize model: {e}")
        model = None
else:
    model = None

# Global chat session
chat_session = None

# Demo responses for oil and gas educational content
DEMO_RESPONSES = {
    "confined space": """Confined Space Safety refers to safety protocols for working in spaces that have limited entry/exit points.

Key Aspects:
- Identification: Tanks, vaults, trenches, vessels
- Requirements: Testing, permits, atmospheric monitoring
- Hazards: Oxygen depletion, toxic gases, engulfment
- Procedures: Pre-entry inspection, ventilation, rescue equipment
- Training: All personnel must be properly trained

[DISCLAIMER] Educational information only. Consult certified safety professionals and follow your organization's procedures.""",

    "ppe": """Personal Protective Equipment (PPE) protects workers from health and safety risks.

Common PPE Items:
- Head Protection: Hard hats, helmets
- Eye Protection: Safety glasses, goggles, face shields
- Respiratory Protection: Masks, respirators
- Hand Protection: Gloves for chemicals/puncture
- Foot Protection: Steel-toed boots
- Body Protection: High-visibility clothing, chemical suits

Proper fit, maintenance, and training are essential. This is educational information only.""",

    "safety zone": """Safety Zones are designated areas with specific safety classifications.

Zone Classification:
- Safe Area: Normal operations, minimal hazards
- Zone 0/1/2: Classified based on flammable atmosphere
- Hazard Areas: Equipment maintenance, chemical storage

Requirements:
- Clearly marked signs and barriers
- Restricted access with authorization
- Equipment must match zone classification
- Regular inspections and maintenance

Consult your facility safety manual for specific definitions.""",

    "emergency procedures": """Emergency procedures establish response protocols for incidents.

Key Components:
- Evacuation Routes: Marked exit paths and assembly points
- Communication: Alert systems, chain of command
- First Aid: Designated stations and trained personnel
- Shutdown Procedures: Safe equipment shutdown
- Incident Reporting: Documentation and investigation

Response Steps:
1. Alert and notify all personnel
2. Evacuate to assembly points
3. Account for all personnel
4. Initiate incident response teams
5. Prevent further hazards

Participate in regular emergency drills and training.""",

    "oil": """Oil (Petroleum) is a naturally occurring liquid hydrocarbon.

Composition:
- Hydrocarbons (hydrogen and carbon compounds)
- Ranges from light to heavy crude
- Contains various chemical compounds

Uses of Oil:
- Fuel: Gasoline, diesel, jet fuel, heating oil
- Energy: Primary energy source for power generation
- Chemicals: Feedstock for plastics, fertilizers, pharmaceuticals
- Lubricants: Industrial and automotive uses
- Bitumen: Roads and roofing

Global Usage:
- Transportation: ~25% of global consumption
- Industrial: ~30% for chemicals and manufacturing
- Power generation: ~10%
- Residential/Commercial: ~15% for heating
- Other: ~20% (plastics, textiles, medicines)

Key Statistics:
- Global daily consumption: ~100 million barrels per day
- Major producers: USA, Saudi Arabia, Russia, Iraq
- Major consumers: USA, China, India, Japan, Germany

Educational information about global oil usage.""",

    "gas": """Natural Gas (Methane) is a fossil fuel found in geological formations.

Characteristics:
- Colorless, odorless hydrocarbon gas
- Less carbon-intensive than oil or coal
- Cleaner burning energy source
- Used for heating and electricity generation

Uses:
- Power Generation: ~30% - electricity production
- Heating: ~25% - residential and commercial
- Industrial: ~30% - chemical manufacturing
- Transportation: ~5% - CNG vehicles
- Feedstock: ~10% - chemical and fertilizer production

Global Usage:
- Major producers: USA, Russia, Iran, Qatar, China
- Major consumers: USA, Russia, Japan, Germany, Canada
- Daily consumption: ~4 billion cubic meters annually

Advantages:
- Lower carbon emissions than coal or oil
- Abundant natural reserves
- Efficient for heating and cooking
- Reliable power generation

Educational information about natural gas usage.""",

    "energy": """Energy in oil and gas industry is conversion of hydrocarbons to power and heat.

Energy Sources:
- Crude Oil: Refined into gasoline, diesel, heating oil
- Natural Gas: Heating, power generation, feedstock
- Petroleum Products: Jet fuel, propane, butane, biofuels

Energy Production:
1. Exploration and drilling
2. Production and extraction
3. Transportation and storage
4. Refining and processing
5. Distribution to end users

Types of Energy:
- Thermal: Combustion for heat
- Electrical: Power plant generation
- Kinetic: Vehicle propulsion
- Chemical: Manufacturing feedstock

Global Energy Mix:
- Oil: ~30% of global primary energy
- Natural Gas: ~25%
- Renewables: ~15% and growing
- Coal: ~25%
- Nuclear: ~5%

Educational overview of energy from oil and gas.""",

    "production": """Oil and Gas Production is extraction and processing of hydrocarbons.

Production Phases:

1. Upstream (Exploration & Extraction)
   - Seismic surveys to locate reserves
   - Drilling wells
   - Pumping to surface
   - Initial separation and handling

2. Midstream (Transportation & Storage)
   - Pipeline transport
   - Storage facilities
   - Terminal operations
   - Custody transfer

3. Downstream (Refining & Distribution)
   - Crude oil refining
   - Product distribution
   - Retail sales
   - End consumer delivery

Production Methods:
- Conventional: Onshore and offshore drilling
- Unconventional: Shale oil, tar sands, tight gas
- Heavy Oil: Special extraction techniques
- Enhanced Recovery: Secondary/tertiary methods

Safety in Production:
- Blowout prevention
- Pressure management
- Environmental protection
- Worker safety protocols
- Emergency response systems

Educational information about production processes.""",

    "equipment": """Oil and Gas Equipment includes machinery used in extraction, processing, and transportation.

Well Equipment:
- Drilling rigs (offshore and onshore)
- Pump jacks and sucker rods
- Wellheads and Christmas trees
- Blowout preventers (BOPs)
- Casing and tubing

Processing Equipment:
- Separators (oil, gas, water separation)
- Compressors for gas
- Dehydrators for moisture removal
- Heaters and coolers
- Filtration systems

Transportation Equipment:
- Pipelines and pipe fittings
- Storage tanks
- Tanker trucks and rail cars
- Barges and ships
- Meters and gauges

Maintenance:
- Regular inspections required
- Preventive maintenance schedules
- Safety testing protocols
- Replacement of worn components
- Certification requirements

Educational overview of equipment types.""",

    "refining": """Oil Refining converts crude oil into usable petroleum products.

Refining Process:
1. Distillation: Separates crude by boiling point
2. Cracking: Breaks large molecules into smaller ones
3. Reforming: Rearranges molecular structure
4. Treating: Removes impurities and sulfur
5. Blending: Combines components for specifications

Main Products:
- Gasoline (petrol)
- Diesel fuel
- Jet fuel (kerosene)
- Heating oil
- Liquefied Petroleum Gas (LPG)
- Bitumen for roads
- Feedstock for chemicals

Refinery Operations:
- Crude oil storage tanks
- Furnaces and heaters
- Distillation columns
- Process control systems
- Safety and environmental controls

Yield and Efficiency:
- Typical barrel produces multiple products
- Light crude yields more gasoline
- Heavy crude requires more processing
- Optimization for market demand
- Energy efficiency improvements

Educational information about refining processes.""",

    "safety": """Oil and Gas Safety encompasses comprehensive protocols to protect workers, equipment, and environment.

Key Safety Areas:
- Personal Safety: PPE, training, certifications
- Process Safety: Equipment design, maintenance, procedures
- Emergency Response: Fire, explosion, spill management
- Environmental Protection: Containment, cleanup
- Health & Hygiene: Medical screening, sanitation

Regulatory Requirements:
- OSHA standards (Occupational Safety & Health)
- EPA regulations (Environmental)
- API standards (American Petroleum Institute)
- Industry best practices
- Local regulations

Safety Management Systems:
- Hazard identification and assessment
- Risk reduction measures
- Incident investigation
- Safety training and drills
- Continuous improvement programs

Critical Safety Topics:
- Confined space entry
- Hot work and fire prevention
- Electrical safety
- Pressure equipment safety
- Fall protection
- Chemical handling

Educational safety information. Follow your organization's procedures and consult certified professionals."""
}

def get_demo_response(query: str) -> str:
    """Get demo response based on query keywords"""
    query_lower = query.lower().strip()
    
    # Direct keyword matching
    for keyword, response in DEMO_RESPONSES.items():
        if keyword in query_lower:
            return response
    
    # Smart variations matching
    smart_matches = {
        "oil across": "oil",
        "global oil": "oil",
        "use of oil": "oil",
        "usage of oil": "oil",
        "natural gas": "gas",
        "methane": "gas",
        "lpg": "gas",
        "propane": "gas",
        "power generation": "energy",
        "electricity": "energy",
        "fuel": "energy",
        "drilling": "production",
        "well": "production",
        "extraction": "production",
        "rig": "equipment",
        "pump": "equipment",
        "compressor": "equipment",
        "tank": "equipment",
        "refine": "refining",
        "gasoline": "refining",
        "diesel": "refining",
        "crude": "refining"
    }
    
    for term, keyword in smart_matches.items():
        if term in query_lower:
            return DEMO_RESPONSES.get(keyword, get_default_response(query))
    
    return get_default_response(query)

def get_default_response(query: str) -> str:
    """Default response when no keywords match"""
    return f"""Thank you for asking: "{query}"

I can help with educational information about oil and gas. Topics I cover:

Energy & Resources:
- Oil: Uses, composition, production worldwide
- Natural Gas: Characteristics, applications, reserves
- Energy: Power generation, global mix, efficiency

Operations:
- Production: Extraction, transportation, refining
- Equipment: Wells, processing, safety systems
- Refining: Converting crude into products

Safety & Procedures:
- Safety: Protocols, regulations, risk management
- Emergency Procedures: Response, evacuation, reporting
- PPE: Personal protective equipment
- Confined Spaces: Hazards, entry, procedures
- Safety Zones: Classifications, access control

Try asking about:
- "What is oil used for globally?"
- "How is natural gas produced?"
- "What equipment is in oil wells?"
- "Explain oil refining"
- "What are safety hazards?"

[DISCLAIMER] This is educational information only. For operational, investment, or safety decisions, consult certified professionals. Follow your organization's procedures."""

def get_chat_session():
    """Get or create chat session"""
    global chat_session
    if chat_session is None and HAS_GENAI and model:
        try:
            chat_session = model.start_chat()
        except Exception as e:
            print(f"Warning: Could not create chat session: {e}")
            chat_session = None
    return chat_session

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'connected',
            'message': 'Safety Bot API is running',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat queries"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'status': 'error', 'message': 'Query is required'}), 400

        query = data.get('query', '').strip()
        if not query:
            return jsonify({'status': 'error', 'message': 'Query cannot be empty'}), 400

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Query: {query}")

        # Try AI first
        if HAS_GENAI and model:
            try:
                session = get_chat_session()
                if session:
                    response = session.send_message(query)
                    return jsonify({
                        'status': 'success',
                        'response': response.text,
                        'timestamp': datetime.now().isoformat(),
                        'mode': 'ai'
                    }), 200
            except Exception as e:
                print(f"AI Error: {e}, using demo")
        
        # Demo fallback
        demo_response = get_demo_response(query)
        return jsonify({
            'status': 'success',
            'response': demo_response,
            'timestamp': datetime.now().isoformat(),
            'mode': 'demo'
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 500

@app.route('/api/info', methods=['GET'])
def info():
    """Get bot information"""
    return jsonify({
        'name': 'Oil & Gas Plant Safety Bot',
        'version': '1.0.0',
        'description': 'Educational chatbot for oil & gas',
        'capabilities': [
            'Oil and gas education',
            'Safety procedures',
            'Equipment information',
            'Energy and refining',
            'Safety training'
        ],
        'limitations': [
            'Educational only',
            'Cannot approve operations',
            'Cannot assess risks',
            'Cannot replace professional audits'
        ]
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Serve index.html"""
    try:
        with open('index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except:
        return jsonify({'error': 'index.html not found'}), 404

@app.route('/style.css', methods=['GET'])
def serve_css():
    """Serve CSS"""
    try:
        with open('style.css', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/css'}
    except:
        return "Not found", 404

@app.route('/script.js', methods=['GET'])
def serve_js():
    """Serve JavaScript"""
    try:
        with open('script.js', 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/javascript'}
    except:
        return "Not found", 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'status': 'error', 'message': 'Server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Oil & Gas Plant Safety Bot - Backend Server")
    print("=" * 60)
    print(f"API Key: {bool(API_KEY)}")
    print(f"Mode: Demo with 11 comprehensive topics")
    print(f"URL: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
