#!/bin/bash
set -e

# CONFIGURATION
PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock
WEB_ROOT=/var/www/nestiq

echo "🛠️ FINAL FIX INITIATED..."

# 1. VERIFY & MOVE FILES
echo " -> Checking frontend files..."
sudo mkdir -p $WEB_ROOT
if [ -d "nestiq-predict-main/dist" ]; then
    echo " -> Copying fresh build files..."
    sudo cp -r nestiq-predict-main/dist/* $WEB_ROOT/
else
    echo "⚠️  WARNING: Dist folder not found. Assuming files are already in /var/www."
fi

# 2. SET PERMISSIONS (FORCE)
echo " -> Setting Permissions..."
sudo chown -R www-data:www-data $WEB_ROOT
sudo chmod -R 755 $WEB_ROOT

# 3. OVERWRITE NGINX CONFIG (FORCE)
echo " -> Overwriting Nginx Config..."
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    root $WEB_ROOT;
    index index.html;

    # FRONTEND
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # BACKEND API
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:$SOCKET_FILE;
    }
    
    # BACKEND ADMIN
    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:$SOCKET_FILE;
    }

    # APP STATIC FILES
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }
}
EOF"

# 4. ENABLE & RESTART
echo " -> Restarting Nginx..."
sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 5. TEST
echo "--------------------------------"
echo "✅ Validating Fix..."
STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost)
echo "HTTP Status: $STATUS"

if [ "$STATUS" == "200" ]; then
    echo "🎉 SUCCESS! Website is serving 200 OK."
else
    echo "⚠️  Returned $STATUS. Check browser."
fi
echo "--------------------------------"
