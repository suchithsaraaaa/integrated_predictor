from properties.services.crime import get_or_create_crime_metric
from properties.services.traffic import get_or_update_traffic_metric
from properties.services.accessibility import get_or_update_accessibility_metric


def build_feature_vector(
    latitude: float,
    longitude: float,
    area_sqft: float,
    bedrooms: int,
    bathrooms: int,
    year: int,
) -> list:
    """
    Build ML feature vector using real-time data.
    Order MUST match training.
    """

    crime = get_or_create_crime_metric(latitude, longitude)
    traffic = get_or_update_traffic_metric(latitude, longitude)
    accessibility = get_or_update_accessibility_metric(latitude, longitude)

    return [
        area_sqft,
        bedrooms,
        bathrooms,
        crime,
        traffic,
        accessibility,
        year,
    ]
