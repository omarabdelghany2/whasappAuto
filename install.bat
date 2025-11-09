@echo off
REM WhatsApp Scheduler - Windows Installation Script
REM This batch file calls the cross-platform Python installer

echo.
echo ================================================
echo WhatsApp Scheduler - Windows Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Run the Python installer
echo Running installation script...
echo.
python install.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo To start the application, run: start.bat
echo Or double-click start.bat
echo.
pause
