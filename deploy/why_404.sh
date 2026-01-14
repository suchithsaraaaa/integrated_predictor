#!/bin/bash
echo "🕵️ WHY IS THIS 404? (LOG ANALYSIS)..."

# 1. TRIGGER THE ERROR
echo " -> Triggering 404 on /videos/home.mp4..."
curl -s -o /dev/null http://localhost/videos/home.mp4

# 2. READ THE LOGS (The absolute truth)
echo " -> NGINX ERROR LOG (Last 5 lines):"
sudo tail -n 5 /var/log/nginx/error.log

# 3. CHECK PATH PERMISSIONS (Chain)
echo " -> Path Permissions:"
namei -l /var/www/nestiq/videos/home.mp4

echo "=========================================="
echo "Check the log above:"
echo "- 'No such file': The path Nginx is looking in is NOT what we think."
echo "- 'Permission denied': Folder permissions are wrong."
echo "=========================================="
