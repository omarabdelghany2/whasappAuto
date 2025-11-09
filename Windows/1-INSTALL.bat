@echo off
REM WhatsApp Scheduler - Windows Installer
REM Double-click this file to install

REM Change to parent directory (go up one level from Windows folder)
cd /d "%~dp0\.."

title WhatsApp Scheduler - Installation
color 0A

echo.
echo ========================================================
echo.
echo          WhatsApp Scheduler - Installation
echo                   for Windows
echo.
echo ========================================================
echo.
echo This will install all required dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: Python is not installed!
    echo ================================================
    echo.
    echo Please install Python first:
    echo   1. Go to: https://www.python.org/downloads/
    echo   2. Download Python 3.7 or higher
    echo   3. Run the installer
    echo   4. IMPORTANT: Check "Add Python to PATH"
    echo   5. Double-click this file again
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: Node.js is not installed!
    echo ================================================
    echo.
    echo Please install Node.js first:
    echo   1. Go to: https://nodejs.org/
    echo   2. Download the LTS version
    echo   3. Run the installer
    echo   4. Double-click this file again
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
echo [OK] Node.js is installed
echo.
echo Starting installation...
echo.
echo This may take 3-5 minutes. Please wait...
echo.

REM Run the Python installer
python install.py

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo.
    echo       Installation Completed Successfully!
    echo.
    echo ========================================================
    echo.
    echo Next step:
    echo   Double-click "2-START.bat" in the Windows folder
    echo.
) else (
    color 0C
    echo.
    echo Installation failed!
    echo Please check the error messages above.
    echo.
)

pause
