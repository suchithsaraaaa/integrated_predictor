import os
import django
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from properties.services.area_insights import get_area_insights
from properties.models import AreaMetrics

# Target List: 5 Major Cities per Major European Country
EUROPE_TARGETS = {
    "United Kingdom": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Palermo"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
    "Belgium": ["Brussels", "Antwerp", "Ghent", "Charleroi", "Liege"],
    "Switzerland": ["Zurich", "Geneva", "Basel", "Lausanne", "Bern"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmo", "Uppsala", "Vasteras"],
    "Norway": ["Oslo", "Bergen", "Trondheim", "Stavanger", "Drammen"],
    "Denmark": ["Copenhagen", "Aarhus", "Odense", "Aalborg", "Esbjerg"],
    "Poland": ["Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan"],
    "Austria": ["Vienna", "Graz", "Linz", "Salzburg", "Innsbruck"],
    "Portugal": ["Lisbon", "Porto", "Vila Nova de Gaia", "Amadora", "Braga"],
    "Ireland": ["Dublin", "Cork", "Limerick", "Galway", "Waterford"],
    "Greece": ["Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa"],
    "Czech Republic": ["Prague", "Brno", "Ostrava", "Plzen", "Liberec"],
    "Hungary": ["Budapest", "Debrecen", "Szeged", "Miskolc", "Pecs"],
    "Finland": ["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu"],
    "Romania": ["Bucharest", "Cluj-Napoca", "Timisoara", "Iasi", "Constanta"],
    "Bulgaria": ["Sofia", "Plovdiv", "Varna", "Burgas", "Ruse"],
    "Croatia": ["Zagreb", "Split", "Rijeka", "Osijek", "Zadar"]
}

# ---------------------------------------------------------
# Grid Generation Logic (Better Coverage)
# ---------------------------------------------------------
GRID_STEP = 0.02  # ~2km spacing
DEFAULT_RADIUS_KM = 6  # 6km radius for European density

def generate_grid_for_radius(center_lat, center_lon, radius_km):
    """
    Generates a grid of points within radius_km of the center.
    """
    coords = []
    lat_step = GRID_STEP
    lon_step = GRID_STEP 
    
    # Approx degrees conversion
    deg_radius = radius_km / 111.0
    
    start_lat = center_lat - deg_radius
    end_lat = center_lat + deg_radius
    start_lon = center_lon - deg_radius
    end_lon = center_lon + deg_radius
    
    curr_lat = start_lat
    while curr_lat <= end_lat:
        curr_lon = start_lon
        while curr_lon <= end_lon:
            # Rounding to match DB precision
            coords.append((round(curr_lat, 3), round(curr_lon, 3)))
            curr_lon += lon_step
        curr_lat += lat_step
        
    return coords

def cache_europe():
    geolocator = Nominatim(user_agent="nestiq_cache_warmer_eur_v2")
    
    # Flatten the dictionary to count total cities
    all_cities = []
    for country, cities in EUROPE_TARGETS.items():
        for city in cities:
            all_cities.append((city, country))
            
    total_cities = len(all_cities)
    print(f"🌍 STARTING GRID CACHE for {total_cities} Cities (Radius: {DEFAULT_RADIUS_KM}km)...")
    
    processed = 0
    errors = 0

    for i, (city, country) in enumerate(all_cities, 1):
        query = f"{city}, {country}"
        print(f"\n[{i}/{total_cities}] 📍 Processing: {query}...")
        
        try:
            # 1. Find Center
            location = geolocator.geocode(query, timeout=10)
            if not location:
                print(f"   ❌ Could not locate: {query}")
                continue
            
            lat, lon = location.latitude, location.longitude
            
            # 2. Generate Grid
            grid = generate_grid_for_radius(lat, lon, DEFAULT_RADIUS_KM)
            print(f"   Generating {len(grid)} points...")
            
            # 3. Process Grid
            for p_lat, p_lon in grid:
                # Check DB first (Fast)
                if AreaMetrics.objects.filter(latitude=p_lat, longitude=p_lon).exists():
                    # print(".", end="", flush=True) # Too noisy
                    continue

                try:
                    # Fetch & Cache
                    get_area_insights(p_lat, p_lon, force_live=True)
                    processed += 1
                    print(f"   ✅ Saved: {p_lat}, {p_lon}")
                    time.sleep(0.1) # Tiny sleep to separate DB writes
                except Exception as e:
                    print(f"   ❌ Error at {p_lat}, {p_lon}: {e}")
                    errors += 1

            print(f"\n   ✅ Done. {processed} new points cached so far.")
            
            # Be nice to Nominatim API between cities
            time.sleep(1)

        except Exception as e:
            print(f"   ⚠️ Major Error on {city}: {e}")

    print(f"\n🎉 EUROPEAN GRID CACHE COMPLETE!")
    print(f"   Total Cached Points: {processed}")
    print(f"   Errors: {errors}")

if __name__ == '__main__':
    cache_europe()
