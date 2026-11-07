#!/usr/bin/env bash
# RAVEN Setup Script for Linux/macOS
# Installs and configures RAVEN (Risk-Aware Autonomous Vulnerability Exploration Network)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
RESET='\033[0m'

success() { echo -e "${GREEN}âœ“${RESET} $*"; }
error() { echo -e "${RED}âœ—${RESET} $*"; }
warning() { echo -e "${YELLOW}âš ${RESET} $*"; }
info() { echo -e "${BLUE}â„¹${RESET} $*"; }
header() { echo -e "\n${BLUE}=== $* ===${RESET}"; }

SKIP_DOCKER=false
SKIP_OLLAMA=false
MINIMAL=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-docker) SKIP_DOCKER=true ;;
        --skip-ollama) SKIP_OLLAMA=true ;;
        --minimal) MINIMAL=true ;;
        --force) FORCE=true ;;
        *) error "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

header "RAVEN Setup - Risk-Aware Autonomous Vulnerability Exploration Network"
info "Project: https://github.com/nandanamin/RAVEN"
info "Author: Nandan Amin"

# Setup status
declare -A STATUS=(
    [Python]=false [Node]=false [Git]=false [Docker]=false
    [Ollama]=false [Nmap]=false [Zap]=false [Venv]=false
    [PyDeps]=false [NodeDeps]=false [Config]=false [Database]=false
    [Migrations]=false [HealthCheck]=false
)

command_exists() { command -v "$1" >/dev/null 2>&1; }

docker_running() { docker version --format '{{.Server.Version}}' >/dev/null 2>&1; }

header "Checking Prerequisites"

# Python
info "Checking Python..."
if command_exists python3; then
    PY_VERSION=$(python3 --version 2>&1)
    if [[ $PY_VERSION =~ Python\ 3\.(1[0-9]|[2-9][0-9]) ]]; then
        success "Found: $PY_VERSION"
        STATUS[Python]=true
    else
        error "Python 3.10+ required. Found: $PY_VERSION"
    fi
else
    error "Python 3 not found. Install via package manager (apt, dnf, brew, etc.)"
fi

# Node.js
info "Checking Node.js..."
if command_exists node; then
    NODE_VERSION=$(node --version)
    if [[ $NODE_VERSION =~ v(1[8-9]|[2-9][0-9])\. ]]; then
        success "Found: $NODE_VERSION"
        STATUS[Node]=true
    else
        error "Node.js 18+ required. Found: $NODE_VERSION"
    fi
else
    error "Node.js not found. Install from https://nodejs.org or via package manager"
fi

# Git
info "Checking Git..."
if command_exists git; then
    success "Found: $(git --version)"
    STATUS[Git]=true
else
    error "Git not found. Install via package manager"
fi

# Docker
if [[ "$SKIP_DOCKER" != "true" ]]; then
    info "Checking Docker..."
    if command_exists docker; then
        success "Found: $(docker --version)"
        if docker_running; then
            success "Docker daemon is running"
            STATUS[Docker]=true
        else
            warning "Docker installed but daemon not running. Start Docker service."
        fi
    else
        warning "Docker not found. Install from https://docker.com"
    fi
else
    info "Skipping Docker check (--skip-docker)"
    STATUS[Docker]=true
fi

# Ollama
if [[ "$SKIP_OLLAMA" != "true" ]]; then
    info "Checking Ollama..."
    if command_exists ollama; then
        success "Found: $(ollama --version)"
        STATUS[Ollama]=true
    else
        warning "Ollama not found. Install from https://ollama.ai"
        info "After installing: ollama pull llama3.1:8b"
    fi
else
    info "Skipping Ollama check (--skip-ollama)"
    STATUS[Ollama]=true
fi

# Nmap
info "Checking Nmap..."
if command_exists nmap; then
    success "Found: $(nmap --version | head -1)"
    STATUS[Nmap]=true
else
    warning "Nmap not found. Install via package manager (apt install nmap, brew install nmap, etc.)"
    [[ "$MINIMAL" != "true" ]] && info "Nmap is required for reconnaissance functionality"
fi

# OWASP ZAP
info "Checking OWASP ZAP..."
if command_exists zap.sh; then
    success "Found: zap.sh in PATH"
    STATUS[Zap]=true
elif [[ -f "/Applications/OWASP ZAP.app/Contents/MacOS/zap.sh" ]]; then
    success "Found: ZAP at default macOS location"
    STATUS[Zap]=true
elif [[ -f "/opt/zaproxy/zap.sh" ]]; then
    success "Found: ZAP at /opt/zaproxy/zap.sh"
    STATUS[Zap]=true
else
    warning "OWASP ZAP not found. Download from https://www.zaproxy.org/download/"
    [[ "$MINIMAL" != "true" ]] && info "ZAP is required for web application scanning"
fi

# Check critical prerequisites
CRITICAL_FAILED=()
[[ "${STATUS[Python]}" != "true" ]] && CRITICAL_FAILED+=("Python")
[[ "${STATUS[Node]}" != "true" ]] && CRITICAL_FAILED+=("Node.js")
[[ "${STATUS[Git]}" != "true" ]] && CRITICAL_FAILED+=("Git")

if [[ ${#CRITICAL_FAILED[@]} -gt 0 ]]; then
    error "Critical prerequisites missing: ${CRITICAL_FAILED[*]}"
    info "Please install missing prerequisites and run setup again."
    exit 1
fi

header "Creating Python Virtual Environment"

VENV_PATH="$SCRIPT_DIR/backend/.venv"
if [[ -d "$VENV_PATH" && "$FORCE" != "true" ]]; then
    warning "Virtual environment already exists at $VENV_PATH"
    info "Use --force to recreate"
    STATUS[Venv]=true
else
    [[ -d "$VENV_PATH" ]] && rm -rf "$VENV_PATH"
    python3 -m venv "$VENV_PATH"
    success "Virtual environment created at $VENV_PATH"
    STATUS[Venv]=true
fi

header "Installing Python Dependencies"

PIP="$VENV_PATH/bin/pip"
REQ_FILE="$SCRIPT_DIR/backend/requirements.txt"

if [[ -f "$REQ_FILE" ]]; then
    "$PIP" install --upgrade pip
    "$PIP" install -r "$REQ_FILE"
    success "Python dependencies installed"
    STATUS[PyDeps]=true
else
    error "requirements.txt not found at $REQ_FILE"
    exit 1
fi

header "Installing Frontend Dependencies"

FRONTEND_DIR="$SCRIPT_DIR/frontend"
if [[ -d "$FRONTEND_DIR" ]]; then
    cd "$FRONTEND_DIR"
    npm install
    success "Frontend dependencies installed"
    STATUS[NodeDeps]=true
    cd "$SCRIPT_DIR"
else
    error "Frontend directory not found"
    exit 1
fi

header "Creating Configuration"

ENV_EXAMPLE="$SCRIPT_DIR/.env.example"
ENV_FILE="$SCRIPT_DIR/.env"

if [[ -f "$ENV_FILE" && "$FORCE" != "true" ]]; then
    warning ".env already exists. Skipping creation."
    info "Use --force to overwrite"
    STATUS[Config]=true
elif [[ -f "$ENV_EXAMPLE" ]]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    success "Created .env from template"
    warning "IMPORTANT: Edit .env and set SECRET_KEY and other sensitive values!"
    STATUS[Config]=true
else
    error ".env.example not found"
    exit 1
fi

header "Initializing Database"

if [[ "${STATUS[Docker]}" == "true" ]]; then
    info "Starting PostgreSQL and Redis via Docker Compose..."
    docker compose up -d postgres redis
    success "Database services started"

    info "Waiting for PostgreSQL to be ready..."
    ATTEMPT=0
    MAX_ATTEMPTS=30
    while [[ $ATTEMPT -lt $MAX_ATTEMPTS ]]; do
        if docker exec raven-postgres pg_isready -U raven -d raven >/dev/null 2>&1; then
            success "PostgreSQL is ready"
            break
        fi
        sleep 2
        ((ATTEMPT++))
    done
    if [[ $ATTEMPT -ge $MAX_ATTEMPTS ]]; then
        error "PostgreSQL did not become ready in time"
        exit 1
    fi
    STATUS[Database]=true
else
    warning "Docker not available. Skipping database initialization."
    info "Ensure PostgreSQL is running on localhost:5432 with database 'raven'"
    info "Connection string: postgresql+asyncpg://raven:raven@localhost:5432/raven"
    STATUS[Database]=true
fi

header "Running Database Migrations"

if [[ "${STATUS[Database]}" == "true" ]]; then
    cd "$SCRIPT_DIR/backend"
    "$PIP" -m alembic upgrade head
    success "Database migrations completed"
    STATUS[Migrations]=true
    cd "$SCRIPT_DIR"
fi

header "Health Checks"

if [[ "${STATUS[Migrations]}" == "true" ]]; then
    info "Testing backend startup..."
    cd "$SCRIPT_DIR/backend"
    "$VENV_PATH/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8001 >/tmp/raven_backend.log 2>&1 &
    BACKEND_PID=$!
    sleep 5

    if curl -sf http://127.0.0.1:8001/health >/dev/null 2>&1; then
        success "Backend health check passed"
        STATUS[HealthCheck]=true
    else
        warning "Backend health endpoint not reachable"
        cat /tmp/raven_backend.log
    fi
    kill $BACKEND_PID 2>/dev/null || true
    cd "$SCRIPT_DIR"
fi

header "Setup Summary"

PASSED=0
TOTAL=${#STATUS[@]}
for step in "${!STATUS[@]}"; do
    if [[ "${STATUS[$step]}" == "true" ]]; then
        ((PASSED++))
        printf "  ${GREEN}âœ“${RESET} %s\n" "$step"
    else
        printf "  ${RED}âœ—${RESET} %s\n" "$step"
    fi
done

info "Steps completed: $PASSED / $TOTAL"

if [[ $PASSED -eq $TOTAL ]]; then
    success "\nSetup completed successfully!"
else
    warning "\nSetup completed with some optional components missing."
    info "Missing optional components will limit functionality but core features will work."
fi

header "Next Steps"

info "1. Edit .env file and configure:"
info "   - SECRET_KEY (generate with: python3 -c \"import secrets; print(secrets.token_hex(32))\")"
info "   - OLLAMA_MODEL (default: llama3.1:8b)"
info "   - DATABASE_URL if using external PostgreSQL"

info "\n2. Start Ollama and pull model (if not done):"
info "   ollama serve"
info "   ollama pull llama3.1:8b"

info "\n3. Start the application:"
info "   Backend:  ./start-backend.sh"
info "   Frontend: ./start-frontend.sh"
info "   Or use:   ./start.sh (starts both)"

info "\n4. Access the application:"
info "   Frontend: http://localhost:5173"
info "   Backend API: http://localhost:8000"
info "   API Docs: http://localhost:8000/docs"

info "\n5. Create your first assessment:"
info "   - Go to Settings > Scopes and define authorized targets"
info "   - Go to Assessments and create a new assessment"
info "   - Select scope and start reconnaissance"

info "\nDocumentation: See docs/ directory for detailed guides"