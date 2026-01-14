#!/bin/bash
set -e

echo "🚀 STARTING MASTER DEPLOYMENT (SSL + VIDEOS + APP)..."

# 1. DETECT IP & DOMAIN
PUBLIC_IP=$(curl -s ifconfig.me)
DOMAIN="${PUBLIC_IP}.nip.io"
PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock

echo " -> Public IP: $PUBLIC_IP"
echo " -> Domain:    $DOMAIN"

# 2. WRITE ROBUST NGINX CONFIG
echo " -> Configuring Nginx (With Video Fix & Domain)..."
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    root /var/www/nestiq;
    index index.html;

    # 1. VIDEO FIX (Explicit Block)
    location /videos/ {
        alias /var/www/nestiq/videos/;
        autoindex on;
        try_files \\\$uri =404;
    }

    # 2. FRONTEND (SPA)
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

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# 3. INSTALL CERTBOT (If missing)
echo " -> Installing Certbot..."
if ! command -v certbot &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y certbot python3-certbot-nginx
fi

# 4. ENABLE SSL
echo " -> Requesting SSL Certificate..."
# Request cert and Force Redirect (Effectively opens Port 443)
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE"
echo "URL: https://$DOMAIN"
echo "=========================================="
