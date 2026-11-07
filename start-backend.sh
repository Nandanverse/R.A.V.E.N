#!/usr/bin/env bash
# RAVEN Backend Startup Script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PATH="$SCRIPT_DIR/backend/.venv"
BACKEND_DIR="$SCRIPT_DIR/backend"

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

echo "Starting RAVEN Backend..."
echo "Backend will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"

cd "$BACKEND_DIR"
"$VENV_PATH/bin/python" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload