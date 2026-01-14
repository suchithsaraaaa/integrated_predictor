#!/bin/bash
set -e

echo "🔧 FORCING VIDEO LOCATION BLOCK..."

PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock

# We add a specific block for /videos/ to debug why it fails
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    root /var/www/nestiq;
    index index.html;

    # 1. EXPLICIT VIDEO BLOCK
    location /videos/ {
        alias /var/www/nestiq/videos/;
        autoindex on;             # Allow listing files
        try_files \\\$uri =404;   # Don't fallback to index.html
    }

    # 2. FRONTEND
    location / {
        try_files \\\$uri \\\$uri/ /index.html;
    }

    # 3. BACKEND API
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:$SOCKET_FILE;
    }
    
    # 4. BACKEND ADMIN
    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:$SOCKET_FILE;
    }

    # 5. STATIC FILES
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }
}
EOF"

echo " -> Restarting Nginx..."
sudo systemctl restart nginx

echo " -> Testing /videos/home.mp4..."
curl -I http://localhost/videos/home.mp4

echo "=========================================="
echo "Visit http://<IP>/videos/ in your browser."
echo "You should see a file list now."
echo "=========================================="
