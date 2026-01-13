import os
import django
import sys
import time
import math
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from properties.services.area_insights import get_area_insights
from properties.models import AreaMetrics

# Configuration
# GRID_STEP = 0.02 # approx 2km spacing
GRID_STEP = 0.02 
DELAY_SECONDS = 0.2
MAX_DB_SIZE_GB = 5.5

# Full list of requested locations
CITIES = [
    # --- India ---
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "radius": 15},#
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "radius": 15},#
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "radius": 15},#
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "radius": 15},#
    {"name": "Secunderabad", "lat": 17.4399, "lon": 78.4983, "radius": 8},#
    {"name": "Hitech City", "lat": 17.4435, "lon": 78.3772, "radius": 6},#
    {"name": "Miyapur", "lat": 17.4968, "lon": 78.3614, "radius": 5},#
    {"name": "Chandanagar", "lat": 17.4933, "lon": 78.3249, "radius": 5},
    {"name": "Lingampally", "lat": 17.4855, "lon": 78.3204, "radius": 5},#
    {"name": "Medchal", "lat": 17.6297, "lon": 78.4814, "radius": 5},#

    # --- UK ---
    {"name": "London", "lat": 51.5074, "lon": -0.1278, "radius": 15},#
    {"name": "Manchester", "lat": 53.4808, "lon": -2.2426, "radius": 8}, #
    {"name": "Belfast", "lat": 54.5973, "lon": -5.9301, "radius": 6}, #
    {"name": "Lords (London)", "lat": 51.5298, "lon": -0.1726, "radius": 3},#

    # --- USA ---
    {"name": "New York", "lat": 40.7128, "lon": -74.0060, "radius": 12}, #
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "radius": 15},#
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "radius": 10},

    # --- Australia & New Zealand ---
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "radius": 12},#
    {"name": "Brisbane", "lat": -27.4698, "lon": 153.0251, "radius": 10},
    {"name": "Adelaide", "lat": -34.9285, "lon": 138.6007, "radius": 8},
    {"name": "Auckland", "lat": -36.8485, "lon": 174.7633, "radius": 10},#

    # --- Europe ---
    {"name": "Madrid", "lat": 40.4168, "lon": -3.7038, "radius": 10}, #
    {"name": "Barcelona", "lat": 41.3851, "lon": 2.1734, "radius": 10},#
    {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041, "radius": 8},#
]

def get_db_size_gb():
    try:
        db_path = 'db.sqlite3'
        if os.path.exists(db_path):
            return os.path.getsize(db_path) / (1024 * 1024 * 1024)
    except:
        return 0
    return 0

def check_size_limit():
    size = get_db_size_gb()
    if size > MAX_DB_SIZE_GB:
        print(f"\n🛑 DB Size Limit Reached ({size:.2f} GB). Stopping Warmer.")
        sys.exit(0)

def generate_grid_for_radius(center_lat, center_lon, radius_km):
    """
    Generates a grid of points within radius_km of the center.
    1 degree lat ~= 111km.
    """
    coords = []
    lat_step = GRID_STEP
    lon_step = GRID_STEP # Simplified
    
    # Calculate box bounds
    deg_radius = radius_km / 111.0
    
    start_lat = center_lat - deg_radius
    end_lat = center_lat + deg_radius
    start_lon = center_lon - deg_radius
    end_lon = center_lon + deg_radius
    
    curr_lat = start_lat
    while curr_lat <= end_lat:
        curr_lon = start_lon
        while curr_lon <= end_lon:
            coords.append((round(curr_lat, 2), round(curr_lon, 2)))
            curr_lon += lon_step
        curr_lat += lat_step
        
    return coords

def run_warmer():
    print(f"🌍 Starting GLOBAL Bulk Cache Warmer")
    print(f"   Target Cities: {len(CITIES)}")
    print(f"   Size Limit: {MAX_DB_SIZE_GB} GB")
    print("---------------------------------------------------------------")

    processed = 0
    errors = 0
    
    # Shuffle cities so we don't get stuck on one continent if script restarts
    random.shuffle(CITIES)

    for city in CITIES:
        check_size_limit()
        
        name = city["name"]
        lat = city["lat"]
        lon = city["lon"]
        radius = city["radius"]
        
        print(f"\n🏙️  Generating grid for {name} ({radius}km radius)...")
        grid = generate_grid_for_radius(lat, lon, radius)
        print(f"   - {len(grid)} points to check.")
        
        # Shuffle grid points too for uniform distribution
        random.shuffle(grid)
        
        for p_lat, p_lon in grid:
            check_size_limit()
            
            exists = AreaMetrics.objects.filter(latitude=p_lat, longitude=p_lon).exists()
            if exists:
                continue
            
            try:
                print(f"   [FETCH] {name} {p_lat}, {p_lon}...", end="", flush=True)
                get_area_insights(p_lat, p_lon)
                print(" ✅ Saved")
                
                processed += 1
                time.sleep(DELAY_SECONDS)
                
            except Exception as e:
                print(f" ❌ Error: {e}")
                errors += 1
                time.sleep(1) 

    print("\n=============================================")
    print(f"🎉 Batch Complete!")
    print(f"   New Locations Cached: {processed}")
    print(f"   Errors: {errors}")
    print("=============================================")

if __name__ == "__main__":
    run_warmer()
