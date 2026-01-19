#!/bin/bash
set -e # Exit on error

# 1. Activate the correct Virtual Environment
# (Using the one defined in systemd/gunicorn)
VENV_PATH="/home/ubuntu/integrated_predictor/house_price_prediction/core/.venv"
source "$VENV_PATH/bin/activate"

echo "==================================================="
echo "🛡️  VERIFICATION 1: Strict Cache Policy (Zero API)"
echo "==================================================="
python3 house_price_prediction/core/verify_cache_strict.py

echo ""
echo "==================================================="
echo "🌍 VERIFICATION 2: Global Accuracy & Currency"
echo "==================================================="
python3 house_price_prediction/core/verify_global_accuracy.py

echo ""
echo "✅ ALL SYSTEMS GO! Production Pipeline Verified."
