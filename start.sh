#!/usr/bin/env bash
# RAVEN Startup Script - Starts both backend and frontend

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PATH="$SCRIPT_DIR/backend/.venv"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

BACKEND_ONLY=false
FRONTEND_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only) BACKEND_ONLY=true ;;
        --frontend-only) FRONTEND_ONLY=true ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

start_backend() {
    echo "Starting RAVEN Backend..."
    cd "$BACKEND_DIR"
    "$VENV_PATH/bin/python" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
}

start_frontend() {
    echo "Starting RAVEN Frontend..."
    cd "$FRONTEND_DIR"
    npm run dev &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
}

if [[ "$BACKEND_ONLY" == "true" ]]; then
    start_backend
    wait
elif [[ "$FRONTEND_ONLY" == "true" ]]; then
    start_frontend
    wait
else
    start_backend
    sleep 3
    start_frontend
    echo ""
    echo "RAVEN is starting up!"
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:5173"
    echo "API Docs: http://localhost:8000/docs"
    wait
fi