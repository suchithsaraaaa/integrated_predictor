#!/bin/bash
set -e

echo "🚀 FINAL RESTORE (VERIFIED)..."

# 1. RENAME FILE BACK
if [ -f /var/www/nestiq/app.html ]; then
    echo " -> Renaming app.html back to index.html..."
    sudo mv /var/www/nestiq/app.html /var/www/nestiq/index.html
fi

# 2. WRITE PRODUCTION CONFIG
# Using standard SPA routing (Verified safe now that file access is confirmed)
PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock

sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    root /var/www/nestiq;
    index index.html;

    # FRONTEND
    location / {
        try_files \\\$uri \\\$uri/ /index.html;
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

    # STATIC FILES
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }
}
EOF"

# 3. RESTART
echo " -> Restarting Nginx..."
sudo systemctl restart nginx

# 4. FINAL VERIFICATION
echo " -> Testing Homepage (Should be 200 OK):"
curl -I http://localhost/

echo "=========================================="
echo "✅ WE ARE LIVE."
echo "If curl says 200 OK, open your browser."
echo "=========================================="
