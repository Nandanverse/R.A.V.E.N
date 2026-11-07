<div align="center">

<img src="assets/banner.svg" alt="R.A.V.E.N">

<br><br>

# R.A.V.E.N

### Risk-Aware Autonomous Vulnerability Exploration Network

> A unified, locally-hosted cybersecurity assessment platform for authorized security testing.
> Built for engineers who value auditability, control, and local-first architecture.

<br><br>

![License](https://img.shields.io/github/license/nandanamin/raven?style=flat-square&color=3d5a80)
![Python](https://img.shields.io/badge/Python-3.12+-3d5a80?style=flat-square&logo=python&logoColor=c9d1d9)
![React](https://img.shields.io/badge/React-18-3d5a80?style=flat-square&logo=react&logoColor=c9d1d9)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-3d5a80?style=flat-square&logo=fastapi&logoColor=c9d1d9)
![Docker](https://img.shields.io/badge/Docker-Ready-3d5a80?style=flat-square&logo=docker&logoColor=c9d1d9)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-3d5a80?style=flat-square)

</div>

---

## Quick Overview

| Aspect | Details |
|--------|---------|
| Purpose | Authorized security assessment automation |
| Architecture | Microservices (Backend + Frontend + Workers) |
| Deployment | Docker Compose / Bare metal / Windows executable |
| Database | PostgreSQL 16 (asyncpg) + Redis 7 |
| Inference | Ollama (local, no API keys) |
| Scanning | Nmap, OWASP ZAP, httpx |
| Intel Feeds | NVD, CISA KEV, EPSS, MITRE ATT&CK |
| Policy | Mandatory allowlist + 3 execution levels |

---

## Architecture

```
+---------------------------------------------------------------+
|                        RAVEN PLATFORM                          |
+---------------------------------------------------------------+
|  +---------------------------------------------------------+  |
|  |  FRONTEND (React 18 + TypeScript + Vite + Tailwind)    |  |
|  |  Overview Assessments Assets Recon Intel               |  |
|  |  Findings Attack Graph Analysis Analytics Reports      |  |
|  +---------------------------------------------------------+  |
+---------------------------------------------------------------+
|  +---------------------------------------------------------+  |
|  |  BACKEND API (FastAPI + Python 3.12 + SQLAlchemy 2.0) |  |
|  |  REST + OpenAPI WebSocket Background Jobs (Celery)     |  |
|  +---------------------------------------------------------+  |
+------------------+------------------+-----------------------+
|  RECON CORE      |  VULN INTEL      |  REASONING ENGINE    |
|  Nmap httpx      |  NVD CISA KEV    |  Ollama Structured   |
|  Service Enum    |  EPSS ATT&CK     |  JSON RAG Policy     |
+------------------+------------------+-----------------------+
|  POLICY ENGINE   |  TEST EXECUTOR   |  EVIDENCE VAULT      |
|  Allowlist L1    |  ZAP Headers     |  SHA-256 Redaction   |
|  L2 L3 Audit     |  AuthZ Injection |  Chain of Custody    |
+------------------+------------------+-----------------------+
|  ATTACK GRAPH    |  RISK ENGINE     |  ANALYTICS  REPORT   |
|  Cytoscape.js    |  CVSS+EPSS+KEV   |  Real Data PDF/HTML  |
+---------------------------------------------------------------+
|  DATA LAYER: PostgreSQL (Primary) Redis (Queue/Cache) FS     |
+---------------------------------------------------------------+
```

---

## Capabilities

<details>
<summary><b>Reconnaissance (ReconCore)</b></summary>

- Authorized target discovery with explicit scope validation
- Host discovery: ping sweep, ARP, TCP SYN
- Port scanning: top-ports, full range, custom
- Service enumeration & version detection
- HTTP endpoint discovery & tech fingerprinting
- Scan history & differential analysis

</details>

<details>
<summary><b>Asset Inventory (SurfaceMapper)</b></summary>

- Normalized database: hosts, IPs, domains, web apps, APIs, ports, services, technologies
- Searchable, filterable inventory with relationships
- Asset criticality tagging & ownership tracking

</details>

<details>
<summary><b>Vulnerability Intelligence (VulnIntel)</b></summary>

- CVE ingestion from NVD (incremental JSON feeds)
- CVSS v3.1 scoring & vector parsing
- EPSS exploit probability enrichment
- CISA Known Exploited Vulnerabilities (KEV) matching
- MITRE ATT&CK technique mapping
- Source attribution & timestamps for all records
- Local caching with explicit refresh operations

</details>

<details>
<summary><b>Reasoning Engine (Local Inference)</b></summary>

- Local inference via Ollama (free, private, no API keys)
- Structured JSON action proposals (not arbitrary commands)
- Optimized prompts for security reasoning
- Retrieval-Augmented Generation for vulnerability context
- Graceful degradation when inference engine unavailable

</details>

<details>
<summary><b>Policy Engine (Mandatory)</b></summary>

- Explicit target authorization with allowlists
- Three execution levels: L1 (Passive), L2 (Controlled), L3 (Intrusive)
- Rate limits, timeouts, assessment budgets
- Human approval required for L3 actions
- Emergency stop functionality
- Audit logging of all policy decisions

</details>

<details>
<summary><b>Test Executor</b></summary>

- Controlled execution through policy-approved integrations
- OWASP ZAP integration for active scanning
- HTTP security header analysis
- Cookie security attribute validation
- CORS misconfiguration detection
- API authorization validation (IDOR/BOLA)
- Input validation & injection probing (safe payloads)
- Rate limiting & DoS resilience checks
- Execution queue with tool availability, timeouts, rate limits

</details>

<details>
<summary><b>Evidence Vault</b></summary>

- Finding details with HTTP request/response evidence
- Tool output storage with SHA-256 integrity hashes
- Automatic secret redaction
- Traceable evidence linked to originating test

</details>

<details>
<summary><b>Attack Graph</b></summary>

- Relationship graph: assets, services, vulnerabilities, findings
- Evidence-backed edges only (no speculative paths)
- Attack path enumeration (bounded depth, cycle detection)
- Cytoscape.js visualization with node/edge inspection

</details>

<details>
<summary><b>Risk Engine</b></summary>

- Contextual scoring: CVSS, EPSS, KEV, asset exposure, service criticality, validation confidence, attack-path relationships
- Transparent score explanations
- No arbitrary scores presented as scientific measurements

</details>

<details>
<summary><b>Analytics</b></summary>

- Real database-backed analytics (no placeholder data)
- Vulnerability distribution by severity, validation status
- Asset exposure analysis
- False positive rate tracking (where ground truth exists)
- Tool execution statistics
- Empty states when no assessment has run

</details>

<details>
<summary><b>Report Forge</b></summary>

- PDF, HTML, and JSON report generation
- Assessment scope, methodology, executive summary
- Discovered assets, findings, severity, evidence, validation status
- Risk analysis & remediation recommendations
- Limitations section

</details>

---

## Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Celery, Redis, structlog |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Cytoscape.js, Plotly.js, TanStack Query, React Router v6, React Hook Form + Zod |
| **Inference** | Ollama, local instruction models, structured JSON output |
| **Security Tools** | Nmap, OWASP ZAP, httpx, custom HTTP testing utilities |
| **Intelligence Feeds** | NVD, CISA KEV, EPSS, MITRE ATT&CK |
| **Infrastructure** | Docker, Docker Compose, PostgreSQL 16, Redis 7 |
| **Testing** | Pytest, Vitest, Playwright |
| **Documentation** | MkDocs Material |

---

## Prerequisites

| Tool | Minimum Version | Purpose |
|------|-----------------|---------|
| Python | 3.12+ | Backend runtime |
| Node.js | 20+ | Frontend build/runtime |
| npm | 10+ | Frontend package manager |
| Git | 2.40+ | Version control |
| Docker | 24+ | Containerized services |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Ollama | Latest | Local inference engine |
| Nmap | 7.94+ | Network scanning |
| OWASP ZAP | 2.14+ | Web application scanning |

> **Note:** Ollama, Nmap, and ZAP are bundled in Docker Compose. Install manually only for bare-metal deployment.

---

## Installation

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/nandanamin/raven.git
cd raven

# 2. Configure environment
cp .env.example .env
# Edit .env - REQUIRED: SECRET_KEY, ALLOWED_TARGETS

# 3. Start all services
docker compose up -d

# 4. Access
# Frontend:     http://localhost
# Backend API:  http://localhost:8000
# API Docs:     http://localhost:8000/docs
```

### Option 2: Windows (PowerShell)

```powershell
git clone https://github.com/nandanamin/raven.git
cd raven
.\setup.ps1          # Creates venv, installs deps, runs migrations
.\start.ps1         # Starts backend + frontend
```

### Option 3: Linux/macOS (Bash)

```bash
git clone https://github.com/nandanamin/raven.git
cd raven
chmod +x setup.sh start.sh
./setup.sh          # Creates venv, installs deps, runs migrations
./start.sh          # Starts backend + frontend
```

### Option 4: Manual (Development)

```bash
# Backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
# Edit backend/.env

# Start infrastructure
docker compose up -d postgres redis ollama zap

# Migrations
cd backend && alembic upgrade head && cd ..

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

---

## Configuration

All settings via `.env` file (see `.env.example`):

| Variable | Required | Description | Default |
|----------|:--------:|-------------|---------|
| `SECRET_KEY` | Yes | JWT signing key (32+ chars, generate: `openssl rand -base64 48`) | — |
| `ALLOWED_TARGETS` | Yes | Comma-separated authorized targets/CIDRs | — |
| `DATABASE_URL` | | PostgreSQL connection string | `postgresql+asyncpg://raven:raven@localhost:5432/raven` |
| `REDIS_URL` | | Redis connection string | `redis://localhost:6379/0` |
| `OLLAMA_BASE_URL` | | Inference engine endpoint | `http://localhost:11434` |
| `OLLAMA_MODEL` | | Model for reasoning | `llama3.1:8b` |
| `ZAP_API_URL` | | ZAP daemon API | `http://localhost:8080` |
| `DEBUG` | | Enable debug mode | `false` |
| `LOG_LEVEL` | | Logging level | `INFO` |
| `ASSESSMENT_TIMEOUT_HOURS` | | Max assessment duration | `24` |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | | API rate limit | `60` |

> **Critical:** `ALLOWED_TARGETS` is enforced by the Policy Engine. RAVEN will **only** scan targets in this list.

---

## Usage Workflow

```mermaid
flowchart LR
    A[Create Assessment] --> B[Define Scope]
    B --> C[Run Reconnaissance]
    C --> D[Review Assets]
    D --> E[Correlate VulnIntel]
    E --> F[Reasoning Engine Proposals]
    F --> G{Policy Review}
    G -->|Approved| H[Execute Tests]
    G -->|Rejected| F
    H --> I[Collect Evidence]
    I --> J[Attack Graph Analysis]
    J --> K[Risk Scoring]
    K --> L[Generate Report]
```

### Step-by-Step

1. **Create Assessment** → `Assessments → New Assessment`
   - Name, description, execution level (L1/L2/L3)
   - Scope: domains, IPs, CIDRs (must be in `ALLOWED_TARGETS`)

2. **Reconnaissance** → `Reconnaissance`
   - Select assessment
   - Choose: Host Discovery / Port Scan / Service Enum / HTTP Discovery
   - Execute → Review discovered assets

3. **Vulnerability Intelligence** → `Intel`
   - Auto-correlates discovered services with CVE/KEV/EPSS/ATT&CK
   - Review matches, confidence scores

4. **Reasoning Engine** → `Analysis`
   - Check Ollama status
   - Review structured proposals (action, target, reason, evidence, risk)
   - Approve/Reject (Policy Engine enforces)

5. **Execute Tests** → `Findings`
   - Policy-approved tests run via Test Executor
   - Evidence auto-collected with SHA-256 hashes

6. **Attack Graph** → `Attack Graph`
   - Visualize asset-service-vuln-finding relationships
   - Evidence-backed paths only

7. **Risk Analysis** → `Analytics`
   - Contextual risk scores with explanations
   - Distribution by severity, validation status

8. **Generate Report** → `Reports`
   - Select format: PDF / HTML / JSON
   - Configure sections
   - Download

---

## Example Lab: OWASP Juice Shop

```bash
# 1. Start target
docker run -d -p 3000:3000 bkimminich/juice-shop

# 2. Authorize target
echo "ALLOWED_TARGETS=localhost,127.0.0.1,::1" >> .env

# 3. Restart backend to pick up config
docker compose restart backend

# 4. In UI:
#    - Create assessment targeting http://localhost:3000
#    - Run L2 reconnaissance
#    - Review assets in Inventory
#    - Check Intel correlations
#    - Run Analysis for proposals
#    - Approve controlled tests
#    - View Attack Graph & Risk
#    - Generate report
```

---

## Building from Source

### Windows Executable

```powershell
cd build
.\build.ps1
# Output: build/dist/raven.exe, start_raven.bat, create_shortcut.ps1
# Optional: RAVEN_Setup_v1.0.0.exe (requires Inno Setup 6)
```

### Linux Executable

```bash
cd build
python build_exe.py
# Output: build/dist/raven
```

### Docker Images

```bash
# Build all
docker compose build

# Or individually
docker compose build backend
docker compose build frontend
```

### Automated Releases (GitHub Actions)

Push a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Triggers: Linux/Windows builds → Docker images → GitHub Release with artifacts

**Release Artifacts:**
- `raven-windows-vX.Y.Z.zip` - Windows executable + launcher
- `raven-linux-vX.Y.Z.gz` - Linux executable
- `checksums.txt` - SHA256 verification
- Docker: `ghcr.io/nandanamin/raven/backend:vX.Y.Z`, `ghcr.io/nandanamin/raven/frontend:vX.Y.Z`

---

## Production Deployment

### Docker Compose (Production)

```bash
# 1. Generate secure secrets
openssl rand -base64 48  # SECRET_KEY

# 2. Configure .env.production
cp .env.example .env.production
# Set: SECRET_KEY, ALLOWED_TARGETS, DEBUG=false, LOG_LEVEL=WARNING
# Use external PostgreSQL/Redis for HA

# 3. Deploy with override
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Production Checklist

- [ ] `SECRET_KEY` generated securely (32+ chars)
- [ ] `ALLOWED_TARGETS` restricted to authorized scope only
- [ ] External PostgreSQL with backups configured
- [ ] External Redis with persistence
- [ ] TLS termination (nginx/Traefik/Caddy)
- [ ] Resource limits on containers
- [ ] Log aggregation (Loki/ELK)
- [ ] Health check monitoring
- [ ] Evidence/reports volume backups

### Kubernetes

Helm chart: *Coming soon*

---

## Testing

```bash
# Backend
cd backend
python -m pytest -v
python -m mypy --strict app
python -m ruff check .

# Frontend
cd frontend
npm run test
npm run typecheck
npm run lint
npm run test:e2e
```

---

## Troubleshooting

| Symptom | Resolution |
|---------|------------|
| `docker compose up` fails | Docker daemon running? Ports 5432, 6379, 11434, 8080 free? |
| Model not found | `ollama pull llama3.1:8b` |
| Nmap not found | Install Nmap, verify in PATH |
| ZAP connection refused | ZAP daemon on 8080? `docker compose logs zap` |
| Migration fails | PostgreSQL healthy? `DATABASE_URL` correct? |
| Frontend build fails | `rm -rf node_modules && npm ci` |
| Backend import errors | Venv active? `pip install -r requirements.txt` |
| Policy blocks scan | Target in `ALLOWED_TARGETS`? CIDR format correct? |
| Ollama unavailable | Check `OLLAMA_BASE_URL`, GPU memory for model |

---

## Security Model

RAVEN is designed for **authorized security testing only**.

**Enforced Controls:**
- Explicit target allowlist (`ALLOWED_TARGETS`) - cannot be bypassed
- Three execution levels: L1 Passive / L2 Controlled / L3 Intrusive
- Human approval mandatory for L3 actions
- Policy Engine decisions are final - inference engine cannot override
- Emergency stop terminates all running assessments
- Full audit trail: every action logged with user, timestamp, decision
- Secrets auto-redacted from evidence & logs
- No destructive exploitation, persistence, credential theft, or stealth
- No lateral movement or third-party system compromise

> **Legal:** Never use RAVEN against systems you do not own or have explicit written authorization to test.

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Foundation: Structure, DB, Config, Policy Core, Docker | Active |
| 2 | Reconnaissance: Nmap, HTTP Discovery, Asset Inventory | Planned |
| 3 | VulnIntel: NVD, CVSS, EPSS, KEV, ATT&CK Correlation | Planned |
| 4 | Reasoning Engine: Ollama, Structured Proposals, RAG | Planned |
| 5 | Test Executor: ZAP, Evidence, Audit Logging | Planned |
| 6 | Attack Graph & Risk: Visualization, Path Analysis, Scoring | Planned |
| 7 | Analytics & Reports: Real Data, PDF/HTML/JSON | Planned |
| 8 | Finalization: Docs, Testing, UI Consistency, Release | Planned |

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Author

**Nandan Amin**

- LinkedIn: [linkedin.com/in/nandanamin](https://www.linkedin.com/in/nandanamin)
- Instagram: [instagram.com/nandanverse](https://www.instagram.com/nandanverse/)
- GitHub: [github.com/nandanamin](https://github.com/nandanverse)

---

## Acknowledgments

- NVD, CISA, EPSS, MITRE ATT&CK - Vulnerability intelligence
- Nmap, OWASP ZAP, httpx - Security tooling
- Ollama - Local inference engine
- FastAPI, React, Tailwind, Cytoscape.js, Plotly.js - Core stack

---

<div align="center">

**RAVEN** - Risk-Aware Autonomous Vulnerability Exploration Network

*Built for cybersecurity engineering. Not marketing dashboards.*

</div>

---

<details>
<summary><b>Project Statistics</b></summary>

![Lines of Code](https://img.shields.io/tokei/lines/github/nandanamin/raven?style=flat-square&color=3d5a80)
![Repo Size](https://img.shields.io/github/repo-size/nandanamin/raven?style=flat-square&color=3d5a80)
![Last Commit](https://img.shields.io/github/last-commit/nandanamin/raven?style=flat-square&color=3d5a80)
![Issues](https://img.shields.io/github/issues/nandanamin/raven?style=flat-square&color=3d5a80)
![Stars](https://img.shields.io/github/stars/nandanamin/raven?style=flat-square&color=3d5a80)
![Forks](https://img.shields.io/github/forks/nandanamin/raven?style=flat-square&color=3d5a80)

</details>
