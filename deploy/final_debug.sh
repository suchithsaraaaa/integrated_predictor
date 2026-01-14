#!/bin/bash
echo "🔍 FINAL DEBUG CHECK..."

# 1. CHECK NGINX CONFIG
echo " -> Nginx Sites Enabled:"
ls -l /etc/nginx/sites-enabled/
echo " -> Content of current config:"
cat /etc/nginx/sites-enabled/nestiq

# 2. CHECK PORTS
echo " -> Listening Ports:"
sudo ss -tulpn | grep -E ":80|:443"

# 3. CHECK VIDEO FILE
echo " -> Video File Check:"
ls -l /var/www/nestiq/videos/home.mp4

# 4. CURL TESTS
echo " -> Local HTTP Curl (Video):"
curl -I http://127.0.0.1/videos/home.mp4
echo " -> Local HTTPS Curl (Index) - (Might fail if cert invalid for localhost):"
curl -k -I https://127.0.0.1/

# 5. SSL CERT CHECK
echo " -> SSL Certs:"
ls -l /etc/letsencrypt/live/

echo "=========================================="
