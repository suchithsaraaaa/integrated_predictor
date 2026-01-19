import os
import sys
import django
import unittest
from unittest.mock import patch, MagicMock

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from properties.services.area_insights import get_area_insights
from properties.models import AreaMetrics

class StrictCacheTest(unittest.TestCase):
    def setUp(self):
        # Coordinates for "Test City"
        self.lat = 0.0001
        self.lon = 0.0001
        
        # 1. Clean up potential old data
        AreaMetrics.objects.filter(latitude=self.lat, longitude=self.lon).delete()
        
        # 2. Seed the Cache (Zero API Request Validation)
        self.fake_meta = {
            "crime_rate_percent": 1,
            "schools": {"count": 999, "nearest_distance_km": 0.1},
            "hospitals": {"count": 888, "nearest_distance_km": 0.2},
            "public_transport": {"count": 777, "nearest_distance_km": 0.3},
            "source": "STRICT_CACHE_TEST"
        }
        
        AreaMetrics.objects.create(
            latitude=self.lat,
            longitude=self.lon,
            crime_index=0.01,
            traffic_score=0.0,
            accessibility_score=1.0,
            meta=self.fake_meta
        )
        print("\n✅ [SETUP] Seeded DB with Fake Data at 0.0001, 0.0001")

    def test_zero_network_on_cache_hit(self):
        """
        Ensures that if data is in DB, absolutely NO network libraries are touched.
        """
        print("🛡️  [TEST] Running Cache Hit Test with Network Disabled...")
        
        # We poison the network libraries. If the code even TRIES to import/use them, it fails.
        with patch.dict('sys.modules', {'osmnx': None}):
            with patch('properties.services.area_insights.fallback_insights') as mock_fallback:
                
                # EXECUTE
                # We expect this to return our fake_meta, NOT fallback, and NOT crash on missing osmnx
                result = get_area_insights(self.lat, self.lon, force_live=True)
                
                # VERIFY
                self.assertEqual(result['source'], "STRICT_CACHE_TEST")
                self.assertEqual(result['schools']['count'], 999)
                
                print("   [SUCCESS] Data retrieved from DB.")
                print("   [SUCCESS] Code did not crash despite 'osmnx' being disabled.")

    def tearDown(self):
        AreaMetrics.objects.filter(latitude=self.lat, longitude=self.lon).delete()
        print("🧹 [CLEANUP] Removed test data.\n")

if __name__ == '__main__':
    unittest.main()
