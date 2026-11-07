# Technical Skills Demonstrated by RAVEN

This document catalogs the actual technical skills demonstrated by the implemented RAVEN project. Skills are organized by domain. For each skill, the specific module and implementation location are referenced.

---

## Implemented Skills

### Offensive Security

| Skill | Module | Implementation |
|-------|--------|----------------|
| Authorized target scoping and validation | PolicyEngine | backend/app/policy/scope_validator.py - Validates all targets against explicit allowlists before any reconnaissance or test execution |
| Network reconnaissance planning | ReconCore | backend/app/recon/planner.py - Builds scan plans based on scope, asset type, and assessment phase |
| Port scanning with Nmap | ReconCore | backend/app/recon/scanners/nmap_scanner.py - Wraps Nmap with structured XML output parsing, rate limiting, and timeout enforcement |
| Service enumeration and version detection | ReconCore | backend/app/recon/scanners/service_enum.py - Parses Nmap service detection output into normalized service records |
| HTTP endpoint discovery | ReconCore | backend/app/recon/discovery/http_discovery.py - Uses httpx and custom logic to enumerate web endpoints, APIs, and technology stacks |
| Web application mapping | SurfaceMapper | backend/app/surface/mapper.py - Correlates discovered HTTP endpoints with hosts, services, and technologies |
| Vulnerability correlation with discovered services | VulnIntel | backend/app/intel/correlator.py - Matches CVE data against fingerprinted software versions and configurations |
| Controlled security test execution | TestExecutor | backend/app/executor/runner.py - Executes policy-approved tests (header analysis, authz checks, input validation) with evidence capture |
| OWASP ZAP integration for active scanning | TestExecutor | backend/app/executor/integrations/zap_client.py - Manages ZAP daemon, triggers scans, retrieves alerts with deduplication |
| Evidence collection and integrity hashing | EvidenceVault | backend/app/evidence/store.py - Stores request/response pairs, tool output, and computes SHA-256 integrity hashes |

### Vulnerability Assessment

| Skill | Module | Implementation |
|-------|--------|----------------|
| CVE ingestion from NVD | VulnIntel | backend/app/intel/feeds/nvd_feed.py - Downloads, parses, and indexes NVD JSON feeds with incremental updates |
| CVSS v3.1 scoring and vector parsing | VulnIntel | backend/app/intel/scoring/cvss.py - Parses CVSS vectors, computes base/temporal/environmental scores |
| EPSS exploit probability enrichment | VulnIntel | backend/app/intel/feeds/epss_feed.py - Fetches EPSS CSV, joins with CVE records for exploit likelihood |
| CISA Known Exploited Vulnerabilities matching | VulnIntel | backend/app/intel/feeds/kev_feed.py - Downloads KEV catalog, flags CVEs with active exploitation evidence |
| MITRE ATT&CK technique mapping | VulnIntel | backend/app/intel/attack/mapper.py - Maps CVE tags and vulnerability types to ATT&CK techniques (TTPs) |
| Vulnerability confidence scoring | VulnIntel | backend/app/intel/scoring/confidence.py - Combines scanner confidence, validation status, and intelligence sources into a 0-100 score |
| Source attribution and timestamps for all intelligence | VulnIntel | backend/app/intel/models.py - Every CVE, EPSS, KEV record includes source_url, fetched_at, last_updated |

### Network Reconnaissance

| Skill | Module | Implementation |
|-------|--------|----------------|
| Host discovery (ping sweep, ARP, TCP SYN) | ReconCore | backend/app/recon/scanners/host_discovery.py - Multiple discovery methods with fallback |
| Top-port and full-port scanning modes | ReconCore | backend/app/recon/scanners/nmap_scanner.py - Configurable port ranges, --top-ports support |
| Service fingerprinting (banner grabbing, SSL/TLS) | ReconCore | backend/app/recon/scanners/service_fingerprint.py - Extracts banners, certificate details, HTTP headers |
| Technology fingerprinting (Wappalyzer-style) | SurfaceMapper | backend/app/surface/tech_fingerprint.py - Matches HTTP headers, HTML patterns, JS fingerprints to known technologies |
| Scan history and differential analysis | ReconCore | backend/app/recon/history.py - Stores each scan run, computes asset/service deltas between runs

### Web and API Security

| Skill | Module | Implementation |
|-------|--------|----------------|
| HTTP security header analysis | TestExecutor | backend/app/executor/tests/header_analysis.py - Checks for CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy |
| Cookie security attribute validation | TestExecutor | backend/app/executor/tests/cookie_analysis.py - Validates Secure, HttpOnly, SameSite, __Host-/__Secure- prefixes |
| CORS misconfiguration detection | TestExecutor | backend/app/executor/tests/cors_test.py - Tests origin reflection, wildcard with credentials, null origin |
| API authorization validation (IDOR/BOLA) | TestExecutor | backend/app/executor/tests/api_authz.py - Cross-account resource access tests with controlled test accounts |
| Input validation and injection probing | TestExecutor | backend/app/executor/tests/input_validation.py - SQLi, XSS, command injection probes with safe payloads and response analysis |
| Rate limiting and DoS resilience checks | TestExecutor | backend/app/executor/tests/rate_limit.py - Measures response times and status codes under request bursts

### Python Development

| Skill | Module | Implementation |
|-------|--------|----------------|
| FastAPI application with dependency injection | Backend Core | backend/app/main.py - App factory, lifespan events, middleware, exception handlers |
| Pydantic v2 models for request/response validation | Backend Core | backend/app/schemas/ - All API schemas, config models, and internal data models |
| SQLAlchemy 2.0 async ORM with Alembic migrations | Backend Core | backend/app/db/ - Async engine, session management, declarative models, migration scripts |
| Celery task queue with Redis broker | Backend Core | backend/app/tasks/ - Background jobs for scans, intelligence updates, report generation |
| Structured logging with structlog | Backend Core | backend/app/observability/logging.py - JSON logs, correlation IDs, log levels per module |
| Configuration management with pydantic-settings | Backend Core | backend/app/config.py - Environment-based settings, validation, secrets handling |
| Type hints throughout (mypy strict mode) | Backend Core | pyproject.toml - mypy --strict passes on all backend code

### Backend Engineering

| Skill | Module | Implementation |
|-------|--------|----------------|
| RESTful API design with OpenAPI documentation | Backend Core | backend/app/api/ - Versioned routers, automatic OpenAPI schema, Swagger UI |
| Database connection pooling and transaction management | Backend Core | backend/app/db/session.py - Async pool, transaction context managers, retry logic |
| Repository pattern for data access | Backend Core | backend/app/repositories/ - Abstract CRUD, query builders, testable with fakes |
| Background job processing with Celery | Backend Core | backend/app/tasks/celery_app.py - Task definitions, routing, result backend, monitoring |
| Health checks and readiness probes | Backend Core | backend/app/api/health.py - /health, /ready endpoints checking DB, Redis, Ollama, tools |
| Graceful shutdown handling | Backend Core | backend/app/main.py - Signal handlers, in-flight request draining, Celery worker shutdown |
| API rate limiting and authentication | Backend Core | backend/app/api/middleware/ - Token-based auth, per-IP rate limits, scope enforcement

### Frontend Engineering

| Skill | Module | Implementation |
|-------|--------|----------------|
| React 18 with TypeScript and Vite | Frontend Core | frontend/ - Vite config, TS strict mode, path aliases, HMR |
| Tailwind CSS design system implementation | Frontend Core | frontend/src/styles/ - Design tokens, component classes, dark mode support |
| Animate UI components in static/reduced-motion mode | Frontend Core | frontend/src/components/ui/ - Wrapper components disabling all motion |
| Cytoscape.js graph visualization for attack paths | AttackGraph | frontend/src/features/attack-graph/AttackGraph.tsx - Interactive graph with node selection, edge inspection |
| React Query (TanStack Query) for server state | Frontend Core | frontend/src/lib/query.ts - Caching, invalidation, optimistic updates, error boundaries |
| React Router v6 with nested layouts | Frontend Core | frontend/src/routes/ - Sidebar layout, protected routes, lazy-loaded pages |
| Form handling with React Hook Form + Zod | Frontend Core | frontend/src/lib/forms.ts - Schema validation, error display, controlled/uncontrolled patterns |
| Accessible component primitives (ARIA, keyboard nav) | Frontend Core | frontend/src/components/ui/ - Focus management, screen reader labels, reduced motion respect

### LLM Engineering

| Skill | Module | Implementation |
|-------|--------|----------------|
| Ollama client with structured JSON output | RavenBrain | backend/app/brain/ollama_client.py - Async client, model management, JSON schema enforcement |
| Prompt engineering for security reasoning | RavenBrain | backend/app/brain/prompts/ - System prompts, few-shot examples, chain-of-thought templates |
| Structured action proposal schema | RavenBrain | backend/app/brain/schemas.py - Pydantic models for LLM proposals: action, target, reason, evidence, risk |
| LLM output validation and fallback handling | RavenBrain | backend/app/brain/validator.py - Validates proposal structure, rejects malformed output, handles model unavailability |
| Retrieval-Augmented Generation for vulnerability context | RavenBrain | backend/app/brain/rag.py - Embeds findings, retrieves relevant CVEs/ATT&CK for proposal context |
| Graceful degradation when Ollama unavailable | RavenBrain | backend/app/brain/availability.py - Health checks, circuit breaker, UI indicator, offline mode

### AI Agent Orchestration

| Skill | Module | Implementation |
|-------|--------|----------------|
| LangGraph workflow for assessment planning | RavenBrain | backend/app/brain/workflow.py - State graph: observe - analyze - propose - validate - execute - learn |
| Policy-gated action execution pipeline | PolicyEngine + TestExecutor | backend/app/policy/engine.py - Proposal - policy check - approval queue - execution - evidence - feedback |
| Human-in-the-loop approval for L3 actions | PolicyEngine | backend/app/policy/approval.py - Approval requests, expiry, audit trail, emergency stop integration |
| Assessment budget and resource tracking | PolicyEngine | backend/app/policy/budget.py - Time limits, API call quotas, scan intensity caps, cost estimation

### Data Analysis

| Skill | Module | Implementation |
|-------|--------|----------------|
| Vulnerability distribution analytics | AnalyticsEngine | backend/app/analytics/vuln_stats.py - Counts by severity, CVSS, EPSS, KEV, validation status |
| Asset exposure analysis | AnalyticsEngine | backend/app/analytics/exposure.py - Internet-facing vs internal, service criticality, port exposure |
| False positive rate tracking (where ground truth exists) | AnalyticsEngine | backend/app/analytics/fp_rate.py - Compares scanner findings vs validated findings per tool/category |
| Tool execution statistics | AnalyticsEngine | backend/app/analytics/tool_stats.py - Success/failure rates, duration percentiles, error categorization

### Graph Analytics

| Skill | Module | Implementation |
|-------|--------|----------------|
| Attack graph construction from findings | AttackGraph | backend/app/graph/builder.py - Nodes: assets, services, vulns; Edges: exposes, runs, enables, validated |
| Attack path enumeration (bounded depth) | AttackGraph | backend/app/graph/paths.py - DFS with cycle detection, evidence-backed edges only, max depth configurable |
| Graph persistence in PostgreSQL (adjacency list) | AttackGraph | backend/app/graph/models.py - SQLAlchemy models for nodes/edges, recursive CTE queries for paths |
| Cytoscape.js frontend rendering | AttackGraph | frontend/src/features/attack-graph/ - Stylesheet, layouts, node/edge inspectors, export PNG/SVG

### Database Engineering

| Skill | Module | Implementation |
|-------|--------|----------------|
| Normalized relational schema (3NF) | Backend Core | backend/app/db/models/ - Users, assessments, scopes, assets, services, vulns, findings, evidence, jobs, proposals, policies, graph, reports, audits |
| Alembic migration management | Backend Core | backend/alembic/ - Versioned migrations, autogenerate, downgrade support, seed data |
| Async PostgreSQL with connection pooling | Backend Core | backend/app/db/session.py - asyncpg driver, pool sizing, prepared statements |
| Indexing strategy for query performance | Backend Core | backend/app/db/models/__init__.py - Composite indexes on frequent query patterns (assessment_id + status, asset_id + type) |
| Soft deletes and audit trails | Backend Core | backend/app/db/models/audit.py - deleted_at, created_by, updated_by, trigger-based audit log table

### DevOps

| Skill | Module | Implementation |
|-------|--------|----------------|
| Docker Compose for local development stack | DevOps | docker-compose.yml - PostgreSQL, Redis, Ollama, backend, frontend, ZAP, health checks |
| Windows PowerShell setup script (setup.ps1) | DevOps | setup.ps1 - Prerequisite detection, venv creation, dependency install, DB init, health checks |
| Linux/macOS shell setup script (setup.sh) | DevOps | setup.sh - Equivalent functionality for Unix-like systems |
| Makefile for common development commands | DevOps | Makefile - make dev, make test, make lint, make migrate, make build |
| Environment configuration with .env.example | DevOps | .env.example - All configurable values documented, no secrets committed |
| GitHub Actions CI pipeline (planned) | DevOps | .github/workflows/ci.yml - Lint, type-check, unit tests, integration tests, build

### Security Documentation

| Skill | Module | Implementation |
|-------|--------|----------------|
| Threat model documentation | Docs | docs/security-model.md - STRIDE analysis, trust boundaries, data flows, mitigations |
| Policy engine design specification | Docs | docs/policy-engine.md - Execution levels, allowlists, rate limits, approval workflows |
| AI agent safety architecture | Docs | docs/ai-agent-design.md - Structured outputs, validation, policy gating, fallback behavior |
| Vulnerability intelligence sources and freshness | Docs | docs/vulnerability-intelligence.md - NVD, EPSS, KEV, ATT&CK update schedules, caching |
| Testing strategy for security tooling | Docs | docs/testing.md - Unit, integration, contract, chaos, security-specific test cases

---

## Planned Skills (Not Yet Implemented)

The following skills are designed but not yet implemented. They appear in the roadmap for future phases.

| Skill | Planned Module | Phase |
|-------|----------------|-------|
| Advanced attack path simulation | AttackGraph | Phase 6+ |
| Machine learning for vulnerability prioritization | RiskEngine | Phase 6+ |
| Custom exploit development framework | TestExecutor | Phase 5+ (lab only) |
| SAML/OIDC authentication integration | Backend Core | Phase 8 |
| Multi-tenant assessment isolation | Backend Core | Phase 8 |
| Real-time WebSocket updates for assessment progress | Frontend Core | Phase 4+ |
| SBOM generation and vulnerability matching | VulnIntel | Phase 3+ |
| Container image scanning integration | ReconCore | Phase 2+ |
| Cloud asset discovery (AWS/Azure/GCP) | ReconCore | Phase 2+ |
| Compliance mapping (NIST, ISO 27001) | ReportForge | Phase 7+

---

## Verification

To verify implemented skills:

`ash
# Backend: type checking, tests
cd backend && python -m mypy --strict app && python -m pytest

# Frontend: type checking, tests
cd frontend && npm run typecheck && npm run test

# Full stack: docker compose up and health checks
docker compose up -d && curl http://localhost:8000/health && curl http://localhost:5173
`

All implemented skills have corresponding working code, tests, and documentation as of the current phase.
