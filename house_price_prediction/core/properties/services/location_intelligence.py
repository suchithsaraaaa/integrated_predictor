import reverse_geocoder as rg

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
    # --- NORTH AMERICA ---
    'US': {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.013, 'growth': 1.04},
    'CA': {'currency': {'symbol': 'C$', 'code': 'CAD'}, 'mult': 0.018, 'growth': 1.04},
    'MX': {'currency': {'symbol': '$', 'code': 'MXN'}, 'mult': 0.25, 'growth': 1.06},

    # --- EUROPE (Eurozone + Others) ---
    'GB': {'currency': {'symbol': '£', 'code': 'GBP'}, 'mult': 0.010, 'growth': 1.03},
    'CH': {'currency': {'symbol': 'CHF', 'code': 'CHF'}, 'mult': 0.012, 'growth': 1.02}, # Swiss
    'NO': {'currency': {'symbol': 'kr', 'code': 'NOK'}, 'mult': 0.12, 'growth': 1.03},
    'SE': {'currency': {'symbol': 'kr', 'code': 'SEK'}, 'mult': 0.12, 'growth': 1.03},
    'DK': {'currency': {'symbol': 'kr', 'code': 'DKK'}, 'mult': 0.09, 'growth': 1.03},
    'RU': {'currency': {'symbol': '₽', 'code': 'RUB'}, 'mult': 1.0, 'growth': 1.05},

    # Eurozone Defaults
    'DE': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.011, 'growth': 1.03},
    'FR': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.011, 'growth': 1.03},
    'IT': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.012, 'growth': 1.02},
    'ES': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.013, 'growth': 1.03},
    'NL': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.011, 'growth': 1.03},
    'IE': {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.011, 'growth': 1.04},
    
    # --- ASIA PACIFIC ---
    'IN': {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.25, 'growth': 1.06}, # Default India
    'JP': {'currency': {'symbol': '¥', 'code': 'JPY'}, 'mult': 1.50, 'growth': 1.01}, # Yen is high denom
    'CN': {'currency': {'symbol': '¥', 'code': 'CNY'}, 'mult': 0.10, 'growth': 1.05},
    'KR': {'currency': {'symbol': '₩', 'code': 'KRW'}, 'mult': 15.0, 'growth': 1.03}, # Won is high denom
    'SG': {'currency': {'symbol': 'S$', 'code': 'SGD'}, 'mult': 0.018, 'growth': 1.03},
    'HK': {'currency': {'symbol': 'HK$', 'code': 'HKD'}, 'mult': 0.10, 'growth': 1.02},
    'AU': {'currency': {'symbol': 'A$', 'code': 'AUD'}, 'mult': 0.016, 'growth': 1.05},
    'NZ': {'currency': {'symbol': 'NZ$', 'code': 'NZD'}, 'mult': 0.017, 'growth': 1.04},
    'ID': {'currency': {'symbol': 'Rp', 'code': 'IDR'}, 'mult': 200.0, 'growth': 1.06}, # Rupiah high denom
    'TH': {'currency': {'symbol': '฿', 'code': 'THB'}, 'mult': 0.45, 'growth': 1.05},
    'VN': {'currency': {'symbol': '₫', 'code': 'VND'}, 'mult': 300.0, 'growth': 1.07}, # Dong high denom

    # --- MIDDLE EAST ---
    'AE': {'currency': {'symbol': 'dh', 'code': 'AED'}, 'mult': 0.05, 'growth': 1.05},
    'SA': {'currency': {'symbol': '﷼', 'code': 'SAR'}, 'mult': 0.05, 'growth': 1.05},
    'TR': {'currency': {'symbol': '₺', 'code': 'TRY'}, 'mult': 0.40, 'growth': 1.08}, # High inflation
    'IL': {'currency': {'symbol': '₪', 'code': 'ILS'}, 'mult': 0.05, 'growth': 1.04},

    # --- AFRICA ---
    'ZA': {'currency': {'symbol': 'R', 'code': 'ZAR'}, 'mult': 0.20, 'growth': 1.05},
    'EG': {'currency': {'symbol': 'E£', 'code': 'EGP'}, 'mult': 0.40, 'growth': 1.07},
    'NG': {'currency': {'symbol': '₦', 'code': 'NGN'}, 'mult': 10.0, 'growth': 1.08},
    'KE': {'currency': {'symbol': 'KSh', 'code': 'KES'}, 'mult': 1.50, 'growth': 1.06},

    # --- SOUTH AMERICA ---
    'BR': {'currency': {'symbol': 'R$', 'code': 'BRL'}, 'mult': 0.07, 'growth': 1.05},
    'AR': {'currency': {'symbol': '$', 'code': 'ARS'}, 'mult': 10.0, 'growth': 1.10}, # Inflation support
    'CO': {'currency': {'symbol': '$', 'code': 'COP'}, 'mult': 50.0, 'growth': 1.05},
    'CL': {'currency': {'symbol': '$', 'code': 'CLP'}, 'mult': 12.0, 'growth': 1.04},
}

# Regional Fallbacks (by continent or rough groups)
DEFAULT_EUR = {'currency': {'symbol': '€', 'code': 'EUR'}, 'mult': 0.012, 'growth': 1.03}
DEFAULT_USD = {'currency': {'symbol': '$', 'code': 'USD'}, 'mult': 0.013, 'growth': 1.04}

def get_location_economics(latitude: float, longitude: float):
    """
    Determines the country and returns calibrated economic data.
    """
    try:
        # 1. Reverse Geocode (Offline, Fast)
        # rg.search returns a list of dicts. We take the first one.
        # mode=2 is fast single-threaded search
        results = rg.search((latitude, longitude), mode=2)
        
        if not results:
            return DEFAULT_USD
            
        country_code = results[0]['cc'] # 'US', 'IN', 'GB'
        print(f"   [GEO] Detected Country: {country_code}")

        # 2. Look up in Map
        econ = ECONOMY_MAP.get(country_code)

        # 3. Handle Special Indian Cities Override (Mumbai/Bangalore)
        # We can still keep the lat/lon check for city-specifics or rely on rg 'admin1'/'name'
        if country_code == 'IN':
            # Mumbai Box
            if 18.5 <= latitude <= 19.5 and 72.5 <= longitude <= 73.5:
                return {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.45, 'growth': 1.08}
            # Bangalore Box
            elif 12.5 <= latitude <= 13.5 and 77.0 <= longitude <= 78.0:
                 return {'currency': {'symbol': '₹', 'code': 'INR'}, 'mult': 0.30, 'growth': 1.09}
            
        if econ:
            return econ
            
        # 4. Smart Fallbacks based on region (Lat/Lon) if country not in map
        # Europe Box
        if 35 <= latitude <= 72 and -10 <= longitude <= 40:
             return DEFAULT_EUR
             
        # Default
        return DEFAULT_USD

    except Exception as e:
        print(f"Error in location intelligence: {e}")
        return DEFAULT_USD
