#!/bin/bash
echo "🕵️ SERVER DIAGNOSTICS: Troubleshooting 500 Error"
echo "================================================="

# Activate Venv
source /home/ubuntu/integrated_predictor/house_price_prediction/core/.venv/bin/activate

# Run Python code
python3 deploy/test_prediction_internal.py
