@echo off
REM WhatsApp Scheduler - Windows Auto-Installer
REM This will guide you to install everything automatically
REM Double-click this file to install

REM Change to parent directory
cd /d "%~dp0\.."

title WhatsApp Scheduler - Automatic Installation
color 0A

echo.
echo ========================================================
echo.
echo      WhatsApp Scheduler - Automatic Installation
echo                   for Windows
echo.
echo ========================================================
echo.
echo This installer will help you install everything needed:
echo   - Python 3
echo   - Node.js
echo   - Google Chrome
echo   - All dependencies
echo.
pause
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    color 0E
    echo ========================================================
    echo   IMPORTANT: Administrator Rights Needed
    echo ========================================================
    echo.
    echo For automatic installation, please:
    echo   1. Right-click this file
    echo   2. Select "Run as Administrator"
    echo.
    echo Or continue with manual installation links below...
    echo.
    pause
)

REM Check for winget (Windows Package Manager)
where winget >nul 2>&1
if %errorlevel% equ 0 (
    set HAS_WINGET=1
    echo [OK] Windows Package Manager detected
) else (
    set HAS_WINGET=0
    echo [!] Windows Package Manager not found
)

echo.
echo ========================================================
echo Step 1: Checking Python 3...
echo ========================================================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo [OK] Python is already installed ^(version: %PYTHON_VER%^)
    goto :nodejs_check
)

REM Python not found - try to install
echo Python 3 is not installed.
echo.

if "%HAS_WINGET%"=="1" (
    echo Installing Python 3 automatically...
    echo This may take a few minutes...
    echo.
    winget install -e --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements

    REM Refresh environment variables
    call refreshenv.cmd >nul 2>&1

    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Python 3 installed successfully!
        goto :nodejs_check
    )
)

REM Manual installation required
color 0C
echo.
echo ========================================================
echo   Python 3 Installation Required
echo ========================================================
echo.
echo Please install Python 3 manually:
echo.
echo 1. Open this link in your browser:
echo    https://www.python.org/downloads/
echo.
echo 2. Download the latest Python 3 installer
echo.
echo 3. Run the installer and CHECK THIS BOX:
echo    [X] Add Python to PATH
echo.
echo 4. After installation, run this installer again
echo.
pause
exit /b 1

:nodejs_check
echo.
echo ========================================================
echo Step 2: Checking Node.js...
echo ========================================================
echo.

node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f %%i in ('node --version') do set NODE_VER=%%i
    echo [OK] Node.js is already installed ^(version: %NODE_VER%^)
    goto :chrome_check
)

REM Node.js not found - try to install
echo Node.js is not installed.
echo.

if "%HAS_WINGET%"=="1" (
    echo Installing Node.js automatically...
    echo This may take a few minutes...
    echo.
    winget install -e --id OpenJS.NodeJS.LTS --silent --accept-source-agreements --accept-package-agreements

    REM Refresh environment variables
    call refreshenv.cmd >nul 2>&1

    node --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Node.js installed successfully!
        goto :chrome_check
    )
)

REM Manual installation required
color 0C
echo.
echo ========================================================
echo   Node.js Installation Required
echo ========================================================
echo.
echo Please install Node.js manually:
echo.
echo 1. Open this link in your browser:
echo    https://nodejs.org/
echo.
echo 2. Download the LTS version
echo.
echo 3. Run the installer ^(keep all default options^)
echo.
echo 4. After installation, run this installer again
echo.
pause
exit /b 1

:chrome_check
echo.
echo ========================================================
echo Step 3: Checking Google Chrome...
echo ========================================================
echo.

REM Check common Chrome installation paths
set CHROME_FOUND=0
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1

if %CHROME_FOUND%==1 (
    echo [OK] Google Chrome is installed
    goto :install_dependencies
)

REM Chrome not found - try to install
echo Google Chrome is not installed.
echo.

if "%HAS_WINGET%"=="1" (
    echo Installing Google Chrome automatically...
    echo This may take a few minutes...
    echo.
    winget install -e --id Google.Chrome --silent --accept-source-agreements --accept-package-agreements

    if %errorlevel% equ 0 (
        echo [OK] Google Chrome installed successfully!
        goto :install_dependencies
    )
)

REM Manual installation
echo.
echo [!] Chrome installation recommended
echo.
echo You can install it from: https://www.google.com/chrome/
echo.
echo Continuing without Chrome ^(you can install it later^)...
echo.
pause

:install_dependencies
color 0A
echo.
echo ========================================================
echo Step 4: Installing pipenv...
echo ========================================================
echo.

REM Check if pipenv is installed
pipenv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pipenv is already installed
    goto :install_python_deps
)

echo Installing pipenv...
python -m pip install --user pipenv

REM Determine Python Scripts path more reliably
for /f "tokens=*" %%i in ('python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))"') do set SCRIPTS_PATH=%%i

echo Detected Python Scripts path: %SCRIPTS_PATH%
echo.

REM Add to current session PATH first
set PATH=%SCRIPTS_PATH%;%PATH%
set PATH=%APPDATA%\Python\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python312\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python313\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python314\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts;%PATH%

REM Verify pipenv is accessible in current session
pipenv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pipenv is accessible in current session
) else (
    echo [!] Warning: pipenv not accessible yet
)

REM Add pipenv to PATH permanently for the current user
echo Adding pipenv to system PATH permanently...
echo.

REM Get current user PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set CURRENT_USER_PATH=%%b

REM Check if Scripts path is already in PATH
echo %CURRENT_USER_PATH% | find /i "%SCRIPTS_PATH%" >nul
if %errorlevel% neq 0 (
    REM Not in PATH, add it
    if defined CURRENT_USER_PATH (
        setx PATH "%CURRENT_USER_PATH%;%SCRIPTS_PATH%" >nul 2>&1
    ) else (
        setx PATH "%SCRIPTS_PATH%" >nul 2>&1
    )

    if %errorlevel% equ 0 (
        echo [OK] Added pipenv to system PATH permanently
        echo [OK] Restart Command Prompt for changes to take effect everywhere
    ) else (
        echo [!] Could not update PATH automatically
        echo [!] You may need to add this manually: %SCRIPTS_PATH%
    )
) else (
    echo [OK] pipenv Scripts path already in system PATH
)

echo.
echo [OK] pipenv installation complete!

:install_python_deps
echo.
echo ========================================================
echo Step 5: Installing Python Dependencies with pipenv...
echo ========================================================
echo.
echo This may take 3-5 minutes. Please wait...
echo.

REM Try to install Python dependencies using pipenv with lock file
pipenv install

if %errorlevel% neq 0 (
    echo.
    echo [!] Installation from lock file failed. Trying without lock file...
    echo.

    REM Delete the lock file and try again
    if exist "Pipfile.lock" (
        echo Removing Pipfile.lock...
        del /f "Pipfile.lock"
    )

    REM Install without lock file
    pipenv install --skip-lock

    if %errorlevel% equ 0 (
        echo [OK] Python dependencies installed successfully!
    ) else (
        color 0C
        echo [ERROR] Failed to install Python dependencies
        echo.
        echo Troubleshooting tips:
        echo   1. Check your internet connection
        echo   2. Try running: pipenv install --skip-lock
        echo   3. Check if any antivirus is blocking the installation
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] Python dependencies installed successfully!
)

echo.
echo ========================================================
echo Step 6: Installing Frontend Dependencies...
echo ========================================================
echo.

if not exist "Frontend" (
    color 0C
    echo [ERROR] Frontend directory not found!
    pause
    exit /b 1
)

cd Frontend

REM Create lib/utils.ts if it doesn't exist (required for shadcn/ui components)
if not exist "src\lib" mkdir "src\lib"
if not exist "src\lib\utils.ts" (
    echo Creating missing utils.ts file...
    (
        echo import { type ClassValue, clsx } from "clsx"
        echo import { twMerge } from "tailwind-merge"
        echo.
        echo export function cn^(...inputs: ClassValue[]^) {
        echo   return twMerge^(clsx^(inputs^)^)
        echo }
    ) > "src\lib\utils.ts"
    echo [OK] Created src\lib\utils.ts
)

echo Installing Node.js packages (this may take a few minutes)...
call npm install

if %errorlevel% equ 0 (
    echo [OK] Frontend dependencies installed successfully!
) else (
    echo [!] npm install encountered issues. Trying with --force flag...
    call npm install --force

    if %errorlevel% equ 0 (
        echo [OK] Frontend dependencies installed successfully!
    ) else (
        color 0C
        echo [ERROR] Failed to install Frontend dependencies
        echo.
        echo Troubleshooting tips:
        echo   1. Check your internet connection
        echo   2. Try running: npm cache clean --force
        echo   3. Delete node_modules folder and try again
        echo.
        cd ..
        pause
        exit /b 1
    )
)

cd ..

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo.
    echo       Installation Completed Successfully!
    echo.
    echo ========================================================
    echo.
    echo Everything is ready!
    echo.
    echo IMPORTANT NOTE:
    echo   If you installed pipenv for the first time, you may need to
    echo   close this window and open a new Command Prompt for PATH
    echo   changes to take effect.
    echo.
    echo Next step:
    echo   Double-click "2-START.bat" in the Windows folder
    echo.
    echo   If it says "pipenv is not recognized", simply:
    echo   1. Close this window
    echo   2. Double-click "2-START.bat" again
    echo.
) else (
    color 0C
    echo.
    echo Installation failed!
    echo Please check the error messages above.
    echo.
)

pause
