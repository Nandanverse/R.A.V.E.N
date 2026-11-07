# Architecture Documentation

## System Overview

RAVEN follows a modular, service-oriented architecture with clear separation of concerns between the frontend, backend API, data layer, and external integrations.

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAVEN Application                         │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript + Vite + Tailwind)                │
│  ├── Pages: Overview, Assessments, Assets, Recon, Intel,        │
│  │       Findings, Attack Graph, AI Analysis, Analytics,        │
│  │       Reports, Settings, About                               │
│  ├── Components: UI primitives, patterns, features              │
│  └── State: TanStack Query (server), React Context (UI)         │
├─────────────────────────────────────────────────────────────────┤
│  Backend API (FastAPI + Python 3.12+)                           │
│  ├── API Layer: REST endpoints, OpenAPI docs, middleware        │
│  ├── Modules:                                                    │
│  │   ├── ReconCore — Host discovery, port scanning, service enum│
│  │   ├── SurfaceMapper — Asset inventory, relationships         │
│  │   ├── VulnIntel — CVE ingestion, CVSS, EPSS, KEV, ATT&CK    │
│  │   ├── RavenBrain — Ollama LLM, structured proposals, RAG    │
│  │   ├── PolicyEngine — Scope validation, execution levels     │
│  │   ├── TestExecutor — Controlled test execution, ZAP         │
│  │   ├── EvidenceVault — Evidence storage, integrity hashes    │
│  │   ├── AttackGraph — Graph building, path enumeration        │
│  │   ├── RiskEngine — Contextual risk scoring                 │
│  │   ├── AnalyticsEngine — Real metrics, dashboards            │
│  │   └── ReportForge — PDF, HTML, JSON reports                │
│  ├── Tasks: Celery background jobs (scans, intel updates, reports)│
│  └── Database: SQLAlchemy 2.0 async ORM + Alembic migrations  │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                      │
│  ├── PostgreSQL 15+ — Primary relational store                 │
│  ├── Redis 7+ — Celery broker, caching, rate limiting          │
│  └── Filesystem — Evidence files, reports, intel caches        │
├─────────────────────────────────────────────────────────────────┤
│  External Integrations                                           │
│  ├── Ollama — Local LLM inference (HTTP API)                   │
│  ├── Nmap — Network scanning (subprocess, XML output)          │
│  ├── OWASP ZAP — Web app scanning (REST API)                   │
│  ├── httpx — HTTP discovery and testing                        │
│  ├── NVD API — CVE data feeds (JSON)                           │
│  ├── EPSS CSV — Exploit prediction scores                      │
│  ├── CISA KEV — Known exploited vulnerabilities                │
│  └── MITRE ATT&CK — Technique mappings (STIX/JSON)             │
└─────────────────────────────────────────────────────────────────┘
```

## Module Boundaries

Each module is a Python package under `backend/app/` with:

- `models.py` — SQLAlchemy models
- `schemas.py` — Pydantic request/response schemas
- `repository.py` — Data access layer
- `service.py` — Business logic
- `api.py` — FastAPI router
- `tests/` — Unit and integration tests

Modules communicate via:
- Direct service calls (same process)
- Database transactions (shared PostgreSQL)
- Celery tasks (async background work)
- Events (for audit logging, notifications)

## Data Flow

### Assessment Lifecycle

```
1. User creates Assessment via API
   → POST /api/v1/assessments
   → Creates Assessment record, Scope records
   → Returns assessment_id

2. User starts Reconnaissance
   → POST /api/v1/recon/scans
   → Celery task: recon.tasks.run_scan(assessment_id, scan_config)
   → Nmap executed, XML parsed, Assets/Services stored
   → ScanHistory record created

3. VulnIntel correlates findings
   → Celery task: intel.tasks.correlate_services(assessment_id)
   → Matches service fingerprints to CVEs
   → Creates Vulnerability records with confidence scores

4. RavenBrain proposes actions
   → Celery task: brain.tasks.analyze_and_propose(assessment_id)
   → Retrieves context (assets, vulns, evidence)
   → Calls Ollama with structured prompt
   → Validates LLM output against proposal schema
   → Creates Proposal records

5. PolicyEngine validates proposals
   → For each proposal: policy.engine.evaluate(proposal)
   → Checks: scope, execution level, rate limits, budgets, approvals
   → Creates PolicyDecision record (approved/rejected)
   → Approved → queued for execution

6. TestExecutor runs approved tests
   → Celery task: executor.tasks.run_test(proposal_id)
   → Executes test (ZAP, header analysis, authz check, etc.)
   → Stores Evidence, creates Finding records
   → Updates Proposal with execution result

7. AttackGraph builds relationships
   → Triggered on Finding creation
   → graph.builder.build_from_findings(assessment_id)
   → Creates GraphNodes, GraphEdges with evidence refs

8. RiskEngine calculates scores
   → Triggered on graph update
   → risk.engine.calculate_contextual_risk(finding_id)
   → Stores RiskScore with factor breakdown

9. AnalyticsEngine aggregates metrics
   → Periodic Celery task or on-demand
   → Queries database for real metrics
   → Caches results for dashboard

10. ReportForge generates reports
    → POST /api/v1/reports/generate
    → Celery task: reports.tasks.generate(assessment_id, format)
    → Renders template with assessment data
    → Stores Report record with file path
```

## Database Schema Overview

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | Local application profiles |
| `assessments` | Assessment metadata, status, config |
| `scopes` | Authorized target definitions (domain, CIDR, IP) |
| `assets` | Discovered hosts, IPs, domains, web apps |
| `services` | Port, protocol, service name, version, fingerprint |
| `vulnerabilities` | CVE records with CVSS, EPSS, KEV, ATT&CK |
| `findings` | Validated/suspected vulnerabilities with evidence |
| `evidence` | HTTP requests/responses, tool output, hashes |
| `scan_history` | Reconnaissance run records |
| `proposals` | LLM action proposals with reasoning |
| `policy_decisions` | Policy engine approval/rejection records |
| `graph_nodes` | Attack graph nodes (assets, services, vulns, findings) |
| `graph_edges` | Attack graph relationships with evidence |
| `risk_scores` | Contextual risk calculations with factors |
| `reports` | Generated report metadata and file references |
| `audit_events` | Immutable audit trail |

### Key Relationships

- Assessment 1:N Scopes, Assets, Services, Findings, Proposals, Reports
- Asset 1:N Services, Findings
- Service 1:N Vulnerabilities (via correlation)
- Finding N:1 Vulnerability, 1:N Evidence
- Proposal 1:1 PolicyDecision, 1:1 ExecutionJob
- GraphNode N:M GraphNode (via GraphEdge)

## Security Model

### Trust Boundaries

```
┌────────────────────────────────────────────────────────────┐
│                     TRUSTED ZONE                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Frontend   │  │   Backend   │  │  Database   │         │
│  │  (Browser)  │◄─┤   (API)     │◄─┤ (PostgreSQL)│         │
│  └─────────────┘  └──────┬──────┘  └─────────────┘         │
│                         │                                    │
│  ┌─────────────┐  ┌──────▼──────┐  ┌─────────────┐         │
│  │   Celery    │  │    Redis    │  │   Files     │         │
│  │  Workers    │◄─┤  (Broker)   │  │  (Evidence) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└────────────────────────────────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
    ┌─────────────┐ ┌─────────┐ ┌──────────┐
    │   Ollama    │ │  Nmap   │ │   ZAP    │
    │  (Local)    │ │ (Local) │ │ (Local)  │
    └─────────────┘ └─────────┘ └──────────┘
            │            │            │
            ▼            ▼            ▼
    ┌─────────────────────────────────────┐
    │        UNTRUSTED / TARGET ZONE       │
    │  Authorized targets only (allowlist) │
    └─────────────────────────────────────┘
```

### Authorization Flow

1. **Scope Definition**: Admin configures `ALLOWED_TARGETS` in environment
2. **Assessment Creation**: User selects targets from allowlist
3. **Pre-Execution Validation**: Every action checked against scope
4. **Policy Decision**: L1/L2 auto-approved within limits; L3 requires human
5. **Audit Trail**: All decisions logged immutably

### Data Protection

- Secrets never logged (structured logging with redaction)
- Evidence integrity: SHA-256 hashes stored, verified on read
- PII minimization: Only target identifiers stored, no user data
- Encryption at rest: PostgreSQL TDE, filesystem encryption recommended
- Encryption in transit: TLS for all service communication

## Deployment Architecture

### Development (Docker Compose)

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: raven
      POSTGRES_USER: raven
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U raven"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD", "ollama", "list"]
      interval: 30s
      timeout: 10s
      retries: 3

  zap:
    image: owasp/zap2docker-stable:latest
    command: zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/JSON/core/view/version/"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql+asyncpg://raven:raven@postgres:5432/raven
      - REDIS_URL=redis://redis:6379/0
      - OLLAMA_BASE_URL=http://ollama:11434
      - ZAP_API_URL=http://zap:8080

  frontend:
    build: ./frontend
    command: npm run dev -- --host 0.0.0.0
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

### Production Considerations

- Backend: Gunicorn + Uvicorn workers, behind reverse proxy (nginx/Traefik)
- Frontend: Static build served by nginx or CDN
- Database: Managed PostgreSQL (Cloud SQL, RDS) with backups
- Redis: Managed Redis (Memorystore, ElastiCache) with persistence
- Ollama: Dedicated GPU instance for model inference
- ZAP: Separate scanning infrastructure, not co-located with API
- Monitoring: Prometheus + Grafana, structured logs to Loki/ELK
- Secrets: External secret manager (HashiCorp Vault, AWS Secrets Manager)

## Scalability Considerations

- **Horizontal scaling**: Backend stateless, multiple replicas behind load balancer
- **Celery workers**: Separate queues per module (recon, intel, brain, executor, reports)
- **Database**: Read replicas for analytics queries, connection pooling (PgBouncer)
- **Caching**: Redis for rate limiting, session data, intel cache
- **File storage**: S3-compatible for evidence/reports in production

## Failure Modes & Mitigations

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| PostgreSQL down | Health check `/ready` fails | Circuit breaker, retry with backoff |
| Redis down | Celery broker unreachable | Fallback to database-backed queue |
| Ollama down | `/health` check fails | Degrade to offline mode, cache proposals |
| Nmap missing | Tool availability check | Skip port scans, flag in UI |
| ZAP down | API health check fails | Queue scans, retry with backoff |
| Intel feed unavailable | Feed fetch errors | Use cached data, alert admin |
| Disk full | Monitoring alert | Log rotation, evidence cleanup policy |

---

*Architecture version: 1.0*
*Last updated: 2026-11-06*
