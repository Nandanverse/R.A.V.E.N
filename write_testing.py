import pathlib
content = """# Testing Strategy

Comprehensive testing approach for RAVEN covering unit, integration, contract, and security-specific tests.

## Test Pyramid

```
        /\  E2E / UI Tests (Playwright) - Few, critical paths
       /  \
      /----\ Integration Tests - Module interactions
     /      \
    /--------\ Contract Tests - API schemas, schemas
   /          \
  /------------\ Unit Tests - Business logic, utilities
 /              \
/----------------\ Static Analysis - Types, lint, security
```

## Backend Testing (pytest)

### Structure

```
backend/
├── tests/
│   ├── unit/
│   │   ├── test_policy_engine.py
│   │   ├── test_scope_validator.py
│   │   ├── test_cvss_calculator.py
│   │   ├── test_confidence_scorer.py
│   │   ├── test_proposal_validator.py
│   │   └── test_evidence_hasher.py
│   ├── integration/
│   │   ├── test_assessment_lifecycle.py
│   │   ├── test_recon_scanning.py
│   │   ├── test_intel_ingestion.py
│   │   ├── test_proposal_to_execution.py
│   │   ├── test_graph_building.py
│   │   └── test_report_generation.py
│   ├── contract/
│   │   ├── test_api_schemas.py
│   │   └── test_openapi_spec.py
│   ├── security/
│   │   ├── test_scope_enforcement.py
│   │   ├── test_llm_output_validation.py
│   │   ├── test_evidence_integrity.py
│   │   └── test_secret_redaction.py
│   ├── fixtures/
│   │   ├── conftest.py
│   │   ├── sample_nvd.json
│   │   ├── sample_nmap.xml
│   │   └── sample_zap_alerts.json
│   └── utils/
│       ├── factories.py
│       └── helpers.py
```

### Unit Test Examples

```python
# test_policy_engine.py
class TestPolicyEngine:
    @pytest.fixture
    def engine(self):
        return PolicyEngine()

    @pytest.fixture
    def assessment_l1(self):
        return Assessment(execution_level=ExecutionLevel.L1)

    @pytest.fixture
    def assessment_l2(self):
        return Assessment(execution_level=ExecutionLevel.L2)

    @pytest.fixture
    def assessment_l3(self):
        return Assessment(execution_level=ExecutionLevel.L3)

    def test_scope_validation_rejects_unauthorized(self, engine):
        proposal = Proposal(target="evil.com", action_type="port_scan")
        assessment = Assessment(scopes=[Scope(target="allowed.com")])
        decision = engine.evaluate(proposal, assessment)
        assert decision.decision == "rejected"
        assert "not in authorized scope" in decision.reason

    def test_l1_allows_passive_only(self, engine, assessment_l1):
        passive_prop = Proposal(action_type="correlate_vulnerabilities")
        active_prop = Proposal(action_type="port_scan")

        assert engine.evaluate(passive_prop, assessment_l1).decision == "approved"
        assert engine.evaluate(active_prop, assessment_l1).decision == "rejected"

    def test_l2_allows_controlled(self, engine, assessment_l2):
        for action in L2_ACTIONS:
            prop = Proposal(action_type=action)
            assert engine.evaluate(prop, assessment_l2).decision == "approved"

    def test_l3_requires_approval(self, engine, assessment_l3):
        prop = Proposal(action_type="exploit_sqli")
        decision = engine.evaluate(prop, assessment_l3)
        assert decision.decision == "requires_approval"

    def test_l3_approved_with_valid_approval(self, engine, assessment_l3):
        prop = Proposal(action_type="exploit_sqli", id=uuid4())
        approval = ApprovalRequest(proposal_id=prop.id, granted=True)
        decision = engine.evaluate(prop, assessment_l3, approval=approval)
        assert decision.decision == "approved"

    def test_rate_limit_enforcement(self, engine, assessment_l2):
        for _ in range(5):
            assert engine.evaluate(Proposal(action_type="port_scan"), assessment_l2).decision == "approved"
        # 6th should be rejected
        assert engine.evaluate(Proposal(action_type="port_scan"), assessment_l2).decision == "rejected"

    def test_emergency_stop_blocks_all(self, engine, assessment_l2):
        engine.activate_emergency_stop()
        assert engine.evaluate(Proposal(action_type="correlate_vulnerabilities"), assessment_l2).decision == "rejected"
```

### Integration Test Examples

```python
# test_assessment_lifecycle.py
class TestAssessmentLifecycle:
    async def test_full_assessment_flow(self, client, db):
        # 1. Create assessment
        resp = await client.post("/api/v1/assessments", json={
            "name": "Test Assessment",
            "targets": ["localhost"],
            "execution_level": "L2"
        })
        assert resp.status_code == 201
        assessment_id = resp.json()["id"]

        # 2. Start reconnaissance
        resp = await client.post(f"/api/v1/recon/scans", json={
            "assessment_id": assessment_id,
            "scan_type": "host_discovery"
        })
        assert resp.status_code == 201
        scan_id = resp.json()["id"]

        # 3. Wait for completion
        await wait_for_scan_completion(client, scan_id)

        # 4. Verify assets discovered
        resp = await client.get(f"/api/v1/assets?assessment_id={assessment_id}")
        assert len(resp.json()["items"]) > 0

        # 5. Run correlation
        await client.post(f"/api/v1/intel/correlate", json={"assessment_id": assessment_id})

        # 6. Generate AI proposals
        await client.post(f"/api/v1/ai/analyze", json={"assessment_id": assessment_id})

        # 7. Approve and execute
        proposals = await client.get(f"/api/v1/ai/proposals?assessment_id={assessment_id}")
        for prop in proposals.json()["items"]:
            if prop["risk_level"] == "L2":
                await client.post(f"/api/v1/ai/proposals/{prop['id']}/approve")

        # 8. Verify findings
        findings = await client.get(f"/api/v1/findings?assessment_id={assessment_id}")
        assert len(findings.json()["items"]) >= 0  # May be 0 if no vulns

        # 9. Generate report
        resp = await client.post("/api/v1/reports/generate", json={
            "assessment_id": assessment_id,
            "format": "json"
        })
        assert resp.status_code == 201
```

### Security-Specific Tests

```python
# test_scope_enforcement.py
class TestScopeEnforcement:
    async def test_nmap_target_validation(self):
        \"\"\"Nmap scanner only scans allowed targets.\"\"\"
        scanner = NmapScanner()

        # Allowed target
        result = await scanner.scan("allowed.com", ["-sn"])
        assert result.status == "completed"

        # Disallowed target - should be rejected before nmap runs
        with pytest.raises(ScopeViolationError):
            await scanner.scan("evil.com", ["-sn"])

    async def test_llm_cannot_bypass_policy(self):
        \"\"\"Even if LLM proposes malicious action, policy rejects.\"\"\"
        malicious_proposal = Proposal(
            action_type="run_command",  # Not in allowed actions
            target="localhost",
            payload={"command": "rm -rf /"}
        )
        decision = await policy_engine.evaluate(malicious_proposal, assessment)
        assert decision.decision == "rejected"
        assert "not in allowed actions" in decision.reason

    async def test_evidence_integrity(self):
        \"\"\"Evidence hash verification detects tampering.\"\"\"
        evidence = Evidence(content=b"original", hash=sha256(b"original").hexdigest())
        assert evidence.verify()

        # Tamper
        evidence.content = b"tampered"
        assert not evidence.verify()

    async def test_secret_redaction(self):
        \"\"\"Secrets redacted from evidence and logs.\"\"\"
        request = HttpRequest(
            headers={"Authorization": "Bearer secret-token", "Cookie": "session=xyz"}
        )
        redacted = redact_secrets(request)
        assert "secret-token" not in str(redacted.headers)
        assert "xyz" not in str(redacted.headers)
        assert "[REDACTED]" in str(redacted.headers)
```

## Frontend Testing (Vitest + React Testing Library)

### Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/
│   │       ├── Button.test.tsx
│   │       ├── Badge.test.tsx
│   │       └── Table.test.tsx
│   ├── features/
│   │   ├── attack-graph/
│   │   │   └── AttackGraph.test.tsx
│   │   ├── findings/
│   │   │   └── FindingsTable.test.tsx
│   │   └── ai-analysis/
│   │       └── ProposalList.test.tsx
│   ├── pages/
│   │   ├── Assessments.test.tsx
│   │   └── Overview.test.tsx
│   └── test/
│       ├── setup.ts
│       ├── utils.tsx
│       └── mocks/
│           ├── handlers.ts
│           └── data.ts
```

### Component Test Examples

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from "@testing-library/react"
import { Button } from "./Button"

describe("Button", () => {
  it("renders with correct variant classes", () => {
    render(<Button variant="primary">Click</Button>)
    expect(screen.getByRole("button")).toHaveClass("bg-sev-info")

    render(<Button variant="secondary">Click</Button>)
    expect(screen.getByRole("button")).toHaveClass("bg-bg-hover")
  })

  it("shows loading state", () => {
    render(<Button loading>Click</Button>)
    expect(screen.getByRole("button")).toBeDisabled()
    expect(screen.getByRole("button")).toContainHTML("svg") // spinner
  })

  it("calls onClick handler", () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByRole("button"))
    expect(handleClick).toHaveBeenCalledOnce()
  })

  it("forwards ref", () => {
    const ref = createRef<HTMLButtonElement>()
    render(<Button ref={ref}>Click</Button>)
    expect(ref.current).toBeInstanceOf(HTMLButtonElement)
  })
})

// AttackGraph.test.tsx
describe("AttackGraph", () => {
  it("renders nodes and edges", () => {
    const nodes = [{ id: "1", type: "asset", label: "Server" }]
    const edges = [{ id: "e1", source: "1", target: "2", edge_type: "exposes" }]

    render(<AttackGraph nodes={nodes} edges={edges} />)

    expect(screen.getByTestId("cytoscape-container")).toBeInTheDocument()
    // Cytoscape elements verified via instance
  })

  it("shows node detail on click", async () => {
    const onNodeClick = vi.fn()
    render(<AttackGraph nodes={nodes} edges={edges} onNodeClick={onNodeClick} />)

    const container = screen.getByTestId("cytoscape-container")
    fireEvent.click(container) // Simplified
    expect(onNodeClick).toHaveBeenCalled()
  })
})
```

## End-to-End Testing (Playwright)

### Critical User Flows

```typescript
// e2e/assessment-flow.spec.ts
import { test, expect } from "@playwright/test"

test.describe("Assessment Flow", () => {
  test("create assessment, run scan, view findings", async ({ page }) => {
    await page.goto("/assessments")
    await page.click("button:has-text('New Assessment')")
    await page.fill("input[name=name]", "E2E Test Assessment")
    await page.fill("input[name=targets]", "localhost")
    await page.selectOption("select[name=execution_level]", "L1")
    await page.click("button:has-text('Create')")

    await expect(page.locator("text=Assessment created")).toBeVisible()

    await page.goto("/recon")
    await page.selectOption("select[name=assessment]", "E2E Test Assessment")
    await page.check("input[value=host_discovery]")
    await page.click("button:has-text('Start Scan')")

    await expect(page.locator("text=completed")).toBeVisible({ timeout: 60000 })

    await page.goto("/assets")
    await expect(page.locator("table tbody tr")).toHaveCount.greaterThan(0)
  })

  test("AI analysis proposes actions", async ({ page }) => {
    await page.goto("/ai")
    await page.selectOption("select[name=assessment]", "E2E Test Assessment")
    await page.click("button:has-text('Analyze')")

    await expect(page.locator("[data-testid=proposal-list]")).toBeVisible()
    await expect(page.locator("[data-testid=proposal]")).toHaveCount.greaterThan(0)
  })

  test("attack graph displays relationships", async ({ page }) => {
    await page.goto("/attack-graph")
    await page.selectOption("select[name=assessment]", "E2E Test Assessment")

    await expect(page.locator("[data-testid=cytoscape-container]")).toBeVisible()
    // Wait for graph to render
    await page.waitForTimeout(2000)

    const nodes = await page.locator("[data-testid=graph-node]").count()
    expect(nodes).toBeGreaterThan(0)
  })
})
```

## Test Data Management

### Fixtures

```python
# tests/fixtures/factories.py
class AssessmentFactory:
    @staticmethod
    def create(db, **overrides) -> Assessment:
        defaults = {
            "name": "Test Assessment",
            "status": "draft",
            "execution_level": "L2",
            "created_by": test_user.id
        }
        defaults.update(overrides)
        assessment = Assessment(**defaults)
        db.add(assessment)
        db.commit()
        return assessment

class ScanFactory:
    @staticmethod
    def create(db, assessment_id, **overrides) -> ScanHistory:
        defaults = {
            "assessment_id": assessment_id,
            "scan_type": "port_scan",
            "status": "completed",
            "statistics": {"hosts_up": 1, "ports_open": 5}
        }
        ...
```

### Sample Data

```
tests/fixtures/
├── sample_nvd.json          # Single CVE item from NVD
├── sample_nmap.xml          # Nmap XML output for parsing tests
├── sample_zap_alerts.json   # ZAP alert format
├── sample_epss.csv          # EPSS CSV rows
└── sample_kev.json          # KEV catalog entry
```

## CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: raven_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: [5432:5432]
        options: >-
          --health-cmd "pg_isready -U test"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports: [6379:6379]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: pip install -r requirements-test.txt
      - run: alembic upgrade head
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/raven_test
      - run: python -m mypy --strict backend/app
      - run: python -m ruff check backend/
      - run: python -m pytest backend/tests/ -v --cov=backend/app --cov-fail-under=80

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20", cache: "npm" }
      - run: cd frontend && npm ci
      - run: cd frontend && npm run typecheck
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test -- --run
      - run: cd frontend && npm run test:e2e
        env:
          CI: true

  docker:
    runs-on: ubuntu-latest
    needs: [backend, frontend]
    steps:
      - uses: actions/checkout@v4
      - run: docker compose -f docker-compose.yml -f docker-compose.test.yml build
      - run: docker compose -f docker-compose.yml -f docker-compose.test.yml up -d
      - run: sleep 30 && curl -f http://localhost:8000/health
      - run: curl -f http://localhost:5173
```

## Test Commands

```bash
# Backend
cd backend
python -m pytest                                    # All tests
python -m pytest tests/unit/                        # Unit only
python -m pytest tests/integration/                 # Integration only
python -m pytest tests/security/                    # Security only
python -m pytest -k "scope"                         # Filter by name
python -m pytest --cov=app --cov-report=html        # Coverage

# Frontend
cd frontend
npm run test                                        # Unit + component
npm run test:e2e                                    # Playwright
npm run test:coverage                               # Coverage

# Full stack
docker compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit
```

## Coverage Targets

| Layer | Target |
|-------|--------|
| Backend unit | 90% |
| Backend integration | 70% |
| Frontend components | 80% |
| Frontend pages | 60% |
| Overall | 80% |

## Future Enhancements

- **Mutation Testing**: Stryker for Python/JS
- **Property-Based Testing**: Hypothesis for complex logic
- **Chaos Engineering**: Litmus/Gremlin for resilience
- **Visual Regression**: Chromatic for UI components
- **API Fuzzing**: Schemathesis for OpenAPI fuzzing

---

*Testing strategy version: 1.0*
*Last updated: 2026-11-06*
"""
pathlib.Path("C:/Users/nanda/OneDrive/Desktop/RAVEN/docs/testing.md").write_text(content, encoding="utf-8")
print("done")
