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

def get_location_economics(latitude: float, longitude: float):
    """
    Determines the country and returns calibrated economic data.
    Gracefully handles missing reverse_geocoder by falling back to bounding boxes.
    """
    try:
        # 1. Reverse Geocode (If Available)
        if HAS_RG:
            results = rg.search((latitude, longitude), mode=2)
            if results:
                country_code = results[0]['cc'] # 'US', 'IN', 'GB'
                
                # Special Override for India Cities
                if country_code == 'IN':
                    if 18.5 <= latitude <= 19.5 and 72.5 <= longitude <= 73.5: # Mb
                        return {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.45, 'growth': 1.08}
                    elif 12.5 <= latitude <= 13.5 and 77.0 <= longitude <= 78.0: # Blr
                         return {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.30, 'growth': 1.09}
                    return ECONOMY_MAP.get('IN', DEFAULT_USD)

                # Return mapped economy
                if country_code in ECONOMY_MAP:
                    return ECONOMY_MAP[country_code]

        # 2. Smart Fallbacks (If RG missing or unknown country)
        # UK Box
        if 49 <= latitude <= 61 and -8 <= longitude <= 2:
            return DEFAULT_GBP
            
        # Europe Box
        if 35 <= latitude <= 72 and -12 <= longitude <= 45:
             return DEFAULT_EUR
             
        # India Box (Broad)
        if 6 <= latitude <= 37 and 68 <= longitude <= 97:
             return ECONOMY_MAP.get('IN')
             
        # Australia Box
        if -45 <= latitude <= -10 and 110 <= longitude <= 155:
            return DEFAULT_AUD
            
        # New Zealand Box
        if -48 <= latitude <= -33 and 165 <= longitude <= 180:
            return DEFAULT_NZD
            
        # Canada Box (Rough)
        if latitude > 48 and -141 <= longitude <= -52:
            return DEFAULT_CAD

        # Default to USD
        return DEFAULT_USD

    except Exception as e:
        print(f"Error in location intelligence: {e}")
        return DEFAULT_USD
