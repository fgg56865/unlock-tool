#!/bin/bash

# Terminal Colors
GREEN="\033[92m"
YELLOW="\033[93m"
CYAN="\033[96m"
RED="\033[91m"
RESET="\033[0m"

echo -e "${CYAN}[*] Updating Termux packages...${RESET}"
pkg update && pkg upgrade -y

echo -e "${CYAN}[*] Installing Python, Git & Android Tools...${RESET}"
pkg install python git android-tools termux-api -y

echo -e "${CYAN}[*] Downloading tool.py from GitHub repository...${RESET}"
curl -s -L -O https://raw.githubusercontent.com/fgg56865/unlock-tool/main/tool.py

if [ -f "tool.py" ]; then
    chmod +x tool.py
    echo -e "${GREEN}[+] tool.py downloaded & permission granted successfully!${RESET}"
else
    echo -e "${RED}[-] Error: Failed to download tool.py! Please check your GitHub repository files.${RESET}"
    exit 1
fi

echo -e "\n${GREEN}==================================================${RESET}"
echo -e "${GREEN}       INSTALLATION COMPLETED SUCCESSFULLY!       ${RESET}"
echo -e "${GREEN}==================================================${RESET}"
echo -e "${YELLOW}To run the tool anytime later, simply type:${RESET}"
echo -e "${CYAN}python tool.py${RESET}\n"
