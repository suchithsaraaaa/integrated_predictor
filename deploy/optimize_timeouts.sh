#!/bin/bash

# Define paths
NGINX_CONF="/etc/nginx/sites-available/nestiq"
SERVICE_FILE="/etc/systemd/system/nestiq.service"

echo "⏳ Optimizing Timeouts for Heavy Data Fetching..."

# 1. Update Nginx Timeout
if [ -f "$NGINX_CONF" ]; then
    echo "   Configuring Nginx..."
    # Check if timeout settings already exist, if not, inject them
    if grep -q "proxy_read_timeout" "$NGINX_CONF"; then
        # Use sed to replace existing values
        sudo sed -i 's/proxy_read_timeout [0-9]*;/proxy_read_timeout 300;/g' "$NGINX_CONF"
        sudo sed -i 's/proxy_connect_timeout [0-9]*;/proxy_connect_timeout 300;/g' "$NGINX_CONF"
        sudo sed -i 's/proxy_send_timeout [0-9]*;/proxy_send_timeout 300;/g' "$NGINX_CONF"
    else
        # Inject into the location /api/ block
        # We look for 'proxy_pass' and append timeout settings before it
        # Actually safer to put it in the server block or location block
        sudo sed -i '/location \/ {/a \        proxy_read_timeout 300;\n        proxy_connect_timeout 300;\n        proxy_send_timeout 300;' "$NGINX_CONF"
        
        # Also ensure /api/ gets it if defined separately, but usually usually properties inherit or are global in 'http'
        # Let's just add it globally to the http block in nginx.conf for safety? No, site config is better.
        # Adding to the main server block
        sudo sed -i '/server_name/a \    client_body_timeout 300;\n    client_header_timeout 300;' "$NGINX_CONF"
    fi
    
    echo "   Nginx configuration updated."
else
    echo "⚠️  Nginx config not found at $NGINX_CONF"
fi

# 2. Update Gunicorn Timeout
if [ -f "$SERVICE_FILE" ]; then
    echo "   Configuring Gunicorn..."
    # Update the ExecStart line to include --timeout 300
    if grep -q "\-\-timeout" "$SERVICE_FILE"; then
         sudo sed -i 's/--timeout [0-9]*/--timeout 300/g' "$SERVICE_FILE"
    else
         # Append timeout to gunicorn command
         sudo sed -i 's/gunicorn/gunicorn --timeout 300/g' "$SERVICE_FILE"
    fi
    echo "   Gunicorn service updated."
else
    echo "⚠️  Systemd service not found at $SERVICE_FILE"
fi

# 3. Reload Everything
echo "🔄 Restarting Services..."
sudo systemctl daemon-reload
sudo systemctl restart nestiq
sudo nginx -t && sudo systemctl restart nginx

echo "✅ Timeouts increased to 300 seconds (5 minutes)."
echo "   NOTE: First fetch for Zurich might still take ~45-60s on t2.micro, but it won't error out now."
