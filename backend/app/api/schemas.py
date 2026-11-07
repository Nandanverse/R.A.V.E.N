 from typing import Generic, TypeVar
 from pydantic import BaseModel, Field
 
 T = TypeVar("T")
 
 
 class PaginatedResponse(BaseModel, Generic[T]):
     items: list[T]
     total: int
     page: int = Field(..., ge=1)
     page_size: int = Field(..., ge=1, le=100)
     total_pages: int
 
 
 class ErrorResponse(BaseModel):
     detail: str
     type: str
     code: Optional[str] = None
 
 
 class SuccessResponse(BaseModel):
     message: str
     data: Optional[dict] = None
