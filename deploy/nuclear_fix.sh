#!/bin/bash

echo "☢️ NUCLEAR FIX INITIATED..."

# 0. FORCE RESYNC (The "Nuclear" part)
echo "🔄 Forcing Git Sync..."
git fetch --all
git reset --hard origin/main

# 1. STOP Service
echo "🛑 Stopping Nestiq Service..."
sudo systemctl stop nestiq

# 2. KILL ALL Gunicorn (Zombie Protection)
echo "🔫 Killing any zombie Gunicorn processes..."
sudo pkill -9 gunicorn || echo "No gunicorn processes found (Good)."

# 3. VERIFY Disk Content
echo "🔍 Checking Disk Content for Hard Cap..."
FILE="house_price_prediction/core/properties/api/views.py"

# ERROR WAS HERE: Code says "Hard Cap at 12%", grep was "HARD CAP 12%"
if grep -i "Hard Cap" "$FILE"; then
    echo "✅ SUCCESS: The HARD CAP code is present on disk."
    grep -i "Hard Cap" "$FILE" -C 2
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
