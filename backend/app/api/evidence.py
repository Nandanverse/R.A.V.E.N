 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Evidence
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class EvidenceResponse(BaseModel):
     id: UUID
     finding_id: Optional[UUID]
     job_id: Optional[UUID]
     type: str
     title: str
     description: Optional[str]
     content_type: Optional[str]
     size_bytes: int
     content_hash: str
     redacted: bool
     metadata: dict
     collected_at: str
     created_at: str
 
     class Config:
         from_attributes = True
 
 
 class EvidenceCreate(BaseModel):
     finding_id: Optional[UUID] = None
     job_id: Optional[UUID] = None
     type: str
     title: str
     description: Optional[str] = None
     content: Optional[str] = None  # Base64 encoded
     content_type: Optional[str] = None
     metadata: dict = Field(default_factory=dict)
 
 
 @router.get("", response_model=PaginatedResponse[EvidenceResponse])
 async def list_evidence(
     finding_id: Optional[UUID] = None,
     job_id: Optional[UUID] = None,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Evidence).order_by(Evidence.collected_at.desc())
     if finding_id:
         query = query.where(Evidence.finding_id == finding_id)
     if job_id:
         query = query.where(Evidence.job_id == job_id)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     evidence = result.scalars().all()
 
     return PaginatedResponse(
         items=evidence,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.post("", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
 async def create_evidence(
     evidence_in: EvidenceCreate,
     db: AsyncSession = Depends(get_db),
 ):
     import hashlib
     import base64
 
     content_bytes = b""
     if evidence_in.content:
         content_bytes = base64.b64decode(evidence_in.content)
 
     content_hash = hashlib.sha256(content_bytes).hexdigest()
 
     evidence = Evidence(
         finding_id=evidence_in.finding_id,
         job_id=evidence_in.job_id,
         type=evidence_in.type,
         title=evidence_in.title,
         description=evidence_in.description,
         content=content_bytes,
         content_hash=content_hash,
         content_type=evidence_in.content_type,
         size_bytes=len(content_bytes),
         metadata=evidence_in.metadata,
     )
     db.add(evidence)
     await db.commit()
     await db.refresh(evidence)
     return evidence
 
 
 @router.get("/{evidence_id}", response_model=EvidenceResponse)
 async def get_evidence(
     evidence_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     evidence = await db.get(Evidence, evidence_id)
     if not evidence:
         raise HTTPException(status_code=404, detail="Evidence not found")
     return evidence
 
 
 @router.get("/{evidence_id}/content")
 async def get_evidence_content(
     evidence_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     evidence = await db.get(Evidence, evidence_id)
     if not evidence:
         raise HTTPException(status_code=404, detail="Evidence not found")
 
     if not evidence.content:
         return {"content": None}
 
     import base64
     return {"content": base64.b64encode(evidence.content).decode()}
