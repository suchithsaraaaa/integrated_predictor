#!/bin/bash

echo "☢️ NUCLEAR FIX INITIATED..."

# 1. STOP Service
echo "🛑 Stopping Nestiq Service..."
sudo systemctl stop nestiq

# 2. KILL ALL Gunicorn (Zombie Protection)
echo "🔫 Killing any zombie Gunicorn processes..."
sudo pkill -9 gunicorn || echo "No gunicorn processes found (Good)."

# 3. VERIFY Disk Content
echo "🔍 Checking Disk Content for Hard Cap..."
FILE="house_price_prediction/core/properties/api/views.py"

if grep -i "HARD CAP 12%" "$FILE"; then
    echo "✅ SUCCESS: The HARD CAP code is present on disk."
    grep -i "HARD CAP 12%" "$FILE" -C 2
else
    echo "❌ CRITICAL FAILURE: The code is NOT on disk."
    echo "Listing file tail:"
    tail -n 20 "$FILE"
    exit 1
fi

# 4. START Service
echo "🚀 Starting Nestiq Service..."
sudo systemctl start nestiq

echo "✅ DONE. Please test again."
