#!/bin/bash

# Define paths (Based on previous findings)
CORE_DIR="/home/ubuntu/integrated_predictor/house_price_prediction/core"
VENV_PYTHON="$CORE_DIR/.venv/bin/python"

echo "🧪 DIAGNOSTIC RUN: Investigating Startup Crash"
echo "==================================================="

# 1. Check Python Interpreter
if [ -f "$VENV_PYTHON" ]; then
    echo "✅ Python found at: $VENV_PYTHON"
    "$VENV_PYTHON" --version
else
    echo "❌ CRITICAL: Python NOT found at $VENV_PYTHON"
    echo "   Checking for ANY venv..."
    find /home/ubuntu/integrated_predictor -name "venv" -o -name ".venv"
    exit 1
fi

# 2. Check Dependencies
echo "---------------------------------------------------"
echo "🔍 Checking Installed Packages..."
"$VENV_PYTHON" -m pip list | grep -E "django|reverse_geocoder|numpy"

# 3. Dry-Run Django (The Moment of Truth)
echo "---------------------------------------------------"
echo "🚀 Attempting Dry-Run of Django (manage.py check)..."
cd "$CORE_DIR"
"$VENV_PYTHON" manage.py check

STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "✅ Django Check PASSED. The code is valid."
else
    echo "❌ Django Check FAILED (Exit Code: $STATUS)"
    echo "   See the Error Traceback above ⬆️"
    exit 1
fi

# 4. Check Service Logs (If code is fine, maybe Gunicorn config is wrong)
echo "---------------------------------------------------"
echo "📜 Last 30 lines of Application Logs:"
journalctl -u nestiq --no-pager -n 30

echo "==================================================="
echo "DIAGNOSIS COMPLETE"
