#!/bin/bash
# ============================================
# Mysterium Node Setup for Oracle Cloud Free Tier
# Run this ONCE after SSH into your Oracle instance
# ============================================

set -e

echo "=== [1/5] Update system ==="
sudo apt update && sudo apt upgrade -y

echo "=== [2/5] Install Docker ==="
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

echo "=== [3/5] Open firewall ports ==="
# Oracle Ubuntu uses iptables by default
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 4449 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p udp --dport 1194 -j ACCEPT
sudo netfilter-persistent save

echo "=== [4/5] Start Mysterium Node ==="
sudo docker run -d \
    --name myst \
    --cap-add NET_ADMIN \
    --net host \
    -v myst-data:/var/lib/mysterium-node \
    --restart always \
    mysteriumnetwork/myst:latest \
    service --agreed-terms-and-conditions

echo "=== [5/5] Setup anti-idle cron ==="
# Prevent Oracle from reclaiming idle instance
# Runs CPU burst 5 seconds every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * nice -n 19 timeout 5 sha256sum /dev/zero > /dev/null 2>&1") | crontab -

echo ""
echo "============================================"
echo "  SETUP COMPLETE!"
echo "============================================"
echo ""
echo "Mysterium Dashboard: http://$(curl -s ifconfig.me):4449"
echo ""
echo "NEXT STEPS:"
echo "1. Open the dashboard URL above in your browser"
echo "2. Set a password for the node"
echo "3. Claim your node at: https://mystnodes.com"
echo "4. (Optional) Stake MYST tokens for higher earnings"
echo ""
echo "Check node status: sudo docker logs myst"
echo "============================================"
