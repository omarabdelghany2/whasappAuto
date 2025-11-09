# WhatsApp Scheduler - Complete Installation Guide

This guide provides detailed, platform-specific installation instructions for Windows, macOS, and Linux.

## Table of Contents

- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Troubleshooting](#troubleshooting)
- [Verifying Installation](#verifying-installation)

---

## Windows Installation

### Prerequisites

Before installing WhatsApp Scheduler, you need to install these prerequisites:

#### 1. Install Python 3

**Option A: Official Installer (Recommended)**

1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. ⚠️ **IMPORTANT**: Check **"Add Python to PATH"** during installation
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```

**Option B: Using Chocolatey**

If you have Chocolatey installed:
```cmd
choco install python
```

**Option C: Using winget**

If you have winget (Windows 10 1809+):
```cmd
winget install Python.Python.3
```

#### 2. Install Node.js

**Option A: Official Installer (Recommended)**

1. Download from: https://nodejs.org/ (LTS version)
2. Run the installer
3. Accept defaults (includes npm)
4. Verify installation:
   ```cmd
   node --version
   npm --version
   ```

**Option B: Using Chocolatey**

```cmd
choco install nodejs
```

**Option C: Using winget**

```cmd
winget install OpenJS.NodeJS
```

#### 3. Install Google Chrome

1. Download from: https://www.google.com/chrome/
2. Run the installer
3. Complete the installation

### Quick Installation

Once prerequisites are installed:

1. **Download/Clone the project** to a folder (e.g., `C:\whatsappAuto`)

2. **Open Command Prompt** in the project folder:
   - Navigate to the folder in File Explorer
   - Type `cmd` in the address bar and press Enter

3. **Run the installer:**
   ```cmd
   install.bat
   ```

   Or simply **double-click** `install.bat` in File Explorer

4. **Wait for installation** to complete (3-5 minutes)

5. **Start the application:**
   ```cmd
   start.bat
   ```

   Or **double-click** `start.bat` in File Explorer

6. **Open your browser** to: http://localhost:5173

### Alternative: Using Python Scripts Directly

```cmd
# Install
python install.py

# Start
python start.py
```

### Common Windows Issues

**Issue: "Python is not recognized"**
- Solution: Make sure Python was added to PATH during installation
- Fix: Reinstall Python and check "Add Python to PATH"
- Or manually add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X` to PATH

**Issue: "npm is not recognized"**
- Solution: Restart Command Prompt after installing Node.js
- Or reinstall Node.js with default options

**Issue: Scripts won't run (security error)**
- Solution: Right-click `install.bat` → "Run as Administrator"

**Issue: Port already in use**
- Solution: Close any apps using ports 8000 or 5173
- Find and kill: `netstat -ano | findstr :8000`

---

## macOS Installation

### Prerequisites

#### 1. Install Homebrew (Package Manager)

Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Python 3

**Option A: Using Homebrew (Recommended)**
```bash
brew install python3
```

**Option B: Official Installer**
1. Download from: https://www.python.org/downloads/
2. Run the .pkg installer
3. Follow installation steps

Verify:
```bash
python3 --version
pip3 --version
```

#### 3. Install Node.js

**Option A: Using Homebrew (Recommended)**
```bash
brew install node
```

**Option B: Official Installer**
1. Download from: https://nodejs.org/ (LTS version)
2. Run the .pkg installer

Verify:
```bash
node --version
npm --version
```

#### 4. Install Google Chrome

**Option A: Using Homebrew**
```bash
brew install --cask google-chrome
```

**Option B: Manual Download**
1. Download from: https://www.google.com/chrome/
2. Drag to Applications folder

### Quick Installation

1. **Download/Clone the project**

2. **Open Terminal** and navigate to the project:
   ```bash
   cd /path/to/whasappAuto
   ```

3. **Make scripts executable:**
   ```bash
   chmod +x install.py start.py install.sh start.sh
   ```

4. **Run the installer:**
   ```bash
   python3 install.py
   ```

   Or use the bash script:
   ```bash
   ./install.sh
   ```

5. **Start the application:**
   ```bash
   python3 start.py
   ```

   Or:
   ```bash
   ./start.sh
   ```

6. **Browser will open automatically** to http://localhost:5173

### Common macOS Issues

**Issue: "command not found: python3"**
- Solution: Install Python via Homebrew or official installer

**Issue: Permission denied**
- Solution: `chmod +x install.py start.py`

**Issue: pipenv not found after installation**
- Solution: Add to PATH in `~/.zshrc` or `~/.bash_profile`:
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```
- Then: `source ~/.zshrc`

**Issue: Chrome not detected**
- Solution: Make sure Chrome is in `/Applications/Google Chrome.app`

---

## Linux Installation

### Ubuntu / Debian

#### Prerequisites

```bash
# Update package list
sudo apt-get update

# Install Python 3 and pip
sudo apt-get install python3 python3-pip python3-venv

# Install Node.js (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

#### Installation

```bash
# Navigate to project
cd /path/to/whasappAuto

# Make executable
chmod +x install.py start.py install.sh start.sh

# Run installer
python3 install.py

# Start application
python3 start.py
```

### Fedora / RHEL / CentOS

#### Prerequisites

```bash
# Install Python 3
sudo dnf install python3 python3-pip

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo dnf install -y nodejs

# Install Chrome
sudo dnf install fedora-workstation-repositories
sudo dnf config-manager --set-enabled google-chrome
sudo dnf install google-chrome-stable
```

#### Installation

```bash
cd /path/to/whasappAuto
chmod +x install.py start.py
python3 install.py
python3 start.py
```

### Arch Linux

#### Prerequisites

```bash
# Install dependencies
sudo pacman -S python python-pip nodejs npm chromium

# Or use Chrome from AUR
yay -S google-chrome
```

#### Installation

```bash
cd /path/to/whasappAuto
chmod +x install.py start.py
python3 install.py
python3 start.py
```

### Common Linux Issues

**Issue: pip not found**
- Solution: `sudo apt-get install python3-pip` (Ubuntu/Debian)

**Issue: Permission errors**
- Solution: Don't use `sudo` with pip. Use `pip install --user`

**Issue: Chrome driver issues**
- Solution: Install chromium-driver: `sudo apt-get install chromium-driver`

**Issue: Port already in use**
- Solution: Kill process on port:
  ```bash
  sudo lsof -ti:8000 | xargs kill -9
  sudo lsof -ti:5173 | xargs kill -9
  ```

---

## Troubleshooting

### Installation Fails

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.7+
   ```

2. **Check Node.js version:**
   ```bash
   node --version  # Should be 18+
   ```

3. **Manually install pipenv:**
   ```bash
   pip3 install --user pipenv
   ```

4. **Manually install dependencies:**
   ```bash
   # Backend
   pipenv install

   # Frontend
   cd Frontend
   npm install
   ```

### Application Won't Start

1. **Check if dependencies are installed:**
   ```bash
   # Check Python environment
   pipenv --venv

   # Check Frontend dependencies
   ls Frontend/node_modules
   ```

2. **Check logs:**
   - `backend.log` - Backend errors
   - `frontend.log` - Frontend errors

3. **Manually start services:**
   ```bash
   # Terminal 1 - Backend
   pipenv run uvicorn server:app --reload

   # Terminal 2 - Frontend
   cd Frontend
   npm run dev
   ```

### WhatsApp Login Issues

1. **Delete Chrome session data:**
   ```bash
   rm -rf chrome_data/
   ```

2. **Try login again** - Click "Login" button in UI

3. **Scan QR code** when browser opens

### Port Conflicts

If ports 8000 or 5173 are already in use:

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

---

## Verifying Installation

After installation, verify everything works:

1. **Check Python environment:**
   ```bash
   pipenv --venv
   pipenv run python --version
   ```

2. **Check Frontend:**
   ```bash
   cd Frontend
   npm list
   ```

3. **Check required files exist:**
   - `schedules.json`
   - `finishedSchedules.json`
   - `group_names.json`
   - `.env`
   - `uploads/` directory
   - `chrome_data/` directory

4. **Test startup:**
   - Run the start script
   - Check http://localhost:8000/docs (Backend API)
   - Check http://localhost:5173 (Frontend UI)

---

## Getting Help

If you encounter issues not covered here:

1. **Check logs:**
   - `backend.log`
   - `frontend.log`
   - `whatsapp_bot.log`

2. **Verify all prerequisites** are installed correctly

3. **Try manual installation** (see README.md)

4. **Report issues** with:
   - Your operating system and version
   - Error messages from logs
   - Steps to reproduce the problem

---

## Next Steps

Once installed:

1. **Start the application**
2. **Login to WhatsApp** (first time only)
3. **Add your group names**
4. **Create your first schedule**
5. **Click "Start"** to begin scheduling

Enjoy automated WhatsApp messaging! 🚀
