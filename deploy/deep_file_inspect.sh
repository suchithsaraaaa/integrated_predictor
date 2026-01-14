#!/bin/bash
set -e

echo "🔎 DEEP FILE INSPECT..."

# 1. SETUP TEST FILES
echo " -> Preparing files in /var/www/nestiq/"
sudo bash -c "echo 'I AM SIMPLE TEXT' > /var/www/nestiq/simple.txt"

# Rename index.html to app.html to stop 'index' directive magic
if [ -f /var/www/nestiq/index.html ]; then
    sudo mv /var/www/nestiq/index.html /var/www/nestiq/app.html
fi

# 2. CONFIG NGINX (Static Serving, Explicit, No Magic)
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;
    root /var/www/nestiq;
    
    # Intentionally valid ONLY for these files
    location /simple.txt {
        try_files \$uri =404;
    }

    location /app.html {
        try_files \$uri =404;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 3. TEST
echo " -> Testing /simple.txt"
curl -I http://localhost/simple.txt

echo " -> Testing /app.html (Formerly index.html)"
curl -I http://localhost/app.html

echo "=========================================="
echo "Verify HEADERS above."
echo "If 200 OK: The caching/index logic was the problem."
echo "If 301/403: The filesystem folder itself is cursed."
echo "=========================================="

# Restore index.html name for safety if needed later
# sudo mv /var/www/nestiq/app.html /var/www/nestiq/index.html
