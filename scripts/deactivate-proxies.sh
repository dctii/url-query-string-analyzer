#!/bin/zsh
# For macOS

ylw='\033[33m'
gr='\033[32m'
rst='\033[0m'

# 🚧 Add your user password here or else the scripts may break.
psw="yourpassword"

echo "${ylw}\nDisabling web proxies...${rst}"
echo $psw | sudo -S networksetup -setwebproxystate "Wi-Fi" off
echo $psw | sudo -S networksetup -setsecurewebproxystate "Wi-Fi" off 

echo "${ylw}\nChecking web proxies...${rst}\n"
zsh ~/.local-scripts/proxy_check.sh

echo "\n${gr}Web proxies disabled.${rst}"

unset psw