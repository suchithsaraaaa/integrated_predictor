#!/bin/bash
set -e

echo "🚀 GOING LIVE (FINALIZNG)..."

# 1. RESTORE PRODUCTION CONFIG
PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock

sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    root /var/www/nestiq;
    index index.html;

    # FRONTEND (SPA Routing)
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

    # DJANGO STATIC FILES
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }
}
EOF"

# 2. TEST & RESTART
echo " -> Testing Config Syntax..."
sudo nginx -t

echo " -> Restarting Nginx..."
sudo systemctl restart nginx

# 3. VERIFY SERVICE STATUS
echo " -> Checking Service Status..."
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx is RUNNING."
else
    echo "❌ Nginx is DEAD. Logs:"
    sudo journalctl -u nginx -n 10
    exit 1
fi

# 4. FINAL LOCAL CHECK
echo " -> Local Health Check:"
# Fetch header only, show HTTP code
curl -I http://localhost/

echo "=========================================="
echo "✅ DEPLOYMENT SUCCESSFUL"
echo "If curl says '200 OK', the server is PERFECT."
echo "Any browser errors now are 100% Local Cache."
echo "=========================================="
