 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import PolicyDecision, Assessment
 from app.policy.engine import policy_engine, ExecutionLevel, PolicyDecisionEnum
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class PolicyDecisionResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     action: str
     target: str
     execution_level: str
     decision: str
     reason: Optional[str]
     conditions: list[str]
     approved_by: Optional[UUID]
     approved_at: Optional[str]
     created_at: str
 
     class Config:
         from_attributes = True
 
 
 class EvaluateRequest(BaseModel):
     assessment_id: UUID
     action: str
     target: str
     execution_level: str = "L2_CONTROLLED"
     context: dict = Field(default_factory=dict)
 
 
 class EvaluateResponse(BaseModel):
     allowed: bool
     decision: str
     reason: str
     conditions: list[str]
     requires_approval: bool
     policy_decision_id: Optional[UUID]
 
 
 @router.post("/evaluate", response_model=EvaluateResponse)
 async def evaluate_action(
     request: EvaluateRequest,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, request.assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     try:
         level = ExecutionLevel(request.execution_level)
     except ValueError:
         raise HTTPException(status_code=400, detail="Invalid execution level")
 
     # Temporarily attach DB to policy engine
     policy_engine.db = db
     result = await policy_engine.evaluate(
         action=request.action,
         target=request.target,
         level=level,
         context=request.context,
         assessment_id=request.assessment_id,
     )
 
     return EvaluateResponse(
         allowed=result.allowed,
         decision=result.decision.value,
         reason=result.reason,
         conditions=result.conditions,
         requires_approval=result.requires_approval,
         policy_decision_id=result.policy_decision_id,
     )
 
 
 @router.get("/decisions", response_model=PaginatedResponse[PolicyDecisionResponse])
 async def list_decisions(
     assessment_id: Optional[UUID] = None,
     decision: Optional[PolicyDecisionEnum] = None,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(PolicyDecision).order_by(PolicyDecision.created_at.desc())
     if assessment_id:
         query = query.where(PolicyDecision.assessment_id == assessment_id)
     if decision:
         query = query.where(PolicyDecision.decision == decision)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     decisions = result.scalars().all()
 
     return PaginatedResponse(
         items=decisions,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/decisions/{decision_id}", response_model=PolicyDecisionResponse)
 async def get_decision(
     decision_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     decision = await db.get(PolicyDecision, decision_id)
     if not decision:
         raise HTTPException(status_code=404, detail="Policy decision not found")
     return decision
 
 
 @router.post("/emergency-stop/activate")
 async def activate_emergency_stop():
     policy_engine.activate_emergency_stop()
     return {"message": "Emergency stop activated"}
 
 
 @router.post("/emergency-stop/deactivate")
 async def deactivate_emergency_stop():
     policy_engine.deactivate_emergency_stop()
     return {"message": "Emergency stop deactivated"}
 
 
 @router.get("/emergency-stop/status")
 async def emergency_stop_status():
     return {"active": policy_engine.emergency_stop_active}
 
 
 @router.post("/emergency-stop/reset")
 async def reset_emergency_stop():
     policy_engine.deactivate_emergency_stop()
     policy_engine.reset_rate_limits()
     return {"message": "Emergency stop reset and rate limits cleared"}
