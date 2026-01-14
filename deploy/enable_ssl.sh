#!/bin/bash
set -e

echo "🔒 ENABLING SSL (HTTPS) WITH NIP.IO..."

# 1. DETECT IP & DOMAIN
# Use a reliable external echo service
PUBLIC_IP=$(curl -s ifconfig.me)
DOMAIN="${PUBLIC_IP}.nip.io"

echo " -> Public IP: $PUBLIC_IP"
echo " -> Magic Domain: $DOMAIN"

# 2. UPDATE NGINX CONFIG
echo " -> Updating Nginx server_name..."
# Replace generic catch-all (_) with specific domain for Certbot
sudo sed -i "s/server_name _;/server_name $DOMAIN;/g" /etc/nginx/sites-available/nestiq

# Reload to apply name change
sudo systemctl reload nginx

# 3. INSTALL CERTBOT
echo " -> Installing Certbot..."
sudo apt-get update -y
sudo apt-get install -y certbot python3-certbot-nginx

# 4. REQUEST CERTIFICATE
echo " -> Requesting Let's Encrypt Certificate..."
# --non-interactive: Don't ask questions
# --agree-tos: Agree to terms
# --register-unsafely-without-email: Don't require email (Simpler for automation)
# --redirect: Update Nginx to force Redirect HTTP->HTTPS
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect

# 5. FINAL RELOAD
sudo systemctl reload nginx

echo "=========================================="
echo "✅ SSL ENABLED!"
echo "Your secure URL is: https://$DOMAIN"
echo "=========================================="
