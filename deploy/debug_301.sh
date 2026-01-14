#!/bin/bash
set -e

echo "🕵️‍♂️ DEBUGGING 301 REDIRECT..."

# 1. CHECK ENABLED SITES
echo " -> contents of sites-enabled:"
ls -l /etc/nginx/sites-enabled/

# 2. TEST DIRECT FILE ACCESS
echo " -> Testing /index.html directly:"
# If this works (200), then 'index' directive or directory handling is broken.
curl -I http://localhost/index.html

# 3. DUMP FULL CONFIG (Grep for 301/302)
echo " -> Scanning config for redirects..."
sudo nginx -T | grep "return 30" || echo "No explicit redirects found."

# 4. DUMP SERVER BLOCK HEADERS
echo " -> checking server blocks:"
sudo nginx -T | grep "server_name"

echo "=========================================="
echo "If /index.html returns 200, the issue 'location /' logic."
echo "If /index.html returns 301, we have a global redirect."
echo "=========================================="
