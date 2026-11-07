 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Vulnerability
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class VulnerabilityResponse(BaseModel):
     id: UUID
     cve_id: Optional[str]
     title: str
     description: Optional[str]
     cvss_score: Optional[float]
     cvss_vector: Optional[str]
     epss_score: Optional[float]
     cisa_kev: bool
     mitre_techniques: list[str]
     source: str
     published_at: Optional[str]
     fetched_at: str
 
     class Config:
         from_attributes = True
 
 
 @router.get("/vulnerabilities", response_model=PaginatedResponse[VulnerabilityResponse])
 async def list_vulnerabilities(
     cve_id: Optional[str] = None,
     min_cvss: Optional[float] = None,
     max_cvss: Optional[float] = None,
     cisa_kev: Optional[bool] = None,
     page: int = Query(1, ge=1),
     page_size: int = Query(50, ge=1, le=200),
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Vulnerability).order_by(Vulnerability.fetched_at.desc())
     if cve_id:
         query = query.where(Vulnerability.cve_id == cve_id.upper())
     if min_cvss is not None:
         query = query.where(Vulnerability.cvss_score >= min_cvss)
     if max_cvss is not None:
         query = query.where(Vulnerability.cvss_score <= max_cvss)
     if cisa_kev is not None:
         query = query.where(Vulnerability.cisa_kev == cisa_kev)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     vulns = result.scalars().all()
 
     return PaginatedResponse(
         items=vulns,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/vulnerabilities/{vuln_id}", response_model=VulnerabilityResponse)
 async def get_vulnerability(
     vuln_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     vuln = await db.get(Vulnerability, vuln_id)
     if not vuln:
         raise HTTPException(status_code=404, detail="Vulnerability not found")
     return vuln
 
 
 @router.get("/vulnerabilities/cve/{cve_id}", response_model=VulnerabilityResponse)
 async def get_vulnerability_by_cve(
     cve_id: str,
     db: AsyncSession = Depends(get_db),
 ):
     result = await db.execute(select(Vulnerability).where(Vulnerability.cve_id == cve_id.upper()))
     vuln = result.scalar_one_or_none()
     if not vuln:
         raise HTTPException(status_code=404, detail="Vulnerability not found")
     return vuln
 
 
 class RefreshRequest(BaseModel):
     sources: Optional[list[str]] = None
 
 
 @router.post("/refresh", status_code=status.HTTP_202_ACCEPTED)
 async def refresh_intelligence(
     request: RefreshRequest,
 ):
     # TODO: Queue intelligence refresh job
     return {"message": "Intelligence refresh queued (not implemented yet)"}
