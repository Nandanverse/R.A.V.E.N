 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Finding, FindingStatus, Severity
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class FindingResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     asset_id: UUID
     vulnerability_id: Optional[UUID]
     title: str
     description: Optional[str]
     severity: Severity
     status: FindingStatus
     cvss_score: Optional[float]
     risk_score: Optional[float]
     evidence_ids: list[UUID]
     remediation: Optional[str]
     tags: list[str]
     discovered_at: str
     validated_at: Optional[str]
     created_at: str
     updated_at: str
 
     class Config:
         from_attributes = True
 
 
 class FindingUpdate(BaseModel):
     status: Optional[FindingStatus] = None
     severity: Optional[Severity] = None
     risk_score: Optional[float] = None
     remediation: Optional[str] = None
     tags: Optional[list[str]] = None
 
 
 @router.get("", response_model=PaginatedResponse[FindingResponse])
 async def list_findings(
     assessment_id: Optional[UUID] = None,
     asset_id: Optional[UUID] = None,
     status: Optional[FindingStatus] = None,
     severity: Optional[Severity] = None,
     page: int = Query(1, ge=1),
     page_size: int = Query(50, ge=1, le=200),
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Finding).order_by(Finding.discovered_at.desc())
     if assessment_id:
         query = query.where(Finding.assessment_id == assessment_id)
     if asset_id:
         query = query.where(Finding.asset_id == asset_id)
     if status:
         query = query.where(Finding.status == status)
     if severity:
         query = query.where(Finding.severity == severity)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     findings = result.scalars().all()
 
     return PaginatedResponse(
         items=findings,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/{finding_id}", response_model=FindingResponse)
 async def get_finding(
     finding_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     finding = await db.get(Finding, finding_id)
     if not finding:
         raise HTTPException(status_code=404, detail="Finding not found")
     return finding
 
 
 @router.patch("/{finding_id}", response_model=FindingResponse)
 async def update_finding(
     finding_id: UUID,
     finding_in: FindingUpdate,
     db: AsyncSession = Depends(get_db),
 ):
     finding = await db.get(Finding, finding_id)
     if not finding:
         raise HTTPException(status_code=404, detail="Finding not found")
 
     update_data = finding_in.model_dump(exclude_unset=True)
     for field, value in update_data.items():
         setattr(finding, field, value)
 
     if finding_in.status == FindingStatus.VALIDATED:
         from datetime import datetime, timezone
         finding.validated_at = datetime.now(timezone.utc)
 
     await db.commit()
     await db.refresh(finding)
     return finding
