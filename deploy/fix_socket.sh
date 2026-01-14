#!/bin/bash
set -e

echo "🔧 Fixing Socket Permissions..."

# Define the new socket location (Inside the project folder where 'ubuntu' has write access)
PROJECT_DIR=/home/ubuntu/integrated_predictor/house_price_prediction/core
SOCKET_FILE=$PROJECT_DIR/nestiq.sock

# 1. Update Systemd Service to use LOCAL socket
# Replace unix:/run/nestiq.sock with unix:/home/ubuntu/.../nestiq.sock
echo " -> Updating Gunicorn Service..."
sudo sed -i "s|unix:/run/nestiq.sock|unix:$SOCKET_FILE|g" /etc/systemd/system/nestiq.service

# 2. Update Nginx Config to use LOCAL socket
echo " -> Updating Nginx Config..."
sudo sed -i "s|unix:/run/nestiq.sock|unix:$SOCKET_FILE|g" /etc/nginx/sites-available/nestiq

# 3. FIX DIRECTORY PERMISSIONS (Crucial!)
# Nginx (user 'www-data') needs to walk through /home/ubuntu to reach the socket and static files
echo " -> Fixing Home Directory Permissions..."
sudo chmod 755 /home/ubuntu
sudo chmod 755 /home/ubuntu/integrated_predictor
sudo chmod 755 /home/ubuntu/integrated_predictor/nestiq-predict-main/dist

# 4. Restart Services
echo " -> Restarting Services..."
sudo systemctl daemon-reload
sudo systemctl restart nestiq
sudo systemctl restart nginx

echo "=========================================="
echo "✅ FIX COMPLETE!"
echo "The socket is now at: $SOCKET_FILE"
echo "Try refreshing your browser now."
echo "=========================================="
