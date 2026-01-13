from django.urls import path
from .views import ingest_country_data

urlpatterns = [
    path('country/', ingest_country_data),
]
