# AI Agent Design

Design specification for RavenBrain - the local LLM reasoning module.

## Overview

RavenBrain provides AI-assisted security reasoning using locally-hosted LLMs via Ollama. It is designed as a **reasoning engine**, not an execution engine.

Key principles:
- **Structured output only** - LLM returns JSON proposals, never commands
- **Policy-gated** - Every proposal validated by independent PolicyEngine
- **Graceful degradation** - Full functionality when Ollama unavailable
- **Transparent reasoning** - All proposals include reasoning and evidence requirements
- **Context-aware** - Retrieves relevant intelligence for each proposal

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      RavenBrain Module                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Ollama      │  │  Prompt      │  │  Output      │       │
│  │  Client      │──►│  Builder     │──►│  Validator   │       │
│  └──────────────┘  └──────────────┘  └──────┬───────┘       │
│                                             │               │
│                          ┌──────────────────┘               │
│                          ▼                                  │
│                 ┌──────────────┐                            │
│                 │  RAG         │                            │
│                 │  Retriever   │                            │
│                 └──────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  PolicyEngine    │
                  │  (Independent)   │
                  └──────────────────┘
```

## Components

### Ollama Client

```python
class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout: int = 120):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def generate(self, prompt: str, schema: dict) -> dict:
        """Generate structured JSON output using schema enforcement."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "format": schema,  # JSON Schema for structured output
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 4096
            }
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return json.loads(response.text)["response"]

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False
```

### Prompt Builder

System prompt template:

```markdown
You are a senior cybersecurity engineer assisting in authorized security assessments.

Your role: Analyze assessment findings and propose the NEXT appropriate test action.

Constraints:
- You ONLY propose structured actions from the allowed action types
- You NEVER execute commands or generate exploit code
- You MUST provide clear reasoning for each proposal
- You MUST specify required evidence for validation
- You MUST classify risk level (L1/L2/L3)

Allowed Action Types:
- test_header_analysis: Check HTTP security headers
- test_cookie_analysis: Validate cookie security attributes
- test_cors: Test CORS configuration
- test_api_authz: Test API authorization (IDOR/BOLA)
- test_input_validation: Probe input validation (safe payloads only)
- test_rate_limit: Measure rate limiting effectiveness
- zap_active_scan: Trigger OWASP ZAP active scan
- zap_passive_scan: Trigger OWASP ZAP passive scan
- correlate_vulnerabilities: Match services to CVEs
- build_attack_graph: Construct attack path relationships
```

Few-shot examples included for each action type.

### Output Validator

```python
class ProposalValidator:
    SCHEMA = {
        "type": "object",
        "required": ["action", "target", "reason", "required_evidence", "risk_level"],
        "properties": {
            "action": {"type": "string", "enum": ALLOWED_ACTIONS},
            "target": {"type": "object"},  # {asset_id, service_id, url, params}
            "reason": {"type": "string", "minLength": 20},
            "required_evidence": {"type": "array", "items": {"type": "string"}},
            "risk_level": {"type": "string", "enum": ["L1", "L2", "L3"]}
        }
    }

    def validate(self, raw_output: str) -> Proposal:
        # Parse JSON
        data = json.loads(raw_output)

        # Validate against schema
        jsonschema.validate(data, self.SCHEMA)

        # Additional semantic validation
        self._validate_target_exists(data["target"])
        self._validate_evidence_requirements(data["action"], data["required_evidence"])
        self._validate_risk_level(data["action"], data["risk_level"])

        return Proposal(**data)
```

### RAG Retriever

Retrieves relevant context for proposal generation:

```python
class RAGRetriever:
    def __init__(self, embedding_model: str = "nomic-embed-text"):
        self.embedding_model = embedding_model

    async def retrieve_context(self, assessment_id: UUID, query: str, k: int = 5) -> list[ContextChunk]:
        """Retrieve relevant CVEs, ATT&CK techniques, findings, evidence."""
        # 1. Embed query
        query_embedding = await self.embed(query)

        # 2. Search vector store (PGVector or FAISS)
        results = await self.vector_store.search(query_embedding, k=k)

        # 3. Format context chunks
        chunks = []
        for result in results:
            if result.type == "cve":
                chunks.append(ContextChunk(
                    type="cve",
                    content=f"CVE: {result.cve_id}, CVSS: {result.cvss}, EPSS: {result.epss}",
                    metadata=result.metadata
                ))
            elif result.type == "attack":
                chunks.append(ContextChunk(
                    type="attack",
                    content=f"ATT&CK: {result.technique_id} - {result.name}",
                    metadata=result.metadata
                ))
            elif result.type == "finding":
                chunks.append(ContextChunk(
                    type="finding",
                    content=f"Finding: {result.title}, Severity: {result.severity}",
                    metadata=result.metadata
                ))

        return chunks
```

## Proposal Schema

```json
{
  "action": "test_api_authz",
  "target": {
    "asset_id": "uuid",
    "service_id": "uuid",
    "url": "https://api.example.com/users/123/profile",
    "method": "GET",
    "params": {"user_id": "123"}
  },
  "reason": "The endpoint exposes a user identifier in the path that requires authorization validation. Similar endpoints in the application have shown IDOR vulnerabilities.",
  "required_evidence": [
    "HTTP response from cross-user request",
    "Authenticated user identity",
    "Authorization decision (allow/deny)"
  ],
  "risk_level": "L2"
}
```

## Action Types Reference

### Passive (L1)

| Action | Description | When to Use |
|--------|-------------|-------------|
| `correlate_vulnerabilities` | Match discovered services to CVE database | After service enumeration |
| `build_attack_graph` | Construct relationship graph from findings | After findings validated |
| `calculate_risk` | Compute contextual risk scores | After graph built |
| `analyze_intelligence` | Query CVE, EPSS, KEV, ATT&CK for context | When proposing tests |

### Controlled (L2)

| Action | Description | Evidence Required |
|--------|-------------|-------------------|
| `test_header_analysis` | Analyze HTTP security headers | Response headers |
| `test_cookie_analysis` | Validate cookie attributes | Set-Cookie headers |
| `test_cors` | Test CORS misconfiguration | CORS response headers |
| `test_api_authz` | Test API authorization (IDOR/BOLA) | Cross-user responses |
| `test_input_validation` | Probe input validation (safe) | Response analysis |
| `test_rate_limit` | Measure rate limiting | Response times/codes |
| `zap_active_scan` | OWASP ZAP active scan | ZAP alerts |
| `zap_passive_scan` | OWASP ZAP passive scan | ZAP alerts |

### Intrusive (L3)

| Action | Description | Approval Required |
|--------|-------------|-------------------|
| `exploit_sqli` | Demonstrate SQLi impact | Yes |
| `exploit_xss` | Demonstrate XSS execution | Yes |
| `exploit_rce` | Demonstrate RCE | Yes |
| `password_spray` | Credential testing | Yes |
| `privilege_escalation` | Test priv esc paths | Yes |
| `data_exfiltration` | Demonstrate data access | Yes |
| `persistence_test` | Test persistence | Yes |
| `lateral_movement` | Test network pivoting | Yes |

## Orchestration (LangGraph)

Assessment workflow as a state graph:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AssessmentState)

workflow.add_node("observe", observe_node)      # Gather current state
workflow.add_node("analyze", analyze_node)      # LLM analyzes findings
workflow.add_node("propose", propose_node)      # Generate proposals
workflow.add_node("validate", validate_node)    # PolicyEngine validates
workflow.add_node("execute", execute_node)      # TestExecutor runs tests
workflow.add_node("learn", learn_node)          # Update state with results

workflow.add_edge("observe", "analyze")
workflow.add_edge("analyze", "propose")
workflow.add_edge("propose", "validate")
workflow.add_conditional_edges(
    "validate",
    route_after_validation,
    {"approved": "execute", "rejected": "learn", "requires_approval": "learn"}
)
workflow.add_edge("execute", "learn")
workflow.add_edge("learn", "observe")
workflow.add_edge("learn", END)

app = workflow.compile()
```

State includes: assessment_id, assets, services, findings, proposals, decisions, evidence, iteration_count, max_iterations.

## Availability & Fallback

### Health Monitoring

```python
class BrainAvailability:
    def __init__(self, client: OllamaClient):
        self.client = client
        self._healthy = True
        self._last_check = None
        self._circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=60)

    async def check(self) -> bool:
        if self._circuit_breaker.open:
            return False

        healthy = await self.client.health_check()
        self._healthy = healthy
        self._last_check = datetime.utcnow()

        if not healthy:
            self._circuit_breaker.record_failure()

        return healthy

    @property
    def status(self) -> BrainStatus:
        return BrainStatus(
            available=self._healthy,
            model=self.client.model,
            last_check=self._last_check,
            circuit_open=self._circuit_breaker.open
        )
```

### Offline Mode

When Ollama unavailable:

1. API returns `BrainStatus(available=False, ...)`
2. UI shows "AI Reasoning Unavailable" banner
3. All other modules function normally
4. Manual proposal creation available in UI
5. PolicyEngine, TestExecutor, EvidenceVault, AttackGraph, RiskEngine all work
6. Cached proposals (if any) remain accessible

## Testing

### Unit Tests

```python
# Test prompt building
prompt = build_prompt(assessment_context, few_shot_examples)
assert "Allowed Action Types" in prompt
assert "test_api_authz" in prompt

# Test output validation
valid_output = {"action": "test_header_analysis", "target": {...}, "reason": "...", "required_evidence": [...], "risk_level": "L2"}
proposal = validator.validate(json.dumps(valid_output))
assert proposal.action == "test_header_analysis"

# Test validation rejects invalid
invalid_output = {"action": "run_nmap", "target": {...}}  # Not allowed
with pytest.raises(ValidationError):
    validator.validate(json.dumps(invalid_output))

# Test malformed JSON
with pytest.raises(JSONDecodeError):
    validator.validate("not json")
```

### Integration Tests

```python
async def test_full_proposal_flow():
    # Setup assessment with findings
    assessment = create_assessment_with_findings()

    # Generate proposals
    proposals = await brain.analyze_and_propose(assessment.id)

    # Validate each proposal
    for prop in proposals:
        assert prop.action in ALLOWED_ACTIONS
        assert prop.risk_level in ["L1", "L2", "L3"]
        assert len(prop.reason) >= 20
        assert len(prop.required_evidence) > 0

        # Policy evaluation
        decision = await policy_engine.evaluate(prop, assessment)
        assert decision.decision in ["approved", "rejected", "requires_approval"]
```

### Failure Scenario Tests

```python
async def test_ollama_unavailable():
    # Mock Ollama failure
    with patch("ollama_client.health_check", return_value=False):
        status = await brain.get_status()
        assert status.available == False

        # Should still support manual proposals
        manual_prop = create_manual_proposal(...)
        decision = await policy_engine.evaluate(manual_prop, assessment)
        assert decision.decision == "approved"
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama API endpoint |
| `OLLAMA_MODEL` | llama3.1:8b | Model for reasoning |
| `OLLAMA_TIMEOUT` | 120 | Request timeout (seconds) |
| `OLLAMA_TEMPERATURE` | 0.1 | Generation temperature |
| `OLLAMA_MAX_TOKENS` | 4096 | Max response tokens |
| `RAG_EMBEDDING_MODEL` | nomic-embed-text | Embedding model |
| `RAG_TOP_K` | 5 | Context chunks retrieved |
| `MAX_PROPOSALS_PER_ANALYSIS` | 10 | Proposal limit |
| `ANALYSIS_ITERATION_LIMIT` | 5 | Max workflow iterations |

## Model Selection

Recommended free models compatible with Ollama:

| Model | Size | Strengths |
|-------|------|-----------|
| `llama3.1:8b` | 4.7 GB | Best overall reasoning, instruction following |
| `llama3.1:70b` | 40 GB | Stronger reasoning (requires GPU) |
| `codellama:13b` | 7.3 GB | Code-aware, good for API analysis |
| `mistral:7b` | 4.1 GB | Fast, good reasoning |
| `phi3:14b` | 7.9 GB | Strong logic, compact |

## Security Considerations

- **Prompt injection**: Input sanitized, output schema enforced
- **Data leakage**: Only assessment data in prompts, no secrets
- **Hallucination**: Schema validation catches invalid actions
- **Availability**: Circuit breaker prevents cascade failures
- **Audit**: All proposals logged with LLM response

---

*AI agent design version: 1.0*
*Last updated: 2026-11-06*
