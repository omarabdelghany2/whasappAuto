#!/usr/bin/env python3
"""
WhatsApp Scheduler - Cross-Platform Startup Script
Supports: Windows, macOS, Linux
"""

import os
import sys
import platform
import subprocess
import signal
import time
import webbrowser
from pathlib import Path

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

    @staticmethod
    def disable():
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

def print_info(text):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {text}")

def print_success(text):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {text}")

def print_error(text):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {text}")

def print_header(text):
    print()
    print(f"{Colors.CYAN}{'=' * 50}{Colors.NC}")
    print(f"{Colors.CYAN}{text}{Colors.NC}")
    print(f"{Colors.CYAN}{'=' * 50}{Colors.NC}")
    print()

class ProcessManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.system = platform.system()

    def cleanup(self, signum=None, frame=None):
        """Stop all processes"""
        print()
        print_info("Shutting down WhatsApp Scheduler...")

        # Stop frontend
        if self.frontend_process and self.frontend_process.poll() is None:
            print_info(f"Stopping frontend (PID: {self.frontend_process.pid})...")
            try:
                if self.system == 'Windows':
                    # Windows needs special handling
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.frontend_process.pid)],
                                 capture_output=True)
                else:
                    self.frontend_process.terminate()
                    self.frontend_process.wait(timeout=5)
            except:
                if self.system != 'Windows':
                    try:
                        self.frontend_process.kill()
                    except:
                        pass

        # Stop backend
        if self.backend_process and self.backend_process.poll() is None:
            print_info(f"Stopping backend (PID: {self.backend_process.pid})...")
            try:
                if self.system == 'Windows':
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.backend_process.pid)],
                                 capture_output=True)
                else:
                    self.backend_process.terminate()
                    self.backend_process.wait(timeout=5)
            except:
                if self.system != 'Windows':
                    try:
                        self.backend_process.kill()
                    except:
                        pass

        # Additional cleanup for any remaining processes
        if self.system == 'Windows':
            subprocess.run('taskkill /F /IM uvicorn.exe 2>nul', shell=True, capture_output=True)
            subprocess.run('taskkill /F /IM node.exe /FI "WINDOWTITLE eq vite*" 2>nul', shell=True, capture_output=True)
        else:
            subprocess.run("pkill -f 'uvicorn server:app'", shell=True, capture_output=True)
            subprocess.run("pkill -f 'vite'", shell=True, capture_output=True)

        print_success("All processes stopped. Goodbye!")
        sys.exit(0)

    def cleanup_old_processes(self):
        """Kill any old processes that might be running on our ports"""
        print_info("Cleaning up old processes...")

        if self.system == 'Windows':
            # Kill processes on ports 8000 and 5173
            subprocess.run('FOR /F "tokens=5" %P IN (\'netstat -ano ^| findstr :8000\') DO taskkill /F /PID %P 2>nul',
                         shell=True, capture_output=True)
            subprocess.run('FOR /F "tokens=5" %P IN (\'netstat -ano ^| findstr :5173\') DO taskkill /F /PID %P 2>nul',
                         shell=True, capture_output=True)
        else:
            # Kill processes on ports 8000 and 5173 (macOS/Linux)
            subprocess.run("lsof -ti:8000 | xargs kill -9 2>/dev/null || true", shell=True, capture_output=True)
            subprocess.run("lsof -ti:5173 | xargs kill -9 2>/dev/null || true", shell=True, capture_output=True)
            subprocess.run("pkill -f 'uvicorn server:app' 2>/dev/null || true", shell=True, capture_output=True)
            subprocess.run("pkill -f 'vite' 2>/dev/null || true", shell=True, capture_output=True)

        # Give processes time to clean up
        time.sleep(1)

    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print_info("Checking dependencies...")

        # Check pipenv
        if not self._command_exists('pipenv'):
            print_error("pipenv is not installed or not in PATH")
            print_info("Run install.py first: python install.py")
            return False

        # Check if virtual environment exists
        try:
            result = subprocess.run(['pipenv', '--venv'], capture_output=True, text=True)
            if result.returncode != 0:
                print_error("Python virtual environment not found")
                print_info("Run install.py first: python install.py")
                return False
        except:
            print_error("Could not verify Python environment")
            return False

        # Check node_modules
        frontend_dir = Path('Frontend')
        if not (frontend_dir / 'node_modules').exists():
            print_error("Frontend dependencies not found")
            print_info("Run install.py first: python install.py")
            return False

        print_success("All dependencies ready!")
        return True

    def _command_exists(self, cmd):
        """Check if a command exists"""
        try:
            if self.system == 'Windows':
                subprocess.run(['where', cmd], capture_output=True, check=True)
            else:
                subprocess.run(['which', cmd], capture_output=True, check=True)
            return True
        except:
            return False

    def start_backend(self):
        """Start the backend server"""
        print_info("Starting backend server on http://localhost:8000...")

        backend_log = open('backend.log', 'w')

        try:
            # Use pipenv to run uvicorn
            cmd = ['pipenv', 'run', 'uvicorn', 'server:app', '--host', '0.0.0.0', '--port', '8000']

            if self.system == 'Windows':
                # Windows needs CREATE_NEW_PROCESS_GROUP for proper cleanup
                self.backend_process = subprocess.Popen(
                    cmd,
                    stdout=backend_log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                self.backend_process = subprocess.Popen(
                    cmd,
                    stdout=backend_log,
                    stderr=subprocess.STDOUT,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )

            # Wait for backend to start
            time.sleep(3)

            # Check if process is still running
            if self.backend_process.poll() is not None:
                print_error("Backend failed to start. Check backend.log for details.")
                return False

            print_success(f"Backend started (PID: {self.backend_process.pid})")
            print_info(f"Backend logs: {Path.cwd() / 'backend.log'}")
            return True

        except Exception as e:
            print_error(f"Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the frontend server"""
        print_info("Starting frontend server on http://localhost:5173...")

        frontend_log = open('frontend.log', 'w')

        try:
            frontend_dir = Path('Frontend')

            if self.system == 'Windows':
                # On Windows, use cmd to run npm
                cmd = 'npm.cmd run dev'
                self.frontend_process = subprocess.Popen(
                    cmd,
                    stdout=frontend_log,
                    stderr=subprocess.STDOUT,
                    cwd=frontend_dir,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                cmd = ['npm', 'run', 'dev']
                self.frontend_process = subprocess.Popen(
                    cmd,
                    stdout=frontend_log,
                    stderr=subprocess.STDOUT,
                    cwd=frontend_dir,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )

            # Wait for frontend to start
            time.sleep(4)

            # Check if process is still running
            if self.frontend_process.poll() is not None:
                print_error("Frontend failed to start. Check frontend.log for details.")
                return False

            print_success(f"Frontend started (PID: {self.frontend_process.pid})")
            print_info(f"Frontend logs: {Path.cwd() / 'frontend.log'}")
            return True

        except Exception as e:
            print_error(f"Failed to start frontend: {e}")
            return False

    def open_browser(self):
        """Open the app in the default browser"""
        try:
            print_info("Opening browser...")
            time.sleep(2)
            webbrowser.open('http://localhost:5173')
        except:
            print_warning("Could not open browser automatically")
            print_info("Please open http://localhost:5173 manually")

    def wait_for_shutdown(self):
        """Wait for user to stop the servers"""
        print()
        print_success("=========================================")
        print_success("WhatsApp Scheduler is now running!")
        print_success("=========================================")
        print()
        print_info(f"Backend API: {Colors.GREEN}http://localhost:8000{Colors.NC}")
        print_info(f"Frontend UI: {Colors.GREEN}http://localhost:5173{Colors.NC}")
        print_info(f"API Docs: {Colors.GREEN}http://localhost:8000/docs{Colors.NC}")
        print()
        print_warning("Press Ctrl+C to stop all services")
        print()

        try:
            # Keep the script running
            while True:
                time.sleep(1)

                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print_error("Backend process stopped unexpectedly!")
                    print_info("Check backend.log for details")
                    self.cleanup()

                if self.frontend_process and self.frontend_process.poll() is not None:
                    print_error("Frontend process stopped unexpectedly!")
                    print_info("Check frontend.log for details")
                    self.cleanup()

        except KeyboardInterrupt:
            self.cleanup()

def main():
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    print_header("WhatsApp Scheduler - Startup")
    print_info(f"Project directory: {script_dir}")
    print_info(f"Operating System: {platform.system()}")

    # Create process manager
    manager = ProcessManager()

    # Register signal handlers
    signal.signal(signal.SIGINT, manager.cleanup)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, manager.cleanup)

    # Clean up any old processes first
    manager.cleanup_old_processes()

    # Check dependencies
    if not manager.check_dependencies():
        sys.exit(1)

    print()

    # Start backend
    if not manager.start_backend():
        manager.cleanup()
        sys.exit(1)

    print()

    # Start frontend
    if not manager.start_frontend():
        manager.cleanup()
        sys.exit(1)

    # Open browser
    manager.open_browser()

    # Wait for shutdown
    manager.wait_for_shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
