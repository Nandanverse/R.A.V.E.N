# Installation Guide

This guide covers installing RAVEN on Windows, Linux, and macOS.

## Prerequisites

### Required Software

| Tool | Minimum Version | Windows | Linux/macOS |
|------|-----------------|---------|-------------|
| Python | 3.12+ | python.org | apt install python3.12 / brew install python@3.12 |
| Node.js | 20+ | nodejs.org | apt install nodejs / brew install node |
| npm | 10+ | Included with Node.js | Included with Node.js |
| Git | 2.40+ | git-scm.com | apt install git / brew install git |
| Docker | 24+ | Docker Desktop | apt install docker.io / brew install docker |
| Docker Compose | 2.20+ | Included with Docker Desktop | apt install docker-compose / Included with Docker |
| Ollama | Latest | ollama.com | curl -fsSL https://ollama.com/install.sh | sh |
| Nmap | 7.94+ | nmap.org | apt install nmap / brew install nmap |
| OWASP ZAP | 2.14+ | zaproxy.org | Included via Docker |

### Verify Prerequisites

```bash
# Check versions
python --version    # Should be 3.12+
node --version      # Should be 20+
npm --version       # Should be 10+
git --version
docker --version
docker compose version
ollama --version
nmap --version
```

## Windows Installation

### Option 1: Automated Setup (Recommended)

```powershell
# Clone repository
git clone https://github.com/nandanamin/raven.git
cd raven

# Run setup script (run as Administrator for Chocolatey installs if needed)
.\setup.ps1

# Start application
.\start.ps1
```

### Option 2: Manual Setup

```powershell
# 1. Clone
git clone https://github.com/nandanamin/raven.git
cd raven

# 2. Create Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install backend dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Configure environment
Copy-Item .env.example .env
# Edit .env with your settings (see Configuration section)

# 6. Start infrastructure services
docker compose up -d postgres redis ollama zap

# 7. Wait for services to be healthy
docker compose ps
# Verify: postgres (healthy), redis (healthy), ollama (healthy), zap (healthy)

# 8. Run database migrations
alembic upgrade head

# 9. Pull Ollama model (in separate terminal)
ollama pull llama3.1:8b

# 10. Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 11. Start frontend (in separate terminal)
cd frontend
npm run dev
```

## Linux/macOS Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/nandanamin/raven.git
cd raven

# Run setup script
chmod +x setup.sh
./setup.sh

# Start application
./start.sh
```

### Option 2: Manual Setup

```bash
# 1. Clone
git clone https://github.com/nandanamin/raven.git
cd raven

# 2. Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Upgrade pip and install backend dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Configure environment
cp .env.example .env
# Edit .env with your settings

# 6. Start infrastructure services
docker compose up -d postgres redis ollama zap

# 7. Wait for services to be healthy
docker compose ps

# 8. Run database migrations
alembic upgrade head

# 9. Pull Ollama model
ollama pull llama3.1:8b

# 10. Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 11. Start frontend (in separate terminal)
cd frontend && npm run dev
```

## Docker-Only Installation

For a fully containerized setup (no local Python/Node required):

```bash
git clone https://github.com/nandanamin/raven.git
cd raven
cp .env.example .env
# Edit .env

# Build and start all services
docker compose up -d --build

# Run migrations
docker compose exec backend alembic upgrade head

# Pull Ollama model
docker compose exec ollama ollama pull llama3.1:8b

# Access:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Post-Installation Verification

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health
# Expected: {"status": "healthy", "checks": {"database": true, "redis": true, "ollama": true, "tools": true}}

# Backend readiness
curl http://localhost:8000/ready
# Expected: {"ready": true}

# Frontend
curl -I http://localhost:5173
# Expected: 200 OK

# Database connectivity
alembic current
# Should show current revision

# Ollama model
ollama list
# Should show llama3.1:8b (or configured model)

# Nmap
nmap --version

# ZAP
curl http://localhost:8080/JSON/core/view/version/
```

### First Assessment

1. Open http://localhost:5173
2. Navigate to Assessments - New Assessment
3. Enter a name and description
4. Add authorized targets (must match ALLOWED_TARGETS in .env)
5. Select execution level L1 (Passive) for first run
6. Click Create Assessment
7. Navigate to Reconnaissance, select the assessment
8. Run a Host Discovery scan
9. Verify assets appear in Asset Inventory

## Troubleshooting Installation

| Issue | Cause | Solution |
|-------|-------|----------|
| docker compose up fails | Port conflicts | Stop services using ports 5432, 6379, 11434, 8080, 8000, 5173 |
| alembic upgrade head fails | Database not ready | Wait for postgres healthcheck, check docker compose logs postgres |
| ollama pull fails | Model not found / network | Check Ollama running, try ollama pull llama3.1:8b manually |
| npm install fails | Node version mismatch | Use Node 20+ (nvm use 20 or fnm use 20) |
| pip install fails | Missing build tools | Windows: pip install --upgrade pip setuptools wheel; Linux: apt install build-essential python3-dev |
| Backend imports fail | Venv not activated | Ensure .venv\Scripts\Activate.ps1 (Win) or source .venv/bin/activate (Unix) |
| Frontend blank page | API URL mismatch | Check VITE_API_URL in frontend/.env matches backend |
| Nmap permission denied | Raw socket permissions | Linux: sudo setcap cap_net_raw+ep $(which nmap) or run as root for scans |

## Uninstallation

```bash
# Stop all services
docker compose down

# Remove containers, volumes, networks
docker compose down -v --remove-orphans

# Remove virtual environment
rm -rf .venv

# Remove frontend dependencies
rm -rf frontend/node_modules

# Remove Ollama models (optional)
ollama rm llama3.1:8b

# Remove project directory
cd .. && rm -rf raven
```

---

Installation guide version: 1.0
Last updated: 2026-11-06
