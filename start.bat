@echo off
REM WhatsApp Scheduler - Windows Startup Script
REM This batch file calls the cross-platform Python startup script

echo.
echo ================================================
echo WhatsApp Scheduler - Starting Application
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "Pipfile" (
    echo [ERROR] Project files not found!
    echo Make sure you're running this from the project directory.
    pause
    exit /b 1
)

if not exist "Frontend\node_modules" (
    echo [WARNING] Dependencies not installed!
    echo Please run install.bat first.
    echo.
    pause
    exit /b 1
)

REM Run the Python startup script
echo Starting WhatsApp Scheduler...
echo.
echo Press Ctrl+C to stop the application
echo.
python start.py

REM If the Python script exits, pause so user can see any error messages
if %errorlevel% neq 0 (
    echo.
    echo Application stopped with errors.
    pause
)
