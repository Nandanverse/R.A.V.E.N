 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Assessment, AssessmentStatus
 
 router = APIRouter()
 
 
 class ScanRequest(BaseModel):
     assessment_id: UUID
     targets: list[str]
     scan_type: str = "tcp_connect"
     ports: str = "1-1000"
     timing_template: str = "T4"
 
 
 class ScanResponse(BaseModel):
     job_id: UUID
     status: str
     message: str
 
 
 @router.post("/scan", response_model=ScanResponse)
 async def start_scan(
     scan_in: ScanRequest,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, scan_in.assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     if assessment.status != AssessmentStatus.RUNNING:
         raise HTTPException(status_code=400, detail="Assessment must be running")
 
     # TODO: Create execution job and queue nmap scan
     return ScanResponse(
         job_id=UUID(int=0),
         status="queued",
         message="Scan queued (not implemented yet)",
     )
 
 
 class DiscoveryRequest(BaseModel):
     assessment_id: UUID
     target: str
     methods: list[str] = ["dns", "http", "certificates"]
 
 
 @router.post("/discover", response_model=ScanResponse)
 async def start_discovery(
     discovery_in: DiscoveryRequest,
     db: AsyncSession = Depends(get_db),
 ):
     # TODO: Implement discovery
     return ScanResponse(
         job_id=UUID(int=0),
         status="queued",
         message="Discovery queued (not implemented yet)",
     )
