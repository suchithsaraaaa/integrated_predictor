#!/bin/bash
echo "🐛 FIXING IDENTICAL PRICE BUG..."

# 1. RESTART SERVICE (To load new python logic)
echo " -> Restarting Nestiq Service..."
sudo systemctl restart nestiq
sleep 2

# 2. CLEAR CACHE (Optional but good)
# We can't easily clear the DB via script without Django shell, 
# but the new logic handles '0.0' values so old bad rows will get updated automatically!
echo " -> Cache logic updated. 'Zero' values will now be recalculated automatically."

echo "=========================================="
echo "✅ Backend updated."
echo "PLEASE TEST COMPARISON AGAIN."
echo "Differences should now appear."
echo "=========================================="
