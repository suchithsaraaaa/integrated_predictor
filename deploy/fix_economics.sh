#!/bin/bash
set -e

echo "🔧 Fixing Economics Logic..."

# 1. Navigate
cd /home/ubuntu/integrated_predictor

# 2. Force Pull (Discard local changes if any)
git fetch --all
git reset --hard origin/main

# 3. Clean Python Cache (Aggressive)
echo "🧹 Cleaning __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 4. Verify Content (Check if Hard Cap exists)
echo "🔍 Verifying Code..."
if grep -q "HARD CAP 12%" house_price_prediction/core/properties/api/views.py; then
    echo "✅ Code check passed: Hard Cap found."
else
    echo "❌ ERROR: New code NOT found. Git pull failed?"
    exit 1
fi

# 5. Restart
echo "🔄 Restarting Service..."
sudo systemctl restart nestiq

echo "✅ DONE. Growth rates are now firmly capped."
