import os
import django
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def run_diagnostics():
    print("--- 1. DJANGO SETUP ---")
    try:
        django.setup()
        print("Django setup success.")
    except Exception:
        print("Django setup FAILED.")
        traceback.print_exc()
        return

    print("\n--- 2. OSMNX CHECK ---")
    try:
        import osmnx as ox
        print(f"OSMnx Version: {ox.__version__}")
    except Exception:
        print("OSMnx import FAILED.")
        traceback.print_exc()

    print("\n--- 3. AREA INSIGHTS CHECK ---")
    try:
        from properties.services.area_insights import get_area_insights
        # Use coordinates that definitely exist (Los Angeles or Hyd)
        # User image showed "Serilingampally, Hyderabad".
        # Let's use Hyderabad coords roughly: 17.48, 78.30
        lat, lon = 17.48, 78.30
        print(f"Fetching insights for {lat}, {lon}...")
        insights = get_area_insights(lat, lon)
        print("Insights keys:", list(insights.keys()))
        print("Insights sample:", insights)
    except Exception:
        print("Area Insights FAILED.")
        traceback.print_exc()

    print("\n--- 4. ML PREDICTION CHECK ---")
    try:
        from ml.predict import predict_price
        from ml.feature_engineering.build_features import build_feature_vector
        
        print("Building features...")
        features = build_feature_vector(
            latitude=17.48,
            longitude=78.30,
            area_sqft=2000.0,
            bedrooms=3,
            bathrooms=3,
            year=2024
        )
        print("Features shape/data:", features)
        
        print("Running prediction...")
        price = predict_price(features)
        print(f"Predicted Price: {price}")
    except Exception:
        print("ML Prediction FAILED.")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        run_diagnostics()
    except Exception:
        traceback.print_exc()
