#!/data/data/com.termux/files/usr/bin/bash
export DEBIAN_FRONTEND=noninteractive

GREEN='\033[0;32m'
RESET='\033[0m'

run_step() {
    local step="$1"
    local desc="$2"
    local cmd="$3"
    printf "%-48s" "[$step] $desc..."
    eval "$cmd" > /dev/null 2>&1 || true
    echo -e " ${GREEN}✓${RESET}"
}

echo ""

if [ ! -d "$HOME/storage" ]; then
    termux-setup-storage > /dev/null 2>&1 || true
fi

run_step "1/7" "Updating system & fixing broken packages" "yes '' 2>/dev/null | pkg update -y -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold'"
run_step "2/7" "Installing Python3" "pkg install -y python python-pip"
run_step "3/7" "Installing python-pip" "pip install --no-cache-dir --break-system-packages rich colorama || pip install --no-cache-dir rich colorama"
run_step "4/7" "Installing libusb" "pkg install -y libusb pv sed p7zip unrar unzip tar git"
run_step "5/7" "Installing termux-api" "pkg install -y termux-api"
run_step "6/7" "Installing termux-adb" "pkg install -y termux-adb || true; ln -sf $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot 2>/dev/null || true; ln -sf $PREFIX/bin/termux-adb $PREFIX/bin/adb 2>/dev/null || true"

INSTALL_DIR="$HOME/.ritiktool"
run_step "7/7" "Installing ritiktool" "rm -rf $INSTALL_DIR && git clone https://github.com/rittik55/ritiktool.git $INSTALL_DIR"

echo '#!/data/data/com.termux/files/usr/bin/bash' > "$PREFIX/bin/ritiktool"
echo 'python3 "$HOME/.ritiktool/run.py" "$@"' >> "$PREFIX/bin/ritiktool"
chmod +x "$PREFIX/bin/ritiktool"

echo -e "\n${GREEN}✓ Installation completed successfully${RESET}\n"
echo -e "Run command: ${GREEN}ritiktool${RESET}\n"
