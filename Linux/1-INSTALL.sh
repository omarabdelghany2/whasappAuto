#!/bin/bash
# WhatsApp Scheduler - Linux Auto-Installer
# This will install EVERYTHING you need automatically
# Double-click this file and select "Run" or "Execute"

# Get the parent directory
cd "$(dirname "$0")/.."

# Function to pause
pause() {
    echo ""
    read -p "Press Enter to continue..."
}

# Clear screen
clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║     WhatsApp Scheduler - Automatic Installation       ║"
echo "║                  for Linux                            ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "This will automatically install everything you need:"
echo "  ✓ Python 3"
echo "  ✓ Node.js"
echo "  ✓ Google Chrome"
echo "  ✓ All dependencies"
echo ""
echo "NOTE: This will ask for your password (sudo access required)"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "❌ Cannot detect Linux distribution"
    pause
    exit 1
fi

echo "Detected: $PRETTY_NAME"
echo ""

# Step 1: Update package manager
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Updating package manager..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

case $DISTRO in
    ubuntu|debian|linuxmint)
        sudo apt-get update
        PKG_MANAGER="apt-get"
        ;;
    fedora|rhel|centos)
        sudo dnf check-update || true
        PKG_MANAGER="dnf"
        ;;
    arch|manjaro)
        sudo pacman -Sy
        PKG_MANAGER="pacman"
        ;;
    *)
        echo "⚠ Unsupported distribution: $DISTRO"
        echo "Please install Python 3, Node.js, and Chrome manually"
        pause
        exit 1
        ;;
esac

echo "✓ Package manager updated"
echo ""

# Step 2: Install Python 3
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Checking Python 3..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python 3 is already installed (version: $PYTHON_VERSION)"
else
    echo "Installing Python 3..."

    case $PKG_MANAGER in
        apt-get)
            sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-pip
            ;;
    esac

    if command -v python3 &> /dev/null; then
        echo "✓ Python 3 installed successfully!"
    else
        echo "❌ Failed to install Python 3"
        pause
        exit 1
    fi
fi

echo ""

# Step 3: Install Node.js
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Checking Node.js..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js is already installed (version: $NODE_VERSION)"
else
    echo "Installing Node.js..."

    case $PKG_MANAGER in
        apt-get)
            # Install NodeSource repository for latest Node.js
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
            ;;
        dnf)
            # Install NodeSource repository for latest Node.js
            curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
            sudo dnf install -y nodejs
            ;;
        pacman)
            sudo pacman -S --noconfirm nodejs npm
            ;;
    esac

    if command -v node &> /dev/null; then
        echo "✓ Node.js installed successfully!"
    else
        echo "❌ Failed to install Node.js"
        pause
        exit 1
    fi
fi

echo ""

# Step 4: Install Google Chrome
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Checking Google Chrome..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v google-chrome &> /dev/null || command -v google-chrome-stable &> /dev/null; then
    echo "✓ Google Chrome is already installed"
elif command -v chromium &> /dev/null || command -v chromium-browser &> /dev/null; then
    echo "✓ Chromium is installed (will work as alternative to Chrome)"
else
    echo "Installing Google Chrome..."

    case $PKG_MANAGER in
        apt-get)
            # Download and install Chrome
            wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
            sudo apt-get install -y /tmp/chrome.deb
            rm /tmp/chrome.deb
            ;;
        dnf)
            # Add Google Chrome repository
            sudo dnf install -y fedora-workstation-repositories
            sudo dnf config-manager --set-enabled google-chrome
            sudo dnf install -y google-chrome-stable
            ;;
        pacman)
            # Install from AUR or use Chromium
            echo "Installing Chromium as alternative..."
            sudo pacman -S --noconfirm chromium
            ;;
    esac

    if command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
        echo "✓ Chrome/Chromium installed successfully!"
    else
        echo "⚠ Chrome installation may have failed"
        echo "You can install it manually from: https://www.google.com/chrome/"
        echo "Or use Chromium as an alternative"
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
    python3 -m pip install --user pipenv

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
    pause
    exit 1
fi

echo ""

# Step 7: Install Frontend dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 7: Installing Frontend dependencies..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d "Frontend" ]; then
    echo "❌ Frontend directory not found!"
    pause
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
    pause
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
    echo "  → Double-click '2-START.sh' in the Linux folder"
    echo ""
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    echo ""
fi

pause
