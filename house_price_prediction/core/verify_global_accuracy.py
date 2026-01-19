import os
import sys
import django
# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from properties.api.views import predict_price_view

def test_location(name, lat, lon, expected_currency):
    print(f"\n🌍 Testing {name} ({lat}, {lon})...")
    
    factory = APIRequestFactory()
    payload = {
        "latitude": lat,
        "longitude": lon,
        "year": 2026,
        "area_sqft": 1000,
        "bedrooms": 2,
        "bathrooms": 1
    }
    request = factory.post('/api/predict/', payload, format='json')
    
    try:
        response = predict_price_view(request)
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Status {response.status_code}")
            print(f"   Error: {response.data}")
            return False
            
        data = response.data
        price = data.get('predicted_price')
        currency = data.get('currency', {}).get('code')
        symbol = data.get('currency', {}).get('symbol')
        
        print(f"   ✅ Price: {symbol} {price:,.2f}")
        print(f"   ✅ Currency: {currency}")
        
        if currency != expected_currency:
            print(f"   ❌ CURRENCY MISMATCH! Expected {expected_currency}, got {currency}")
            return False
            
        if price <= 0:
            print(f"   ❌ INVALID PRICE! Got {price}")
            return False

        return True
        
    except Exception as e:
        print(f"   ❌ CRASH: {e}")
        return False

# Test Cases
locations = [
    ("London, UK", 51.5074, -0.1278, "GBP"),
    ("New York, USA", 40.7128, -74.0060, "USD"),
    ("Mumbai, India", 19.0760, 72.8777, "INR"),
    ("Tokyo, Japan", 35.6762, 139.6503, "JPY"),
    ("Berlin, Germany", 52.5200, 13.4050, "EUR"),
    ("Sydney, Australia", -33.8688, 151.2093, "AUD"),
]

print("🚀 Starting Global Accuracy Check...")
passed = 0
for loc in locations:
    if test_location(*loc):
        passed += 1

print(f"\n🏁 Result: {passed}/{len(locations)} Pas sed.")
if passed == len(locations):
    print("✅ GLOBAL PIPELINE VERIFIED.")
else:
    print("❌ SOME TESTS FAILED.")
    sys.exit(1)
