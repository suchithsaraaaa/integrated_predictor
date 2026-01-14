#!/bin/bash
set -e

echo "🧱 INCREMENTAL FIX: STEP 1 (STATIC ONLY)..."

# 1. STOP EVERYTHING
sudo systemctl stop nginx

# 2. WRITE MINIMAL CONFIG (No API, No SPA Fallback)
echo " -> Writing Minimal Static Config..."
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;
    root /var/www/nestiq;
    index index.html;

    # Just serve existing files. Return 404 if missing.
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/

# 3. VERIFY FILE EXISTS
if [ ! -f /var/www/nestiq/index.html ]; then
    echo "❌ CRITICAL: index.html is missing! Creating dummy."
    echo "<h1>DUMMY INDEX</h1>" | sudo tee /var/www/nestiq/index.html
fi

# 4. START
sudo systemctl start nginx

# 5. TEST
echo " -> Testing Request..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
echo "HTTP CODE: $RESPONSE"

if [ "$RESPONSE" == "200" ]; then
    echo "✅ STEP 1 SUCCESS: Static files are serving."
    echo "The site should be visible (but API calls will fail)."
else
    echo "❌ STEP 1 FAILED: Still getting $RESPONSE."
    echo "Outputting Headers:"
    curl -I http://localhost/
fi
