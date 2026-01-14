#!/bin/bash

echo "🚑 FORCE INSTALLER: Fixing Dependencies..."

# 1. Locate Venv
VENV_PATH="/home/ubuntu/integrated_predictor/house_price_prediction/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "❌ CRITICAL: Venv not found at $VENV_PATH"
    exit 1
fi

echo "   Found Venv at: $VENV_PATH"

# 2. Fix Permissions (in case sudo messed them up)
echo "   Fixing permissions (chown ubuntu:ubuntu)..."
chown -R ubuntu:ubuntu "/home/ubuntu/integrated_predictor"

# 3. Install reverse_geocoder as UBUNTU user (not root)
echo "   Installing reverse_geocoder..."
sudo -u ubuntu "$VENV_PATH/bin/pip" install reverse_geocoder
sudo -u ubuntu "$VENV_PATH/bin/pip" install -r /home/ubuntu/integrated_predictor/house_price_prediction/core/requirements.txt

# 4. Verify Import
echo "   Verifying Installation..."
if sudo -u ubuntu "$VENV_PATH/bin/python" -c "import reverse_geocoder; print('✅ SUCCESS')"; then
    echo "   Library is ready!"
else
    echo "❌ PRE-FLIGHT CHECK FAILED: reverse_geocoder still missing."
    exit 1
fi

# 5. Restart Service
echo "🔄 Restarting NestIQ..."
systemctl restart nestiq
sleep 2

# 6. Check Status
systemctl status nestiq --no-pager | grep "Active"

echo "✅ DONE. Try the website now!"
