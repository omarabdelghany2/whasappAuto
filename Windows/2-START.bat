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

REM Check if dependencies are installed
if not exist "Frontend\node_modules" (
    color 0C
    echo.
    echo ================================================
    echo   ERROR: App is not installed yet!
    echo ================================================
    echo.
    echo Please run installation first:
    echo   Double-click "1-INSTALL.bat" in the Windows folder
    echo.
    pause
    exit /b 1
)

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

REM Run the Python starter
python start.py

REM If we get here, the app was stopped
echo.
echo App stopped.
pause
