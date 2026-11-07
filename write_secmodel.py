import pathlib
content = """# Security Model

Threat model, trust boundaries, and security controls for RAVEN.

## Threat Model (STRIDE)

### Spoofing

| Threat | Target | Mitigation |
|--------|--------|------------|
| User impersonation | Authentication | JWT with HS256/RS256, short expiry, secure storage |
| Service impersonation | Inter-service comms | mTLS in production, API keys for ZAP/Ollama |
| Target spoofing | Scope validation | Strict allowlist, DNS resolution verification |

### Tampering

| Threat | Target | Mitigation |
|--------|--------|------------|
| Evidence modification | Evidence files | SHA-256 integrity hashes, immutable storage |
| Database tampering | PostgreSQL | Parameterized queries, least-privilege DB user |
| Configuration tampering | .env files | File permissions, external secret manager in prod |
| Scan result injection | Nmap/ZAP output | Output parsing with validation, schema enforcement |
| LLM output injection | RavenBrain proposals | Structured JSON schema validation, policy engine gate |

### Repudiation

| Threat | Target | Mitigation |
|--------|--------|------------|
| Action denial | All operations | Immutable audit log with timestamp, actor, outcome |
| Scan execution denial | Reconnaissance | Scan history with config, results, signatures |
| Approval denial | Policy decisions | Policy decision records with reviewer, timestamp |

### Information Disclosure

| Threat | Target | Mitigation |
|--------|--------|------------|
| Secret leakage | Logs, evidence | Structured logging with redaction, secret scanning |
| Target exposure | Asset inventory | Access control, audit logging on read |
| Vulnerability intel exposure | CVE database | No sensitive data in intel feeds |
| Assessment data leakage | Reports, API | Role-based access, encryption at rest/in transit |
| LLM prompt injection | RavenBrain | Input validation, output schema enforcement |

### Denial of Service

| Threat | Target | Mitigation |
|--------|--------|------------|
| Resource exhaustion | Backend API | Rate limiting, request timeouts, circuit breakers |
| Scan overload | Nmap/ZAP | Concurrency limits, scan timeouts, resource quotas |
| LLM overload | Ollama | Request queue, timeout, fallback to offline mode |
| Database overload | PostgreSQL | Connection pooling, query timeouts, read replicas |
| Storage exhaustion | Evidence/files | Size limits, retention policies, monitoring |

### Elevation of Privilege

| Threat | Target | Mitigation |
|--------|--------|------------|
| LLM bypasses policy | PolicyEngine | Policy engine independent of LLM, mandatory gate |
| Unauthorized scan execution | TestExecutor | Scope validation on every execution, allowlist enforcement |
| L3 action without approval | Approval workflow | Human-in-the-loop required, expiry, audit trail |
| Admin privilege escalation | User management | Role-based access, separation of duties |

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRUSTED INTERNAL ZONE                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Frontend   │  │   Backend    │  │  PostgreSQL  │              │
│  │  (Browser)   │◄─┤    (API)     │◄─┤   (Primary)  │              │
│  └──────────────┘  └──────┬───────┘  └──────────────┘              │
│                           │                                         │
│         ┌─────────────────┼─────────────────┐                      │
│         ▼                 ▼                 ▼                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │    Redis     │  │   Files      │  │   Celery     │              │
│  │  (Broker)    │  │  (Evidence)  │  │  (Workers)   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       ┌─────────────┐ ┌─────────┐ ┌──────────┐
       │   Ollama    │ │  Nmap   │ │   ZAP    │
       │  (Local)    │ │ (Local) │ │ (Local)  │
       └─────────────┘ └─────────┘ └──────────┘
              │            │            │
              ▼            ▼            ▼
       ┌─────────────────────────────────────────┐
       │           UNTRUSTED TARGET ZONE          │
       │  Only explicitly authorized targets      │
       │  (ALLOWED_TARGETS allowlist enforced)    │
       └─────────────────────────────────────────┘
```

### Boundary Controls

| Boundary | Control |
|----------|---------|
| Browser → API | JWT auth, CORS, CSP, rate limiting, input validation |
| API → Database | Parameterized queries, connection pooling, least privilege |
| API → Redis | Auth (if configured), command allowlist |
| API → Filesystem | Path traversal prevention, size limits, type validation |
| API → Ollama | Request validation, timeout, structured output schema |
| API → Nmap | Allowlist targets, timeout, output parsing, no shell injection |
| API → ZAP | API key auth, scan config validation, result schema |
| API → Targets | **Mandatory** scope validation against ALLOWED_TARGETS |

## Data Flow Security

### Assessment Creation

```
User → Frontend → API → Validate targets against ALLOWED_TARGETS
                → Create assessment, scopes
                → Audit log: assessment_created
                → Return assessment_id
```

### Reconnaissance Execution

```
User → API → PolicyEngine: validate(assessment_id, scan_config)
                → Check: scope, rate limits, concurrent scans
                → Queue Celery task
Celery → Nmap (subprocess with validated args)
       → Parse XML output
       → Store assets, services, scan_history
       → Audit log: scan_completed
```

### AI Proposal Generation

```
Celery → Retrieve context (assets, vulns, findings)
       → Build structured prompt
       → Call Ollama with JSON schema
       → Validate response against proposal schema
       → Store proposal
       → PolicyEngine: evaluate(proposal)
       → Store policy_decision
```

### Test Execution

```
PolicyEngine → Approved proposal → Queue execution job
Executor → Validate target in scope
         → Execute test (ZAP, HTTP, etc.)
         → Collect evidence, compute hashes
         → Store finding, evidence
         → Update proposal status
         → Audit log: test_executed
```

## Authorization Model

### Execution Levels

| Level | Name | Description | Approval Required | Examples |
|-------|------|-------------|-------------------|----------|
| L1 | Passive | Offline analysis, passive intel, asset correlation | No | CVE correlation, attack graph, risk scoring |
| L2 | Controlled | Port scanning, service enum, non-destructive tests | Auto (within limits) | Nmap, header analysis, authz checks, input validation |
| L3 | Intrusive | State-changing actions, exploitation, DoS | **Explicit human** | Password spray, SQLi exploitation, buffer overflow |

### Allowlist Enforcement

All targets validated against `ALLOWED_TARGETS`:

```python
def validate_target(target: str, allowlist: list[str]) -> bool:
    # Exact match
    if target in allowlist:
        return True
    # CIDR containment
    for allowed in allowlist:
        if '/' in allowed and ip_in_cidr(target, allowed):
            return True
        # Wildcard subdomain
        if allowed.startswith('*.') and target.endswith(allowed[1:]):
            return True
    return False
```

**Never** bypassed. PolicyEngine validates on every action.

### Rate Limits

| Resource | Limit | Scope |
|----------|-------|-------|
| API requests | 60/min | Per IP (unauth), per user (auth) |
| Scan starts | 5/min | Per assessment |
| Concurrent scans | 2 | Global |
| LLM proposals | 10/min | Per assessment |
| Report generation | 2/min | Per user |
| Evidence upload | 10 MB/file | Per request |

### Assessment Budgets

```python
class AssessmentBudget:
    max_duration_minutes: int = 120
    max_api_calls: int = 10000
    max_scan_targets: int = 256
    max_evidence_mb: int = 500
    max_findings: int = 1000
```

Exceeding budget pauses assessment, requires admin override.

## Evidence Integrity

### Hash Verification

```python
def store_evidence(content: bytes, metadata: dict) -> Evidence:
    hash = sha256(content).hexdigest()
    evidence = Evidence(
        content=content,
        hash=hash,
        metadata=metadata
    )
    db.save(evidence)
    return evidence

def verify_evidence(evidence: Evidence) -> bool:
    return sha256(evidence.content).hexdigest() == evidence.hash
```

### Redaction

Automatic redaction for:
- Authorization headers (Bearer tokens, Basic auth)
- Cookie values (session IDs, tokens)
- Query parameters (api_key, token, password)
- JSON body fields (password, secret, token, key)
- Credit card numbers, SSNs (regex patterns)

Manual redaction available in evidence viewer.

## Audit Logging

All security-relevant events logged immutably:

| Event Type | When |
|------------|------|
| `assessment_created` | Assessment created |
| `assessment_started` | Assessment execution started |
| `assessment_stopped` | Assessment stopped/paused |
| `scope_added` | Target added to assessment |
| `scan_started` | Reconnaissance scan started |
| `scan_completed` | Scan finished (success/failure) |
| `finding_created` | Finding recorded |
| `finding_validated` | Finding marked validated |
| `finding_rejected` | Finding marked false positive |
| `proposal_generated` | LLM proposal created |
| `proposal_approved` | Policy approved proposal |
| `proposal_rejected` | Policy rejected proposal |
| `approval_requested` | Human approval requested (L3) |
| `approval_granted` | Human approved L3 action |
| `approval_denied` | Human denied L3 action |
| `test_executed` | Security test executed |
| `evidence_stored` | Evidence saved |
| `report_generated` | Report created |
| `emergency_stop` | Emergency stop triggered |
| `config_changed` | Settings modified |
| `user_login` | User authentication |
| `user_failed_login` | Failed authentication |

Audit log stored in `audit_events` table with:
- Timestamp (UTC, nanosecond precision)
- Actor (user ID or 'system')
- Resource type and ID
- Action and outcome
- Details (JSON, no secrets)
- Client IP address

## Encryption

| Data | At Rest | In Transit |
|------|---------|------------|
| Database | PostgreSQL TDE / filesystem encryption | TLS 1.3 |
| Redis | Redis encryption (if enabled) | TLS 1.3 |
| Evidence files | Filesystem encryption | TLS 1.3 (API) |
| Reports | Filesystem encryption | TLS 1.3 (download) |
| Configuration | External secret manager | N/A |
| Inter-service | N/A | mTLS (production) |

## Secret Management

### Development

- `.env` file (gitignored)
- `SECRET_KEY` generated locally
- Database passwords in `.env`

### Production

- **Required**: External secret manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Secrets injected at container startup
- No secrets in environment variables visible to processes
- Rotation via secret manager

## Network Security

### Development (Docker Compose)

- Services on user-defined bridge network
- Only frontend (5173) and backend (8000) exposed to host
- Database (5432), Redis (6379), Ollama (11434), ZAP (8080) internal only

### Production

- Backend: Private subnet, load balancer only
- Database: Private subnet, no internet access
- Redis: Private subnet, auth enabled
- Ollama: Dedicated GPU subnet
- ZAP: Scanning subnet, isolated
- TLS termination at load balancer
- mTLS between services
- WAF in front of API

## Vulnerability Management

### Dependencies

```bash
# Backend
pip-audit -r requirements.txt

# Frontend
npm audit
```

### Container Images

```bash
# Scan images
trivy image raven/backend:latest
trivy image raven/frontend:latest
```

### Runtime

- Regular base image updates
- Distroless/minimal images where possible
- Non-root user in containers
- Read-only root filesystem
- Dropped capabilities

## Incident Response

### Emergency Stop

```http
POST /api/v1/policy/emergency-stop
```

Effects:
- Cancels all running Celery tasks
- Rejects all pending proposals
- Blocks new scan/test execution
- Logs `emergency_stop` audit event
- Requires admin to reset

### Evidence Preservation

On suspected compromise:
1. Trigger emergency stop
2. Export audit logs
3. Snapshot database
4. Preserve evidence files
5. Rotate all secrets
6. Investigate via audit trail

## Compliance Considerations

| Standard | Coverage |
|----------|----------|
| ISO 27001 | Audit logging, access control, encryption, vulnerability management |
| NIST 800-53 | AU-2, AU-3, AC-2, AC-3, AC-6, SC-8, SC-13, SI-3, SI-4 |
| SOC 2 | Security, Availability, Confidentiality criteria |
| GDPR | Data minimization, right to erasure (audit logs excepted), encryption |

---

*Security model version: 1.0*
*Last updated: 2026-11-06*
"""
pathlib.Path("C:/Users/nanda/OneDrive/Desktop/RAVEN/docs/security-model.md").write_text(content, encoding="utf-8")
print("done")
