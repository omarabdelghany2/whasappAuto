#!/bin/bash

# WhatsApp Scheduler Startup Script
# This script starts both the backend and frontend servers
# Press Ctrl+C to stop everything

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Store PIDs
BACKEND_PID=""
FRONTEND_PID=""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Cleanup function to stop all processes
cleanup() {
    echo ""
    print_info "Shutting down WhatsApp Scheduler..."

    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        print_info "Stopping frontend (PID: $FRONTEND_PID)..."
        kill -TERM $FRONTEND_PID 2>/dev/null || true
        wait $FRONTEND_PID 2>/dev/null || true
    fi

    # Kill backend process
    if [ ! -z "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
        print_info "Stopping backend (PID: $BACKEND_PID)..."
        kill -TERM $BACKEND_PID 2>/dev/null || true
        wait $BACKEND_PID 2>/dev/null || true
    fi

    # Kill any remaining uvicorn or vite processes (safety measure)
    pkill -f "uvicorn server:app" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true

    print_success "All processes stopped. Goodbye!"
    exit 0
}

# Trap EXIT, INT, and TERM signals
trap cleanup EXIT INT TERM

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    print_error "pipenv is not installed. Please install it first:"
    print_info "pip install pipenv"
    exit 1
fi

# Check if node is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install it first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install it first."
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_info "Starting WhatsApp Scheduler..."
print_info "Project directory: $SCRIPT_DIR"
echo ""

# Check if Python dependencies are installed
print_info "Checking Python dependencies..."
if ! pipenv --venv &> /dev/null; then
    print_warning "Virtual environment not found. Installing Python dependencies..."
    pipenv install
fi

# Check if node_modules exists in Frontend
if [ ! -d "Frontend/node_modules" ]; then
    print_warning "Frontend dependencies not found. Installing..."
    cd Frontend
    npm install
    cd ..
fi

print_success "All dependencies are ready!"
echo ""

# Start backend server
print_info "Starting backend server on http://localhost:8000..."
pipenv run uvicorn server:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend failed to start. Check backend.log for details."
    exit 1
fi

print_success "Backend started (PID: $BACKEND_PID)"
print_info "Backend logs: $SCRIPT_DIR/backend.log"
echo ""

# Start frontend server
print_info "Starting frontend server on http://localhost:5173..."
cd Frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend failed to start. Check frontend.log for details."
    exit 1
fi

print_success "Frontend started (PID: $FRONTEND_PID)"
print_info "Frontend logs: $SCRIPT_DIR/frontend.log"
echo ""

print_success "========================================="
print_success "WhatsApp Scheduler is now running!"
print_success "========================================="
echo ""
print_info "Backend API: ${GREEN}http://localhost:8000${NC}"
print_info "Frontend UI: ${GREEN}http://localhost:5173${NC}"
print_info "API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
print_warning "Press Ctrl+C to stop all services"
echo ""

# Open browser (optional - works on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Opening browser..."
    sleep 2
    open http://localhost:5173 2>/dev/null || true
fi

# Wait indefinitely (script will run until Ctrl+C)
wait
