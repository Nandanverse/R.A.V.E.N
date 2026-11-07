 from fastapi import APIRouter
 from pydantic import BaseModel
 
 router = APIRouter()
 
 
 class HealthResponse(BaseModel):
     status: str
     service: str
     version: str
 
 
 @router.get("", response_model=HealthResponse)
 async def health():
     return HealthResponse(status="ok", service="RAVEN", version="0.1.0")
 
 
 @router.get("/live")
 async def liveness():
     return {"status": "alive"}
