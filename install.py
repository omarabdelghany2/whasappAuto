#!/usr/bin/env python3
"""
WhatsApp Scheduler - Cross-Platform Installation Script
Supports: Windows, macOS, Linux
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# ANSI color codes (work on most terminals, including Windows 10+)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def disable():
        """Disable colors for Windows cmd that doesn't support ANSI"""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.NC = ''

# Enable ANSI colors on Windows 10+
if platform.system() == 'Windows':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        Colors.disable()

def print_header(text):
    print()
    print(f"{Colors.CYAN}{'=' * 50}{Colors.NC}")
    print(f"{Colors.CYAN}{text}{Colors.NC}")
    print(f"{Colors.CYAN}{'=' * 50}{Colors.NC}")
    print()

def print_info(text):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {text}")

def print_success(text):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {text}")

def print_error(text):
    print(f"{Colors.RED}[✗]{Colors.NC} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}[!]{Colors.NC} {text}")

def print_step(text):
    print()
    print(f"{Colors.CYAN}→ {text}{Colors.NC}")

def run_command(cmd, check=True, shell=False):
    """Run a command and return success status"""
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        result = subprocess.run(cmd, check=check, capture_output=True, text=True, shell=shell)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except FileNotFoundError:
        return False, "Command not found"

def check_command(cmd):
    """Check if a command exists"""
    return shutil.which(cmd) is not None

def get_package_manager():
    """Detect the package manager for the current OS"""
    system = platform.system()

    if system == 'Darwin':  # macOS
        if check_command('brew'):
            return 'brew'
        return None
    elif system == 'Linux':
        if check_command('apt-get'):
            return 'apt-get'
        elif check_command('yum'):
            return 'yum'
        elif check_command('dnf'):
            return 'dnf'
        elif check_command('pacman'):
            return 'pacman'
        return None
    elif system == 'Windows':
        if check_command('choco'):
            return 'choco'
        elif check_command('scoop'):
            return 'scoop'
        elif check_command('winget'):
            return 'winget'
        return None
    return None

def install_python():
    """Guide user to install Python"""
    system = platform.system()
    pkg_mgr = get_package_manager()

    print_warning("Python 3 is required but not found.")
    print()

    if system == 'Windows':
        print("Installation options for Windows:")
        print(f"  1. Download from: {Colors.CYAN}https://www.python.org/downloads/{Colors.NC}")
        print(f"     Make sure to check 'Add Python to PATH' during installation!")
        print()
        if pkg_mgr == 'choco':
            print(f"  2. Using Chocolatey: {Colors.CYAN}choco install python{Colors.NC}")
        elif pkg_mgr == 'winget':
            print(f"  2. Using winget: {Colors.CYAN}winget install Python.Python.3{Colors.NC}")
    elif system == 'Darwin':
        print("Installation options for macOS:")
        print(f"  1. Download from: {Colors.CYAN}https://www.python.org/downloads/{Colors.NC}")
        print()
        if pkg_mgr == 'brew':
            print(f"  2. Using Homebrew: {Colors.CYAN}brew install python3{Colors.NC}")
        else:
            print(f"  2. Install Homebrew first: {Colors.CYAN}https://brew.sh/{Colors.NC}")
            print(f"     Then run: {Colors.CYAN}brew install python3{Colors.NC}")
    elif system == 'Linux':
        print("Installation options for Linux:")
        if pkg_mgr == 'apt-get':
            print(f"  Run: {Colors.CYAN}sudo apt-get update && sudo apt-get install python3 python3-pip{Colors.NC}")
        elif pkg_mgr in ['yum', 'dnf']:
            print(f"  Run: {Colors.CYAN}sudo {pkg_mgr} install python3 python3-pip{Colors.NC}")
        elif pkg_mgr == 'pacman':
            print(f"  Run: {Colors.CYAN}sudo pacman -S python python-pip{Colors.NC}")
        else:
            print(f"  Use your distribution's package manager to install python3")

    print()
    print_error("Please install Python 3 and run this script again.")
    return False

def install_nodejs():
    """Guide user to install Node.js"""
    system = platform.system()
    pkg_mgr = get_package_manager()

    print_warning("Node.js is required but not found.")
    print()

    if system == 'Windows':
        print("Installation options for Windows:")
        print(f"  1. Download from: {Colors.CYAN}https://nodejs.org/{Colors.NC}")
        print()
        if pkg_mgr == 'choco':
            print(f"  2. Using Chocolatey: {Colors.CYAN}choco install nodejs{Colors.NC}")
        elif pkg_mgr == 'winget':
            print(f"  2. Using winget: {Colors.CYAN}winget install OpenJS.NodeJS{Colors.NC}")
    elif system == 'Darwin':
        print("Installation options for macOS:")
        print(f"  1. Download from: {Colors.CYAN}https://nodejs.org/{Colors.NC}")
        print()
        if pkg_mgr == 'brew':
            print(f"  2. Using Homebrew: {Colors.CYAN}brew install node{Colors.NC}")
        else:
            print(f"  2. Install Homebrew first: {Colors.CYAN}https://brew.sh/{Colors.NC}")
            print(f"     Then run: {Colors.CYAN}brew install node{Colors.NC}")
    elif system == 'Linux':
        print("Installation options for Linux:")
        if pkg_mgr == 'apt-get':
            print(f"  Run: {Colors.CYAN}curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -{Colors.NC}")
            print(f"       {Colors.CYAN}sudo apt-get install -y nodejs{Colors.NC}")
        elif pkg_mgr in ['yum', 'dnf']:
            print(f"  Run: {Colors.CYAN}curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -{Colors.NC}")
            print(f"       {Colors.CYAN}sudo {pkg_mgr} install -y nodejs{Colors.NC}")
        else:
            print(f"  Visit: {Colors.CYAN}https://nodejs.org/{Colors.NC}")

    print()
    print_error("Please install Node.js and run this script again.")
    return False

def main():
    print_header("WhatsApp Scheduler - Installation")

    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    print_info(f"Installation directory: {script_dir}")
    print_info(f"Operating System: {platform.system()} {platform.release()}")
    print_info(f"Python Version: {sys.version.split()[0]}")

    # Step 1: Check system requirements
    print_step("Step 1: Checking System Requirements")

    requirements_met = True

    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 7:
        print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} found")
    else:
        print_error(f"Python 3.7+ required, found {python_version.major}.{python_version.minor}")
        requirements_met = False

    # Check pip
    if check_command('pip') or check_command('pip3'):
        print_success("pip found")
        pip_cmd = 'pip3' if check_command('pip3') else 'pip'
    else:
        print_error("pip not found")
        print_info("pip should come with Python installation")
        requirements_met = False
        pip_cmd = 'pip3'

    # Check Node.js
    if check_command('node'):
        success, output = run_command('node --version')
        if success:
            print_success(f"Node.js found (version: {output.strip()})")
        else:
            print_warning("Node.js found but version check failed")
    else:
        print_error("Node.js not found")
        install_nodejs()
        requirements_met = False

    # Check npm
    if check_command('npm'):
        success, output = run_command('npm --version')
        if success:
            print_success(f"npm found (version: {output.strip()})")
        else:
            print_warning("npm found but version check failed")
    else:
        print_error("npm not found")
        print_info("npm should come with Node.js installation")
        requirements_met = False

    # Check Chrome/Chromium
    system = platform.system()
    chrome_found = False

    if system == 'Darwin':
        if Path('/Applications/Google Chrome.app').exists():
            print_success("Google Chrome found")
            chrome_found = True
    elif system == 'Windows':
        chrome_paths = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / 'Google' / 'Chrome' / 'Application' / 'chrome.exe',
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / 'Google' / 'Chrome' / 'Application' / 'chrome.exe',
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'Application' / 'chrome.exe',
        ]
        for chrome_path in chrome_paths:
            if chrome_path.exists():
                print_success(f"Google Chrome found at {chrome_path}")
                chrome_found = True
                break
    elif system == 'Linux':
        if check_command('google-chrome') or check_command('chromium') or check_command('chromium-browser'):
            print_success("Chrome/Chromium found")
            chrome_found = True

    if not chrome_found:
        print_warning("Chrome not detected")
        print_info("Chrome is required for WhatsApp Web automation")
        print_info(f"Download from: {Colors.CYAN}https://www.google.com/chrome/{Colors.NC}")

    # Exit if requirements not met
    if not requirements_met:
        print()
        print_error("Please install missing requirements and run this script again")
        sys.exit(1)

    print_success("All system requirements met!")

    # Step 2: Install pipenv
    print_step("Step 2: Setting up Python Environment")

    if not check_command('pipenv'):
        print_warning("pipenv not found. Installing pipenv...")
        success, output = run_command(f'{pip_cmd} install --user pipenv')
        if success:
            print_success("pipenv installed")
            print_info("Note: If 'pipenv' command is not found after this:")
            if system == 'Windows':
                print_info("  Add Python Scripts to PATH: %APPDATA%\\Python\\Python3X\\Scripts")
            else:
                print_info("  Add to ~/.bashrc or ~/.zshrc: export PATH=\"$HOME/.local/bin:$PATH\"")
        else:
            print_error("Failed to install pipenv")
            print_info(f"Try manually: {pip_cmd} install --user pipenv")
            sys.exit(1)
    else:
        print_success("pipenv is already installed")

    # Step 3: Install Python dependencies
    print_step("Step 3: Installing Python Dependencies")

    print_info("This may take a few minutes...")

    # Use pipenv
    pipenv_cmd = 'pipenv'
    success, output = run_command(f'{pipenv_cmd} install', shell=True)

    if success:
        print_success("Python dependencies installed successfully")
    else:
        print_error("Failed to install Python dependencies")
        print_info("Error details:")
        print(output)
        print_info(f"Try running manually: pipenv install")
        sys.exit(1)

    # Step 4: Install Frontend dependencies
    print_step("Step 4: Installing Frontend Dependencies")

    frontend_dir = Path('Frontend')
    if not frontend_dir.exists():
        print_error("Frontend directory not found!")
        sys.exit(1)

    os.chdir(frontend_dir)
    print_info("Installing Node.js packages (this may take a few minutes)...")

    success, output = run_command('npm install', shell=True)

    if success:
        print_success("Frontend dependencies installed successfully")
    else:
        print_error("Failed to install frontend dependencies")
        print_info("Error details:")
        print(output)
        print_info("Try running manually: cd Frontend && npm install")
        sys.exit(1)

    os.chdir(script_dir)

    # Step 5: Create necessary directories
    print_step("Step 5: Creating Required Directories")

    dirs = ['uploads', 'chrome_data']
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print_success(f"Created {dir_name}/ directory")

    # Step 6: Setup configuration files
    print_step("Step 6: Setting up Configuration Files")

    # Create .env
    env_file = Path('.env')
    if not env_file.exists():
        env_example = Path('.env.example')
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print_success("Created .env file from .env.example")
        else:
            with open(env_file, 'w') as f:
                f.write('GROUP_NAME=Cairo\n')
                f.write('CHROME_PROFILE_PATH=\n')
            print_success("Created default .env file")
        print_info("You can edit .env to customize settings")
    else:
        print_info(".env file already exists (skipping)")

    # Create JSON files
    json_files = {
        'schedules.json': [],
        'finishedSchedules.json': [],
        'group_names.json': []
    }

    for filename, default_content in json_files.items():
        file_path = Path(filename)
        if not file_path.exists():
            import json
            with open(file_path, 'w') as f:
                json.dump(default_content, f)
            print_success(f"Created {filename}")
        else:
            print_info(f"{filename} already exists (skipping)")

    # Step 7: Verify installation
    print_step("Step 7: Verifying Installation")

    verification_passed = True

    # Check pipenv environment
    success, output = run_command('pipenv --venv', shell=True)
    if success:
        print_success("Python virtual environment ready")
    else:
        print_error("Python virtual environment check failed")
        verification_passed = False

    # Check Frontend node_modules
    if (frontend_dir / 'node_modules').exists():
        print_success("Frontend dependencies ready")
    else:
        print_error("Frontend node_modules not found")
        verification_passed = False

    # Check required files
    required_files = ['server.py', 'scheduler.py', 'whatsapp_bot.py', 'main.py']
    for filename in required_files:
        if Path(filename).exists():
            print_success(f"Found {filename}")
        else:
            print_warning(f"Missing {filename} (may cause issues)")

    # Installation complete
    print_header("Installation Complete!")

    if verification_passed:
        print_success("All components installed successfully!")
    else:
        print_warning("Installation completed with some warnings")

    print()
    print(f"{Colors.GREEN}Next Steps:{Colors.NC}")
    print()
    print("  1. Start the application:")

    if system == 'Windows':
        print(f"     {Colors.CYAN}python start.py{Colors.NC}")
        print(f"     or double-click: {Colors.CYAN}start.bat{Colors.NC}")
    else:
        print(f"     {Colors.CYAN}python3 start.py{Colors.NC}")
        print(f"     or: {Colors.CYAN}./start.sh{Colors.NC}")

    print()
    print("  2. Open your browser to:")
    print(f"     {Colors.CYAN}http://localhost:5173{Colors.NC}")
    print()
    print("  3. First time? You'll need to scan WhatsApp QR code")
    print("     Click the 'Login' button in the UI")
    print()
    print(f"{Colors.YELLOW}Useful Commands:{Colors.NC}")

    if system == 'Windows':
        print(f"  View logs:       {Colors.CYAN}type backend.log{Colors.NC} or {Colors.CYAN}type frontend.log{Colors.NC}")
        print(f"  CLI mode:        {Colors.CYAN}pipenv run python main.py --help{Colors.NC}")
    else:
        print(f"  View logs:       {Colors.CYAN}tail -f backend.log{Colors.NC} or {Colors.CYAN}tail -f frontend.log{Colors.NC}")
        print(f"  CLI mode:        {Colors.CYAN}pipenv run python3 main.py --help{Colors.NC}")

    print()
    print(f"{Colors.GREEN}Happy Scheduling! 🚀{Colors.NC}")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
