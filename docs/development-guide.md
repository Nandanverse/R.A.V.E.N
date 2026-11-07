 # Development Guide
 
 ## Overview
 
 This guide covers the development workflow, coding standards, and tooling for the RAVEN project.
 
 ## Prerequisites
 
 - Python 3.12+
 - Node.js 18+
 - Docker & Docker Compose
 - Git
 - PostgreSQL 16+
 - Redis 7+
 - Ollama
 - Nmap
 - OWASP ZAP (or Docker)
 
 ## Project Structure
 
 ```
 RAVEN/
 ├── backend/
 │   ├── app/
 │   │   ├── main.py                 # FastAPI application entry point
 │   │   ├── config.py               # Pydantic settings
 │   │   ├── db/                     # Database models, session, migrations
 │   │   ├── api/                    # API routes (REST endpoints)
 │   │   ├── policy/                 # Policy engine (L1/L2/L3)
 │   │   ├── recon/                  # ReconCore module
 │   │   ├── intel/                  # VulnIntel module
 │   │   ├── brain/                  # RavenBrain (LLM integration)
 │   │   ├── executor/               # TestExecutor module
 │   │   ├── evidence/               # EvidenceVault module
 │   │   ├── graph/                  # AttackGraph module
 │   │   ├── risk/                   # RiskEngine module
 │   │   ├── analytics/              # AnalyticsEngine module
 │   │   ├── reports/                # ReportForge module
 │   │   └── tasks/                  # Celery tasks
 │   ├── tests/                      # Backend tests
 │   ├── requirements.txt
 │   ├── pyproject.toml
 │   └── alembic/
 ├── frontend/
 │   ├── src/
 │   │   ├── components/
 │   │   │   ├── ui/                 # Base UI components (Animate UI wrappers)
 │   │   │   ├── layout/             # Layout components (Sidebar, Header)
 │   │   │   ├── patterns/           # Composite patterns
 │   │   │   └── features/           # Feature-specific components
 │   │   ├── pages/                  # Page components (12 pages)
 │   │   ├── routes/                 # Routing configuration
 │   │   ├── lib/                    # Utilities, API client, hooks
 │   │   ├── styles/                 # Global styles, design tokens
 │   │   ├── main.tsx                # Entry point
 │   │   └── App.tsx                 # Root component
 │   ├── package.json
 │   ├── vite.config.ts
 │   ├── tailwind.config.js
 │   └── tsconfig.json
 ├── docker-compose.yml
 ├── setup.ps1 / setup.sh
 ├── start.ps1 / start.sh
 ├── Makefile
 ├── .env.example
 ├── .gitignore
 └── LICENSE
 ```
 
 ## Development Workflow
 
 ### 1. Initial Setup
 
 ```bash
 # Clone repository
 git clone <repo-url>
 cd RAVEN
 
 # Run setup script (installs dependencies, initializes DB)
 # Windows
 .\setup.ps1
 
 # Linux/macOS
 ./setup.sh
 ```
 
 ### 2. Start Development Servers
 
 **Option A: Docker (recommended for full stack)**
 ```bash
 docker compose up -d
 # Backend: http://localhost:8000
 # Frontend: http://localhost:5173
 ```
 
 **Option B: Local development (faster iteration)**
 ```bash
 # Terminal 1: Backend
 cd backend
 .venv\Scripts\activate  # Windows
 source .venv/bin/activate  # Linux/macOS
 python -m app.main
 
 # Terminal 2: Frontend
 cd frontend
 npm run dev
 
 # Terminal 3: Celery worker (optional, for async tasks)
 cd backend
 .venv\Scripts\activate
 celery -A app.tasks.celery_app worker --loglevel=info
 ```
 
 ### 3. Running Tests
 
 ```bash
 # Backend tests
 cd backend
 python -m pytest                    # All tests
 python -m pytest tests/unit/        # Unit tests only
 python -m pytest tests/integration/ # Integration tests
 python -m pytest -v                 # Verbose
 python -m pytest --cov=app          # With coverage
 
 # Frontend tests
 cd frontend
 npm run test                        # Unit/component tests
 npm run test:coverage               # With coverage
 npm run test:e2e                    # Playwright E2E tests
 
 # Type checking
 cd backend && python -m mypy --strict app
 cd frontend && npm run typecheck
 
 # Linting
 cd backend && python -m ruff check app
 cd frontend && npm run lint
 ```
 
 ### 4. Database Migrations
 
 ```bash
 cd backend
 
 # Create new migration
 alembic revision --autogenerate -m "description"
 
 # Apply migrations
 alembic upgrade head
 
 # Check current revision
 alembic current
 
 # Rollback (development only)
 alembic downgrade -1
 ```
 
 ### 5. Code Quality Checks
 
 **Pre-commit hooks** (install once):
 ```bash
 # Backend
 pip install pre-commit
 pre-commit install
 
 # Frontend
 cd frontend && npm install
 ```
 
 **Manual checks**:
 ```bash
 # Backend
 python -m ruff check app --fix      # Auto-fix linting
 python -m mypy --strict app         # Type checking
 python -m pytest                    # Tests
 
 # Frontend
 npm run lint -- --fix               # Auto-fix linting
 npm run typecheck                   # Type checking
 npm run test                        # Tests
 ```
 
 ## Coding Standards
 
 ### Python (Backend)
 
 - **Style**: Ruff (replaces Black, isort, flake8)
 - **Types**: mypy strict mode
 - **Docstrings**: Google style
 - **Line length**: 100 characters
 - **Imports**: Absolute imports preferred
 
 ```python
 # Good
 from app.models.assessment import Assessment
 from app.db.session import AsyncSessionLocal
 
 # Avoid
 from ..models.assessment import Assessment
 ```
 
 - **Async**: Use async/await for I/O operations
 - **Error handling**: Explicit try/except, no bare except
 - **Logging**: Structured logging with structlog
 - **Validation**: Pydantic models for all external input
 
 ### TypeScript (Frontend)
 
 - **Style**: ESLint + Prettier
 - **Types**: Strict mode enabled
 - **Components**: Functional components with hooks
 - **State**: TanStack Query for server state, React Context for UI state
 - **Styling**: Tailwind CSS utility classes
 - **Icons**: Lucide React
 
 ```tsx
 // Good
 interface Props {
   title: string;
   onAction: () => void;
 }
 
 export function Card({ title, onAction }: Props) {
   return (
     <div className="bg-bg-elevated border border-separator rounded-sm p-4">
       <h3 className="font-mono text-fg-primary">{title}</h3>
       <button onClick={onAction} className="btn-primary mt-2">Action</button>
     </div>
   );
 }
 ```
 
 - **No inline styles**: Use Tailwind classes
 - **No unnecessary re-renders**: Use React.memo, useCallback, useMemo
 - **Accessibility**: Semantic HTML, ARIA attributes, keyboard navigation
 
 ## Design System Compliance
 
 ### Mandatory Rules (from design.md)
 
 **PROHIBITED**:
 - Gradients
 - Emojis
 - Decorative colored borders
 - Box shadows
 - Glassmorphism
 - Glowing effects
 - Excessive rounded cards (use `--radius-sm: 4px`)
 - Animated backgrounds
 - On-hover movement, scaling, bouncing, sliding
 - Unnecessary animations
 - Decorative AI-generated illustrations
 - Excessive empty dashboard cards
 - Fake activity feeds or fabricated findings
 
 **REQUIRED**:
 - Flat surfaces
 - Neutral backgrounds (`--bg-base: #0d0d0d`, `--bg-elevated: #141414`)
 - High-contrast typography (`--fg-primary: #e8e8e8`)
 - Thin, neutral separators (`--separator: #2a2a2a`)
 - Consistent spacing (`--space-4: 16px` base unit)
 - Simple rectangular/slightly rounded components
 - Clear information hierarchy
 - Monospaced for technical identifiers (`--font-mono: 'JetBrains Mono'`)
 - Restrained color for security states only
 
 ### Animate UI Usage
 
 - Import from specific paths: `@animate-ui/react/button`
 - Disable motion: Use `reduceMotion` prop or CSS `prefers-reduced-motion`
 - Static configuration only
 - No entrance effects, hover transforms, animated transitions
 
 ## Module Development Guidelines
 
 ### Adding a New Module
 
 1. Create module directory under `backend/app/<module_name>/`
 2. Add `__init__.py` with exports
 3. Create models, schemas, services, routes
 4. Register routes in `backend/app/api/router.py`
 5. Add tests in `backend/tests/unit/test_<module>.py`
 6. Update API documentation
 
 ### Policy Engine Integration
 
 All executable actions MUST go through the policy engine:
 
 ```python
 from app.policy.engine import PolicyEngine, ExecutionLevel
 
 policy = PolicyEngine()
 decision = policy.evaluate(
     action="test_api_authorization",
     target="api.example.com",
     level=ExecutionLevel.L2_CONTROLLED,
     context={"assessment_id": assessment_id}
 )
 
 if decision.allowed:
     # Execute action
 else:
     # Log rejection, notify user
 ```
 
 ### Evidence Integrity
 
 All evidence MUST have SHA-256 integrity hash:
 
 ```python
 import hashlib
 
 evidence_hash = hashlib.sha256(evidence_data).hexdigest()
 # Store with evidence record
 ```
 
 ### Secret Redaction
 
 Never log secrets. Use the redaction utility:
 
 ```python
 from app.utils.redaction import redact_secrets
 
 log_data = redact_secrets(raw_data)
 logger.info("Request", data=log_data)
 ```
 
 ## Testing Guidelines
 
 ### Unit Tests
 
 - Test pure functions in isolation
 - Mock external dependencies (DB, HTTP, LLM)
 - Use pytest fixtures for common setup
 - Target: >80% coverage for critical modules
 
 ```python
 # Example
 def test_policy_engine_rejects_l3_without_approval():
     policy = PolicyEngine()
     decision = policy.evaluate(
         action="exploit",
         target="target.example.com",
         level=ExecutionLevel.L3_INTRUSIVE,
         context={}
     )
     assert not decision.allowed
     assert decision.reason == "L3 requires human approval"
 ```
 
 ### Integration Tests
 
 - Test API endpoints with real database
 - Use testcontainers or Docker for PostgreSQL/Redis
 - Test policy engine with real scope validation
 
 ### Frontend Tests
 
 - Component tests with Vitest + React Testing Library
 - E2E tests with Playwright for critical flows
 - Test error states, loading states, empty states
 
 ## Debugging
 
 ### Backend Debugging
 
 ```bash
 # Debug logging
 LOG_LEVEL=DEBUG python -m app.main
 
 # Database inspection
 python -c "
 from app.db.session import AsyncSessionLocal
 from app.models.assessment import Assessment
 import asyncio
 async def check():
     async with AsyncSessionLocal() as db:
         result = await db.execute(select(Assessment))
         for a in result.scalars():
             print(f'{a.id}: {a.name} - {a.status}')
 asyncio.run(check())
 "
 
 # Celery inspection
 celery -A app.tasks.celery_app inspect active
 celery -A app.tasks.celery_app inspect reserved
 ```
 
 ### Frontend Debugging
 
 ```bash
 # React DevTools (browser extension)
 # Redux DevTools (if using)
 # Network tab for API calls
 
 # Console logging
 localStorage.setItem('debug', 'raven:*')
 ```
 
 ### Common Issues
 
 | Issue | Solution |
 |-------|----------|
 | Port 8000 in use | `netstat -ano | findstr :8000` then `taskkill /PID <pid> /F` |
 | DB connection refused | Check PostgreSQL running, verify DATABASE_URL |
 | Redis connection refused | Check Redis running, verify REDIS_URL |
 | Ollama unavailable | `ollama serve`, check model loaded |
 | Migration conflicts | `alembic downgrade base && alembic upgrade head` (dev only) |
 | Frontend styles missing | Restart dev server, check tailwind.config.js content paths |
 
 ## Performance Profiling
 
 ```bash
 # Backend profiling
 python -m cProfile -o profile.stats -m app.main
 python -m pstats profile.stats
 
 # Database query analysis
 EXPLAIN ANALYZE SELECT * FROM assessments;
 
 # Frontend profiling
 # Chrome DevTools Performance tab
 # React DevTools Profiler
 ```
 
 ## Security Considerations
 
 - Never commit secrets, API keys, credentials
 - Use `.env` for local config, `.env.example` for template
 - Validate all input with Pydantic
 - Scope validation on every action
 - Audit logging for all assessment actions
 - Evidence integrity verification
 - Rate limiting on API endpoints
 
 ## Release Checklist
 
 - [ ] All tests pass
 - [ ] Type checking passes (mypy strict, tsc)
 - [ ] Linting passes (ruff, eslint)
 - [ ] Documentation updated
 - [ ] CHANGELOG updated
 - [ ] Version bumped
 - [ ] Docker images build successfully
 - [ ] Database migrations tested
 - [ ] Security scan (bandit, npm audit)
 
 ---
 
 *Last updated: 2026-11-06*
