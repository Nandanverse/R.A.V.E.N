# Policy Engine Design

Detailed specification of the RAVEN Policy Engine - the mandatory gate between AI proposals and test execution.

## Overview

The Policy Engine is a deterministic, independent validation layer that every proposed action must pass before execution. It is the single point of enforcement for:

- Target authorization (allowlist)
- Execution level limits (L1/L2/L3)
- Rate limiting and resource budgets
- Human approval requirements
- Emergency stop

The LLM never executes actions directly. It only proposes structured actions. The Policy Engine evaluates each proposal and produces an explicit approval or rejection with reasoning.

## Architecture

```
RavenBrain (LLM) --> PolicyEngine (Deterministic) --> TestExecutor (Execution)
                           |
              Allowlist Check, Budgets Check, Approvals Check
                           |
                           v
                    PolicyDecision
                    (approved/rejected/requires_approval)
```

## Policy Decision Flow

```python
def evaluate(proposal, context):
    # 1. Scope validation (MANDATORY - always first)
    if not validate_scope(proposal.target, context.assessment.scopes):
        return PolicyDecision.rejected("Target not in authorized scope")

    # 2. Execution level check
    required_level = get_required_level(proposal.action_type)
    if required_level > context.assessment.execution_level:
        if required_level == ExecutionLevel.L3:
            return PolicyDecision.requires_approval(
                "L3 action requires human approval"
            )
        return PolicyDecision.rejected(
            f"Action requires {required_level}, assessment limited to {context.assessment.execution_level}"
        )

    # 3. Rate limits
    if not check_rate_limits(proposal, context):
        return PolicyDecision.rejected("Rate limit exceeded")

    # 4. Assessment budgets
    if not check_budgets(proposal, context):
        return PolicyDecision.rejected("Assessment budget exceeded")

    # 5. Tool availability
    if not check_tool_availability(proposal.action_type):
        return PolicyDecision.rejected(f"Required tool not available: {proposal.action_type}")

    # 6. Emergency stop
    if is_emergency_stop_active(context.assessment_id):
        return PolicyDecision.rejected("Emergency stop active")

    # 7. L3 human approval
    if required_level == ExecutionLevel.L3:
        approval = get_pending_approval(proposal.id)
        if not approval or not approval.granted:
            return PolicyDecision.requires_approval("L3 action requires human approval")
        if approval.expired:
            return PolicyDecision.rejected("Approval expired")

    # All checks passed
    return PolicyDecision.approved()
```

## Execution Levels

### L1 - Passive

Definition: Actions that only read existing data, perform offline analysis, or correlate intelligence. No network traffic to targets.

Actions: correlate_vulnerabilities, build_attack_graph, calculate_risk, generate_report, analyze_intelligence, query_assets

Approval: Automatic (within rate limits)

### L2 - Controlled

Definition: Active but non-destructive interactions with targets. May send network traffic but does not alter target state.

Actions: host_discovery, port_scan, service_enumeration, http_discovery, test_header_analysis, test_cookie_analysis, test_cors, test_api_authz, test_input_validation, test_rate_limit, zap_active_scan, zap_passive_scan

Approval: Automatic (within rate limits and budgets)

### L3 - Intrusive

Definition: Actions that may alter application and system state, extract data, or demonstrate exploitability. Require explicit human approval.

Actions: exploit_sqli, exploit_xss, exploit_rce, password_spray, privilege_escalation, data_exfiltration, persistence_test, lateral_movement

Approval: Human-in-the-loop required

### Level Enforcement

```python
EXECUTION_LEVELS = {
    ExecutionLevel.L1: {L1_ACTIONS},
    ExecutionLevel.L2: {L1_ACTIONS} | {L2_ACTIONS},
    ExecutionLevel.L3: {L1_ACTIONS} | {L2_ACTIONS} | {L3_ACTIONS},
}

def get_required_level(action_type):
    for level, actions in EXECUTION_LEVELS.items():
        if action_type in actions:
            return level
    return ExecutionLevel.L3  # Default to most restrictive
```

## Allowlist Validation

Target Formats: Domain (example.com), Wildcard subdomain (*.example.com), IPv4 (192.168.1.100), IPv6 (2001:db8::1), CIDR IPv4 (192.168.1.0/24), CIDR IPv6 (2001:db8::/32)

Validation Logic:

```python
def validate_target(target, allowlist):
    parsed = parse_target(target)
    if not parsed:
        return ValidationResult(valid=False, reason="Invalid target format")

    for allowed in allowlist:
        if allowed == target:
            return ValidationResult(valid=True, matched=allowed)

        if allowed.startswith("*."):
            suffix = allowed[1:]  # .example.com
            if parsed.domain and parsed.domain.endswith(suffix):
                return ValidationResult(valid=True, matched=allowed)

        if "/" in allowed:  # CIDR
            if ip_in_cidr(parsed.ip, allowed):
                return ValidationResult(valid=True, matched=allowed)

    return ValidationResult(valid=False, reason=f"Target not in allowlist: {target}")
```

## Rate Limiting

Per-Assessment Limits: Scan starts 5/min, Concurrent scans 2, L2 test executions 50/min, L3 approval requests 5/hour, Proposal generations 10/min

Global Limits: API requests 60/min per IP, Authenticated API 120/min per user, Evidence upload 10 MB per request, Report generation 2/min per user

## Assessment Budgets

```python
@dataclass
class AssessmentBudget:
    max_duration_minutes: int = 120
    max_api_calls: int = 10000
    max_scan_targets: int = 256
    max_evidence_mb: int = 500
    max_findings: int = 1000
    max_concurrent_tasks: int = 3

async def check_budget(assessment_id, action):
    budget = await get_budget(assessment_id)
    usage = await get_usage(assessment_id)

    checks = {
        "duration": usage.duration_minutes < budget.max_duration_minutes,
        "api_calls": usage.api_calls < budget.max_api_calls,
        "targets": usage.scan_targets < budget.max_scan_targets,
        "evidence": usage.evidence_mb < budget.max_evidence_mb,
        "findings": usage.findings < budget.max_findings,
    }

    if not all(checks.values()):
        return BudgetCheck(allowed=False, exceeded=[k for k, v in checks.items() if not v])

    return BudgetCheck(allowed=True)
```

## Human Approval Workflow (L3)

Approval Request includes: id, proposal_id, assessment_id, action_type, target, risk_level, reasoning, requested_by, requested_at, expires_at, status, reviewer, reviewed_at, review_reason

Approval Flow: 1) PolicyEngine returns requires_approval for L3 action, 2) Creates ApprovalRequest with 24-hour expiry, 3) Notifies reviewers, 4) Reviewer accesses Approvals page, 5) Reviewer sees action, target, reasoning, risk, evidence requirements, 6) Reviewer clicks Approve or Deny with mandatory reason, 7) PolicyEngine re-evaluates proposal

Approval Constraints: Only users with reviewer role can approve, Approver cannot be the same as requester, Approval reason mandatory, Approval logged in audit trail, Expired approvals require new request, Emergency stop revokes all pending approvals

## Emergency Stop

Effects: All running scans/tests terminated, All pending proposals rejected, New proposals auto-rejected, New scan/test execution blocked, Assessment status set to emergency_stopped, Requires admin action to clear

## Policy Decision Records

Every evaluation creates an immutable record in policy_decisions table with: id, proposal_id, decision, reason, checks, reviewer, expires_at, created_at

## Configuration

Settings: ASSESSMENT_TIMEOUT_MINUTES=120, RATE_LIMIT_SCANS_PER_MINUTE=5, RATE_LIMIT_L2_TESTS_PER_MINUTE=50, RATE_LIMIT_L3_APPROVALS_PER_HOUR=5, APPROVAL_EXPIRY_HOURS=24, MAX_CONCURRENT_SCANS=2, MAX_EVIDENCE_MB=500, EMERGENCY_STOP_TTL_HOURS=24

## Testing

Unit tests for scope validation, level enforcement, rate limits, emergency stop. Integration tests for full L3 flow.

## Future Enhancements

- Time-based policies: Restrict scanning to maintenance windows
- Target criticality policies: Stricter limits for critical assets
- Compliance policies: Enforce NIST/ISO control mappings
- Dynamic budgets: ML-based anomaly detection
- Policy-as-code: Version-controlled policy definitions (OPA/Rego)

---

Policy engine design version: 1.0
Last updated: 2026-11-06
