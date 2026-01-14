#!/bin/bash
set -e

echo "🚀 RESTORING FULL APPLICATION..."

# 1. COPY REAL FRONTEND FILES
echo " -> Deploying React App..."
sudo cp -r nestiq-predict-main/dist/* /var/www/nestiq/
sudo chown -R www-data:www-data /var/www/nestiq

# 2. WRITE PRODUCTION CONFIG
echo " -> Applying Production Nginx Config..."
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

# 3. SWITCH CONFIGS
sudo rm -f /etc/nginx/sites-enabled/nuclear
sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/

# 4. RESTART
echo " -> Restarting Nginx..."
sudo systemctl restart nginx

echo "=========================================="
echo "✅ APP RESTORED!"
echo "Go to http://3.110.121.21 in your browser."
echo "You should see the Nestiq App now (not just 'VICTORY')."
echo "=========================================="
