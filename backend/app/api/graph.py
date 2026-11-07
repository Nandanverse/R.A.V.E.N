 from typing import Optional
 from uuid import UUID
 
 from fastapi import APIRouter, Depends, HTTPException, Query
 from pydantic import BaseModel, Field
 from sqlalchemy import select, func
 from sqlalchemy.ext.asyncio import AsyncSession
 
 from app.db.session import get_db
 from app.db.models import GraphNode, GraphEdge, AttackPath
 from app.api.schemas import PaginatedResponse
 
 router = APIRouter()
 
 
 class GraphNodeResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     asset_id: Optional[UUID]
     node_type: str
     label: str
     data: dict
     x: Optional[float]
     y: Optional[float]
     created_at: str
     updated_at: str
 
     class Config:
         from_attributes = True
 
 
 class GraphEdgeResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     source_id: UUID
     target_id: UUID
     edge_type: str
     label: Optional[str]
     weight: float
     evidence_ids: list[UUID]
     data: dict
     created_at: str
 
     class Config:
         from_attributes = True
 
 
 class AttackPathResponse(BaseModel):
     id: UUID
     assessment_id: UUID
     name: str
     description: Optional[str]
     node_ids: list[UUID]
     edge_ids: list[UUID]
     risk_score: float
     max_severity: str
     is_validated: bool
     created_at: str
     updated_at: str
 
     class Config:
         from_attributes = True
 
 
 class GraphDataResponse(BaseModel):
     nodes: list[GraphNodeResponse]
     edges: list[GraphEdgeResponse]
 
 
 @router.get("/assessments/{assessment_id}/graph", response_model=GraphDataResponse)
 async def get_attack_graph(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     nodes_result = await db.execute(
         select(GraphNode).where(GraphNode.assessment_id == assessment_id)
     )
     nodes = nodes_result.scalars().all()
 
     edges_result = await db.execute(
         select(GraphEdge).where(GraphEdge.assessment_id == assessment_id)
     )
     edges = edges_result.scalars().all()
 
     return GraphDataResponse(nodes=nodes, edges=edges)
 
 
 @router.get("/assessments/{assessment_id}/nodes", response_model=PaginatedResponse[GraphNodeResponse])
 async def list_nodes(
     assessment_id: UUID,
     node_type: Optional[str] = None,
     page: int = 1,
     page_size: int = 100,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(GraphNode).where(GraphNode.assessment_id == assessment_id)
     if node_type:
         query = query.where(GraphNode.node_type == node_type)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     nodes = result.scalars().all()
 
     return PaginatedResponse(
         items=nodes,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/assessments/{assessment_id}/edges", response_model=PaginatedResponse[GraphEdgeResponse])
 async def list_edges(
     assessment_id: UUID,
     page: int = 1,
     page_size: int = 100,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(GraphEdge).where(GraphEdge.assessment_id == assessment_id)
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     edges = result.scalars().all()
 
     return PaginatedResponse(
         items=edges,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.get("/assessments/{assessment_id}/paths", response_model=PaginatedResponse[AttackPathResponse])
 async def list_attack_paths(
     assessment_id: UUID,
     page: int = 1,
     page_size: int = 50,
     db: AsyncSession = Depends(get_db),
 ):
     query = select(AttackPath).where(AttackPath.assessment_id == assessment_id).order_by(AttackPath.risk_score.desc())
 
     count_query = select(func.count()).select_from(query.subquery())
     total = (await db.execute(count_query)).scalar() or 0
 
     offset = (page - 1) * page_size
     query = query.offset(offset).limit(page_size)
     result = await db.execute(query)
     paths = result.scalars().all()
 
     return PaginatedResponse(
         items=paths,
         total=total,
         page=page,
         page_size=page_size,
         total_pages=(total + page_size - 1) // page_size,
     )
 
 
 @router.post("/assessments/{assessment_id}/paths/find")
 async def find_attack_paths(
     assessment_id: UUID,
     db: AsyncSession = Depends(get_db),
 ):
     # TODO: Implement attack path finding algorithm
     return {"message": "Attack path finding not yet implemented", "paths": []}
