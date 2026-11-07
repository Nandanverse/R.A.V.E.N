 from fastapi import APIRouter
 
 from app.api import (
     assessments,
     assets,
     findings,
     recon,
     intel,
     brain,
     executor,
     evidence,
     graph,
     risk,
     analytics,
     reports,
     scopes,
     policy,
     health,
 )
 
 api_router = APIRouter()
 
 # Include all sub-routers
 api_router.include_router(health.router, prefix="/health", tags=["Health"])
 api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
 api_router.include_router(scopes.router, prefix="/scopes", tags=["Scopes"])
 api_router.include_router(assets.router, prefix="/assets", tags=["Assets"])
 api_router.include_router(recon.router, prefix="/recon", tags=["Reconnaissance"])
 api_router.include_router(intel.router, prefix="/intel", tags=["Vulnerability Intelligence"])
 api_router.include_router(findings.router, prefix="/findings", tags=["Findings"])
 api_router.include_router(brain.router, prefix="/brain", tags=["AI Analysis"])
 api_router.include_router(executor.router, prefix="/executor", tags=["Test Execution"])
 api_router.include_router(evidence.router, prefix="/evidence", tags=["Evidence"])
 api_router.include_router(graph.router, prefix="/graph", tags=["Attack Graph"])
 api_router.include_router(risk.router, prefix="/risk", tags=["Risk Analysis"])
 api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
 api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
 api_router.include_router(policy.router, prefix="/policy", tags=["Policy Engine"])
