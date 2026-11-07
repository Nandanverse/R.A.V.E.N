# Configuration Guide

All RAVEN configuration is managed through environment variables. The application uses Pydantic Settings for validation and type coercion.

## Environment Files

| File | Purpose | Committed |
|------|---------|-----------|
| `.env.example` | Template with all options documented | Yes |
| `.env` | Local overrides (gitignored) | No |
| `.env.local` | Machine-specific overrides (gitignored) | No |

Load order: `.env.example` → `.env` → `.env.local` (later overrides earlier)

## Required Settings

These must be set before starting the application.

### Database

```bash
# PostgreSQL connection string (asyncpg driver)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# Example for local Docker Compose
DATABASE_URL=postgresql+asyncpg://raven:raven@localhost:5432/raven
```

### Redis

```bash
# Redis connection string (for Celery broker and caching)
REDIS_URL=redis://localhost:6379/0

# With password
REDIS_URL=redis://:password@localhost:6379/0
```

### Security

```bash
# Secret key for JWT signing (generate with: openssl rand -hex 32)
SECRET_KEY=your-64-character-hex-string

# Algorithm for JWT
JWT_ALGORITHM=HS256

# Access token expiration (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Target Authorization (CRITICAL)

```bash
# Comma-separated list of authorized targets
# Supports: domains, IPs, CIDR ranges
# Wildcards allowed for subdomains: *.example.com
ALLOWED_TARGETS=localhost,127.0.0.1,::1,192.168.1.0/24,*.example.com

# Examples:
# Single host: example.com
# IP range: 10.0.0.0/8
# Multiple: localhost,192.168.1.100,test.example.com
```

**Never** use RAVEN against targets not in this list. The policy engine will reject any action targeting unauthorized scopes.

## Optional Settings

### Ollama (Local LLM)

```bash
# Ollama API base URL
OLLAMA_BASE_URL=http://localhost:11434

# Model to use for reasoning (must be pulled in Ollama)
OLLAMA_MODEL=llama3.1:8b

# Request timeout (seconds)
OLLAMA_TIMEOUT=120

# Maximum tokens for response
OLLAMA_MAX_TOKENS=4096

# Temperature for generation (0.0-1.0)
OLLAMA_TEMPERATURE=0.1
```

### OWASP ZAP

```bash
# ZAP daemon API URL
ZAP_API_URL=http://localhost:8080

# ZAP API key (if authentication enabled)
ZAP_API_KEY=

# Scan timeout (seconds)
ZAP_SCAN_TIMEOUT=3600
```

### Nmap

```bash
# Nmap binary path (if not in PATH)
NMAP_PATH=nmap

# Default scan timeout (seconds)
NMAP_TIMEOUT=300

# Maximum concurrent scans
NMAP_MAX_CONCURRENT=2
```

### Assessment Limits

```bash
# Maximum assessment duration (minutes)
ASSESSMENT_TIMEOUT_MINUTES=120

# Maximum concurrent assessments per user
MAX_CONCURRENT_ASSESSMENTS=3

# Rate limit: API requests per minute per IP
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Rate limit: Scan requests per minute
RATE_LIMIT_SCANS_PER_MINUTE=5
```

### File Storage

```bash
# Base directory for evidence files, reports, caches
STORAGE_BASE_PATH=./data

# Maximum evidence file size (bytes)
MAX_EVIDENCE_SIZE=10485760  # 10 MB

# Evidence retention (days, 0 = forever)
EVIDENCE_RETENTION_DAYS=90
```

### Logging

```bash
# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Log format: json, console
LOG_FORMAT=json

# Log file path (optional, stdout if empty)
LOG_FILE=
```

### Frontend (Vite)

Create `frontend/.env`:

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000

# WebSocket URL (for future real-time features)
VITE_WS_URL=ws://localhost:8000

# Application name
VITE_APP_NAME=RAVEN
```

## Configuration by Deployment

### Development (Local)

```bash
# .env
DATABASE_URL=postgresql+asyncpg://raven:raven@localhost:5432/raven
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_TARGETS=localhost,127.0.0.1,::1
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
ZAP_API_URL=http://localhost:8080
LOG_LEVEL=DEBUG
LOG_FORMAT=console
STORAGE_BASE_PATH=./data
```

### Docker Compose

```bash
# .env (used by docker-compose.yml)
POSTGRES_PASSWORD=secure-random-password
SECRET_KEY=secure-random-64-char-hex
ALLOWED_TARGETS=localhost,127.0.0.1,host.docker.internal
OLLAMA_MODEL=llama3.1:8b

# Backend container gets these via environment:
DATABASE_URL=postgresql+asyncpg://raven:${POSTGRES_PASSWORD}@postgres:5432/raven
REDIS_URL=redis://redis:6379/0
OLLAMA_BASE_URL=http://ollama:11434
ZAP_API_URL=http://zap:8080
```

### Production

```bash
# Use external secret manager for these:
DATABASE_URL=postgresql+asyncpg://user:pass@managed-db:5432/raven
REDIS_URL=redis://:pass@managed-redis:6379/0
SECRET_KEY=from-vault
ALLOWED_TARGETS=from-config-management

# Application settings
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/raven/app.log

# Resource limits
ASSESSMENT_TIMEOUT_MINUTES=240
MAX_CONCURRENT_ASSESSMENTS=10
RATE_LIMIT_REQUESTS_PER_MINUTE=120

# External storage
STORAGE_BASE_PATH=/mnt/raven-data
EVIDENCE_RETENTION_DAYS=365
```

## Generating Secure Secrets

```bash
# SECRET_KEY (64 hex chars)
openssl rand -hex 32

# POSTGRES_PASSWORD
openssl rand -base64 32

# JWT keys (if using RS256)
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

## Validation

The application validates configuration on startup:

1. Required fields present
2. `DATABASE_URL` is valid PostgreSQL asyncpg URL
3. `REDIS_URL` is valid Redis URL
4. `SECRET_KEY` is at least 32 characters
4. `ALLOWED_TARGETS` is non-empty and parseable
5. `OLLAMA_BASE_URL` is reachable (warning only)
6. `ZAP_API_URL` is reachable (warning only)
7. `NMAP_PATH` executable exists (warning only)

Invalid configuration prevents startup with clear error messages.

## Runtime Configuration Changes

Some settings can be changed without restart via the **Settings** page:

- Assessment timeout
- Rate limits
- Log level
- Evidence retention
- Ollama model (requires model to be pre-pulled)

Changes via UI are stored in database and take effect immediately for new assessments.

---

*Configuration guide version: 1.0*
*Last updated: 2026-11-06*
