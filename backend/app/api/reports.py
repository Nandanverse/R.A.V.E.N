 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Report, ReportFormat, Assessment
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class ReportResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     name: str
     format: ReportFormat
     size_bytes: int
     file_path: Optional[str]
     generated_at: str
     generated_by: UUID
 
     class Config:
         from_attributes = True
 
 
 class ReportGenerateRequest(BaseModel):
     assessment_id: UUID
     name: str
     format: ReportFormat = ReportFormat.HTML
     template: Optional[str] = None
 
 
 @router.get("", response_model=PaginatedResponse[ReportResponse])
 async def list_reports(
     assessment_id: Optional[UUID] = None,
     page: int = 1,
     page_size: int = 20,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Report).order_by(Report.generated_at.desc())
     if assessment_id:
         query = query.where(Report.assessment_id == assessment_id)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     reports = result.scalars().all()
 
     return PaginatedResponse(
         items=reports,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
 async def generate_report(
     request: ReportGenerateRequest,
     db: AsyncSession = Depends(get_db),
 ):
     assessment = await db.get(Assessment, request.assessment_id)
     if not assessment:
         raise HTTPException(status_code=404, detail="Assessment not found")
 
     # TODO: Actually generate report (PDF/HTML/JSON)
     # For now, create a placeholder
     report = Report(
         assessment_id=request.assessment_id,
         name=request.name,
         format=request.format,
         size_bytes=0,
         generated_by=UUID(int=0),  # TODO: Get from auth
     )
     db.add(report)
     await db.commit()
     await db.refresh(report)
     return report
 
 
 @router.get("/{report_id}", response_model=ReportResponse)
 async def get_report(
     report_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     report = await db.get(Report, report_id)
     if not report:
         raise HTTPException(status_code=404, detail="Report not found")
     return report
 
 
 @router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
 async def delete_report(
     report_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     report = await db.get(Report, report_id)
     if not report:
         raise HTTPException(status_code=404, detail="Report not found")
 
     await db.delete(report)
     await db.commit()
