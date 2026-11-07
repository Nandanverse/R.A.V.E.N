 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Finding, Severity, Vulnerability
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class RiskSummary(BaseModel):
     assessment_id: UUID
     total_findings: int
     critical: int
     high: int
     medium: int
     low: int
     info: int
     validated_count: int
     avg_risk_score: Optional[float]
     max_risk_score: Optional[float]
     cisa_kev_findings: int
     epss_above_50: int
 
 
 @router.get("/assessments/{assessment_id}/summary", response_model=RiskSummary)
 async def get_risk_summary(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     # Get all findings for assessment
     result = await db.execute(
         select(Finding).where(Finding.assessment_id == assessment_id)
     )
     findings = result.scalars().all()
 
     total = len(findings)
     by_severity = {s: 0 for s in Severity}
     validated = 0
     risk_scores = []
     cisa_kev = 0
     epss_50 = 0
 
     for f in findings:
         by_severity[f.severity] += 1
         if f.status == "VALIDATED":
             validated += 1
         if f.risk_score is not None:
             risk_scores.append(f.risk_score)
         if f.vulnerability_id:
             vuln = await db.get(Vulnerability, f.vulnerability_id)
             if vuln and vuln.cisa_kev:
                 cisa_kev += 1
             if vuln and vuln.epss_score and vuln.epss_score > 0.5:
                 epss_50 += 1
 
     return RiskSummary(
         assessment_id=assessment_id,
         total_findings=total,
         critical=by_severity[Severity.CRITICAL],
         high=by_severity[Severity.HIGH],
         medium=by_severity[Severity.MEDIUM],
         low=by_severity[Severity.LOW],
         info=by_severity[Severity.INFO],
         validated_count=validated,
         avg_risk_score=sum(risk_scores) / len(risk_scores) if risk_scores else None,
         max_risk_score=max(risk_scores) if risk_scores else None,
         cisa_kev_findings=cisa_kev,
         epss_above_50=epss_50,
     )
 
 
 class FindingRiskDetail(BaseModel):
     finding_id: UUID
     title: str
     severity: Severity
     cvss_score: Optional[float]
     epss_score: Optional[float]
     cisa_kev: bool
     risk_score: Optional[float]
     risk_factors: list[str]
 
 
 @router.get("/assessments/{assessment_id}/findings", response_model=PaginatedResponse[FindingRiskDetail])
 async def list_findings_with_risk(
     assessment_id: UUID,
     min_risk: Optional[float] = None,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Finding).where(Finding.assessment_id == assessment_id)
     if min_risk is not None:
         query = query.where(Finding.risk_score >= min_risk)
     query = query.order_by(Finding.risk_score.desc().nullslast())
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     findings = result.scalars().all()
 
     items = []
     for f in findings:
         factors = []
         if f.cvss_score and f.cvss_score >= 7.0:
             factors.append(f"High CVSS: {f.cvss_score}")
         if f.vulnerability_id:
             vuln = await db.get(Vulnerability, f.vulnerability_id)
             if vuln:
                 if vuln.cisa_kev:
                     factors.append("CISA KEV")
                 if vuln.epss_score and vuln.epss_score > 0.5:
                     factors.append(f"High EPSS: {vuln.epss_score:.2f}")
         if f.status == "VALIDATED":
             factors.append("Validated")
 
         items.append(FindingRiskDetail(
             finding_id=f.id,
             title=f.title,
             severity=f.severity,
             cvss_score=f.cvss_score,
             epss_score=vuln.epss_score if f.vulnerability_id and (vuln := await db.get(Vulnerability, f.vulnerability_id)) else None,
             cisa_kev=vuln.cisa_kev if f.vulnerability_id and (vuln := await db.get(Vulnerability, f.vulnerability_id)) else False,
             risk_score=f.risk_score,
             risk_factors=factors,
         ))
 
     return PaginatedResponse(
         items=items,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
