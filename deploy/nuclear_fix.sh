#!/bin/bash
set -e

echo "☢️  NUCLEAR FIX INITIATED..."

# 1. STOP & KILL NGINX (Ensure no zombie processes)
echo " -> Stopping Nginx Service..."
sudo systemctl stop nginx || true
echo " -> Killing lingering processes..."
sudo pkill nginx || true
sleep 2

# 2. CLEAN CONFIGS (Remove ANY lurking redirects)
echo " -> Cleaning Config Directories..."
sudo rm -f /etc/nginx/sites-enabled/*
sudo rm -f /etc/nginx/conf.d/*

# 3. ENSURE TEST FILE
sudo mkdir -p /var/www/nestiq
echo "<h1>VICTORY - SERVER IS RESET</h1>" | sudo tee /var/www/nestiq/index.html > /dev/null
sudo chown -R www-data:www-data /var/www/nestiq

# 4. WRITE PURE STATIC CONFIG (No try_files, No complex logic)
echo " -> Writing Pure Config..."
sudo bash -c "cat > /etc/nginx/sites-available/nuclear <<EOF
server {
    listen 80;
    server_name _;
    
    # HARDCODED ROOT
    root /var/www/nestiq;
    index index.html;
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nuclear /etc/nginx/sites-enabled/

# 5. START FRESH
echo " -> Starting Nginx..."
sudo systemctl start nginx

# 6. VERIFY WITH CURL -v (Follow Redirects)
echo "--------------------------------"
echo "✅ Testing connection..."
# -L follows redirects, -v shows headers
curl -v http://localhost/ 2>&1 | head -n 20

echo "--------------------------------"
echo "If you see 'VICTORY' in the output above, we are back in business."
