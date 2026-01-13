import random
import pandas as pd
from typing import List, Dict

# Simulated country data (lat/lon ranges)
COUNTRY_BOUNDS = {
    "US": {"lat": (30.0, 48.0), "lon": (-120.0, -75.0), "base_price": 400000},
    "IN": {"lat": (8.0, 32.0), "lon": (70.0, 88.0), "base_price": 6000000},  # ~ INR 60L
    "UK": {"lat": (50.0, 58.0), "lon": (-5.0, 1.0), "base_price": 350000},   # ~ GBP 350k
    "CA": {"lat": (43.0, 60.0), "lon": (-130.0, -60.0), "base_price": 550000}, # ~ CAD 550k
    "AU": {"lat": (-38.0, -12.0), "lon": (113.0, 154.0), "base_price": 700000}, # ~ AUD 700k
}

def generate_mock_data(country_code: str, count: int = 100) -> pd.DataFrame:
    """
    Generates realistic-looking housing data for a given country.
    """
    bounds = COUNTRY_BOUNDS.get(country_code, COUNTRY_BOUNDS["US"])
    base = bounds["base_price"]
    
    data = []
    for _ in range(count):
        lat = random.uniform(bounds["lat"][0], bounds["lat"][1])
        lon = random.uniform(bounds["lon"][0], bounds["lon"][1])
        
        bedrooms = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.3, 0.4, 0.15, 0.05])[0]
        bathrooms = max(1, bedrooms - random.choice([0, 1]))
        area_sqft = bedrooms * 400 + random.randint(-100, 300)
        year = random.randint(1990, 2024)
        
        # Price correlates with size and year
        price_factor = (area_sqft / 1000) * (1 + (year - 1990) * 0.01)
        price = base * price_factor * random.uniform(0.8, 1.2)
        
        data.append({
            "latitude": lat,
            "longitude": lon,
            "area_sqft": area_sqft,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "year": year,
            "price": round(price, 2)
        })
        
    return pd.DataFrame(data)
