import pandas as pd
from homeharvest import scrape_property
from properties.models import Property


def ingest_properties(location: str, past_days: int = 7) -> int:
    """
    Pull real-time property data using HomeHarvest,
    clean it, and store it in the database.
    """

    df = scrape_property(
        location=location,
        listing_type="for_sale",
        past_days=past_days
    )

    if df is None or df.empty:
        return 0

    created = 0

    for _, row in df.iterrows():
        try:
            lat = row.get("latitude")
            lon = row.get("longitude")

            if pd.isna(lat) or pd.isna(lon):
                continue

            Property.objects.create(
                latitude=float(lat),
                longitude=float(lon),
                price=_safe_float(row.get("price")),
                area_sqft=_safe_float(row.get("sqft")),
                bedrooms=_safe_int(row.get("beds")),
                bathrooms=_safe_int(row.get("baths")),
                year_built=_safe_int(row.get("year_built")),
                listing_date=_safe_date(row.get("listing_date")),
                source="homeharvest",
            )

            created += 1

        except Exception:
            continue

    return created


def _safe_float(val):
    try:
        return float(val)
    except Exception:
        return None


def _safe_int(val):
    try:
        return int(val)
    except Exception:
        return None


def _safe_date(val):
    try:
        return pd.to_datetime(val).date()
    except Exception:
        return None
