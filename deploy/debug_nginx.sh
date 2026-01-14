#!/bin/bash
echo "🕵️‍♂️ DEBUGGING NGINX..."

echo "1. Checking File Structure in /var/www/nestiq:"
ls -F /var/www/nestiq/

echo "--------------------------------"

echo "2. Checking index.html presence:"
if [ -f /var/www/nestiq/index.html ]; then
    echo "✅ index.html FOUND."
else
    echo "❌ index.html MISSING!"
    echo "   (Did it get copied as /var/www/nestiq/dist/index.html?)"
    ls -F /var/www/nestiq/dist/ 2>/dev/null
fi

echo "--------------------------------"

echo "3. Testing Local Request (curl -I):"
curl -I http://localhost

echo "--------------------------------"

echo "4. Checking Nginx Error Log (Last 5 lines):"
sudo tail -n 5 /var/log/nginx/error.log
