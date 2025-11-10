@echo off
REM WhatsApp Scheduler - PATH Fix for Windows
REM Run this if you get "pipenv is not recognized" error

title WhatsApp Scheduler - PATH Fix
color 0E

echo.
echo ========================================================
echo.
echo      WhatsApp Scheduler - PATH Fix Utility
echo.
echo ========================================================
echo.
echo This tool will add pipenv to your system PATH.
echo.
echo Run this if you see "pipenv is not recognized" error.
echo.
pause
echo.

REM Change to parent directory
cd /d "%~dp0\.."

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed!
    echo Please run 1-INSTALL.bat first.
    pause
    exit /b 1
)

echo Detecting Python Scripts path...
echo.

REM Get Python user site packages path
for /f "tokens=*" %%i in ('python -c "import site; print(site.USER_SITE)"') do set USER_SITE=%%i

REM Calculate Scripts path
for %%i in ("%USER_SITE%") do set PARENT=%%~dpi
set SCRIPTS_PATH=%PARENT%Scripts

echo Found Python Scripts at: %SCRIPTS_PATH%
echo.

REM Check if pipenv exists there
if exist "%SCRIPTS_PATH%\pipenv.exe" (
    echo [OK] pipenv.exe found at: %SCRIPTS_PATH%\pipenv.exe
) else (
    echo [!] pipenv.exe not found. You may need to install it first.
    echo Run: python -m pip install --user pipenv
    pause
    exit /b 1
)

echo.
echo Adding to system PATH...
echo.

REM Add to PATH permanently
setx PATH "%PATH%;%SCRIPTS_PATH%"

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo.
    echo            PATH Updated Successfully!
    echo.
    echo ========================================================
    echo.
    echo IMPORTANT: You must close this window and open a new
    echo Command Prompt for the changes to take effect.
    echo.
    echo After closing this window:
    echo   1. Open a NEW Command Prompt or File Explorer
    echo   2. Double-click "2-START.bat"
    echo.
    echo The "pipenv is not recognized" error should be gone!
    echo.
) else (
    color 0C
    echo.
    echo [ERROR] Failed to update PATH
    echo.
    echo You may need to add it manually:
    echo   1. Open System Properties
    echo   2. Click "Environment Variables"
    echo   3. Edit "Path" under User variables
    echo   4. Add: %SCRIPTS_PATH%
    echo.
)

pause
