#!/usr/bin/env bash
# RAVEN Frontend Startup Script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

FRONTEND_DIR="$SCRIPT_DIR/frontend"

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    echo "Frontend dependencies not installed. Run ./setup.sh first."
    exit 1
fi

echo "Starting RAVEN Frontend..."
echo "Frontend will be available at: http://localhost:5173"

cd "$FRONTEND_DIR"
npm run dev