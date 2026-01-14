#!/bin/bash
set -e

echo "🧪 STARTING ISOLATION TEST..."

# 1. SETUP TEST FILE
echo " -> Creating /var/www/nestiq/test.html..."
sudo mkdir -p /var/www/nestiq
echo "<h1>HELLO WORLD - NGINX IS WORKING</h1>" | sudo tee /var/www/nestiq/test.html > /dev/null
sudo chown www-data:www-data /var/www/nestiq/test.html

# 2. NUKE CONFIG & WRITE SIMPLEST POSSIBLE CONFIG
echo " -> Writing Barebones Nginx Config..."
sudo rm -f /etc/nginx/sites-enabled/*

sudo bash -c "cat > /etc/nginx/sites-available/simple_test <<EOF
server {
    listen 80;
    server_name _;
    root /var/www/nestiq;
    index test.html;

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/simple_test /etc/nginx/sites-enabled/

# 3. RESTART
echo " -> Restarting Nginx..."
sudo systemctl restart nginx

# 4. TEST LOCAL
echo " -> Testing curl http://localhost/ ..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
echo "HTTP CODE: $HTTP_CODE"

if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ SUCCESS: Nginx can serve files!"
    echo "The issue is likely the React 'index.html' or the specific try_files directive."
else
    echo "❌ FAILURE: Nginx returned $HTTP_CODE."
    echo "Dump of error log:"
    sudo tail -n 5 /var/log/nginx/error.log
fi
