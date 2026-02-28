"""
AI Recommendation Engine – Rule-Based + Weighted Scoring
Generates personalised interior design recommendations based on user inputs.
"""

import random

# ── Design Knowledge Base ──────────────────────────────────────────────────────

COLOR_PALETTES = {
    "Warm Neutrals": {
        "primary": "#C4A882", "secondary": "#8B6F47", "accent": "#E8DCC8",
        "wall": "#F5ECD7", "description": "Warm beige and tan tones create a cosy, inviting atmosphere."
    },
    "Cool Blues": {
        "primary": "#4A90D9", "secondary": "#2C5F8A", "accent": "#B8D4F0",
        "wall": "#E8F1FA", "description": "Calming blue palette inspired by ocean and sky, perfect for relaxation."
    },
    "Earthy Greens": {
        "primary": "#5A8A5E", "secondary": "#2D5C30", "accent": "#A8C8A8",
        "wall": "#E8F2E8", "description": "Nature-inspired greens bring freshness and harmony indoors."
    },
    "Monochrome Elegance": {
        "primary": "#2C2C2C", "secondary": "#5A5A5A", "accent": "#C0C0C0",
        "wall": "#F5F5F5", "description": "Timeless black and white with grey accents for a sophisticated look."
    },
    "Vibrant Bold": {
        "primary": "#E84393", "secondary": "#FF6B35", "accent": "#FFD700",
        "wall": "#FFF8E7", "description": "Bold, energetic colours for a lively and expressive space."
    },
    "Pastel Dream": {
        "primary": "#FFB3C6", "secondary": "#B3D9FF", "accent": "#B3FFD9",
        "wall": "#FFF0F5", "description": "Soft pastels create a dreamy, gentle, and airy environment."
    },
    "Dark Luxury": {
        "primary": "#1A1A2E", "secondary": "#16213E", "accent": "#C9A84C",
        "wall": "#0F3460", "description": "Deep jewel tones with gold accents for opulent, dramatic interiors."
    },
    "Terracotta Warmth": {
        "primary": "#C1440E", "secondary": "#8B3A0F", "accent": "#F4A460",
        "wall": "#FFF0E6", "description": "Earthy terracotta hues for a Mediterranean, sun-kissed ambiance."
    },
}

FURNITURE_RECOMMENDATIONS = {
    "Modern": {
        "Living Room": ["Sectional sofa with clean lines", "Glass coffee table", "LED floor lamp", "Minimalist TV unit", "Abstract wall art"],
        "Bedroom": ["Platform bed with upholstered headboard", "Floating nightstands", "Built-in wardrobe", "Pendant bedside lights", "Geometric rug"],
        "Kitchen": ["Handle-less cabinets", "Quartz countertops", "Island with bar stools", "Integrated appliances", "Pendant lights over island"],
        "Bathroom": ["Wall-mounted vanity", "Frameless glass shower", "Freestanding bathtub", "Backlit mirror", "Floating shelves"],
        "Office": ["Ergonomic desk", "Gaming/office chair", "Monitor arm", "Cable management system", "Acoustic panels"],
        "Dining Room": ["Extendable dining table", "Upholstered chairs", "Buffet sideboard", "Chandelier", "Abstract centerpiece"],
    },
    "Classic": {
        "Living Room": ["Chesterfield sofa", "Wooden coffee table", "Crystal chandelier", "Bookshelf with display", "Persian rug"],
        "Bedroom": ["Four-poster bed", "Antique dresser", "Armoire wardrobe", "Bedside lamps with shades", "Floral or damask rug"],
        "Kitchen": ["Shaker-style cabinets", "Marble countertops", "Butler's pantry", "Farmhouse sink", "Brass fixtures"],
        "Bathroom": ["Clawfoot bathtub", "Pedestal sink", "Wainscoting walls", "Ornate mirror", "Towel rail"],
        "Office": ["Roll-top desk", "Leather executive chair", "Bookcase with ladder", "Brass desk lamp", "Globe"],
        "Dining Room": ["Pedestal dining table", "Wingback chairs", "China cabinet", "Wainscoting", "Candelabra"],
    },
    "Minimalist": {
        "Living Room": ["Low-profile sofa", "Slim coffee table", "Single floor lamp", "Floating media console", "One statement artwork"],
        "Bedroom": ["Simple platform bed", "One small nightstand", "Sliding wardrobe", "Blackout curtains", "Neutral area rug"],
        "Kitchen": ["Flat-panel cabinets", "Concrete countertops", "Hidden storage", "Under-cabinet lighting", "Clean open shelves"],
        "Bathroom": ["Wall-hung toilet", "Vessel sink", "Walk-in shower", "Minimal accessories", "Frameless mirror"],
        "Office": ["Simple desk", "Task chair", "Hidden storage ottoman", "Minimal decor", "Smart desk lamp"],
        "Dining Room": ["Simple rectangular table", "Bentwood chairs", "Pendant light", "Single plant", "Bare table"],
    },
    "Rustic": {
        "Living Room": ["Reclaimed wood sofa table", "Leather couch", "Stone fireplace", "Woven baskets", "Antler chandelier"],
        "Bedroom": ["Log bed frame", "Distressed wood dresser", "Vintage quilt", "Mason jar lights", "Braided rug"],
        "Kitchen": ["Open wooden shelves", "Butcher block counters", "Farmhouse sink", "Vintage stove", "Herb garden window"],
        "Bathroom": ["Wooden vanity", "Stone vessel sink", "Rainfall shower", "Rope accents", "Vintage mirror"],
        "Office": ["Reclaimed wood desk", "Leather chair", "Industrial shelving", "Vintage map art", "Edison bulb lamp"],
        "Dining Room": ["Trestle dining table", "Bench seating", "Mason jar chandelier", "Galvanized metal accents", "Wildflower centerpiece"],
    },
    "Bohemian": {
        "Living Room": ["Macramé wall hanging", "Floor cushions", "Rattan chairs", "Layered colourful rugs", "Plants everywhere"],
        "Bedroom": ["Canopy bed with sheer drapes", "Vintage dresser", "Tapestry wall art", "Mix of pillows", "Jute rug"],
        "Kitchen": ["Open shelves with eclectic items", "Colourful tiles", "Hanging plants", "Vintage accessories", "Woven placemats"],
        "Bathroom": ["Moroccan tiles", "Vintage mirror", "Rattan storage", "Hanging plants", "Colourful towels"],
        "Office": ["Vintage desk", "Colourful chair", "Gallery wall", "Trailing plants", "Eclectic accessories"],
        "Dining Room": ["Mismatched chairs", "Colourful tablecloth", "Eclectic centrepiece", "Lantern chandelier", "Tribal rug"],
    },
    "Industrial": {
        "Living Room": ["Metal and wood sofa", "Steel coffee table", "Edison bulb lights", "Exposed brick wall", "Metal shelving"],
        "Bedroom": ["Metal bed frame", "Reclaimed wood dresser", "Concrete lamp", "Exposed pipes", "Vintage locker"],
        "Kitchen": ["Stainless steel appliances", "Butcher block", "Metal bar stools", "Open shelves", "Edison pendant lights"],
        "Bathroom": ["Concrete sink", "Black fixtures", "Walk-in shower", "Industrial mirror", "Metal towel hooks"],
        "Office": ["Steel desk", "Industrial chair", "Metal shelving", "Factory window art", "Concrete accessories"],
        "Dining Room": ["Metal dining table", "Industrial chairs", "Pendant cage lights", "Exposed brick", "Metal wine rack"],
    },
    "Scandinavian": {
        "Living Room": ["Light wood sofa table", "White couch", "Sheepskin throws", "Geometric rug", "Simple potted plants"],
        "Bedroom": ["White bed frame", "Light wood dresser", "Simple curtains", "Hygge accessories", "Wool blanket"],
        "Kitchen": ["White cabinets", "Light wood countertops", "Simple hardware", "Open shelves", "Potted herbs"],
        "Bathroom": ["White tiles", "Wood accents", "Simple mirror", "Linen towels", "Minimal accessories"],
        "Office": ["White desk", "Ergonomic chair", "Simple shelves", "Few plants", "Clean desk lamp"],
        "Dining Room": ["Light wood table", "Tulip chairs", "Simple pendant", "Candles", "Linen runner"],
    },
}

LAYOUT_TIPS = {
    "Living Room": [
        "🛋️ Anchor the seating area with a large area rug to define the zone.",
        "💡 Layer lighting: overhead, floor lamps, and table lamps for ambiance.",
        "🪴 Place plants in corners to fill dead space and add life.",
        "📐 Leave 45–50 cm walkways between furniture for easy movement.",
        "🎨 Create a focal point (fireplace, TV unit, or statement wall).",
        "🪞 Use mirrors to visually expand a small room and reflect light.",
    ],
    "Bedroom": [
        "🛏️ Center the bed on the main wall for balanced feng shui.",
        "💡 Use bedside lamps instead of ceiling-only lighting for warmth.",
        "🚪 Ensure 75 cm clearance on each side of the bed.",
        "🪟 Position the bed away from drafty windows for comfort.",
        "🪴 Calming plants like lavender or peace lily improve sleep quality.",
        "📦 Use under-bed storage to maximise space in small rooms.",
    ],
    "Kitchen": [
        "🔺 Follow the work triangle: sink → stove → refrigerator for efficiency.",
        "💡 Install task lighting under cabinets for prep areas.",
        "🗄️ Keep frequently used items at arm level for easy access.",
        "🪴 A small herb garden on the windowsill adds freshness and function.",
        "🎨 Use a contrasting backsplash as a visual feature wall.",
        "📐 Leave 120 cm minimum between parallel counters for movement.",
    ],
    "Bathroom": [
        "💡 Install vanity lighting at eye level to eliminate shadows.",
        "🪞 Large mirrors make a small bathroom feel more spacious.",
        "🌿 Humidity-loving plants like ferns add spa vibes.",
        "🛁 Place towel rails within reach of the shower and bath.",
        "📐 Ensure 75 cm clearance in front of toilet and vanity.",
        "🎨 Use large-format tiles to reduce grout lines and add spaciousness.",
    ],
    "Office": [
        "💻 Position the desk facing the door but not directly in line with it.",
        "💡 Use natural light from the side to reduce screen glare.",
        "🪴 Plants boost productivity — try a snake plant or pothos.",
        "📚 Organise cables and wires to maintain a clear headspace.",
        "🎨 Choose calm, focus-boosting colours like green, blue, or grey.",
        "🔊 Add acoustic panels or bookshelves on walls to reduce echo.",
    ],
    "Dining Room": [
        "🍽️ Hang the chandelier 75–90 cm above the dining table surface.",
        "📐 Choose a rug that extends 60 cm beyond all sides of the table.",
        "💡 Dimmers allow you to shift from bright dining to romantic ambiance.",
        "🪴 A centrepiece plant or floral arrangement adds elegance.",
        "🪞 A buffet or sideboard provides storage and display space.",
        "🎨 Bold wallpaper or a statement wall creates drama in dining rooms.",
    ],
}

BUDGET_ADVICE = {
    "Under ₹50,000 / $600": {
        "label": "Budget-Friendly",
        "tips": ["Focus on paint and soft furnishings for maximum impact.", "Shop second-hand or thrift stores for unique pieces.", "DIY art and decor can personalise without big spend.", "Invest in 1–2 quality statement pieces, keep the rest minimal."],
        "allocation": {"Furniture": 40, "Paint & Walls": 20, "Lighting": 15, "Decor & Accessories": 15, "Plants": 10},
    },
    "₹50,000–₹1,50,000 / $600–$1,800": {
        "label": "Mid-Range",
        "tips": ["Mix mid-range and budget pieces strategically.", "Invest in the sofa and bed — you use them most.", "Consider flat-pack furniture with quality styling.", "Add personality through curated art and plants."],
        "allocation": {"Furniture": 45, "Paint & Walls": 15, "Lighting": 15, "Decor & Accessories": 15, "Plants & Greenery": 10},
    },
    "₹1,50,000–₹5,00,000 / $1,800–$6,000": {
        "label": "Premium",
        "tips": ["Prioritise quality materials that last — solid wood, real leather.", "Consider professional consultation for layout planning.", "Custom joinery adds value and perfect fit.", "Invest in smart home features like automated lighting."],
        "allocation": {"Furniture": 40, "Joinery & Built-ins": 20, "Lighting": 15, "Decor & Art": 15, "Plants & Styling": 10},
    },
    "Above ₹5,00,000 / $6,000+": {
        "label": "Luxury",
        "tips": ["Engage a full-service interior designer.", "Consider bespoke furniture and custom art commissions.", "Premium materials: marble, solid hardwood, designer lighting.", "Smart home automation is a worthwhile investment at this level."],
        "allocation": {"Custom Furniture": 35, "Built-ins & Joinery": 25, "Lighting & Smart Home": 20, "Art & Accessories": 15, "Plants & Styling": 5},
    },
}

STYLE_DESCRIPTIONS = {
    "Modern": "Clean lines, open spaces, and a 'less is more' philosophy define modern design. Neutral palettes with bold accents, innovative materials like glass and steel.",
    "Classic": "Timeless elegance with ornate details, rich woods, and traditional patterns. Symmetry, craftsmanship, and a sense of permanence.",
    "Minimalist": "Radical simplicity — only what is essential remains. Calm, uncluttered spaces that promote peace of mind and intentional living.",
    "Rustic": "Warmth and authenticity through natural materials like wood, stone, and leather. Imperfect beauty that celebrates nature's textures.",
    "Bohemian": "Fearless layering of colours, patterns, and global influences. A traveller's collection brought to life with plants, textiles, and art.",
    "Industrial": "Inspired by factories and urban lofts — exposed brick, metal, and raw materials combined with comfort and sophistication.",
    "Scandinavian": "Hygge philosophy: functional, beautiful, and cosy. Light woods, whites, and textures that celebrate simplicity and comfort.",
}

def generate_recommendations(room_type, room_size, budget, color_theme, furniture_style, lifestyle, special_notes):
    """Generate AI-powered design recommendations."""
    
    # Map color theme to palette
    palette_map = {
        "Warm & Cosy": "Warm Neutrals",
        "Cool & Calm": "Cool Blues",
        "Nature Inspired": "Earthy Greens",
        "Bold & Vibrant": "Vibrant Bold",
        "Neutral & Elegant": "Monochrome Elegance",
        "Soft Pastels": "Pastel Dream",
        "Dark & Luxurious": "Dark Luxury",
        "Mediterranean": "Terracotta Warmth",
    }
    palette_key = palette_map.get(color_theme, "Warm Neutrals")
    palette = COLOR_PALETTES[palette_key]

    # Get furniture recommendations
    style_key = furniture_style if furniture_style in FURNITURE_RECOMMENDATIONS else "Modern"
    room_key = room_type if room_type in FURNITURE_RECOMMENDATIONS.get(style_key, {}) else "Living Room"
    furniture = FURNITURE_RECOMMENDATIONS.get(style_key, {}).get(room_key, [])

    # Get layout tips
    layout = LAYOUT_TIPS.get(room_type, LAYOUT_TIPS["Living Room"])

    # Get budget advice
    budget_info = BUDGET_ADVICE.get(budget, list(BUDGET_ADVICE.values())[1])

    # Generate AI design score
    compatibility_score = calculate_compatibility(room_type, furniture_style, color_theme, lifestyle)

    # Build design concepts
    concepts = build_design_concepts(room_type, style_key, palette_key, room_size)

    return {
        "palette": palette,
        "palette_name": palette_key,
        "furniture": furniture,
        "layout_tips": random.sample(layout, min(4, len(layout))),
        "budget_info": budget_info,
        "style_description": STYLE_DESCRIPTIONS.get(furniture_style, ""),
        "compatibility_score": compatibility_score,
        "concepts": concepts,
        "estimated_time": estimate_completion_time(room_size, budget),
        "sustainability_tips": get_sustainability_tips(furniture_style),
        "smart_home": get_smart_home_suggestions(room_type, lifestyle),
    }

def calculate_compatibility(room_type, style, color_theme, lifestyle):
    """Score how well the choices complement each other."""
    score = 70  # base

    # Style-lifestyle compatibility
    lifestyle_style = {
        "Family with Kids": ["Rustic", "Scandinavian", "Classic"],
        "Young Professional": ["Modern", "Minimalist", "Industrial"],
        "Couple": ["Bohemian", "Modern", "Scandinavian"],
        "Senior Living": ["Classic", "Scandinavian", "Rustic"],
        "Work From Home": ["Minimalist", "Scandinavian", "Modern"],
        "Entertainer": ["Modern", "Bohemian", "Classic"],
    }
    preferred = lifestyle_style.get(lifestyle, [])
    if style in preferred:
        score += 15

    # Color-room compatibility bonus
    color_room = {
        "Cool & Calm": ["Bedroom", "Bathroom", "Office"],
        "Warm & Cosy": ["Living Room", "Dining Room", "Bedroom"],
        "Bold & Vibrant": ["Living Room", "Dining Room"],
        "Nature Inspired": ["Bedroom", "Office", "Living Room"],
    }
    if room_type in color_room.get(color_theme, []):
        score += 10

    return min(score + random.randint(0, 5), 99)

def build_design_concepts(room_type, style, palette, room_size):
    """Create 3 distinct design concept variations."""
    concepts = [
        {
            "name": f"Signature {style}",
            "description": f"A pure expression of {style.lower()} design — staying true to the style's defining principles with carefully curated pieces.",
            "highlights": ["Statement focal point", "Cohesive colour story", "Thoughtful lighting layers"],
            "mood": "Timeless & Authentic",
        },
        {
            "name": f"Contemporary Fusion",
            "description": f"A blend of {style.lower()} elements with modern comfort touches, creating a space that feels fresh yet familiar.",
            "highlights": ["Mixed textures", "Modern functionality", "Personalised accents"],
            "mood": "Fresh & Eclectic",
        },
        {
            "name": f"Luxe {style}",
            "description": f"An elevated take on {style.lower()} design with premium materials, bespoke details, and a considered colour palette.",
            "highlights": ["Premium materials", "Curated art", "Architectural details"],
            "mood": "Sophisticated & Refined",
        },
    ]
    return concepts

def estimate_completion_time(room_size, budget):
    """Estimate project completion time."""
    size_weeks = {"Small (< 100 sq ft)": 2, "Medium (100–250 sq ft)": 3, "Large (250–500 sq ft)": 5, "Very Large (500+ sq ft)": 8}
    budget_weeks = {
        "Under ₹50,000 / $600": 1,
        "₹50,000–₹1,50,000 / $600–$1,800": 2,
        "₹1,50,000–₹5,00,000 / $1,800–$6,000": 3,
        "Above ₹5,00,000 / $6,000+": 5,
    }
    base = size_weeks.get(room_size, 3) + budget_weeks.get(budget, 2)
    return f"{base}–{base + 2} weeks"

def get_sustainability_tips(style):
    tips = {
        "Modern": ["Choose FSC-certified wood furniture", "LED lighting throughout", "Low-VOC paints and finishes"],
        "Rustic": ["Reclaimed wood is inherently sustainable", "Upcycle vintage finds", "Natural linseed or beeswax finishes"],
        "Minimalist": ["Buy less, choose quality — reduces waste long-term", "Donate rather than discard old furniture", "Natural materials only"],
        "Scandinavian": ["Invest in durable Scandinavian brands known for longevity", "Natural wool and linen textiles", "Energy-efficient lighting"],
        "Bohemian": ["Shop vintage and second-hand for authentic bohemian pieces", "Support artisan makers", "Natural dye fabrics"],
        "Industrial": ["Repurpose industrial salvage for authentic pieces", "Metal is highly recyclable", "Energy-efficient Edison LED bulbs"],
        "Classic": ["Antique and vintage furniture is the ultimate sustainable choice", "Natural fabrics like silk, wool, linen", "Quality over quantity"],
    }
    return tips.get(style, ["Choose sustainable materials", "Support local makers", "Invest in quality over quantity"])

def get_smart_home_suggestions(room_type, lifestyle):
    base = ["Smart LED colour-changing bulbs", "Voice assistant integration (Alexa/Google)"]
    room_specific = {
        "Living Room": ["Smart TV with ambient screen mode", "Automated blinds/curtains", "Multi-room audio system"],
        "Bedroom": ["Smart sleep tracker", "Automated blackout blinds", "Sunrise alarm clock lights"],
        "Kitchen": ["Smart refrigerator", "Touchless faucet", "Under-cabinet LED strips"],
        "Office": ["Smart monitor lighting", "Sit-stand desk with memory positions", "Noise-cancelling smart speakers"],
        "Bathroom": ["Smart mirror with weather display", "Heated towel rail timer", "Smart shower controller"],
        "Dining Room": ["Smart dimmable pendant lights", "Wireless charging table", "Smart speaker for ambiance"],
    }
    return base + room_specific.get(room_type, [])
