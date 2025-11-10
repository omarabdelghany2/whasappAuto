@echo off
REM WhatsApp Scheduler - Windows Starter
REM Double-click this file to start the app

REM Change to parent directory (go up one level from Windows folder)
cd /d "%~dp0\.."

title WhatsApp Scheduler - Running
color 0B

echo.
echo ========================================================
echo.
echo          WhatsApp Scheduler - Starting...
echo.
echo ========================================================
echo.

REM Add pipenv to PATH for this session BEFORE checking
set PATH=%APPDATA%\Python\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python312\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python313\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python314\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts;%PATH%
set PATH=%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts;%PATH%

echo Checking system requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed!
    echo Please run: 1-INSTALL.bat
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Node.js is not installed!
    echo Please run: 1-INSTALL.bat
    pause
    exit /b 1
)

REM Check if pipenv is installed
pipenv --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: pipenv is not installed!
    echo ================================================
    echo.
    echo Please run installation first:
    echo   Double-click "1-INSTALL.bat" in the Windows folder
    echo.
    echo Note: If you just installed, try:
    echo   1. Close this window
    echo   2. Open a new Command Prompt
    echo   3. Run this file again
    echo.
    pause
    exit /b 1
)

echo [OK] Python, Node.js, and pipenv are installed
echo.

REM Check if pipenv environment exists
pipenv --venv >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: Virtual environment not found!
    echo ================================================
    echo.
    echo Please run installation first:
    echo   Double-click "1-INSTALL.bat" in the Windows folder
    echo.
    echo If you just installed, the installation may have failed.
    echo Try running 1-INSTALL.bat again.
    echo.
    pause
    exit /b 1
)

REM Get the virtual environment path
for /f "tokens=*" %%i in ('pipenv --venv 2^>nul') do set VENV_PATH=%%i
echo [OK] Virtual environment found at: %VENV_PATH%
echo.

REM Check if Frontend dependencies are installed
if not exist "Frontend\node_modules" (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: Frontend not installed!
    echo ================================================
    echo.
    echo Please run installation first:
    echo   Double-click "1-INSTALL.bat" in the Windows folder
    echo.
    pause
    exit /b 1
)

REM Ensure lib/utils.ts exists (auto-fix common issue)
if not exist "Frontend\src\lib" mkdir "Frontend\src\lib"
if not exist "Frontend\src\lib\utils.ts" (
    echo [!] Creating missing utils.ts file...
    (
        echo import { type ClassValue, clsx } from "clsx"
        echo import { twMerge } from "tailwind-merge"
        echo.
        echo export function cn^(...inputs: ClassValue[]^) {
        echo   return twMerge^(clsx^(inputs^)^)
        echo }
    ) > "Frontend\src\lib\utils.ts"
    echo [OK] Fixed missing utils.ts
    echo.
)

echo Checking dependencies...
echo.

REM Check and install any missing Python dependencies
echo Verifying Python dependencies...
pipenv install --deploy >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Some dependencies may be missing or outdated. Installing/updating...
    pipenv install --skip-lock
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to install dependencies
        echo Please try running 1-INSTALL.bat again
        pause
        exit /b 1
    )
)

echo.
echo Starting WhatsApp Scheduler...
echo.
echo The app will open in your browser at:
echo   http://localhost:5173
echo.
echo ========================================================
echo.
echo              TO STOP THE APP:
echo         Press Ctrl+C in this window
echo.
echo ========================================================
echo.

REM Ensure pipenv and all tools are in PATH for subprocesses
set PIPENV_VERBOSITY=-1
set PIPENV_YES=1

REM Set environment variable to tell start.py we've already checked dependencies
set WHATSAPP_SKIP_CHECKS=1

REM Export the virtual environment path for start.py
set VIRTUAL_ENV=%VENV_PATH%

REM Run the Python starter using pipenv
echo Starting application...
echo.
pipenv run python start.py

REM If we get here, the app was stopped
echo.
echo.
echo ========================================================
echo App stopped.
echo ========================================================
pause
