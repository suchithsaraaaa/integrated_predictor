
import random
import datetime
import math
from properties.models import Property
from properties.services.crime import compute_crime_index
from properties.services.traffic import compute_traffic_score

def generate_synthetic_data(n=5000):
    print(f"Generating {n} synthetic properties...")
    
    # Define Regions (Lat/Lon centers and spread)
    regions = [
        {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "spread": 0.15, "base_price_sft": 6000},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "spread": 0.10, "base_price_sft": 18000}, # 3x Hyd
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946, "spread": 0.15, "base_price_sft": 8500},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "spread": 0.10, "base_price_sft": 45000}, # ~7-8x in INR terms (approx)
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "spread": 0.10, "base_price_sft": 55000},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "spread": 0.15, "base_price_sft": 35000},
    ]

    new_props = []

    for _ in range(n):
        region = random.choice(regions)
        
        # 1. Generate Location
        lat = region["lat"] + random.uniform(-region["spread"], region["spread"])
        lon = region["lon"] + random.uniform(-region["spread"], region["spread"])
        
        # 2. House Details
        area = random.randint(800, 5000)
        beds = random.randint(1, 5)
        baths = max(1, min(beds + random.choice([0, 1]), 5))
        year = random.randint(1990, 2024)
        
        # 3. Compute Metrics (Global Logic)
        crime = compute_crime_index(lat, lon)
        traffic = compute_traffic_score(lat, lon)
        # Accessibility (Simulate: closer to center = better)
        dist_from_center = math.sqrt((lat - region["lat"])**2 + (lon - region["lon"])**2)
        accessibility = max(0.2, 1.0 - (dist_from_center * 5)) # rough approximation
        
        # 4. Calculate Price (The "Ground Truth" formula)
        # Price = (Area * BaseRate) * (DetailsFactor) * (MetricsFactor) * (Noise)
        
        details_factor = 1.0 + (beds * 0.05) + (baths * 0.03) + ((year - 2000) * 0.005)
        
        # Good metrics (Low crime, Low traffic, High access) -> Higher Price
        # Crime: 0(Good) -> 1(Bad). Traffic: 0(Good) -> 1(Bad). Access: 0(Bad) -> 1(Good).
        metrics_factor = (1.0 - (crime * 0.3)) * (1.0 - (traffic * 0.2)) * (0.8 + (accessibility * 0.4))
        
        base_val = area * region["base_price_sft"]
        
        final_price = base_val * details_factor * metrics_factor
        
        # Random noise +/- 10%
        noise = random.uniform(0.90, 1.10)
        final_price *= noise
        
        p = Property(
            latitude=round(lat, 5),
            longitude=round(lon, 5),
            price=round(final_price, 2),
            area_sqft=area,
            bedrooms=beds,
            bathrooms=baths,
            year_built=year,
            listing_date=datetime.date(year, 1, 1),
            source="synthetic_v1"
        )
        new_props.append(p)
        
    # Bulk Create
    print("Saving to DB...")
    Property.objects.bulk_create(new_props)
    print(f"✅ Successfully inserted {len(new_props)} records.")

if __name__ == "__main__":
    generate_synthetic_data()
