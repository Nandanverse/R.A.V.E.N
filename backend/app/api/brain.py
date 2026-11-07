 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import AIProposal, Assessment, AssessmentStatus
 from app.api.schemas import PaginatedResponse
 from app.policy.engine import policy_engine, ExecutionLevel
 
 router = APIRouter()
 
 
 class AIProposalResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     action: str
     target: str
     reason: str
     required_evidence: list[str]
     risk_level: str
     confidence: float
     status: str
     created_at: str
     executed_at: Optional[str]
 
     class Config:
         from_attributes = True
 
 
 class ProposalRequest(BaseModel):
     assessment_id: UUID
     context: dict = Field(default_factory=dict)
 
 
 @router.get("/proposals", response_model=PaginatedResponse[AIProposalResponse])
 async def list_proposals(
     assessment_id: Optional[UUID] = None,
     status: Optional[str] = None,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(AIProposal).order_by(AIProposal.created_at.desc())
     if assessment_id:
         query = query.where(AIProposal.assessment_id == assessment_id)
     if status:
         query = query.where(AIProposal.status == status)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     proposals = result.scalars().all()
 
     return PaginatedResponse(
         items=proposals,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.post("/propose", response_model=AIProposalResponse)
 async def generate_proposal(
     request: ProposalRequest,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, request.assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status != AssessmentStatus.RUNNING:
         raise HTTPException(status_code=400, detail="Assessment must be running")
 
     # TODO: Call Ollama/LLM to generate proposal
     # For now, return a mock proposal
     proposal = AIProposal(
         assessment_id=request.assessment_id,
         action="test_api_authorization",
         target="api.example.com",
         reason="Mock proposal - LLM integration not yet implemented",
         required_evidence=["HTTP response", "test account", "authorization result"],
         risk_level="medium",
         confidence=0.5,
         raw_response={"mock": True},
         status="pending",
     )
     db.add(proposal)
     await db.commit()
     await db.refresh(proposal)
     return proposal
 
 
 @router.post("/proposals/{proposal_id}/evaluate")
 async def evaluate_proposal(
     proposal_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     proposal = await db.get(AIProposal, proposal_id)
     if not proposal:
         raise HTTPException(status_code=404, detail="Proposal not found")
 
     # Evaluate through policy engine
     level = policy_engine.get_execution_level_for_action(proposal.action)
     result = await policy_engine.evaluate(
         action=proposal.action,
         target=proposal.target,
         level=level,
         context={"proposal_id": str(proposal_id)},
         assessment_id=proposal.assessment_id,
     )
 
     # Update proposal with policy decision
     proposal.policy_decision_id = result.policy_decision_id
     proposal.status = "approved" if result.allowed else "rejected"
     await db.commit()
 
     return {
         "allowed": result.allowed,
         "decision": result.decision.value,
         "reason": result.reason,
         "conditions": result.conditions,
         "requires_approval": result.requires_approval,
     }
 
 
 @router.get("/ollama/status")
 async def ollama_status():
     # TODO: Check Ollama availability
     return {
         "available": False,
         "model": "llama3.1:8b",
         "message": "Ollama integration not yet implemented",
     }
