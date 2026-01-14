#!/bin/bash
set -e

echo "🔬 DEBUG PORT 80 + STATIC STRING..."

# 1. WRITE TEST CONFIG (Port 80, No Filesystem)
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    location / {
        return 200 'HELLO FROM PORT 80 - NO FILESYSTEM';
        add_header Content-Type text/plain;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/

# 2. RESTART
sudo systemctl restart nginx

# 3. TEST 80
echo " -> Testing Port 80..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
echo "HTTP CODE: $RESPONSE"

if [ "$RESPONSE" == "200" ]; then
    echo "✅ SUCCESS: Port 80 responds 200 (When not touching disk)."
    echo "Conclusion: The issue is 100% Filesystem/Permissions."
else
    echo "❌ FAILED: Port 80 returned $RESPONSE."
    echo "Conclusion: Something is interfering with Port 80 globally."
    curl -I http://localhost/
fi
