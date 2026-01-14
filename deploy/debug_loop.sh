#!/bin/bash
set -e

echo "🕵️‍♂️ DEBUGGING PERMISSIONS & LOOP..."

# 1. CHECK PATH PERMISSIONS (Walk the tree)
echo " -> Checking full path permissions..."
# namei might not be installed, so manual ls
ls -ld /var
ls -ld /var/www
ls -ld /var/www/nestiq
ls -l /var/www/nestiq/index.html

# 2. CHECK IF NGINX CAN READ IT (As www-data)
echo " -> Testing readability as www-data user..."
sudo -u www-data head -n 1 /var/www/nestiq/index.html && echo "✅ www-data can read file." || echo "❌ www-data CANNOT read file!"

# 3. BREAK THE LOOP (Change config to return 404 instead of fallback)
echo " -> Modifying Nginx to break loop..."
# Removing /index.html fallback temporarily
sudo sed -i 's/try_files $uri $uri\/ \/index.html;/try_files $uri $uri\/ =404;/g' /etc/nginx/sites-available/nestiq

echo " -> Reloading Nginx..."
sudo systemctl reload nginx

# 4. CURL TEST
echo " -> Curling localhost..."
curl -v http://localhost/ 2>&1 | head -n 10

echo "--------------------------------"
echo "If you see '403 Forbidden', it's permissions."
echo "If you see '404 Not Found', the file path is wrong."
echo "If you see '200 OK', the file works but SPA routing was looping."
echo "--------------------------------"
