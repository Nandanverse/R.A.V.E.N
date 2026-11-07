 import enum
 import logging
 from dataclasses import dataclass, field
 from typing import Optional
 from uuid import UUID, uuid4
 
 from sqlalchemy import select
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.models import (
     Assessment,
     PolicyDecision,
     ExecutionLevel,
     PolicyDecision as PolicyDecisionEnum,
     Scope,
 )
 from app.config import settings
 
 
 logger = logging.getLogger(__name__)
 
 
 class ExecutionLevel(str, enum.Enum):
     L1_PASSIVE = "L1_PASSIVE"
     L2_CONTROLLED = "L2_CONTROLLED"
     L3_INTRUSIVE = "L3_INTRUSIVE"
 
 
 @dataclass
 class PolicyDecisionResult:
     allowed: bool
     decision: PolicyDecisionEnum
     reason: str
     conditions: list[str] = field(default_factory=list)
     requires_approval: bool = False
     policy_decision_id: Optional[UUID] = None
 
 
 class PolicyEngine:
     """
     Policy Engine - Enforces assessment scope, execution levels, and approval requirements.
     
     This is the mandatory gate that ALL actions must pass through before execution.
     The LLM never bypasses this engine.
     """
 
     # L1 - Passive: No interaction with target systems
     L1_ACTIONS = {
         "passive_dns_lookup",
         "whois_lookup",
         "certificate_transparency_search",
         "search_engine_reconnaissance",
         "threat_intelligence_lookup",
         "offline_analysis",
         "asset_correlation",
     }
 
     # L2 - Controlled: Non-destructive interaction with target
     L2_ACTIONS = {
         "port_scan",
         "service_enumeration",
         "banner_grabbing",
         "web_crawl",
         "directory_enumeration",
         "technology_fingerprint",
         "ssl_tls_scan",
         "http_header_analysis",
         "api_discovery",
         "auth_test_basic",
         "authorization_test",
         "input_validation_test",
         "session_management_test",
     }
 
     # L3 - Intrusive: May alter state, requires explicit human approval
     L3_ACTIONS = {
         "exploit",
         "privilege_escalation",
         "persistence_test",
         "credential_test_bruteforce",
         "sql_injection_exploit",
         "command_injection_exploit",
         "file_upload_exploit",
         "authentication_bypass",
         "authorization_bypass",
         "data_exfiltration_test",
         "lateral_movement_test",
     }
 
     # Rate limits per execution level (requests per minute)
     RATE_LIMITS = {
         ExecutionLevel.L1_PASSIVE: 120,
         ExecutionLevel.L2_CONTROLLED: 30,
         ExecutionLevel.L3_INTRUSIVE: 5,
     }
 
     # Actions requiring human approval (always L3)
     APPROVAL_REQUIRED_ACTIONS = {
         "exploit",
         "privilege_escalation",
         "persistence_test",
         "credential_test_bruteforce",
         "sql_injection_exploit",
         "command_injection_exploit",
         "file_upload_exploit",
         "authentication_bypass",
         "authorization_bypass",
         "data_exfiltration_test",
         "lateral_movement_test",
     }
 
     def __init__(self, db: Optional[AsyncSession] = None):
         self.db = db
         self._emergency_stop = False
         self._action_counts: dict[str, int] = {}
 
     @property
     def emergency_stop_active(self) -> bool:
         return self._emergency_stop
 
     def activate_emergency_stop(self) -> None:
         self._emergency_stop = True
         logger.critical("EMERGENCY STOP ACTIVATED - All assessments halted")
 
     def deactivate_emergency_stop(self) -> None:
         self._emergency_stop = False
         logger.info("Emergency stop deactivated")
 
     def get_execution_level_for_action(self, action: str) -> ExecutionLevel:
         """Determine the execution level required for an action."""
         if action in self.L1_ACTIONS:
             return ExecutionLevel.L1_PASSIVE
         elif action in self.L2_ACTIONS:
             return ExecutionLevel.L2_CONTROLLED
         elif action in self.L3_ACTIONS:
             return ExecutionLevel.L3_INTRUSIVE
         else:
             # Unknown actions default to L3 for safety
             logger.warning(f"Unknown action '{action}', defaulting to L3_INTRUSIVE")
             return ExecutionLevel.L3_INTRUSIVE
 
     def is_approval_required(self, action: str, level: ExecutionLevel) -> bool:
         """Check if an action requires human approval."""
         if action in self.APPROVAL_REQUIRED_ACTIONS:
             return True
         if level == ExecutionLevel.L3_INTRUSIVE:
             return True
         return False
 
     async def evaluate(
         self,
         action: str,
         target: str,
         level: ExecutionLevel,
         context: dict,
         assessment_id: Optional[UUID] = None,
     ) -> PolicyDecisionResult:
         """
         Evaluate an action against policy rules.
         
         This is the MAIN entry point - ALL actions must pass through here.
         """
         # 1. Emergency stop check
         if self._emergency_stop:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason="Emergency stop is active - all actions blocked",
                 conditions=["EMERGENCY_STOP_ACTIVE"],
             )
 
         # 2. Validate execution level matches action
         required_level = self.get_execution_level_for_action(action)
         if level.value < required_level.value:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason=f"Action '{action}' requires {required_level.value}, but {level.value} was requested",
                 conditions=["INSUFFICIENT_EXECUTION_LEVEL"],
             )
 
         # 3. Scope validation
         if assessment_id and self.db:
             scope_check = await self._validate_scope(target, assessment_id)
             if not scope_check.allowed:
                 return scope_check
 
         # 4. Approval requirements
         requires_approval = self.is_approval_required(action, level)
         if requires_approval:
             # Check if already approved
             if not await self._check_approval(action, target, assessment_id):
                 return PolicyDecisionResult(
                     allowed=False,
                     decision=PolicyDecisionEnum.REQUIRES_APPROVAL,
                     reason=f"Action '{action}' requires explicit human approval",
                     conditions=["HUMAN_APPROVAL_REQUIRED"],
                     requires_approval=True,
                 )
 
         # 5. Rate limiting
         rate_limit_check = self._check_rate_limit(action, level)
         if not rate_limit_check.allowed:
             return rate_limit_check
 
         # 6. Assessment budget check
         if assessment_id and self.db:
             budget_check = await self._check_assessment_budget(assessment_id)
             if not budget_check.allowed:
                 return budget_check
 
         # All checks passed
         policy_decision = await self._record_decision(
             assessment_id=assessment_id,
             action=action,
             target=target,
             level=level,
             decision=PolicyDecisionEnum.ALLOWED,
             reason="All policy checks passed",
             conditions=[],
         )
 
         return PolicyDecisionResult(
             allowed=True,
             decision=PolicyDecisionEnum.ALLOWED,
             reason="All policy checks passed",
             conditions=[],
             policy_decision_id=policy_decision.id if policy_decision else None,
         )
 
     async def _validate_scope(self, target: str, assessment_id: UUID) -> PolicyDecisionResult:
         """Validate target is within assessment scope."""
         assessment = await self.db.get(Assessment, assessment_id)
         if not assessment or not assessment.scope_id:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason="Assessment has no scope defined",
                 conditions=["NO_SCOPE_DEFINED"],
             )
 
         scope = await self.db.get(Scope, assessment.scope_id)
         if not scope or not scope.is_active:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason="Scope is not active",
                 conditions=["SCOPE_INACTIVE"],
             )
 
         # Check allowlist
         allowed = False
         for allowed_target in scope.targets:
             if self._target_matches(target, allowed_target):
                 allowed = True
                 break
 
         if not allowed:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason=f"Target '{target}' not in authorized scope",
                 conditions=["SCOPE_VIOLATION"],
             )
 
         # Check denylist
         for excluded_target in scope.excluded_targets:
             if self._target_matches(target, excluded_target):
                 return PolicyDecisionResult(
                     allowed=False,
                     decision=PolicyDecisionEnum.REJECTED,
                     reason=f"Target '{target}' is explicitly excluded from scope",
                     conditions=["SCOPE_EXCLUDED"],
                 )
 
         return PolicyDecisionResult(allowed=True, decision=PolicyDecisionEnum.ALLOWED, reason="Scope validation passed")
 
     def _target_matches(self, target: str, pattern: str) -> bool:
         """Check if target matches a scope pattern (supports wildcards)."""
         import fnmatch
         return fnmatch.fnmatch(target.lower(), pattern.lower())
 
     async def _check_approval(self, action: str, target: str, assessment_id: Optional[UUID]) -> bool:
         """Check if action has been approved for this assessment."""
         if not assessment_id or not self.db:
             return False
 
         from sqlalchemy import and_
         result = await self.db.execute(
             select(PolicyDecision).where(
                 and_(
                     PolicyDecision.assessment_id == assessment_id,
                     PolicyDecision.action == action,
                     PolicyDecision.target == target,
                     PolicyDecision.decision == PolicyDecisionEnum.ALLOWED,
                     PolicyDecision.approved_by.is_not(None),
                 )
             )
         )
         return result.scalar_one_or_none() is not None
 
     def _check_rate_limit(self, action: str, level: ExecutionLevel) -> PolicyDecisionResult:
         """Check rate limits for action."""
         limit = self.RATE_LIMITS.get(level, 10)
         key = f"{action}:{level.value}"
         current = self._action_counts.get(key, 0)
 
         if current >= limit:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason=f"Rate limit exceeded for {action} at {level.value} ({limit}/min)",
                 conditions=["RATE_LIMIT_EXCEEDED"],
             )
 
         self._action_counts[key] = current + 1
         return PolicyDecisionResult(allowed=True, decision=PolicyDecisionEnum.ALLOWED, reason="Rate limit OK")
 
     async def _check_assessment_budget(self, assessment_id: UUID) -> PolicyDecisionResult:
         """Check assessment budget (time, concurrent jobs)."""
         assessment = await self.db.get(Assessment, assessment_id)
         if not assessment:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason="Assessment not found",
                 conditions=["ASSESSMENT_NOT_FOUND"],
             )
 
         # Check concurrent assessments for owner
         from sqlalchemy import func, select
         from app.db.models import Assessment as AssessmentModel
 
         result = await self.db.execute(
             select(func.count()).select_from(AssessmentModel).where(
                 AssessmentModel.owner_id == assessment.owner_id,
                 AssessmentModel.status.in_([AssessmentStatus.RUNNING, AssessmentStatus.PAUSED]),
             )
         )
         concurrent = result.scalar() or 0
 
         if concurrent >= settings.MAX_CONCURRENT_ASSESSMENTS:
             return PolicyDecisionResult(
                 allowed=False,
                 decision=PolicyDecisionEnum.REJECTED,
                 reason=f"Maximum concurrent assessments ({settings.MAX_CONCURRENT_ASSESSMENTS}) reached",
                 conditions=["MAX_CONCURRENT_ASSESSMENTS_EXCEEDED"],
             )
 
         return PolicyDecisionResult(allowed=True, decision=PolicyDecisionEnum.ALLOWED, reason="Budget check passed")
 
     async def _record_decision(
         self,
         assessment_id: Optional[UUID],
         action: str,
         target: str,
         level: ExecutionLevel,
         decision: PolicyDecisionEnum,
         reason: str,
         conditions: list[str],
     ) -> Optional[PolicyDecision]:
         """Record policy decision for audit trail."""
         if not self.db or not assessment_id:
             return None
 
         policy_decision = PolicyDecision(
             assessment_id=assessment_id,
             action=action,
             target=target,
             execution_level=level,
             decision=decision,
             reason=reason,
             conditions=conditions,
         )
         self.db.add(policy_decision)
         await self.db.flush()
         return policy_decision
 
     def reset_rate_limits(self) -> None:
         """Reset rate limit counters (call periodically)."""
         self._action_counts.clear()
 
 
 # Global policy engine instance
 policy_engine = PolicyEngine()
