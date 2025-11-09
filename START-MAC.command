#!/bin/bash
# WhatsApp Scheduler - macOS Starter
# Double-click this file to start the app

# Get the directory where this script is located
cd "$(dirname "$0")"

# Clear screen for better visibility
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          WhatsApp Scheduler - Starting...             ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if dependencies are installed
if [ ! -d "Frontend/node_modules" ]; then
    echo "❌ ERROR: App is not installed yet!"
    echo ""
    echo "Please run installation first:"
    echo "  → Double-click 'INSTALL-MAC.command'"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo "Starting WhatsApp Scheduler..."
echo ""
echo "The app will open in your browser at:"
echo "  http://localhost:5173"
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║              TO STOP THE APP:                          ║"
echo "║         Press Ctrl+C in this window                    ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Run the Python starter
python3 start.py

# If we get here, the app was stopped
echo ""
echo "App stopped."
read -p "Press Enter to close..."
