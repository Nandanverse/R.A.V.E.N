 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import ExecutionJob, JobStatus, Assessment
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class ExecutionJobResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     name: str
     tool: str
     command: str
     status: JobStatus
     execution_level: str
     started_at: Optional[str]
     completed_at: Optional[str]
     duration_ms: Optional[int]
     exit_code: Optional[int]
     error: Optional[str]
     created_at: str
 
     class Config:
         from_attributes = True
 
 
 class JobCreate(BaseModel):
     assessment_id: UUID
     name: str
     tool: str
     command: str
     args: dict = Field(default_factory=dict)
     execution_level: str = "L2_CONTROLLED"
 
 
 @router.get("/jobs", response_model=PaginatedResponse[ExecutionJobResponse])
 async def list_jobs(
     assessment_id: Optional[UUID] = None,
     status: Optional[JobStatus] = None,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(ExecutionJob).order_by(ExecutionJob.created_at.desc())
     if assessment_id:
         query = query.where(ExecutionJob.assessment_id == assessment_id)
     if status:
         query = query.where(ExecutionJob.status == status)
 
     # Pagination would go here
     result = await db.execute(query.limit(page_size).offset((page - 1) * page_size))
     jobs = result.scalars().all()
 
     return PaginatedResponse(
         items=jobs,
         total=len(jobs),
         page=page,
         page_size=page_size,
         total_pages=1,
     )
 
 
 @router.post("/jobs", response_model=ExecutionJobResponse, status_code=status.HTTP_201_CREATED)
 async def create_job(
     job_in: JobCreate,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, job_in.assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     job = ExecutionJob(
         assessment_id=job_in.assessment_id,
         name=job_in.name,
         tool=job_in.tool,
         command=job_in.command,
         args=job_in.args,
         execution_level=job_in.execution_level,
         status=JobStatus.PENDING,
     )
     db.add(job)
     await db.commit()
     await db.refresh(job)
     return job
 
 
 @router.post("/jobs/{job_id}/execute")
 async def execute_job(
     job_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     job = await db.get(ExecutionJob, job_id)
     if not job:
         raise HTTPException(status_code=404, detail="Job not found")
 
     if job.status != JobStatus.PENDING:
         raise HTTPException(status_code=400, detail=f"Job is in {job.status} status")
 
     # TODO: Validate through policy engine, then execute
     job.status = JobStatus.RUNNING
     from datetime import datetime, timezone
     job.started_at = datetime.now(timezone.utc)
     await db.commit()
 
     # TODO: Actually execute the tool
     # For now, just mark as completed
     job.status = JobStatus.COMPLETED
     job.completed_at = datetime.now(timezone.utc)
     job.duration_ms = 0
     job.exit_code = 0
     job.stdout = "Mock execution (not implemented)"
     await db.commit()
 
     return {"message": "Job executed (mock)", "job_id": str(job_id)}
