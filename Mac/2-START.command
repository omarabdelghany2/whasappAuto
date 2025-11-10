#!/bin/bash
# WhatsApp Scheduler - macOS Starter
# Double-click this file to start the app

# Get the parent directory (go up one level from Mac folder)
cd "$(dirname "$0")/.."

# Clear screen for better visibility
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          WhatsApp Scheduler - Starting...             ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "❌ ERROR: pipenv is not installed!"
    echo ""
    echo "Please run installation first:"
    echo "  → Double-click '1-INSTALL.command' in the Mac folder"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Check if pipenv environment exists
if ! pipenv --venv &> /dev/null; then
    echo "❌ ERROR: App is not installed yet!"
    echo ""
    echo "Please run installation first:"
    echo "  → Double-click '1-INSTALL.command' in the Mac folder"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Check if Frontend dependencies are installed
if [ ! -d "Frontend/node_modules" ]; then
    echo "❌ ERROR: Frontend dependencies not installed!"
    echo ""
    echo "Please run installation first:"
    echo "  → Double-click '1-INSTALL.command' in the Mac folder"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo "Checking dependencies..."
echo ""

# Check and install any missing Python dependencies
pipenv install --deploy

if [ $? -ne 0 ]; then
    echo "⚠ Some dependencies may be missing. Attempting to install..."
    pipenv install
fi

echo ""
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

# Add pipenv to PATH if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# Run the Python starter using pipenv
pipenv run python3 start.py

# If we get here, the app was stopped
echo ""
echo "App stopped."
read -p "Press Enter to close..."
