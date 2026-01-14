#!/bin/bash
echo "🛡️ DEEP FIREWALL & HAIRPIN TEST..."

# 1. IPTABLES FULL DUMP
echo " -> Dumping IP Tables Rules:"
sudo iptables -S

# 2. CHECK HTTPS LISTENER
echo " -> Is anyone on 443?"
sudo ss -tulpn | grep :443 || echo "NO ONE on 443 (HTTPS is DEAD)."

# 3. HAIRPIN TEST (Can I see myself?)
PUBLIC_IP=$(curl -s ifconfig.me)
echo " -> Curling Public IP ($PUBLIC_IP) from inside..."
curl -v --connect-timeout 5 http://$PUBLIC_IP/ 2>&1 | head -n 10

echo "=========================================="
echo "ANALYSIS:"
echo "1. If Curl works here, the server is innocent. The block is AWS or Your ISP."
echo "2. If Curl fails here too, the Server OS is blocking its own IP."
echo "=========================================="
