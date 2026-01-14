#!/bin/bash
set -e

echo "🏗️  FORCE REBUILDING FRONTEND..."

# 1. GO TO FRONTEND DIR
cd /home/ubuntu/integrated_predictor/nestiq-predict-main

# 2. CHECK IF DIST EXISTS (DEBUG)
if [ -f "dist/index.html" ]; then
    echo "ℹ️  Found existing build. Rebuilding anyway to be sure..."
else
    echo "⚠️  dist/index.html MISSING! This explains the loop."
fi

# 3. BUILD
echo " -> Running npm install..."
npm install
echo " -> Running npm run build..."
npm run build

# 4. VERIFY BUILD
if [ ! -f "dist/index.html" ]; then
    echo "❌ BUILD FAILED! dist/index.html still missing."
    exit 1
fi
echo "✅ Build Successful."

# 5. DEPLOY TO VAR/WWW
echo " -> Copying to /var/www/nestiq..."
sudo cp -r dist/* /var/www/nestiq/
sudo chown -R www-data:www-data /var/www/nestiq
sudo chmod -R 755 /var/www/nestiq

# 6. VERIFY DEPLOYMENT
echo " -> verifying /var/www/nestiq/ contents:"
ls -la /var/www/nestiq/

if [ -f "/var/www/nestiq/index.html" ]; then
    echo "🎉 index.html is present in webroot!"
else
    echo "❌ index.html is MISSING from webroot!"
fi

echo " -> Restarting Nginx..."
sudo systemctl restart nginx

echo "=========================================="
echo "✅ REBUILD & DEPLOY COMPLETE"
echo "Try your site now."
echo "=========================================="
