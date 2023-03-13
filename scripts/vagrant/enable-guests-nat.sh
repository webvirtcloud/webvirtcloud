#!/usr/bin/env bash
set -e

# Ubuntu, Debian 
if [[ $(ip r s | grep 169.254.0.0/16) ]]; then
    sudo ip r d 169.254.0.0/16
fi

# Default iptables rules for NAT
sudo iptables -I INPUT -d 172.64.0.0/24 -j ACCEPT
sudo iptables -I FORWARD -d 172.64.0.0/24  -j ACCEPT
sudo iptables -I FORWARD -d 192.168.33.0/24 -j ACCEPT
sudo iptables -I FORWARD -d 10.132.0.0/24 -j ACCEPT
sudo iptables -t nat -I POSTROUTING -d 172.64.0.0/24 -j MASQUERADE
sudo iptables -t nat -I POSTROUTING -s 192.168.33.0/24 -j MASQUERADE
sudo iptables -t nat -I POSTROUTING -d 10.132.0.0/24 -j MASQUERADE

exit 0
