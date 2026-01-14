#!/bin/bash
echo "📦 Updating Python Dependencies on Server..."

# Activate Virtual Env if it exists, otherwise standard python3
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Navigate to code
cd house_price_prediction/core || exit

# Update Pip
python3 -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Manually verify reverse_geocoder just in case
pip install reverse_geocoder

# Restart Service
echo "🔄 Restarting NestIQ..."
sudo systemctl restart nestiq

echo "✅ Dependencies Updated & Service Restarted."
