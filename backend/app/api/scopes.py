 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query, status
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import Scope
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class ScopeCreate(BaseModel):
     name: str = Field(..., min_length=1, max_length=255)
     description: Optional[str] = None
     targets: list[str] = Field(default_factory=list)
     excluded_targets: list[str] = Field(default_factory=list)
     allowed_ports: Optional[list[int]] = None
     allowed_protocols: Optional[list[str]] = None
     max_rate_limit: Optional[int] = None
 
 
 class ScopeUpdate(BaseModel):
     name: Optional[str] = Field(None, min_length=1, max_length=255)
     description: Optional[str] = None
     targets: Optional[list[str]] = None
     excluded_targets: Optional[list[str]] = None
     allowed_ports: Optional[list[int]] = None
     allowed_protocols: Optional[list[str]] = None
     max_rate_limit: Optional[int] = None
     is_active: Optional[bool] = None
 
 
 class ScopeResponse(BaseModel):
     id: UUID
     name: str
     description: Optional[str]
     targets: list[str]
     excluded_targets: list[str]
     allowed_ports: Optional[list[int]]
     allowed_protocols: Optional[list[str]]
     max_rate_limit: Optional[int]
     is_active: bool
     created_at: str
     updated_at: str
 
     class Config:
         from_attributes = True
 
 
 @router.post("", response_model=ScopeResponse, status_code=status.HTTP_201_CREATED)
 async def create_scope(
     scope_in: ScopeCreate,
     db: AsyncSession = Depends(get_db),
 ):
     scope = Scope(**scope_in.model_dump())
     db.add(scope)
     await db.commit()
     await db.refresh(scope)
     return scope
 
 
 @router.get("", response_model=PaginatedResponse[ScopeResponse])
 async def list_scopes(
     page: int = Query(1, ge=1),
     page_size: int = Query(20, ge=1, le=100),
     is_active: Optional[bool] = None,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(Scope).order_by(Scope.created_at.desc())
     if is_active is not None:
         query = query.where(Scope.is_active == is_active)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     scopes = result.scalars().all()
 
     return PaginatedResponse(
         items=scopes,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/{scope_id}", response_model=ScopeResponse)
 async def get_scope(
     scope_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     scope = await db.get(Scope, scope_id)
     if not scope:
         raise HTTPException(status_code=404, detail="Scope not found")
     return scope
 
 
 @router.patch("/{scope_id}", response_model=ScopeResponse)
 async def update_scope(
     scope_id: UUID,
     scope_in: ScopeUpdate,
     db: AsyncSession = Depends(get_db),
 ):
     scope = await db.get(Scope, scope_id)
     if not scope:
         raise HTTPException(status_code=404, detail="Scope not found")
 
     update_data = scope_in.model_dump(exclude_unset=True)
     for field, value in update_data.items():
         setattr(scope, field, value)
 
     await db.commit()
     await db.refresh(scope)
     return scope
 
 
 @router.delete("/{scope_id}", status_code=status.HTTP_204_NO_CONTENT)
 async def delete_scope(
     scope_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     scope = await db.get(Scope, scope_id)
     if not scope:
         raise HTTPException(status_code=404, detail="Scope not found")
 
     await db.delete(scope)
     await db.commit()
