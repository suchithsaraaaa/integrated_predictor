import os
import sys
import django
import traceback

# 1. Setup Django
try:
    sys.path.append('/home/ubuntu/integrated_predictor/house_price_prediction/core')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    print("✅ Django Setup: OK")
except Exception as e:
    print(f"❌ Django Setup Failed: {e}")
    sys.exit(1)

# 2. Test Imports (Pandas, Joblib, RG)
print("\n🔍 Testing Critical Imports...")
modules = ['pandas', 'joblib', 'reverse_geocoder', 'shapely', 'osmnx', 'geopy']
for mod in modules:
    try:
        __import__(mod)
        print(f"   - {mod}: OK")
    except ImportError as e:
        print(f"   ❌ MISSING MODULE: {mod} ({e})")
    except Exception as e:
        print(f"   ❌ ERROR loading {mod}: {e}")

# 3. Test Database (AreaMetrics)
print("\n🔍 Testing Database (AreaMetrics)...")
try:
    from properties.models import AreaMetrics
    count = AreaMetrics.objects.count()
    print(f"   - Table Exists. Row Count: {count}")
except Exception as e:
    print(f"   ❌ DATABASE ERROR: {e}")
    print("   👉 TIP: Did you run 'python manage.py migrate'?")

# 4. Mock Prediction Logic
print("\n🔍 Testing Logic (Mock Prediction)...")
try:
    from properties.api.views import predict_price_view
    from rest_framework.test import APIRequestFactory
    
    # Mock Data (London)
    payload = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "year": 2026,
        "area_sqft": 1000,
        "bedrooms": 2,
        "bathrooms": 1
    }
    
    factory = APIRequestFactory()
    request = factory.post('/api/predict/', payload, format='json')
    
    # We need to call the view manually. 
    # Since it's decorated with @api_view, we treat it as a callable view
    
    print("   ... Calling predict_price_view(request) ...")
    response = predict_price_view(request)
    
    print(f"   - Response Code: {response.status_code}")
    print(f"   - Body: {response.data}")
    
    if response.status_code == 200:
        print("\n✅ Internal Logic Checks Passed!")
    else:
        print(f"\n❌ API Returned Error: {response.data}")
    
except Exception as e:
    print(f"\n❌ LOGIC CRASH: {e}")
    traceback.print_exc()
