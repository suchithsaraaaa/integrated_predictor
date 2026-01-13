from django.db import models


class Property(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    price = models.FloatField(null=True, blank=True)
    area_sqft = models.FloatField(null=True, blank=True)

    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)

    year_built = models.IntegerField(null=True, blank=True)
    listing_date = models.DateField(null=True, blank=True)

    source = models.CharField(max_length=100)  # homeharvest, api, csv
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"Property @ ({self.latitude}, {self.longitude})"

class AreaMetrics(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    crime_index = models.FloatField(help_text="0 (safe) → 1 (unsafe)")
    traffic_score = models.FloatField(help_text="0 (free) → 1 (congested)")
    accessibility_score = models.FloatField(help_text="0 (poor) → 1 (excellent)")
    
    meta = models.JSONField(default=dict, blank=True) # Cache for full insights

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("latitude", "longitude")
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"AreaMetrics @ ({self.latitude}, {self.longitude})"
