try:
    import reverse_geocoder as rg
    HAS_RG = True
except Exception:
    HAS_RG = False
    print("⚠️ WARNING: reverse_geocoder module failed to load. Running in fallback mode.")

# ---------------------------------------------------------
# GLOBAL ECONOMY MAP
# ---------------------------------------------------------
# Multipliers are roughly calibrated to target realistic property prices 
# relative to the base model output (~60M raw units).
# Base = 0.013 (~$800k USD).
# Tier 1 (Rich): 0.010 - 0.018
# Tier 2 (Mid): 0.05 - 0.15
# Tier 3 (Developing): 0.20 - 0.60
# ---------------------------------------------------------

ECONOMY_MAP = {
    # ... (Keep existing map for reference when RG works) ...
    'US': {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.013, 'growth': 1.04},
    'CA': {'currency': {'symbol': 'C$', 'code': 'CAD'}, 'mult': 0.018, 'growth': 1.04},
    'GB': {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.010, 'growth': 1.03},
    'IN': {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.25, 'growth': 1.06},
    'AU': {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.016, 'growth': 1.05},
    'NZ': {'currency': {'symbol': 'NZ$', 'code': 'NZD'}, 'mult': 0.017, 'growth': 1.04},
    'DE': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.011, 'growth': 1.03},
    # ... (Shortened for brevity in code, but full dict is fine) ...
    'JP': {'currency': {'symbol': '¥', 'code': 'JPY'}, 'mult': 1.50, 'growth': 1.01},
}

# Regional Fallbacks (by continent or rough groups)
DEFAULT_EUR = {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.012, 'growth': 1.03}
DEFAULT_USD = {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.013, 'growth': 1.04}
DEFAULT_GBP = {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.010, 'growth': 1.03}
DEFAULT_CAD = {'currency': {'symbol': 'C$', 'code': 'CAD'}, 'mult': 0.018, 'growth': 1.04}
DEFAULT_AUD = {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.016, 'growth': 1.05}
DEFAULT_NZD = {'currency': {'symbol': 'NZ$', 'code': 'NZD'}, 'mult': 0.017, 'growth': 1.04}

import math

# ---------------------------------------------------------
# MAJOR CITY HUBS (Explicit Overrides)
# ---------------------------------------------------------
# These take priority over general country logic.
# ---------------------------------------------------------
# MAJOR CITY HUBS (Explicit Overrides)
# ---------------------------------------------------------
MAJOR_CITIES = {
    # --- INDIA ---
    (19.0760, 72.8777): {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.45, 'growth': 1.06}, # Mumbai
    (12.9716, 77.5946): {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.31, 'growth': 1.07}, # Bangalore
    (17.3850, 78.4867): {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.29, 'growth': 1.07}, # Hyderabad
    (28.7041, 77.1025): {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.35, 'growth': 1.06}, # Delhi
    (13.0827, 80.2707): {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.25, 'growth': 1.05}, # Chennai
    
    # --- UK ---
    (51.5074, -0.1278): {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.0125, 'growth': 1.03}, # London
    (53.4808, -2.2426): {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.0085, 'growth': 1.04}, # Manchester
    (52.4862, -1.8904): {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.0080, 'growth': 1.03}, # Birmingham
    
    # --- USA ---
    (40.7128, -74.0060): {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.0150, 'growth': 1.04}, # NYC
    (34.0522, -118.2437): {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.0145, 'growth': 1.05}, # LA
    (41.8781, -87.6298):  {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.0110, 'growth': 1.03}, # Chicago
    (37.7749, -122.4194): {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.0190, 'growth': 1.06}, # SF (High!)
    (25.7617, -80.1918):  {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.0135, 'growth': 1.05}, # Miami

    # --- AUSTRALIA ---
    (-33.8688, 151.2093): {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.0180, 'growth': 1.05}, # Sydney
    (-37.8136, 144.9631): {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.0160, 'growth': 1.05}, # Melbourne
    (-27.4705, 153.0260): {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.0140, 'growth': 1.06}, # Brisbane
    
    # --- CANADA ---
    (43.6532, -79.3832): {'currency': {'symbol': 'C$', 'code': 'CAD'}, 'mult': 0.0190, 'growth': 1.05}, # Toronto
    (49.2827, -123.1207): {'currency': {'symbol': 'C$', 'code': 'CAD'}, 'mult': 0.0210, 'growth': 1.04}, # Vancouver
    
    # --- GERMANY ---
    (52.5200, 13.4050): {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.0130, 'growth': 1.04}, # Berlin
    (48.1351, 11.5820): {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.0150, 'growth': 1.03}, # Munich
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def _apply_deterministic_variance(data, lat, lon):
    """
    Applies a deterministic 'micro-variance' to the multiplier.
    Ensures that even two locations in the same city/region have slightly different base values.
    Variation: +/- 10% based on coordinates.
    """
    if not data: return data
    
    # Create a deep copy to avoid mutating the global constant maps
    import copy
    new_data = copy.deepcopy(data)
    
    # Deterministic noise (-0.10 to +0.10)
    seed = (math.sin(lat * 800) + math.cos(lon * 400)) / 10.0
    
    # Apply to multiplier
    new_data['mult'] = new_data['mult'] * (1.0 + seed)
    
    return new_data

def _get_hub_economics(latitude: float, longitude: float):
    """
    Checks if the location is within 50km of a major city hub.
    Returns specific city economics if found.
    """
    for (city_lat, city_lon), data in MAJOR_CITIES.items():
        dist = haversine_distance(latitude, longitude, city_lat, city_lon)
        if dist < 50: # 50km Radius
            print(f"   [HUB HIT] Location is {dist:.1f}km from Hub. Using Override.")
            return data
    return None

def get_location_economics(latitude: float, longitude: float):
    """
    Determines the country and returns calibrated economic data.
    PRIORITY:
    1. Major City Hub (<50km) - High Accuracy
    2. Reverse Geocode (Country Level) - Medium Accuracy
    3. Regional Bounding Box - Low Accuracy Fallback
    """
    try:
        # 1. Check City Hubs FIRST (Robust to RG failure)
        hub_data = _get_hub_economics(latitude, longitude)
        if hub_data:
            return _apply_deterministic_variance(hub_data, latitude, longitude)

        # 2. Reverse Geocode (If Available)
        if HAS_RG:
            results = rg.search((latitude, longitude), mode=2)
            if results:
                country_code = results[0]['cc'] # 'US', 'IN', 'GB'
                
                # Return mapped economy
                if country_code in ECONOMY_MAP:
                    return _apply_deterministic_variance(ECONOMY_MAP[country_code], latitude, longitude)

        # 3. Smart Fallbacks (If RG missing or unknown country)
        # UK Box
        if 49 <= latitude <= 61 and -8 <= longitude <= 2:
            return _apply_deterministic_variance(DEFAULT_GBP, latitude, longitude)
            
        # Europe Box
        if 35 <= latitude <= 72 and -12 <= longitude <= 45:
             return _apply_deterministic_variance(DEFAULT_EUR, latitude, longitude)
             
        # India Box (Broad)
        if 6 <= latitude <= 37 and 68 <= longitude <= 97:
             return _apply_deterministic_variance(ECONOMY_MAP.get('IN'), latitude, longitude)
             
        # Australia Box
        if -45 <= latitude <= -10 and 110 <= longitude <= 155:
            return _apply_deterministic_variance(DEFAULT_AUD, latitude, longitude)
            
        # New Zealand Box
        if -48 <= latitude <= -33 and 165 <= longitude <= 180:
            return _apply_deterministic_variance(DEFAULT_NZD, latitude, longitude)
            
        # Canada Box (Rough)
        if latitude > 48 and -141 <= longitude <= -52:
            return _apply_deterministic_variance(DEFAULT_CAD, latitude, longitude)

        # Default to USD
        return _apply_deterministic_variance(DEFAULT_USD, latitude, longitude)

    except Exception as e:
        print(f"Error in location intelligence: {e}")
        return _apply_deterministic_variance(DEFAULT_USD, latitude, longitude)
