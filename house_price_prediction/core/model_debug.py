import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ml.predict import predict_price

def test_sensitivity():
    print("🔬 TESTING MODEL SENSITIVITY...")
    
    # Base Case: 2000 sqft, 3 bed, 2 bath, 2025
    # We will vary Crime, Traffic, Access from 0.0 to 1.0
    
    base_features = [2000, 3, 2, 0.5, 0.5, 0.5, 2025] # Midpoint
    
    price_mid = predict_price(base_features)[0]
    print(f"Base Price (All 0.5): {price_mid:,.2f}")
    
    # Test Crime (Index 3)
    f_crime_low = list(base_features); f_crime_low[3] = 0.0
    f_crime_high = list(base_features); f_crime_high[3] = 1.0
    p_crime_low = predict_price(f_crime_low)[0]
    p_crime_high = predict_price(f_crime_high)[0]
    print(f"Crime 0.0: {p_crime_low:,.2f} | Crime 1.0: {p_crime_high:,.2f} | Diff: {p_crime_high - p_crime_low:,.2f}")

    # Test Traffic (Index 4)
    f_traffic_low = list(base_features); f_traffic_low[4] = 0.0
    f_traffic_high = list(base_features); f_traffic_high[4] = 1.0
    p_traffic_low = predict_price(f_traffic_low)[0]
    p_traffic_high = predict_price(f_traffic_high)[0]
    print(f"Traffic 0.0: {p_traffic_low:,.2f} | Traffic 1.0: {p_traffic_high:,.2f} | Diff: {p_traffic_high - p_traffic_low:,.2f}")

    # Test Accessibility (Index 5)
    f_access_low = list(base_features); f_access_low[5] = 0.0
    f_access_high = list(base_features); f_access_high[5] = 1.0
    p_access_low = predict_price(f_access_low)[0]
    p_access_high = predict_price(f_access_high)[0]
    print(f"Access 0.0: {p_access_low:,.2f} | Access 1.0: {p_access_high:,.2f} | Diff: {p_access_high - p_access_low:,.2f}")

if __name__ == "__main__":
    test_sensitivity()
