#!/bin/bash
echo "🛡️ DEBUGGING EXTERNAL CONNECTION..."

# 1. CHECK FIREWALL (UFW)
echo " -> Checking UFW Status..."
sudo ufw status verbose

# 2. CHECK SOCKET BINDING
echo " -> Checking who is listening on Port 80..."
# Look for 0.0.0.0:80 (Good) vs 127.0.0.1:80 (Bad for external)
sudo ss -tulpn | grep :80

# 3. CHECK PUBLIC IP
echo " -> Verifying Public IP..."
CURRENT_IP=$(curl -s ifconfig.me)
echo "Current Public IP: $CURRENT_IP"

# 4. CHECK IPTABLES (Raw rules)
echo " -> Checking IP Tables (Input Chain)..."
sudo iptables -L INPUT -n --line-numbers | grep "dpt:80" || echo "No explicit Port 80 rules found."

echo "=========================================="
echo "ANALYSIS:"
echo "1. If UFW is 'active' and no '80/tcp ALLOW', run: sudo ufw allow 80/tcp"
echo "2. If 'ss' shows '127.0.0.1:80', Nginx config is restricted to localhost."
echo "3. If IP is different, update your browser URL."
echo "=========================================="
