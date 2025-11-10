========================================
WhatsApp Scheduler - Windows Quick Start
========================================

This folder contains easy-to-use batch files for Windows users.

INSTALLATION:
-------------
1. Double-click "1-INSTALL.bat"
   - This will automatically install:
     * Python 3
     * Node.js
     * Google Chrome (if needed)
     * All dependencies

   Note: If you get a "pipenv not recognized" error after installation,
         just close the window and try again. This is normal after first install.

STARTING THE APP:
-----------------
2. Double-click "2-START.bat"
   - This will start both backend and frontend servers
   - Your browser will open automatically at http://localhost:5173
   - Keep the window open while using the app
   - Press Ctrl+C to stop the app

TROUBLESHOOTING:
----------------
If you see "pipenv is not recognized" error:
  1. Close the command window
  2. Open a new command window
  3. Try running the file again

If installation fails:
  - Make sure you have a stable internet connection
  - Try running the install file as Administrator:
    Right-click -> "Run as Administrator"

PATH FIX (if needed):
---------------------
If pipenv still doesn't work after installation:
  - Double-click "FIX-PATH.bat" to add pipenv to your system PATH

PORTABLE TO OTHER LAPTOPS:
---------------------------
To use this on another laptop:
  1. Copy the entire project folder
  2. Run "1-INSTALL.bat" on the new laptop
  3. Everything will be installed automatically

SYSTEM REQUIREMENTS:
--------------------
- Windows 10 or later
- Internet connection (for installation)
- At least 2GB free disk space

For more information, visit:
https://github.com/anthropics/claude-code

========================================
