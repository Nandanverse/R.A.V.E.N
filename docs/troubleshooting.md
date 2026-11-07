 # Troubleshooting Guide
 
 ## Table of Contents
 
 1. [Installation Issues](#installation-issues)
 2. [Backend Startup Failures](#backend-startup-failures)
 3. [Frontend Build Errors](#frontend-build-errors)
 4. [Database Connection Problems](#database-connection-problems)
 5. [Redis Connection Issues](#redis-connection-issues)
 6. [Ollama Integration Problems](#ollama-integration-problems)
 7. [Nmap / ZAP Integration Issues](#nmap--zap-integration-issues)
 8. [Authentication & Authorization](#authentication--authorization)
 9. [Performance & Resource Issues](#performance--resource-issues)
 10. [Common Error Codes](#common-error-codes)
 11. [Debugging Commands](#debugging-commands)
 12. [Getting Help](#getting-help)
 
 ---
 
 ## Installation Issues
 
 ### Python Not Found or Wrong Version
 
 **Symptom**: python: command not found or version < 3.12
 
 **Solution**:
 ```bash
 # Windows (PowerShell)
 winget install Python.Python.3.12
 
 # Linux (Ubuntu/Debian)
 sudo apt update && sudo apt install python3.12 python3.12-venv
 
 # macOS
 brew install python@3.12
 ```
 
 Verify:
 ```bash
 python --version  # Should show 3.12.x
 ```
 
 ### Node.js Not Found or Wrong Version
 
 **Symptom**: node: command not found or version < 18
 
 **Solution**:
 ```bash
 # Windows (PowerShell)
 winget install OpenJS.NodeJS
 
 # Linux (Ubuntu/Debian)
 curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
 sudo apt install -y nodejs
 
 # macOS
 brew install node@18
 ```
 
 Verify:
 ```bash
 node --version  # Should show v18.x.x or higher
 npm --version
 ```
 
 ### Docker Not Running
 
 **Symptom**: Cannot connect to the Docker daemon
 
 **Solution**:
 - Windows: Start Docker Desktop application
 - Linux: sudo systemctl start docker && sudo systemctl enable docker
 - macOS: Start Docker Desktop application
 
 Verify:
 ```bash
 docker version
 docker compose version
 ```
 
 ### Ollama Not Installed
 
 **Symptom**: ollama: command not found or connection refused on localhost:11434
 
 **Solution**:
 ```bash
 # Windows (PowerShell)
 winget install Ollama.Ollama
 
 # Linux
 curl -fsSL https://ollama.com/install.sh | sh
 
 # macOS
 brew install ollama
 ```
 
 Then start Ollama service:
 ```bash
 # Windows: Ollama runs as a service automatically
 # Linux/macOS:
 ollama serve
 ```
 
 Pull required model:
 ```bash
 ollama pull llama3.1:8b
 ```
 
 Verify:
 ```bash
 ollama list
 curl http://localhost:11434/api/tags
 ```
 
 ### Nmap Not Available
 
 **Symptom**: nmap: command not found
 
 **Solution**:
 ```bash
 # Windows (PowerShell)
 winget install Nmap.Nmap
 
 # Linux (Ubuntu/Debian)
 sudo apt install nmap
 
 # macOS
 brew install nmap
 ```
 
 Verify:
 ```bash
 nmap --version
 ```
 
 ### OWASP ZAP Not Available
 
 **Symptom**: zap.sh: command not found or zap.bat: command not found
 
 **Solution**:
 - Download from https://www.zaproxy.org/download/
 - Extract and add to PATH
 - Or use Docker: docker run -d -p 8080:8080 ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true
 
 Verify:
 ```bash
 # If installed locally
 zap.sh -version
 
 # If using Docker
 docker ps | grep zap
 ```
 
 ---
 
 ## Backend Startup Failures
 
 ### Port 8000 Already in Use
 
 **Symptom**: OSError: [Errno 98] Address already in use or Error: listen EADDRINUSE
 
 **Solution**:
 ```bash
 # Find process using port 8000
 # Windows
 netstat -ano | findstr :8000
 taskkill /PID <PID> /F
 
 # Linux/macOS
 lsof -i :8000
 kill -9 <PID>
 ```
 
 Or change port in .env:
 ```env
 API_PORT=8001
 ```
 
 ### ModuleNotFoundError: No module named 'app'
 
 **Symptom**: Import errors when running python -m app.main
 
 **Solution**:
 ```bash
 # Ensure you are in the backend directory
 cd backend
 
 # Ensure virtual environment is activated
 # Windows
 .venv\Scripts\activate
 
 # Linux/macOS
 source .venv/bin/activate
 
 # Install dependencies
 pip install -r requirements.txt
 
 # Run from backend root
 python -m app.main
 ```
 
 ### Pydantic Settings Validation Errors
 
 **Symptom**: pydantic_settings.SettingsError or validation errors on startup
 
 **Solution**:
 1. Check .env file exists in backend directory
 2. Copy from example: cp .env.example .env
 3. Verify all required variables are set:
 ```env
 DATABASE_URL=postgresql+asyncpg://raven:raven@localhost:5432/raven
 REDIS_URL=redis://localhost:6379/0
 OLLAMA_BASE_URL=http://localhost:11434
 OLLAMA_MODEL=llama3.1:8b
 SECRET_KEY=your-secret-key-here-min-32-chars
 API_HOST=0.0.0.0
 API_PORT=8000
 ```
 
 ### Alembic Migration Failures
 
 **Symptom**: alembic.util.exc.CommandError or migration conflicts
 
 **Solution**:
 ```bash
 cd backend
 
 # Check current migration head
 alembic current
 
 # If database is empty, run migrations
 alembic upgrade head
 
 # If migration conflicts exist (development only)
 alembic downgrade base
 alembic upgrade head
 
 # For production - create new migration instead
 alembic revision --autogenerate -m description
 alembic upgrade head
 ```
 
 ### Structlog Configuration Errors
 
 **Symptom**: AttributeError: module structlog has no attribute configure
 
 **Solution**:
 ```bash
 pip install --upgrade structlog
 ```
 
 ---
 
 ## Frontend Build Errors
 
 ### Port 5173 Already in Use
 
 **Symptom**: Error: listen EADDRINUSE: address already in use :::5173
 
 **Solution**:
 ```bash
 # Windows
 netstat -ano | findstr :5173
 taskkill /PID <PID> /F
 
 # Linux/macOS
 lsof -i :5173
 kill -9 <PID>
 ```
 
 Or change in vite.config.ts:
 ```typescript
 server: {
   port: 5174
 }
 ```
 
 ### Tailwind CSS Not Applying Styles
 
 **Symptom**: Styles missing, utility classes not working
 
 **Solution**:
 1. Verify tailwind.config.js content paths:
 ```javascript
 content: [
   "./index.html",
   "./src/**/*.{js,ts,jsx,tsx}",
 ]
 ```
 
 2. Verify @tailwind base; @tailwind components; @tailwind utilities; in src/styles/globals.css
 
 3. Restart dev server:
 ```bash
 npm run dev
 ```
 
 ### TypeScript Errors: Cannot find module '@/*'
 
 **Symptom**: Import errors for path aliases
 
 **Solution**:
 Verify tsconfig.json has:
 ```json
 {
   "compilerOptions": {
     "baseUrl": ".",
     "paths": {
       "@/*": ["src/*"]
     }
   }
 }
 ```
 
 And vite.config.ts:
 ```typescript
 import path from 'path'
 
 resolve: {
   alias: {
     "@": path.resolve(__dirname, "./src"),
   },
 }
 ```
 
 ### Animate UI Components Not Rendering
 
 **Symptom**: Components missing or showing errors
 
 **Solution**:
 1. Verify installation: npm list @animate-ui/react
 2. Install if missing: npm install @animate-ui/react
 3. Check import paths - Animate UI uses specific component imports:
 ```tsx
 import { Card } from '@animate-ui/react/card'
 import { Button } from '@animate-ui/react/button'
 ```
 
 4. Ensure reduced motion is configured in Tailwind:
 ```javascript
 // tailwind.config.js
 module.exports = {
   // ...
   corePlugins: {
     // Disable animations that violate design restrictions
   },
 }
 ```
 
 ---
 
 ## Database Connection Problems
 
 ### PostgreSQL Connection Refused
 
 **Symptom**: psycopg2.OperationalError: could not connect to server: Connection refused
 
 **Solution**:
 1. Check PostgreSQL is running:
 ```bash
 # Windows
 Get-Service postgresql*
 
 # Linux
 sudo systemctl status postgresql
 
 # macOS
 brew services list | grep postgresql
 ```
 
 2. Start PostgreSQL:
 ```bash
 # Windows
 Start-Service postgresql-x64-16
 
 # Linux
 sudo systemctl start postgresql
 
 # macOS
 brew services start postgresql@16
 ```
 
 3. Verify connection:
 ```bash
 psql -h localhost -p 5432 -U raven -d raven
 ```
 
 ### Database Does Not Exist
 
 **Symptom**: FATAL: database "raven" does not exist
 
 **Solution**:
 ```bash
 # Create database
 psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE raven;"
 
 # Or using createdb
 createdb -h localhost -p 5432 -U postgres raven
 ```
 
 ### Authentication Failed
 
 **Symptom**: FATAL: password authentication failed for user "raven"
 
 **Solution**:
 ```bash
 # Connect as postgres superuser
 psql -h localhost -p 5432 -U postgres
 
 # Create user and grant permissions
 CREATE USER raven WITH PASSWORD 'raven';
 GRANT ALL PRIVILEGES ON DATABASE raven TO raven;
 ALTER USER raven CREATEDB;
 ```
 
 ### Migration Table Locked
 
 **Symptom**: OperationalError: database is locked or migration hangs
 
 **Solution**:
 ```bash
 # Check for active connections
 psql -h localhost -p 5432 -U raven -d raven -c "
   SELECT pid, state, query 
   FROM pg_stat_activity 
   WHERE datname = 'raven';"
 
 # Terminate stuck connections
 psql -h localhost -p 5432 -U raven -d raven -c "
   SELECT pg_terminate_backend(pid) 
   FROM pg_stat_activity 
   WHERE datname = 'raven' AND pid <> pg_backend_pid();"
 
 # Then retry migration
 alembic upgrade head
 ```
 
 ---
 
 ## Redis Connection Issues
 
 ### Redis Connection Refused
 
 **Symptom**: redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379
 
 **Solution**:
 1. Check Redis is running:
 ```bash
 # Windows (if using Docker)
 docker ps | grep redis
 
 # Linux
 sudo systemctl status redis
 
 # macOS
 brew services list | grep redis
 ```
 
 2. Start Redis:
 ```bash
 # Windows (Docker)
 docker run -d -p 6379:6379 redis:7-alpine
 
 # Linux
 sudo systemctl start redis
 
 # macOS
 brew services start redis
 ```
 
 3. Verify:
 ```bash
 redis-cli ping  # Should return PONG
 ```
 
 ### Redis Authentication Required
 
 **Symptom**: NOAUTH Authentication required
 
 **Solution**:
 Update .env:
 ```env
 REDIS_URL=redis://:yourpassword@localhost:6379/0
 ```
 
 Or disable auth in redis.conf:
 ```
 requirepass ""
 ```
 
 ---
 
 ## Ollama Integration Problems
 
 ### Ollama Server Not Running
 
 **Symptom**: httpx.ConnectError: Cannot connect to host localhost:11434
 
 **Solution**:
 ```bash
 # Start Ollama service
 # Windows: Runs automatically as service
 # Linux/macOS:
 ollama serve
 ```
 
 Verify:
 ```bash
 curl http://localhost:11434/api/tags
 ```
 
 ### Model Not Found
 
 **Symptom**: {"error":"model 'llama3.1:8b' not found"}
 
 **Solution**:
 ```bash
 # Pull the model
 ollama pull llama3.1:8b
 
 # Verify
 ollama list
 ```
 
 ### Model Too Large for Available Memory
 
 **Symptom**: OOM errors, slow responses, or cuda out of memory
 
 **Solution**:
 1. Use smaller model:
 ```bash
 ollama pull llama3.1:3b
 ```
 
 2. Update .env:
 ```env
 OLLAMA_MODEL=llama3.1:3b
 ```
 
 3. Or configure GPU offloading in Ollama:
 ```bash
 # Set environment variable before starting ollama serve
 export OLLAMA_NUM_GPU=0  # CPU only
 ```
 
 ### Request Timeout
 
 **Symptom**: httpx.TimeoutException after 30+ seconds
 
 **Solution**:
 Increase timeout in .env:
 ```env
 OLLAMA_TIMEOUT=120
 ```
 
 Or reduce model complexity:
 ```env
 OLLAMA_MODEL=llama3.1:3b
 ```
 
 ### Structured Output Parsing Failures
 
 **Symptom**: json.JSONDecodeError or Pydantic validation errors from LLM response
 
 **Solution**:
 1. Check Ollama model supports JSON mode (llama3.1 does)
 2. Verify prompt template requests JSON output
 3. Check backend logs for raw LLM response
 4. Adjust temperature in .env:
 ```env
 OLLAMA_TEMPERATURE=0.1
 ```
 
 ---
 
 ## Nmap / ZAP Integration Issues
 
 ### Nmap Permission Denied
 
 **Symptom**: nmap: You requested a scan type which requires root privileges
 
 **Solution**:
 ```bash
 # Linux/macOS - run with sudo (not recommended for production)
 sudo nmap -sS target
 
 # Better: Configure capabilities
 sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip $(which nmap)
 
 # Or use TCP connect scan (no root needed)
 nmap -sT target
 ```
 
 ### Nmap Scan Hangs
 
 **Symptom**: Scan runs indefinitely
 
 **Solution**:
 Add timeout in scan configuration:
 ```python
 # In backend/app/recon/nmap_scanner.py
 scan_args = "-T4 --max-retries 1 --host-timeout 30s"
 ```
 
 ### ZAP API Connection Failed
 
 **Symptom**: Connection refused to localhost:8080
 
 **Solution**:
 1. Verify ZAP is running:
 ```bash
 # Docker
 docker ps | grep zap
 
 # Local
 ps aux | grep zap
 ```
 
 2. Start ZAP:
 ```bash
 # Docker (recommended)
 docker run -d -p 8080:8080 \
   ghcr.io/zaproxy/zaproxy:stable \
   zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true
 
 # Local
 zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true
 ```
 
 3. Verify API:
 ```bash
 curl http://localhost:8080/JSON/core/view/version/
 ```
 
 ### ZAP Scan Stuck
 
 **Symptom**: Active scan never completes
 
 **Solution**:
 Configure scan limits in ZAP or via API:
 ```bash
 # Set max scan duration
 curl "http://localhost:8080/JSON/ascan/action/setOptionMaxScanDurationInMins/?Integer=30"
 
 # Set max alerts per rule
 curl "http://localhost:8080/JSON/ascan/action/setOptionMaxAlertsPerRule/?Integer=10"
 ```
 
 ---
 
 ## Authentication & Authorization
 
 ### JWT Token Expired
 
 **Symptom**: 401 Unauthorized with Token has expired
 
 **Solution**:
 1. Login again to get new token
 2. Check token expiry in .env:
 ```env
 ACCESS_TOKEN_EXPIRE_MINUTES=30
 REFRESH_TOKEN_EXPIRE_DAYS=7
 ```
 
 ### Scope Validation Failed
 
 **Symptom**: 403 Forbidden: Target not in authorized scope
 
 **Solution**:
 1. Check assessment scope configuration in Settings > Assessments
 2. Verify target is in allowlist
 3. Check policy engine logs for rejection reason
 
 ### Emergency Stop Active
 
 **Symptom**: All assessment actions rejected with Emergency stop active
 
 **Solution**:
 1. Go to Settings > Policy Engine
 2. Click Reset Emergency Stop
 3. Or via API:
 ```bash
 curl -X POST http://localhost:8000/api/policy/emergency-stop/reset \
   -H "Authorization: Bearer <token>"
 ```
 
 ---
 
 ## Performance & Resource Issues
 
 ### High Memory Usage
 
 **Symptom**: Backend/frontend consuming excessive RAM
 
 **Solutions**:
 - Reduce Celery worker concurrency:
 ```env
 CELERY_WORKER_CONCURRENCY=2
 ```
 - Limit Ollama context window:
 ```env
 OLLAMA_NUM_CTX=2048
 ```
 - Enable swap if on Linux:
 ```bash
 sudo fallocate -l 4G /swapfile
 sudo chmod 600 /swapfile
 sudo mkswap /swapfile
 sudo swapon /swapfile
 ```
 
 ### Slow Database Queries
 
 **Symptom**: API responses > 5 seconds
 
 **Solutions**:
 1. Run ANALYZE on tables:
 ```sql
 ANALYZE;
 ```
 2. Check missing indexes (see docs/database-schema.md)
 3. Increase PostgreSQL work_mem:
 ```sql
 SET work_mem = '256MB';
 ```
 
 ### Celery Tasks Not Executing
 
 **Symptom**: Tasks stuck in PENDING state
 
 **Solutions**:
 1. Check worker is running:
 ```bash
 celery -A app.tasks.celery_app inspect active
 ```
 2. Check Redis connection
 3. Restart worker:
 ```bash
 cd backend
 celery -A app.tasks.celery_app worker --loglevel=info
 ```
 
 ---
 
 ## Common Error Codes
 
 | Code | HTTP Status | Description | Resolution |
 |------|-------------|-------------|------------|
 | SCOPE_VIOLATION | 403 | Target outside authorized scope | Add target to assessment scope |
 | POLICY_REJECTED | 403 | Policy engine rejected action | Check policy rules, adjust risk level |
 | LLM_UNAVAILABLE | 503 | Ollama not responding | Start Ollama, check model loaded |
 | TOOL_MISSING | 503 | Required tool (nmap/zap) not found | Install tool, verify PATH |
 | VALIDATION_ERROR | 422 | Request body invalid | Check API schema, fix request |
 | RATE_LIMITED | 429 | Too many requests | Respect rate limits, add delay |
 | EVIDENCE_INTEGRITY_FAILED | 500 | Evidence hash mismatch | Check storage, re-run collection |
 | MIGRATION_CONFLICT | 500 | Database schema mismatch | Run migrations, check alembic_version |
 
 ---
 
 ## Debugging Commands
 
 ### Backend Debugging
 
 ```bash
 # Run with debug logging
 cd backend
 LOG_LEVEL=DEBUG python -m app.main
 
 # Run specific module tests
 python -m pytest tests/unit/test_policy_engine.py -v
 
 # Check database state
 python -c "
 from app.db.session import AsyncSessionLocal
 from app.models.assessment import Assessment
 import asyncio
 
 async def check():
     async with AsyncSessionLocal() as db:
         result = await db.execute(select(Assessment))
         for a in result.scalars():
             print(f'Assessment: {a.id} - {a.name} - {a.status}')
 
 asyncio.run(check())
 "
 
 # Inspect Celery queue
 celery -A app.tasks.celery_app inspect reserved
 celery -A app.tasks.celery_app inspect scheduled
 ```
 
 ### Frontend Debugging
 
 ```bash
 # Build with verbose output
 npm run build -- --verbose
 
 # Type check
 npm run typecheck
 
 # Lint
 npm run lint
 
 # Test with coverage
 npm run test -- --coverage
 
 # Preview production build
 npm run build && npm run preview
 ```
 
 ### Database Debugging
 
 ```bash
 # Connect to database
 psql -h localhost -p 5432 -U raven -d raven
 
 # Useful queries
 \dt                          # List tables
 \d+ assessments              # Describe table
 SELECT * FROM assessments;   # View data
 SELECT * FROM alembic_version;  # Check migration version
 ```
 
 ### Docker Debugging
 
 ```bash
 # View logs
 docker compose logs -f backend
 docker compose logs -f frontend
 docker compose logs -f postgres
 docker compose logs -f redis
 
 # Exec into container
 docker compose exec backend bash
 docker compose exec postgres psql -U raven -d raven
 
 # Restart services
 docker compose restart backend
 docker compose up -d --force-recreate
 ```
 
 ---
 
 ## Getting Help
 
 ### Log Locations
 
 - Backend: Console output (structured JSON logs)
 - Frontend: Browser DevTools Console, Network tab
 - Database: PostgreSQL logs (varies by OS)
 - Redis: redis-cli INFO for stats
 - Ollama: journalctl -u ollama (Linux) or Event Viewer (Windows)
 - Docker: docker compose logs <service>
 
 ### Health Check Endpoints
 
 ```bash
 # Backend health
 curl http://localhost:8000/health
 
 # Backend readiness (includes DB, Redis, Ollama)
 curl http://localhost:8000/ready
 
 # Frontend
 curl http://localhost:5173
 ```
 
 ### Reporting Issues
 
 When reporting issues, include:
 1. Operating system and version
 2. Docker version (if using Docker)
 3. Python/Node versions
 4. Relevant log excerpts (redact sensitive data)
 5. Steps to reproduce
 6. Expected vs actual behavior
 
 ### Useful Resources
 
 - FastAPI Documentation: https://fastapi.tiangolo.com/
 - SQLAlchemy 2.0 Documentation: https://docs.sqlalchemy.org/en/20/
 - React Documentation: https://react.dev/
 - Tailwind CSS Documentation: https://tailwindcss.com/
 - Ollama Documentation: https://github.com/ollama/ollama
 - Nmap Reference: https://nmap.org/book/man.html
 - OWASP ZAP API: https://www.zaproxy.org/docs/api/
 - Cytoscape.js Documentation: https://js.cytoscape.org/
 - Plotly.js Documentation: https://plotly.com/javascript/
 
 ---
 
 *Last updated: 2026-11-06*
