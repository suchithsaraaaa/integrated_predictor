#!/bin/bash
set -e

echo "🔄 Moving Frontend to /var/www to fix Redirect Loop..."

# 1. Create Public Web Directory
sudo mkdir -p /var/www/nestiq
sudo chown -R $USER:$USER /var/www/nestiq

# 2. Copy Build Files
echo " -> Copying files..."
# Ensure we are copying from the correct place
cp -r nestiq-predict-main/dist/* /var/www/nestiq/

# 3. Set Permissions for Nginx
echo " -> Setting Permissions..."
sudo chown -R www-data:www-data /var/www/nestiq
sudo chmod -R 755 /var/www/nestiq

# 4. Update Nginx Config
echo " -> Updating Nginx Root Path..."
# We need to find the old root line and replace it, or just overwrite the file.
# Overwriting is safer to ensure correctness.

PROJECT_DIR=$(readlink -f house_price_prediction/core)
SOCKET_FILE=/home/ubuntu/integrated_predictor/house_price_prediction/core/nestiq.sock

sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    # FRONTEND (Now in /var/www/nestiq)
    location / {
        root /var/www/nestiq;
        index index.html;
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

# 5. Restart Nginx
echo " -> Restarting Nginx..."
sudo systemctl restart nginx

echo "=========================================="
echo "✅ FIXED!"
echo "Try clearing your browser cache and refreshing."
echo "=========================================="
