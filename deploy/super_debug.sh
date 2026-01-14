#!/bin/bash

echo "🕵️ SUPER DEBUGGER: Investigating Server Issues..."

echo "---------------------------------------------------"
echo "1. 🧠 MEMORY CHECK (Is it OOM?)"
echo "---------------------------------------------------"
free -h
echo "Swap Usage:"
swapon --show

echo ""
echo "---------------------------------------------------"
echo "2. 🐍 PYTHON IMPORT TEST (Is reverse_geocoder working?)"
echo "---------------------------------------------------"
# Try to import the new library
cd house_price_prediction/core
../../house_price_prediction/venv/bin/python -c "import reverse_geocoder; print('✅ reverse_geocoder imported successfully')" || echo "❌ python import FAILED"

echo ""
echo "---------------------------------------------------"
echo "3. ⏱️ TIMEOUT CONFIG CHECK"
echo "---------------------------------------------------"
echo "Checking Nginx Config for 'timeout'..."
grep "timeout" /etc/nginx/sites-available/nestiq

echo "Checking Gunicorn Service for 'timeout'..."
grep "timeout" /etc/systemd/system/nestiq.service

echo ""
echo "---------------------------------------------------"
echo "4. 📜 RECENT ERROR LOGS (Nginx)"
echo "---------------------------------------------------"
sudo tail -n 20 /var/log/nginx/error.log

echo ""
echo "---------------------------------------------------"
echo "5. 📜 RECENT SERVICE LOGS (Gunicorn)"
echo "---------------------------------------------------"
sudo journalctl -u nestiq --no-pager -n 20

echo ""
echo "---------------------------------------------------"
echo "DIAGNOSIS COMPLETE"
echo "---------------------------------------------------"
