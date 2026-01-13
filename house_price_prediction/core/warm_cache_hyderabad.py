import os
import django
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from properties.services.area_insights import get_area_insights

# Key locations in Hyderabad (Lat, Lon)
LOCATIONS = [
    ("Gachibowli", 17.4401, 78.3489),
    ("Hitech City", 17.4435, 78.3772),
    ("Jubilee Hills", 17.4311, 78.4112),
    ("Banjara Hills", 17.4126, 78.4398),
    ("Madhapur", 17.4483, 78.3915),
    ("Kondapur", 17.4615, 78.3681),
    ("Kukatpally", 17.4948, 78.3996),
    ("Manikonda", 17.4012, 78.3927),
    ("Begumpet", 17.4447, 78.4602),
    ("Secunderabad", 17.4399, 78.4983),
    ("Miyapur", 17.4968, 78.3614),
    ("Ameerpet", 17.4375, 78.4487),
    ("Uppal", 17.3984, 78.5583),
    ("L.B. Nagar", 17.3537, 78.5491),
    ("Serilingampally", 17.4833, 78.3160), # From user screenshot
    ("Nallagandla", 17.4699, 78.3072),
    ("Financial District", 17.4109, 78.3370),
    ("Kokapet", 17.3946, 78.3323)
]

def warm_cache():
    print(f"🔥 Warming cache for {len(LOCATIONS)} Hyderabad locations...")
    print("This fetches data from OpenStreetMap and saves it to your local database.")
    
    success_count = 0
    
    for name, lat, lon in LOCATIONS:
        print(f"\n📍 Processing {name} ({lat}, {lon})...")
        try:
            start = time.time()
            # This triggers the fetch and save to DB
            insights = get_area_insights(lat, lon)
            duration = time.time() - start
            
            # Verify cache hit
            is_cached = " (First Fetch)" if duration > 1.0 else " (Cached Hit)"
            print(f"✅ Done in {duration:.2f}s{is_cached}")
            
            # Simple validation
            schools = insights.get('schools', {}).get('count', 0)
            print(f"   Details: Schools={schools}, Hospitals={insights.get('hospitals', {}).get('count')}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed for {name}: {e}")

    print(f"\n✨ Completed! {success_count}/{len(LOCATIONS)} locations pre-cached.")
    print("During your demo, these locations will return results INSTANTLY.")

if __name__ == "__main__":
    warm_cache()
