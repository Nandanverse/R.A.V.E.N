 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Assessment, AssessmentStatus, User, Scope
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class AssessmentCreate(BaseModel):
     name: str = Field(..., min_length=1, max_length=255)
     description: Optional[str] = None
     scope_id: Optional[UUID] = None
     policy_level: str = "L2_CONTROLLED"
 
 
 class AssessmentUpdate(BaseModel):
     name: Optional[str] = Field(None, min_length=1, max_length=255)
     description: Optional[str] = None
     status: Optional[AssessmentStatus] = None
     policy_level: Optional[str] = None
 
 
 class AssessmentResponse(BaseModel):
     id: UUID
     name: str
     description: Optional[str]
     status: AssessmentStatus
     scope_id: Optional[UUID]
     policy_level: str
     owner_id: UUID
     started_at: Optional[str]
     completed_at: Optional[str]
     created_at: str
     updated_at: str
 
     class Config:
         from_attributes = True
 
 
 @router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
 async def create_assessment(
     assessment_in: AssessmentCreate,
     db: AsyncSession = Depends(get_db),
 ):
     # TODO: Get current user from auth
     # For now, create a placeholder owner
     owner_result = await db.execute(select(User).limit(1))
     owner = owner_result.scalar_one_or_none()
     if not owner:
         raise HTTPException(status_code=400, detail="No users exist. Create a user first.")
 
     # Validate scope if provided
     if assessment_in.scope_id:
         scope = await db.get(Scope, assessment_in.scope_id)
         if not scope:
             raise HTTPException(status_code=400, detail="Scope not found")
         if not scope.is_active:
             raise HTTPException(status_code=400, detail="Scope is not active")
 
     assessment = Assessment(
         name=assessment_in.name,
         description=assessment_in.description,
         scope_id=assessment_in.scope_id,
         policy_level=assessment_in.policy_level,
         owner_id=owner.id,
         status=AssessmentStatus.DRAFT,
     )
     db.add(assessment)
     await db.commit()
     await db.refresh(assessment)
     return assessment
 
 
 @router.get("", response_model=PaginatedResponse[AssessmentResponse])
 async def list_assessments(
     page: int = Query(1, ge=1),
     page_size: int = Query(20, ge=1, le=100),
     status: Optional[AssessmentStatus] = None,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Assessment).order_by(Assessment.created_at.desc())
     if status:
         query = query.where(Assessment.status == status)
 
     # Count total
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     # Paginate
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     assessments = result.scalars().all()
 
     return PaginatedResponse(
         items=assessments,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/{assessment_id}", response_model=AssessmentResponse)
 async def get_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
     return assessment
 
 
 @router.patch("/{assessment_id}", response_model=AssessmentResponse)
 async def update_assessment(
     assessment_id: UUID,
     assessment_in: AssessmentUpdate,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     update_data = assessment_in.model_dump(exclude_unset=True)
     for field, value in update_data.items():
         setattr(assessment, field, value)
 
     await db.commit()
     await db.refresh(assessment)
     return assessment
 
 
 @router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
 async def delete_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     await db.delete(assessment)
     await db.commit()
 
 
 @router.post("/{assessment_id}/start", response_model=AssessmentResponse)
 async def start_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status != AssessmentStatus.DRAFT:
         raise HTTPException(status_code=400, detail=f"Cannot start assessment in {assessment.status} status")
 
     if not assessment.scope_id:
         raise HTTPException(status_code=400, detail="Assessment must have a scope defined")
 
     assessment.status = AssessmentStatus.RUNNING
     from datetime import datetime, timezone
     assessment.started_at = datetime.now(timezone.utc)
 
     await db.commit()
     await db.refresh(assessment)
     return assessment
 
 
 @router.post("/{assessment_id}/pause", response_model=AssessmentResponse)
 async def pause_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status != AssessmentStatus.RUNNING:
         raise HTTPException(status_code=400, detail=f"Cannot pause assessment in {assessment.status} status")
 
     assessment.status = AssessmentStatus.PAUSED
     await db.commit()
     await db.refresh(assessment)
     return assessment
 
 
 @router.post("/{assessment_id}/resume", response_model=AssessmentResponse)
 async def resume_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status != AssessmentStatus.PAUSED:
         raise HTTPException(status_code=400, detail=f"Cannot resume assessment in {assessment.status} status")
 
     assessment.status = AssessmentStatus.RUNNING
     await db.commit()
     await db.refresh(assessment)
     return assessment
 
 
 @router.post("/{assessment_id}/cancel", response_model=AssessmentResponse)
 async def cancel_assessment(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status in [AssessmentStatus.COMPLETED, AssessmentStatus.CANCELLED, AssessmentStatus.FAILED]:
         raise HTTPException(status_code=400, detail=f"Cannot cancel assessment in {assessment.status} status")
 
     assessment.status = AssessmentStatus.CANCELLED
     from datetime import datetime, timezone
     assessment.completed_at = datetime.now(timezone.utc)
 
     await db.commit()
     await db.refresh(assessment)
     return assessment
