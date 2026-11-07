 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Asset, AssetType
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class AssetResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     type: AssetType
     identifier: str
     display_name: Optional[str]
     metadata: dict
     discovered_at: str
     updated_at: str
     confidence: float
     source: str
 
     class Config:
         from_attributes = True
 
 
 @router.get("", response_model=PaginatedResponse[AssetResponse])
 async def list_assets(
     assessment_id: Optional[UUID] = None,
     type: Optional[AssetType] = None,
     page: int = Query(1, ge=1),
     page_size: int = Query(50, ge=1, le=200),
     search: Optional[str] = None,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Asset).order_by(Asset.discovered_at.desc())
     if assessment_id:
         query = query.where(Asset.assessment_id == assessment_id)
     if type:
         query = query.where(Asset.type == type)
     if search:
         query = query.where(Asset.identifier.ilike(f"%{search}%"))
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     assets = result.scalars().all()
 
     return PaginatedResponse(
         items=assets,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/{asset_id}", response_model=AssetResponse)
 async def get_asset(
     asset_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     asset = await db.get(Asset, asset_id)
     if not asset:
         raise HTTPException(status_code=404, detail="Asset not found")
     return asset
