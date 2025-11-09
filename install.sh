#!/bin/bash

# WhatsApp Scheduler Installation Script
# This script installs all dependencies and sets up the project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
print_header() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_step() {
    echo ""
    echo -e "${CYAN}→ $1${NC}"
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_header "WhatsApp Scheduler - Installation"

print_info "Installation directory: $SCRIPT_DIR"

# Check system requirements
print_step "Step 1: Checking System Requirements"

REQUIREMENTS_MET=true

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 3 found (version: $PYTHON_VERSION)"
else
    print_error "Python 3 is not installed"
    print_info "Please install Python 3 from: https://www.python.org/downloads/"
    REQUIREMENTS_MET=false
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is not installed"
    print_info "Please install pip3"
    REQUIREMENTS_MET=false
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found (version: $NODE_VERSION)"
else
    print_error "Node.js is not installed"
    print_info "Please install Node.js from: https://nodejs.org/"
    REQUIREMENTS_MET=false
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm found (version: $NPM_VERSION)"
else
    print_error "npm is not installed"
    print_info "npm should come with Node.js installation"
    REQUIREMENTS_MET=false
fi

# Check Chrome (macOS specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -d "/Applications/Google Chrome.app" ]; then
        print_success "Google Chrome found"
    else
        print_warning "Google Chrome not found at default location"
        print_info "The bot requires Chrome for WhatsApp Web automation"
        print_info "Install from: https://www.google.com/chrome/"
    fi
elif command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
    print_success "Chrome/Chromium found"
else
    print_warning "Chrome/Chromium not detected"
    print_info "The bot requires Chrome for WhatsApp Web automation"
fi

# Exit if requirements not met
if [ "$REQUIREMENTS_MET" = false ]; then
    echo ""
    print_error "Please install missing requirements and run this script again"
    exit 1
fi

print_success "All system requirements met!"

# Install pipenv if not available
print_step "Step 2: Setting up Python Environment"

if ! command -v pipenv &> /dev/null; then
    print_warning "pipenv not found. Installing pipenv..."
    pip3 install --user pipenv
    print_success "pipenv installed"

    # Add pipenv to PATH suggestion
    print_info "If pipenv command is not found after this, add this to your ~/.bashrc or ~/.zshrc:"
    print_info "export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    print_success "pipenv is already installed"
fi

# Install Python dependencies
print_step "Step 3: Installing Python Dependencies"

print_info "This may take a few minutes..."
if pipenv install; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    print_info "Try running manually: pipenv install"
    exit 1
fi

# Install Frontend dependencies
print_step "Step 4: Installing Frontend Dependencies"

if [ ! -d "Frontend" ]; then
    print_error "Frontend directory not found!"
    exit 1
fi

cd Frontend
print_info "Installing Node.js packages (this may take a few minutes)..."

if npm install; then
    print_success "Frontend dependencies installed successfully"
else
    print_error "Failed to install frontend dependencies"
    print_info "Try running manually: cd Frontend && npm install"
    exit 1
fi

cd ..

# Create necessary directories
print_step "Step 5: Creating Required Directories"

mkdir -p uploads
print_success "Created uploads/ directory"

mkdir -p chrome_data
print_success "Created chrome_data/ directory"

# Setup configuration files
print_step "Step 6: Setting up Configuration Files"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env file from .env.example"
        print_info "You can edit .env to customize settings"
    else
        # Create basic .env
        cat > .env << 'EOF'
GROUP_NAME=Cairo
CHROME_PROFILE_PATH=
EOF
        print_success "Created default .env file"
    fi
else
    print_info ".env file already exists (skipping)"
fi

# Create empty schedules.json if it doesn't exist
if [ ! -f "schedules.json" ]; then
    echo "[]" > schedules.json
    print_success "Created empty schedules.json"
else
    print_info "schedules.json already exists (skipping)"
fi

# Create empty finishedSchedules.json if it doesn't exist
if [ ! -f "finishedSchedules.json" ]; then
    echo "[]" > finishedSchedules.json
    print_success "Created empty finishedSchedules.json"
else
    print_info "finishedSchedules.json already exists (skipping)"
fi

# Create empty group_names.json if it doesn't exist
if [ ! -f "group_names.json" ]; then
    echo "[]" > group_names.json
    print_success "Created empty group_names.json"
else
    print_info "group_names.json already exists (skipping)"
fi

# Verify installation
print_step "Step 7: Verifying Installation"

VERIFICATION_PASSED=true

# Check if pipenv environment exists
if pipenv --venv &> /dev/null; then
    print_success "Python virtual environment ready"
else
    print_error "Python virtual environment check failed"
    VERIFICATION_PASSED=false
fi

# Check if Frontend node_modules exists
if [ -d "Frontend/node_modules" ]; then
    print_success "Frontend dependencies ready"
else
    print_error "Frontend node_modules not found"
    VERIFICATION_PASSED=false
fi

# Check if required files exist
REQUIRED_FILES=("server.py" "scheduler.py" "whatsapp_bot.py" "main.py" "start.sh")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found $file"
    else
        print_warning "Missing $file (may cause issues)"
    fi
done

# Installation summary
print_header "Installation Complete!"

if [ "$VERIFICATION_PASSED" = true ]; then
    print_success "All components installed successfully!"
else
    print_warning "Installation completed with some warnings"
fi

echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo ""
echo -e "  1. Start the application:"
echo -e "     ${CYAN}./start.sh${NC}"
echo ""
echo -e "  2. Open your browser to:"
echo -e "     ${CYAN}http://localhost:5173${NC}"
echo ""
echo -e "  3. First time? You'll need to scan WhatsApp QR code"
echo -e "     Click the 'Login' button in the UI"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  Start app:       ${CYAN}./start.sh${NC}"
echo -e "  Stop app:        Press ${CYAN}Ctrl+C${NC}"
echo -e "  View logs:       ${CYAN}tail -f backend.log${NC} or ${CYAN}tail -f frontend.log${NC}"
echo -e "  CLI mode:        ${CYAN}pipenv run python main.py --help${NC}"
echo ""
echo -e "${GREEN}Happy Scheduling! 🚀${NC}"
echo ""

# Make start.sh executable if it exists
if [ -f "start.sh" ]; then
    chmod +x start.sh
    print_info "Made start.sh executable"
fi
