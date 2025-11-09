#!/bin/bash
# WhatsApp Scheduler - Linux Starter
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
echo "║          WhatsApp Scheduler - Starting...             ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if dependencies are installed
if [ ! -d "Frontend/node_modules" ]; then
    echo "❌ ERROR: App is not installed yet!"
    echo ""
    echo "Please run installation first:"
    echo "  → Double-click '1-INSTALL.sh' in the Linux folder"
    echo ""
    pause
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

# Make sure start.py is executable
chmod +x start.py 2>/dev/null

# Run the Python starter
python3 start.py

# If we get here, the app was stopped
echo ""
echo "App stopped."
pause
