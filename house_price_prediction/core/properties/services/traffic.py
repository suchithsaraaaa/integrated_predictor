import datetime
from properties.models import AreaMetrics


def compute_traffic_score(latitude: float, longitude: float) -> float:
    """
    Compute traffic congestion score (0–1)
    based on time-of-day heuristics.
    """

    now = datetime.datetime.now().hour

    # Peak hour multiplier
    if 8 <= now <= 10 or 17 <= now <= 20:
        time_factor = 0.9
    elif 11 <= now <= 16:
        time_factor = 0.6
    else:
        time_factor = 0.3

    # Location factor - use variable deterministic hash
    # to differentiate between different parts of a city
    loc_seed = (latitude * longitude * 10000) % 1
    
    # Combine time factor (global) with location factor (local)
    # Traffic is usually 0.3 to 0.9
    traffic_score = 0.3 + (time_factor * 0.4) + (loc_seed * 0.2)

    return round(traffic_score, 2)


def get_or_update_traffic_metric(latitude: float, longitude: float) -> float:
    """
    Fetch or compute traffic metric and cache it.
    OPTIMIZED: Uses 1.5km fuzzy lookup and AVOIDS re-computation if found.
    """
    
    # 1. FUZZY CACHE LOOKUP
    TOLERANCE = 0.015 
    metric = AreaMetrics.objects.filter(
        latitude__range=(latitude - TOLERANCE, latitude + TOLERANCE),
        longitude__range=(longitude - TOLERANCE, longitude + TOLERANCE)
    ).first()

    if metric:
        return metric.traffic_score

    # 2. COMPUTATION (Only if missing)
    score = compute_traffic_score(latitude, longitude)
    
    # 3. SAVE
    AreaMetrics.objects.create(
        latitude=round(latitude, 4),
        longitude=round(longitude, 4),
        traffic_score=score,
        crime_index=0.0, # Defaults
        accessibility_score=0.0
    )

    return score
