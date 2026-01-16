from typing import Dict
from shapely.geometry import Point

from properties.models import AreaMetrics
from properties.services.crime import compute_crime_index


# -----------------------------
# Fallback (city-level estimate)
# -----------------------------
def fallback_insights() -> Dict:
    return {
        "crime_rate_percent": 10,
        "schools": {
            "nearest_distance_km": 1.5,
            "count": 6,
        },
        "hospitals": {
            "nearest_distance_km": 2.0,
            "count": 4,
        },
        "public_transport": {
            "nearest_distance_km": 0.8,
            "count": 8,
        },
        "note": "Estimated using city-level averages (OSM data sparse)",
    }


# -----------------------------
# Core computation helpers
# -----------------------------
def _nearest_distance_and_count(latitude: float, longitude: float, tags: dict):
    try:
        import osmnx as ox
        gdf = ox.features_from_point(
            (latitude, longitude),
            tags=tags,
            dist=2000,  # Reduced to 2km for speed/stability
        )

        if gdf.empty:
            return None, 0

        # 🔑 Project to meters (critical for distance accuracy)
        gdf = gdf.to_crs(epsg=3857)

        point = Point(longitude, latitude)
        # Fix for OSMnx 2.x: project_geometry moved to projection module
        point_proj = ox.projection.project_geometry(
            point, crs="EPSG:4326", to_crs="EPSG:3857"
        )[0]

        gdf["distance"] = gdf.geometry.distance(point_proj)

        nearest_km = round(float(gdf["distance"].min()) / 1000, 2)
        return nearest_km, int(len(gdf))

    except Exception as e:
        print(f"OSMnx Error: {e}")
        return None, 0


# -----------------------------
# Main public API
# -----------------------------
# -----------------------------
# Main public API
# -----------------------------
def get_area_insights(latitude: float, longitude: float, force_live: bool = False) -> Dict:
    """
    Returns cached or computed area intelligence for a location.
    OPTIMIZATION: Bounding Box Search (1.5km radius)
    """

    # 1. FASTER DB QUERY: Bounding Box instead of exact match
    # 0.015 degrees approx 1.6km. This finds *any* cached point nearby.
    TOLERANCE = 0.015 
    
    cached = AreaMetrics.objects.filter(
        latitude__range=(latitude - TOLERANCE, latitude + TOLERANCE),
        longitude__range=(longitude - TOLERANCE, longitude + TOLERANCE)
    ).first()

    # 🚀 Instant return if cached (Hit)
    if cached and cached.meta:
        print(f"   [CACHE HIT] Found nearby data for {latitude}, {longitude}")
        return cached.meta
        
    print(f"   [CACHE MISS] Fetching live data for {latitude}, {longitude}...")

    # -----------------------------
    # Lite Mode check (Protect Server)
    # -----------------------------
    if not force_live:
        print(f"   [LITE MODE] Skipping live OSM fetch for {latitude},{longitude}. Using Fallback.")
        return fallback_insights()

    # -----------------------------
    # Live computation (High Quality)
    # -----------------------------
    try:
        # Increase timeout/settings for OSM
        import osmnx as ox
        ox.settings.timeout = 30 
        ox.settings.use_cache = True
        ox.settings.cache_folder = 'cache' 
        
        crime_percent = int(compute_crime_index(latitude, longitude) * 100)

        school_dist, school_count = _nearest_distance_and_count(
            latitude, longitude, {"amenity": "school"}
        )
        
        hospital_dist, hospital_count = _nearest_distance_and_count(
            latitude, longitude, {"amenity": "hospital"}
        )

        transport_dist, transport_count = _nearest_distance_and_count(
            latitude, longitude, {
                "public_transport": True,
                "railway": True,
                "highway": "bus_stop",
            }
        )
        
        result = {
            "crime_rate_percent": crime_percent,
            "schools": {
                "nearest_distance_km": school_dist or 5.0, 
                "count": school_count,
            },
            "hospitals": {
                "nearest_distance_km": hospital_dist or 5.0,
                "count": hospital_count,
            },
            "public_transport": {
                "nearest_distance_km": transport_dist or 5.0,
                "count": transport_count,
            },
        }

    except Exception as e:
        # Log the actual error
        print(f"Area Insights Error for {latitude},{longitude}: {e}")
        return fallback_insights()

    # -----------------------------
    # Cache result
    # -----------------------------
    # Use get_or_create to avoid IntegrityError on missing fields
    
    defaults = {
        "crime_index": result["crime_rate_percent"] / 100.0,
        "traffic_score": 0.5,       # Default, will be updated by traffic service later
        "accessibility_score": 0.5, # Default, will be updated by accessibility service later
        "meta": result
    }
    
    metric, created = AreaMetrics.objects.get_or_create(
        latitude=latitude,
        longitude=longitude,
        defaults=defaults
    )
    
    if not created:
        metric.meta = result
        metric.crime_index = result["crime_rate_percent"] / 100.0
        metric.save(update_fields=["meta", "crime_index"])

    return result
