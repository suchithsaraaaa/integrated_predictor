#!/bin/bash
echo "🔍 INSPECTING NGINX CONFIGURATION..."
cat /etc/nginx/sites-available/nestiq
echo "-----------------------------------"
echo "🔍 ERROR LOGS (Nginx - Last 20)"
sudo tail -n 20 /var/log/nginx/error.log
