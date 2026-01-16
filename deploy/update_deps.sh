#!/bin/bash
echo "📦 Updating Python Dependencies on Server..."

# Expecting to be run from project root (e.g., ~/integrated_predictor)
# Expecting to be run from project root (e.g., ~/integrated_predictor)
VENV_PATH="./house_price_prediction/core/.venv"

# Fallback to absolute path if running from weird context
if [ ! -d "$VENV_PATH" ]; then
    echo "⚠️  Virtual Environment not found at relative path."
    echo "    Trying absolute path /home/ubuntu/integrated_predictor/house_price_prediction/core/.venv"
    VENV_PATH="/home/ubuntu/integrated_predictor/house_price_prediction/core/.venv"
fi

if [ -d "$VENV_PATH" ]; then
    echo "✅ Using Virtual Environment: $VENV_PATH"
    
    # Use explicit binary paths to avoid 'externally-managed-environment' error
    "$VENV_PATH/bin/python" -m pip install --upgrade pip
    "$VENV_PATH/bin/pip" install -r house_price_prediction/core/requirements.txt
    "$VENV_PATH/bin/pip" install reverse_geocoder
    
    echo "🔄 Restarting NestIQ Service..."
    systemctl restart nestiq
    echo "✅ Success! Dependencies updated."
else
    echo "❌ CRITICAL: Could not find virtual environment at $VENV_PATH"
    exit 1
fi
