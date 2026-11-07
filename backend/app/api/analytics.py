 from typing import Optional
 from uuid import UUID
 from datetime import datetime, timedelta
 
 from fastapi import APIRouter, Depends, Query
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func, and_
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import (
     Assessment, Asset, Finding, Evidence, ExecutionJob,
     AssessmentStatus, FindingStatus, Severity, JobStatus
 )
 
 router = APIRouter()
 
 
 class OverviewStats(BaseModel):
     total_assessments: int
     running_assessments: int
     completed_assessments: int
     total_assets: int
     total_findings: int
     validated_findings: int
     critical_findings: int
     high_findings: int
     total_evidence: int
     total_jobs: int
 
 
 @router.get("/overview", response_model=OverviewStats)
 async def get_overview(
     db: AsyncSession = Depends(get_db),
 ):
     total_assessments = (await db.execute(select(func.count(Assessment.id)))).scalar() or 0
     running_assessments = (await db.execute(
         select(func.count(Assessment.id)).where(Assessment.status == AssessmentStatus.RUNNING)
     )).scalar() or 0
     completed_assessments = (await db.execute(
         select(func.count(Assessment.id)).where(Assessment.status == AssessmentStatus.COMPLETED)
     )).scalar() or 0
 
     total_assets = (await db.execute(select(func.count(Asset.id)))).scalar() or 0
     total_findings = (await db.execute(select(func.count(Finding.id)))).scalar() or 0
     validated_findings = (await db.execute(
         select(func.count(Finding.id)).where(Finding.status == FindingStatus.VALIDATED)
     )).scalar() or 0
 
     critical_findings = (await db.execute(
         select(func.count(Finding.id)).where(Finding.severity == Severity.CRITICAL)
     )).scalar() or 0
     high_findings = (await db.execute(
         select(func.count(Finding.id)).where(Finding.severity == Severity.HIGH)
     )).scalar() or 0
 
     total_evidence = (await db.execute(select(func.count(Evidence.id)))).scalar() or 0
     total_jobs = (await db.execute(select(func.count(ExecutionJob.id)))).scalar() or 0
 
     return OverviewStats(
         total_assessments=total_assessments,
         running_assessments=running_assessments,
         completed_assessments=completed_assessments,
         total_assets=total_assets,
         total_findings=total_findings,
         validated_findings=validated_findings,
         critical_findings=critical_findings,
         high_findings=high_findings,
         total_evidence=total_evidence,
         total_jobs=total_jobs,
     )
 
 
 class FindingDistribution(BaseModel):
     severity: str
     count: int
     percentage: float
 
 
 @router.get("/findings/distribution")
 async def get_finding_distribution(
     assessment_id: Optional[UUID] = None,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Finding.severity, func.count(Finding.id)).group_by(Finding.severity)
     if assessment_id:
         query = query.where(Finding.assessment_id == assessment_id)
 
     result = await db.execute(query)
     rows = result.all()
 
     total = sum(r[1] for r in rows)
     return [
         FindingDistribution(
             severity=r[0].value if hasattr(r[0], 'value') else str(r[0]),
             count=r[1],
             percentage=round(r[1] / total * 100, 1) if total > 0 else 0
         )
         for r in rows
     ]
 
 
 class AssetTypeDistribution(BaseModel):
     type: str
     count: int
 
 
 @router.get("/assets/distribution")
 async def get_asset_distribution(
     assessment_id: Optional[UUID] = None,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Asset.type, func.count(Asset.id)).group_by(Asset.type)
     if assessment_id:
         query = query.where(Asset.assessment_id == assessment_id)
 
     result = await db.execute(query)
     return [
         AssetTypeDistribution(type=r[0].value if hasattr(r[0], 'value') else str(r[0]), count=r[1])
         for r in result.all()
     ]
 
 
 class JobStats(BaseModel):
     tool: str
     count: int
     success_rate: float
     avg_duration_ms: Optional[float]
 
 
 @router.get("/jobs/stats")
 async def get_job_stats(
     assessment_id: Optional[UUID] = None,
     days: int = 30,
     db: AsyncSession = Depends(get_db),
 ):
     since = datetime.utcnow() - timedelta(days=days)
     query = select(
         ExecutionJob.tool,
         func.count(ExecutionJob.id),
         func.avg(ExecutionJob.duration_ms),
         func.sum(func.case((ExecutionJob.status == JobStatus.COMPLETED, 1), else_=0))
     ).where(ExecutionJob.created_at >= since).group_by(ExecutionJob.tool)
 
     if assessment_id:
         query = query.where(ExecutionJob.assessment_id == assessment_id)
 
     result = await db.execute(query)
     return [
         JobStats(
             tool=r[0],
             count=r[1],
             success_rate=round(r[3] / r[1] * 100, 1) if r[1] > 0 else 0,
             avg_duration_ms=r[2],
         )
         for r in result.all()
     ]
 
 
 class TimelinePoint(BaseModel):
     date: str
     assessments: int
     findings: int
 
 
 @router.get("/timeline")
 async def get_timeline(
     days: int = 30,
     db: AsyncSession = Depends(get_db),
 ):
     since = datetime.utcnow() - timedelta(days=days)
     
     assessments_q = select(
         func.date(Assessment.created_at).label("date"),
         func.count(Assessment.id).label("count")
     ).where(Assessment.created_at >= since).group_by(func.date(Assessment.created_at))
     
     findings_q = select(
         func.date(Finding.discovered_at).label("date"),
         func.count(Finding.id).label("count")
     ).where(Finding.discovered_at >= since).group_by(func.date(Finding.discovered_at))
 
     assessments_r = await db.execute(assessments_q)
     findings_r = await db.execute(findings_q)
 
     assessment_map = {str(r[0]): r[1] for r in assessments_r.all()}
     findings_map = {str(r[0]): r[1] for r in findings_r.all()}
     
     all_dates = set(assessment_map.keys()) | set(findings_map.keys())
     
     return [
         TimelinePoint(
             date=d,
             assessments=assessment_map.get(d, 0),
             findings=findings_map.get(d, 0),
         )
         for d in sorted(all_dates)
     ]
