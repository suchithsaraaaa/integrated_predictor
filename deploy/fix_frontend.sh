#!/bin/bash

echo "🎨 FIXING FRONTEND: Rebuilding & Permissions..."

PROJECT_DIR="/home/ubuntu/integrated_predictor"
FRONTEND_DIR="$PROJECT_DIR/nestiq-predict-main"
WEB_ROOT="/var/www/nestiq"

# 1. Check Node/NPM
echo "   Checking Build Tools..."
node -v
npm -v

# 2. Install Dependencies & Build
echo "   Building React App (This may take a minute)..."
cd "$FRONTEND_DIR"
# Clean install to be safe
rm -rf node_modules
npm install
npm run build

if [ ! -d "dist" ]; then
    echo "❌ BUILD FAILED: 'dist' folder not created."
    exit 1
fi

# 3. Deploy to Web Root
echo "   Deploying to $WEB_ROOT..."
# Create dir if missing
sudo mkdir -p "$WEB_ROOT"
# Clear old files
sudo rm -rf "$WEB_ROOT/*"
# Copy new files
sudo cp -r dist/* "$WEB_ROOT/"

# 4. Fix Permissions
echo "   Fixing Nginx Permissions..."
# Nginx user (www-data) needs to read these files
sudo chown -R www-data:www-data "$WEB_ROOT"
sudo chmod -R 755 "$WEB_ROOT"

# 5. Fix Nginx Config (Ensure it points to /var/www/nestiq)
NGINX_CONF="/etc/nginx/sites-available/nestiq"
echo "   Verifying Nginx Config..."
if grep -q "/var/www/nestiq" "$NGINX_CONF"; then
    echo "   ✅ Nginx is pointing to correct root."
else
    echo "   ⚠️ UPDATING NGINX ROOT..."
    sudo sed -i 's|root .*;|root /var/www/nestiq;|g' "$NGINX_CONF"
fi

# 6. Restart Nginx
echo "🔄 Restarting Nginx..."
sudo systemctl restart nginx

echo "✅ Frontend Repaired. Try the site now!"
