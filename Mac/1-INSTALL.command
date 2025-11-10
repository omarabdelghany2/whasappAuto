#!/bin/bash
# WhatsApp Scheduler - macOS Auto-Installer
# This will install EVERYTHING you need automatically
# Double-click this file to install

# Get the parent directory (go up one level from Mac folder)
cd "$(dirname "$0")/.."

# Clear screen for better visibility
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║     WhatsApp Scheduler - Automatic Installation       ║"
echo "║                  for macOS                            ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "This will automatically install everything you need:"
echo "  ✓ Homebrew (package manager)"
echo "  ✓ Python 3"
echo "  ✓ Node.js"
echo "  ✓ All dependencies"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Install Homebrew if not present
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Homebrew (Mac package manager)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command_exists brew; then
    echo "✓ Homebrew is already installed"
else
    echo "Installing Homebrew..."
    echo "This may take a few minutes and will ask for your password..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    if command_exists brew; then
        echo "✓ Homebrew installed successfully!"
    else
        echo "❌ Failed to install Homebrew"
        echo "Please install manually from: https://brew.sh"
        read -p "Press Enter to close..."
        exit 1
    fi
fi

echo ""

# Step 2: Install Python 3
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Checking Python 3..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python 3 is already installed (version: $PYTHON_VERSION)"
else
    echo "Installing Python 3..."
    brew install python3

    if command_exists python3; then
        echo "✓ Python 3 installed successfully!"
    else
        echo "❌ Failed to install Python 3"
        read -p "Press Enter to close..."
        exit 1
    fi
fi

echo ""

# Step 3: Install Node.js
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Checking Node.js..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command_exists node; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js is already installed (version: $NODE_VERSION)"
else
    echo "Installing Node.js..."
    brew install node

    if command_exists node; then
        echo "✓ Node.js installed successfully!"
    else
        echo "❌ Failed to install Node.js"
        read -p "Press Enter to close..."
        exit 1
    fi
fi

echo ""

# Step 4: Install Chrome (optional but recommended)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Checking Google Chrome..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✓ Google Chrome is already installed"
else
    echo "Installing Google Chrome..."
    brew install --cask google-chrome

    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "✓ Google Chrome installed successfully!"
    else
        echo "⚠ Chrome installation may have failed"
        echo "You can install it manually from: https://www.google.com/chrome/"
    fi
fi

echo ""

# Step 5: Install pipenv
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Installing pipenv (Python environment manager)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v pipenv &> /dev/null; then
    echo "✓ pipenv is already installed"
else
    echo "Installing pipenv..."
    pip3 install --user pipenv

    # Add pipenv to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi

    if command -v pipenv &> /dev/null; then
        echo "✓ pipenv installed successfully!"
    else
        echo "⚠ pipenv installed but not in PATH"
        echo "Adding to PATH..."
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

echo ""

# Step 6: Install Python dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Installing Python dependencies with pipenv..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "This may take 3-5 minutes. Please wait..."
echo ""

# Install Python dependencies using pipenv
pipenv install

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed successfully!"
else
    echo "❌ Failed to install Python dependencies"
    read -p "Press Enter to close..."
    exit 1
fi

echo ""

# Step 7: Install Frontend dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 7: Installing Frontend dependencies..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d "Frontend" ]; then
    echo "❌ Frontend directory not found!"
    read -p "Press Enter to close..."
    exit 1
fi

cd Frontend
echo "Installing Node.js packages (this may take a few minutes)..."
npm install

if [ $? -eq 0 ]; then
    echo "✓ Frontend dependencies installed successfully!"
else
    echo "❌ Failed to install Frontend dependencies"
    cd ..
    read -p "Press Enter to close..."
    exit 1
fi

cd ..

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                        ║"
    echo "║         ✓ Installation Completed Successfully!        ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "Everything is ready!"
    echo ""
    echo "Next step:"
    echo "  → Double-click '2-START.command' in the Mac folder"
    echo ""
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    echo ""
fi

read -p "Press Enter to close..."
