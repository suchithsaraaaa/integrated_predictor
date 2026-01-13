import os
import django
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from properties.services.area_insights import get_area_insights

# Key locations for instant demo coverage
PRIORITY_LOCATIONS = {
    "London": [
        ("Westminster", 51.5000, -0.1248),
        ("City of London", 51.5123, -0.0908),
        ("Camden Town", 51.5390, -0.1425),
        ("Chelsea", 51.4875, -0.1687),
        ("Canary Wharf", 51.5034, -0.0163),
        ("Kensington", 51.4984, -0.1917),
        ("Brixton", 51.4627, -0.1146),
        ("Stratford", 51.5432, 0.0006),
        ("Greenwich", 51.4820, -0.0076),
        ("Notting Hill", 51.5096, -0.2043),
    ],
    "San Francisco": [
        ("Downtown SF", 37.7749, -122.4194),
        ("Mission District", 37.7599, -122.4148),
        ("The Castro", 37.7609, -122.4350),
        ("Haight-Ashbury", 37.7692, -122.4484),
        ("Fisherman's Wharf", 37.8080, -122.4177),
        ("SoMa", 37.7785, -122.3918),
        ("Pacific Heights", 37.7925, -122.4382),
    ],
    "Los Angeles": [
        ("Downtown LA", 34.0407, -118.2468),
        ("Hollywood", 34.0928, -118.3287),
        ("Santa Monica", 34.0195, -118.4912),
        ("Venice Beach", 33.9850, -118.4695),
        ("Beverly Hills", 34.0736, -118.4004),
        ("Pasadena", 34.1478, -118.1445),
        ("West Hollywood", 34.0900, -118.3617),
    ],
    "Sydney": [
        ("Sydney CBD", -33.8688, 151.2093),
        ("Bondi Beach", -33.8915, 151.2767),
        ("Parramatta", -33.8150, 151.0011),
        ("Surry Hills", -33.8861, 151.2111),
        ("Manly", -33.7969, 151.2841),
        ("Chat'swood", -33.7961, 151.1780),
        ("Newtown", -33.8970, 151.1793),
    ],
    "Brisbane": [
        ("Brisbane CBD", -27.4698, 153.0251),
        ("South Bank", -27.4766, 153.0167),
        ("Fortitude Valley", -27.4573, 153.0333),
        ("West End", -27.4818, 153.0037),
        ("New Farm", -27.4682, 153.0545),
    ],
    "Adelaide": [
        ("Adelaide CBD", -34.9285, 138.6007),
        ("North Adelaide", -34.9085, 138.5946),
        ("Glenelg", -34.9806, 138.5147),
        ("Norwood", -34.9213, 138.6366),
        ("Unley", -34.9482, 138.6095),
    ]
}

def warm_priority_cache():
    total = sum(len(l) for l in PRIORITY_LOCATIONS.values())
    print(f"🚀 Starting EXPRESS Priority Cache Warmer for {total} Key Locations...")
    print("This will be MUCH faster than the bulk grid.")

    success_count = 0
    errors = 0
    
    for city, spots in PRIORITY_LOCATIONS.items():
        print(f"\n🏙️  {city} ({len(spots)} locations)")
        
        for name, lat, lon in spots:
            print(f"   📍 {name}...", end="", flush=True)
            try:
                start = time.time()
                get_area_insights(lat, lon)
                duration = time.time() - start
                
                cached_msg = "⚡ (Instant)" if duration < 1.0 else f"✅ ({duration:.1f}s)"
                print(f" {cached_msg}")
                success_count += 1
            except Exception as e:
                print(f" ❌ Failed: {e}")
                errors += 1
                
    print("\n" + "="*50)
    print(f"✨ Priority Batch Complete! {success_count}/{total} Cached.")
    print("These popular spots are now ready for your demo.")
    print("You can upload 'db.sqlite3' now.")
    print("="*50)

if __name__ == "__main__":
    warm_priority_cache()
