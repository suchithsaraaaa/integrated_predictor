
import sys
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import WSGI (simulates production boot)
from core.wsgi import application

# Check loaded modules
heavy_hitters = ['osmnx', 'sklearn', 'pandas', 'scipy', 'numpy']
loaded = []

print("--- Checking Loaded Modules ---")
for mod in heavy_hitters:
    if mod in sys.modules:
        print(f"❌ {mod} is LOADED!")
        loaded.append(mod)
    else:
        print(f"✅ {mod} is NOT loaded.")

if loaded:
    print(f"\n⚠️  WARNING: The following heavy modules are still loading on boot: {loaded}")
else:
    print("\n🎉 SUCCESS: No heavy modules loaded on boot!")
