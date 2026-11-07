 import logging
 from contextlib import asynccontextmanager
 from uuid import UUID
 
 from fastapi import FastAPI, Request, status
 from fastapi.middleware.cors import CORSMiddleware
 from fastapi.responses import JSONResponse
 from pydantic import BaseModel
 
 from app.config import settings
 from app.db.session import init_db, close_db, AsyncSessionLocal
 from app.api.router import api_router
 from app.policy.engine import policy_engine
 
 
 # Configure structured logging
 logging.basicConfig(
     level=getattr(logging, settings.LOG_LEVEL),
     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
 )
 logger = logging.getLogger(__name__)
 
 
 class HealthResponse(BaseModel):
     status: str
     version: str
     service: str
 
 
 class ReadinessResponse(BaseModel):
     status: str
     checks: dict
 
 
 @asynccontextmanager
 async def lifespan(app: FastAPI):
     # Startup
     logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
     await init_db()
     logger.info("Database initialized")
     
     # Initialize policy engine with DB session
     async with AsyncSessionLocal() as db:
         policy_engine.db = db
     
     yield
     
     # Shutdown
     logger.info(f"Shutting down {settings.APP_NAME}")
     await close_db()
 
 
 app = FastAPI(
     title=settings.APP_NAME,
     version=settings.APP_VERSION,
     description="Risk-Aware Autonomous Vulnerability Exploration Network",
     docs_url="/docs" if settings.DEBUG else None,
     redoc_url="/redoc" if settings.DEBUG else None,
     lifespan=lifespan,
 )
 
 # CORS
 app.add_middleware(
     CORSMiddleware,
     allow_origins=settings.CORS_ORIGINS,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )
 
 
 @app.middleware("http")
 async def add_request_id(request: Request, call_next):
     """Add request ID to response headers for tracing."""
     request_id = request.headers.get("X-Request-ID", "unknown")
     response = await call_next(request)
     response.headers["X-Request-ID"] = request_id
     return response
 
 
 @app.exception_handler(Exception)
 async def global_exception_handler(request: Request, exc: Exception):
     logger.exception(f"Unhandled exception: {exc}")
     return JSONResponse(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
         content={"detail": "Internal server error", "type": "INTERNAL_ERROR"},
     )
 
 
 @app.get("/health", response_model=HealthResponse, tags=["Health"])
 async def health_check():
     """Basic health check - returns OK if service is running."""
     return HealthResponse(
         status="ok",
         version=settings.APP_VERSION,
         service=settings.APP_NAME,
     )
 
 
 @app.get("/ready", response_model=ReadinessResponse, tags=["Health"])
 async def readiness_check():
     """Readiness check - verifies all dependencies are available."""
     checks = {}
     overall_ready = True
 
     # Check database
     try:
         async with AsyncSessionLocal() as db:
             await db.execute("SELECT 1")
         checks["database"] = {"status": "ok", "detail": "Connected"}
     except Exception as e:
         checks["database"] = {"status": "fail", "detail": str(e)}
         overall_ready = False
 
     # Check Redis
     try:
         import redis.asyncio as redis
         r = redis.from_url(settings.REDIS_URL)
         await r.ping()
         await r.close()
         checks["redis"] = {"status": "ok", "detail": "Connected"}
     except Exception as e:
         checks["redis"] = {"status": "fail", "detail": str(e)}
         overall_ready = False
 
     # Check Ollama
     try:
         import httpx
         async with httpx.AsyncClient(timeout=5.0) as client:
             resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
             if resp.status_code == 200:
                 checks["ollama"] = {"status": "ok", "detail": "Available"}
             else:
                 checks["ollama"] = {"status": "degraded", "detail": f"HTTP {resp.status_code}"}
     except Exception as e:
         checks["ollama"] = {"status": "degraded", "detail": str(e)}
         # Ollama is optional - don't fail readiness
 
     # Check external tools
     import shutil
     checks["nmap"] = {"status": "ok" if shutil.which("nmap") else "fail", "detail": "Available" if shutil.which("nmap") else "Not found in PATH"}
     checks["httpx"] = {"status": "ok" if shutil.which("httpx") else "fail", "detail": "Available" if shutil.which("httpx") else "Not found in PATH"}
 
     return ReadinessResponse(
         status="ready" if overall_ready else "not_ready",
         checks=checks,
     )
 
 
 # Include API router
 app.include_router(api_router, prefix="/api")
 
 
 if __name__ == "__main__":
     import uvicorn
     uvicorn.run(
         "app.main:app",
         host=settings.API_HOST,
         port=settings.API_PORT,
         reload=settings.DEBUG,
     )
