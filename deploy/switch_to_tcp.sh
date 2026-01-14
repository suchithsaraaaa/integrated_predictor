#!/bin/bash
echo "🔌 SWITCHING TO TCP: Solving Socket Permission Issues..."

# 1. Update Gunicorn Service (Systemd)
SERVICE_FILE="/etc/systemd/system/nestiq.service"
echo "   Updating Gunicorn Service..."

# Replace sock file path with 127.0.0.1:8000
# We use a broad regex to catch whatever bind argument was there
if grep -q "unix:" "$SERVICE_FILE"; then
    sudo sed -i 's|unix:/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock|127.0.0.1:8000|g' "$SERVICE_FILE"
    # If the path was slightly different or regex failed, we might need a backup sed
    # But usually it's unix:/path. Let's also just try replacing the bind flag entirely if it exists.
fi

# Ensure it binds to port 8000
# (Assuming the original command format: gunicorn --workers 3 --bind unix:... core.wsgi:application)
# We change it to: gunicorn --workers 3 --bind 127.0.0.1:8000 core.wsgi:application
sudo sed -i 's|--bind unix:[^ ]*|--bind 127.0.0.1:8000|g' "$SERVICE_FILE"


# 2. Update Nginx Config
NGINX_CONF="/etc/nginx/sites-available/nestiq"
echo "   Updating Nginx Config..."

# Replace proxy_pass unix:... with proxy_pass http://127.0.0.1:8000;
sudo sed -i 's|proxy_pass http://unix:[^;]*;|proxy_pass http://127.0.0.1:8000;|g' "$NGINX_CONF"

# 3. Reload & Restart
echo "🔄 Reloading Systemd & Restarting Services..."
sudo systemctl daemon-reload
sudo systemctl restart nestiq
sudo systemctl restart nginx

# 4. Verify Ports
echo "👀 Checking Port 8000..."
sudo lsof -i :8000

echo "✅ NETWORK SWITCH COMPLETE. Try the site now!"
