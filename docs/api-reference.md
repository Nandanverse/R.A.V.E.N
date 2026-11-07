# API Reference

RAVEN provides a RESTful API with OpenAPI 3.0 documentation.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/health`, `/ready`, `/docs`, `/openapi.json`) require authentication via JWT Bearer token.

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using the Token

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Error Responses

All errors follow RFC 7807 Problem Details:

```json
{
  "type": "https://raven.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Request validation failed",
  "instance": "/api/v1/assessments",
  "errors": [
    {
      "field": "targets",
      "message": "At least one target required"
    }
  ]
}
```

Common status codes:
- `200` — Success
- `201` — Created
- `204` — No Content
- `400` — Bad Request
- `401` — Unauthorized
- `403` — Forbidden (scope violation, insufficient permissions)
- `404` — Not Found
- `409` — Conflict (duplicate, state conflict)
- `422` — Validation Error
- `429` — Rate Limited
- `500` — Internal Server Error
- `503` — Service Unavailable (dependency down)

## Pagination

List endpoints support cursor-based pagination:

```http
GET /api/v1/assessments?limit=20&cursor=eyJpZCI6MTIzfQ==
```

Response:
```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ==",
  "has_more": true
}
```

## Filtering and Sorting

```
GET /api/v1/findings?assessment_id=1&severity=critical,high&status=validated&sort=-created_at
```

| Parameter | Description |
|-----------|-------------|
| `limit` | Max items (default 20, max 100) |
| `cursor` | Pagination cursor |
| `sort` | Field to sort by, prefix `-` for descending |
| `field=value` | Exact match filter |
| `field=val1,val2` | In-list filter |
| `field__gt=value` | Greater than |
| `field__gte=value` | Greater than or equal |
| `field__lt=value` | Less than |
| `field__lte=value` | Less than or equal |
| `field__contains=value` | Substring match (case-insensitive) |

## Endpoints

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check (no auth) |
| GET | `/ready` | Readiness check (no auth) |

### Assessments

| Method | Path | Description |
|--------|------|-------------|
| POST | `/assessments` | Create assessment |
| GET | `/assessments` | List assessments |
| GET | `/assessments/{id}` | Get assessment details |
| PATCH | `/assessments/{id}` | Update assessment |
| DELETE | `/assessments/{id}` | Delete assessment |
| POST | `/assessments/{id}/start` | Start assessment |
| POST | `/assessments/{id}/pause` | Pause assessment |
| POST | `/assessments/{id}/stop` | Stop assessment |
| POST | `/assessments/{id}/clone` | Clone assessment |

### Scopes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/assessments/{id}/scopes` | Add scope to assessment |
| GET | `/assessments/{id}/scopes` | List assessment scopes |
| DELETE | `/scopes/{id}` | Remove scope |

### Assets

| Method | Path | Description |
|--------|------|-------------|
| GET | `/assets` | List assets (with filters) |
| GET | `/assets/{id}` | Get asset details |
| GET | `/assets/{id}/services` | List asset services |
| GET | `/assets/{id}/vulnerabilities` | List asset vulnerabilities |
| GET | `/assets/{id}/findings` | List asset findings |
| GET | `/assets/{id}/evidence` | List asset evidence |
| GET | `/assets/{id}/scan-history` | Asset scan history |

### Services

| Method | Path | Description |
|--------|------|-------------|
| GET | `/services` | List services (with filters) |
| GET | `/services/{id}` | Get service details |
| GET | `/services/{id}/vulnerabilities` | Correlated vulnerabilities |

### Reconnaissance

| Method | Path | Description |
|--------|------|-------------|
| POST | `/recon/scans` | Start scan |
| GET | `/recon/scans` | List scans |
| GET | `/recon/scans/{id}` | Get scan details |
| GET | `/recon/scans/{id}/results` | Get scan results |
| POST | `/recon/scans/{id}/cancel` | Cancel running scan |
| GET | `/recon/scans/{id}/raw` | Download raw Nmap XML |

### Vulnerability Intelligence

| Method | Path | Description |
|--------|------|-------------|
| GET | `/intel/cves` | Search CVEs |
| GET | `/intel/cves/{cve_id}` | Get CVE details |
| POST | `/intel/correlate` | Correlate services with CVEs |
| GET | `/intel/feeds/status` | Feed refresh status |
| POST | `/intel/feeds/refresh` | Trigger feed refresh |
| GET | `/intel/attack/techniques` | List ATT&CK techniques |
| GET | `/intel/attack/techniques/{id}` | Get technique details |

### Findings

| Method | Path | Description |
|--------|------|-------------|
| GET | `/findings` | List findings (with filters) |
| GET | `/findings/{id}` | Get finding details |
| PATCH | `/findings/{id}` | Update finding (status, remediation) |
| POST | `/findings/{id}/validate` | Mark as validated |
| POST | `/findings/{id}/reject` | Mark as false positive |
| GET | `/findings/{id}/evidence` | List finding evidence |
| GET | `/findings/{id}/attack-paths` | Attack paths involving finding |

### Evidence

| Method | Path | Description |
|--------|------|-------------|
| GET | `/evidence/{id}` | Get evidence details |
| GET | `/evidence/{id}/download` | Download evidence file |
| POST | `/evidence` | Upload evidence (multipart) |
| DELETE | `/evidence/{id}` | Delete evidence |

### AI Analysis (RavenBrain)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ai/status` | Ollama connection status |
| POST | `/ai/analyze` | Request analysis for assessment |
| GET | `/ai/proposals` | List proposals (with filters) |
| GET | `/ai/proposals/{id}` | Get proposal details |
| POST | `/ai/proposals/{id}/approve` | Approve proposal |
| POST | `/ai/proposals/{id}/reject` | Reject proposal |
| GET | `/ai/proposals/{id}/execution` | Get execution result |

### Policy Engine

| Method | Path | Description |
|--------|------|-------------|
| GET | `/policy/decisions` | List policy decisions |
| GET | `/policy/decisions/{id}` | Get decision details |
| POST | `/policy/approvals` | Request human approval (L3) |
| GET | `/policy/approvals/{id}` | Get approval request |
| POST | `/policy/approvals/{id}/approve` | Grant approval |
| POST | `/policy/approvals/{id}/deny` | Deny approval |
| POST | `/policy/emergency-stop` | Emergency stop all execution |

### Test Execution

| Method | Path | Description |
|--------|------|-------------|
| GET | `/executor/jobs` | List execution jobs |
| GET | `/executor/jobs/{id}` | Get job details |
| GET | `/executor/jobs/{id}/logs` | Get job logs |
| POST | `/executor/jobs/{id}/retry` | Retry failed job |
| GET | `/executor/tools/status` | Tool availability status |

### Attack Graph

| Method | Path | Description |
|--------|------|-------------|
| GET | `/graph/nodes` | List graph nodes |
| GET | `/graph/nodes/{id}` | Get node details |
| GET | `/graph/edges` | List graph edges |
| GET | `/graph/paths` | Find attack paths |
| GET | `/graph/export` | Export graph (PNG, SVG, JSON) |
| POST | `/graph/rebuild` | Rebuild graph for assessment |

### Risk Engine

| Method | Path | Description |
|--------|------|-------------|
| GET | `/risk/scores` | List risk scores |
| GET | `/risk/scores/{id}` | Get risk score details |
| GET | `/risk/assets/{asset_id}/summary` | Asset risk summary |
| POST | `/risk/recalculate` | Recalculate scores for assessment |

### Analytics

| Method | Path | Description |
|--------|------|-------------|
| GET | `/analytics/summary` | Dashboard summary |
| GET | `/analytics/assets` | Asset metrics |
| GET | `/analytics/vulnerabilities` | Vulnerability metrics |
| GET | `/analytics/scans` | Scan metrics |
| GET | `/analytics/findings` | Finding metrics |
| GET | `/analytics/risk` | Risk metrics |
| GET | `/analytics/tools` | Tool performance metrics |

### Reports

| Method | Path | Description |
|--------|------|-------------|
| POST | `/reports/generate` | Generate report |
| GET | `/reports` | List reports |
| GET | `/reports/{id}` | Get report details |
| GET | `/reports/{id}/download` | Download report file |
| DELETE | `/reports/{id}` | Delete report |

### Settings

| Method | Path | Description |
|--------|------|-------------|
| GET | `/settings` | Get all settings |
| PATCH | `/settings` | Update settings |
| GET | `/settings/categories/{category}` | Get settings by category |

### Audit

| Method | Path | Description |
|--------|------|-------------|
| GET | `/audit/events` | List audit events |
| GET | `/audit/events/{id}` | Get event details |

## WebSocket (Future)

Real-time updates for:
- Assessment progress
- Scan status
- Proposal generation
- Execution results
- Graph updates

```
ws://localhost:8000/api/v1/ws
```

## Rate Limiting

- Default: 60 requests/minute per IP
- Authenticated: 120 requests/minute per user
- Scan endpoints: 5 requests/minute per user
- Report generation: 2 requests/minute per user

Headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1699999999
```

## Versioning

API version in URL path: `/api/v1/`
Breaking changes require new version: `/api/v2/`

## OpenAPI Documentation

Interactive docs: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`
OpenAPI JSON: `http://localhost:8000/openapi.json`

---

*API reference version: 1.0*
*Last updated: 2026-11-06*
