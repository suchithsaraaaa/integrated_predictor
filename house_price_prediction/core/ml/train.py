import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from properties.models import Property, AreaMetrics


def train_model():
    qs = Property.objects.exclude(area_sqft__isnull=True)

    data = []

    for p in qs[:5000]: # Increased limit
        try:
            # We assume data is already ingested with price
            if not p.price or not p.area_sqft:
                 continue

            # For training, we ideally want pre-computed metrics
            # But if missing, we can use defaults or simple hash
            # to avoid hitting external APIs during training loop
            
            # FAST PATH: Logic to use stored metrics if available
            # using the SAME functions used in generation/inference
            from properties.services.crime import compute_crime_index
            from properties.services.traffic import compute_traffic_score
            
            crime = compute_crime_index(p.latitude, p.longitude)
            traffic = compute_traffic_score(p.latitude, p.longitude)
            # Accessibility approximation matching generation logic
            # (In real prod, we'd query the AreaMetrics table, but this is fast for training)
            accessibility = 0.5 # Simplified for training speed or query AreaMetrics if needed
            
            data.append({
                "area_sqft": p.area_sqft,
                "bedrooms": p.bedrooms if p.bedrooms is not None else 2,
                "bathrooms": p.bathrooms if p.bathrooms is not None else 2,
                "crime": crime,
                "traffic": traffic,
                "accessibility": accessibility,
                "year": p.listing_date.year if p.listing_date else 2024,
                "price": p.price,
            })

        except Exception:
            continue

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("❌ No training data available")

    X = df[
        ["area_sqft", "bedrooms", "bathrooms", "crime", "traffic", "accessibility", "year"]
    ]
    y = df["price"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, "ml/price_model.pkl")
    print(f"✅ Model trained on {len(df)} records and saved")


if __name__ == "__main__":
    train_model()
    print("Starting model training...")