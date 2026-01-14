#!/bin/bash
echo "🕵️ SHERLOCK IS INVESTIGATING..."

# 1. READ MAIN CONFIG
echo " -> Reading /etc/nginx/nginx.conf..."
cat /etc/nginx/nginx.conf

# 2. CHECK INCLUDES
echo " -> Checking /etc/nginx/sites-enabled/:"
ls -F /etc/nginx/sites-enabled/
echo " -> Checking /etc/nginx/conf.d/:"
ls -F /etc/nginx/conf.d/

# 3. CHECK PORT OWNERSHIP
echo " -> Who is on Port 80?"
sudo ss -tulpn | grep :80

# 4. CHECK DEFAULT FILE
if [ -f /etc/nginx/sites-available/default ]; then
    echo " -> Contents of default site (if exists):"
    cat /etc/nginx/sites-available/default
fi

echo "=========================================="
echo "Report Complete."
echo "=========================================="
