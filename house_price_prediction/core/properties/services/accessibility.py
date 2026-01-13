from shapely.geometry import Point
from properties.models import AreaMetrics


def compute_accessibility_score(latitude: float, longitude: float) -> float:
    """
    Compute accessibility score (0–1) based on distance to
    schools, hospitals, and public transport using OSM data.
    """


    import osmnx as ox
    point = Point(longitude, latitude)

    tags = {
        "school": {"amenity": "school"},
        "hospital": {"amenity": "hospital"},
        "transport": {"public_transport": True},
    }

    distances = []

    for tag in tags.values():
        try:
            gdf = ox.features_from_point(
                (latitude, longitude),
                tags=tag,
                dist=6000,
            )

            if gdf.empty:
                continue

            # Project geometries to meters
            gdf = gdf.to_crs(epsg=3857)
            # Fix for OSMnx 2.x: project_geometry moved to projection module
            point_projected = ox.projection.project_geometry(
                point, crs="EPSG:4326", to_crs="EPSG:3857"
            )[0]

            gdf["distance"] = gdf.geometry.distance(point_projected)
            distances.append(gdf["distance"].min())

        except Exception as e:
            print(f"Accessibility Error: {e}")
            continue

    if not distances:
        return 0.2

    avg_distance_m = sum(distances) / len(distances)

    score = max(0.1, min(1.0, 1 / (avg_distance_m / 1000 + 0.5)))
    return round(score, 2)


def get_or_update_accessibility_metric(latitude: float, longitude: float) -> float:
    """
    Fetch or compute accessibility metric and cache it.
    OPTIMIZED: Uses 1.5km fuzzy lookup and AVOIDS re-computation if found.
    """
    
    # 1. FUZZY CACHE LOOKUP
    TOLERANCE = 0.015 
    metric = AreaMetrics.objects.filter(
        latitude__range=(latitude - TOLERANCE, latitude + TOLERANCE),
        longitude__range=(longitude - TOLERANCE, longitude + TOLERANCE)
    ).first()

    if metric:
        # Check if we have a valid score (not 0.0 default)
        if metric.accessibility_score > 0:
            return metric.accessibility_score
            
        # If 0.0, maybe we need to compute it (but avoid if possible)
        # For now, let's treat existing record as valid source of truth
        # unless it was a placeholder.
        
    # 2. COMPUTATION (Only if missing)
    score = compute_accessibility_score(latitude, longitude)
    
    # 3. SAVE (Create new record or update found one)
    if metric:
        metric.accessibility_score = score
        metric.save(update_fields=["accessibility_score"])
    else:
        AreaMetrics.objects.create(
            latitude=round(latitude, 4),
            longitude=round(longitude, 4),
            accessibility_score=score,
            crime_index=0.0, # Defaults
            traffic_score=0.0
        )

    return score
