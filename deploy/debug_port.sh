#!/bin/bash
set -e

echo "🔬 DEBUG PORT 8080 & STATIC STRING..."

# 1. WRITE TEST CONFIG (Port 8080, No Filesystem)
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 8080;
    server_name _;

    location / {
        return 200 'HELLO FROM 8080 - NGINX IS WORKING';
        add_header Content-Type text/plain;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/

# 2. RESTART
sudo systemctl restart nginx

# 3. TEST 8080
echo " -> Testing Port 8080..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/)
echo "HTTP CODE: $RESPONSE"

if [ "$RESPONSE" == "200" ]; then
    echo "✅ SUCCESS: Port 8080 + Static String works."
    echo "This proves Nginx is OK. The issue is Port 80 or the Filesystem."
else
    echo "❌ FAILED: Still getting $RESPONSE on 8080."
    curl -I http://localhost:8080/
fi
