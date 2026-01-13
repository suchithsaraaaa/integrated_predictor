import django
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    import osmnx as ox
    print(f"OSMnx Version: {ox.__version__}")
    
    try:
        f = ox.features_from_point
        print("ox.features_from_point exists at top level")
    except AttributeError:
        print("ox.features_from_point MISSING at top level")
        
    try:
        f = ox.features.features_from_point
        print("ox.features.features_from_point exists")
    except AttributeError:
        print("ox.features.features_from_point MISSING")
    
    try:
        p = ox.project_geometry
        print("ox.project_geometry exists")
    except AttributeError:
        print("ox.project_geometry MISSING (Expected for 2.0)")

    try:
        p = ox.projection.project_geometry
        print("ox.projection.project_geometry exists")
    except AttributeError:
        print("ox.projection.project_geometry MISSING")

except Exception as e:
    print(e)
