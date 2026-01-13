import os
import django
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def test_api():
    try:
        django.setup()
        import osmnx as ox
        print(f"OSMnx: {ox.__version__}")
        
        from properties.services.area_insights import get_area_insights
        print("Testing get_area_insights...")
        res = get_area_insights(17.48, 78.30)
        print("Insights OK:", list(res.keys()))

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test_api()
