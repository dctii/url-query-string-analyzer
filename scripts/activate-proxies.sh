#!/bin/zsh
# For macOS

ylw='\033[33m'
gr='\033[32m'
rst='\033[0m'

# 🚧 Add your user password here or else the scripts may break.
psw="yourpassword"
IPADDR=$(ipconfig getifaddr en0)
PORT=8081

echo "${ylw}Enabling web proxies...${rst}"
echo $psw | sudo -S networksetup -setwebproxy "Wi-Fi" ${IPADDR} ${PORT}
echo $psw | sudo -S networksetup -setsecurewebproxy "Wi-Fi" ${IPADDR} ${PORT}

echo "${ylw}\nChecking web proxies...${rst}\n"

zsh ~/.local-scripts/proxy_check.sh

echo "\n${gr}Web proxies enabled...${rst}\n"

unset psw