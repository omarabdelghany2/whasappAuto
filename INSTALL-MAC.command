#!/bin/bash
# WhatsApp Scheduler - macOS Installer
# Double-click this file to install

# Get the directory where this script is located
cd "$(dirname "$0")"

# Clear screen for better visibility
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        WhatsApp Scheduler - Installation              ║"
echo "║                  for macOS                            ║"
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
    echo "  Option 1: Download from https://www.python.org/downloads/"
    echo "  Option 2: Install Homebrew, then run: brew install python3"
    echo ""
    echo "After installing Python, double-click this file again."
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js is not installed!"
    echo ""
    echo "Please install Node.js first:"
    echo "  Option 1: Download from https://nodejs.org/"
    echo "  Option 2: Install Homebrew, then run: brew install node"
    echo ""
    echo "After installing Node.js, double-click this file again."
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo "✓ Python 3 is installed"
echo "✓ Node.js is installed"
echo ""
echo "Starting installation..."
echo ""

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
    echo "  → Double-click 'START-MAC.command' to run the app"
    echo ""
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    echo ""
fi

read -p "Press Enter to close..."
