#!/bin/bash
set -e

echo "🔧 FIXING SYNTAX & RETESTING..."

# Ensure test files exist
sudo bash -c "echo 'I AM SIMPLE TEXT' > /var/www/nestiq/simple.txt"
if [ -f /var/www/nestiq/index.html ]; then
    sudo mv /var/www/nestiq/index.html /var/www/nestiq/app.html
fi

# FIX: Use 3 backslashes to survive double shell expansion
# 1. Outer Shell: \\\$ -> \$
# 2. Inner Bash Heredoc: \$ -> $ (Literal Dollar)
sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;
    root /var/www/nestiq;
    
    location /simple.txt {
        try_files \\\$uri =404;
    }

    location /app.html {
        try_files \\\$uri =404;
    }
}
EOF"

echo " -> Restarting Nginx..."
sudo systemctl restart nginx

echo " -> Testing /simple.txt"
curl -I http://localhost/simple.txt

echo " -> Testing /app.html"
curl -I http://localhost/app.html

echo "=========================================="
echo "Verify HEADERS above."
echo "If 200 OK: The caching/index logic was the problem."
echo "If 301/403: The filesystem folder itself is cursed."
echo "=========================================="
