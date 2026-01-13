import pandas as pd
from properties.models import Property, AreaMetrics
from .utils import generate_mock_data

def ingest_data_for_country(country_code: str, count: int = 500) -> int:
    """
    Generates and stores data for a country. 
    Returns the number of records created.
    """
    df = generate_mock_data(country_code=country_code, count=count)
    
    properties_to_create = []
    for _, row in df.iterrows():
        properties_to_create.append(Property(
            latitude=row["latitude"],
            longitude=row["longitude"],
            area_sqft=row["area_sqft"],
            bedrooms=row["bedrooms"],
            bathrooms=row["bathrooms"],
            price=row["price"],
            listing_date=pd.Timestamp(f"{int(row['year'])}-01-01").date() 
            # Note: Model might need 'year' field or we derive it. 
            # Existing train.py derives year from listing_date.
        ))
    
    Property.objects.bulk_create(properties_to_create)

    # 🚀 CACHE WARMING: Pre-compute AreaMetrics
    # Since this is "mock" ingestion, we can mock the metrics too!
    # This prevents the slow OSMnx lookup later.
    metrics_to_create = []
    
    # Needs to match coarse rounding in area_insights.py
    for row in df.to_dict('records'):
        lat = round(row["latitude"], 2)
        lon = round(row["longitude"], 2)
        
        # Simple deterministic mock based on coords to be consistent
        # In a real app, this might fetch from a faster data layer
        crime = (hash((lat, lon)) % 100) / 100.0
        
        # Avoid duplicate keys for bulk_create
        # In real scenario we'd use ignore_conflicts=True
        
        metrics_to_create.append(AreaMetrics(
            latitude=lat,
            longitude=lon,
            crime_index=crime,
            traffic_score=0.5, # Default
            accessibility_score=0.5, # Default
            meta={
                "crime_rate_percent": int(crime * 100),
                "schools": {"nearest_distance_km": 0.5, "count": 10},
                "hospitals": {"nearest_distance_km": 1.2, "count": 5},
                "public_transport": {"nearest_distance_km": 0.3, "count": 15},
                "note": "Pre-computed ingestion data"
            }
        ))
        
    AreaMetrics.objects.bulk_create(metrics_to_create, ignore_conflicts=True)

    return len(properties_to_create)
