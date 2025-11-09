#!/bin/bash
# WhatsApp Scheduler - Linux Installer
# Double-click this file and select "Run" or "Execute"
# Or right-click → Properties → Permissions → Allow executing as program

# Get the parent directory (go up one level from Linux folder)
cd "$(dirname "$0")/.."

# Function to pause at the end
pause() {
    echo ""
    read -p "Press Enter to close..."
}

# Clear screen for better visibility
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        WhatsApp Scheduler - Installation              ║"
echo "║                  for Linux                            ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "This will install all required dependencies..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python first:"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get update"
    echo "    sudo apt-get install python3 python3-pip"
    echo ""
    echo "  Fedora/RHEL:"
    echo "    sudo dnf install python3 python3-pip"
    echo ""
    echo "  Arch:"
    echo "    sudo pacman -S python python-pip"
    echo ""
    echo "After installing Python, double-click this file again."
    pause
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js is not installed!"
    echo ""
    echo "Please install Node.js first:"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -"
    echo "    sudo apt-get install -y nodejs"
    echo ""
    echo "  Fedora/RHEL:"
    echo "    curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -"
    echo "    sudo dnf install -y nodejs"
    echo ""
    echo "  Or download from: https://nodejs.org/"
    echo ""
    echo "After installing Node.js, double-click this file again."
    pause
    exit 1
fi

echo "✓ Python 3 is installed"
echo "✓ Node.js is installed"
echo ""
echo "Starting installation..."
echo ""

# Make sure install.py is executable
chmod +x install.py 2>/dev/null

# Run the Python installer
python3 install.py

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                        ║"
    echo "║         ✓ Installation Completed Successfully!        ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "Next step:"
    echo "  → Double-click '2-START.sh' in the Linux folder"
    echo ""
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    echo ""
fi

pause
