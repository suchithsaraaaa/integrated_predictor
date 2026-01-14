#!/bin/bash

# CAUSE FOUND: 
# The systemd service is using 'house_price_prediction/core/.venv'
# But we were fixing 'house_price_prediction/venv'
# This script targets the ACTUAL service environment.

PROJECT_DIR="/home/ubuntu/integrated_predictor"
CORE_DIR="$PROJECT_DIR/house_price_prediction/core"
VENV_DIR="$CORE_DIR/.venv"

echo "🎯 TARGETING GUNICORN VENV: $VENV_DIR"

# 1. Install system basics
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip python3-full

# 2. Destroy old venv
if [ -d "$VENV_DIR" ]; then
    echo "   Removing old/corrupt venv..."
    rm -rf "$VENV_DIR"
fi

# 3. Create fresh venv
echo "   Creating fresh venv..."
python3 -m venv "$VENV_DIR"

# 4. Install dependencies
echo "   Installing dependencies..."
# Use the pip inside the new venv
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$CORE_DIR/requirements.txt"
"$VENV_DIR/bin/pip" install reverse_geocoder

# 5. Fix Ownership (Ensure ubuntu user owns it)
chown -R ubuntu:ubuntu "$PROJECT_DIR"

# 6. Restart Service
echo "🔄 Restarting NestIQ..."
systemctl restart nestiq

echo "✅ Environment Fixed. The 'Network Error' should be gone!"
