 from functools import lru_cache
 from typing import Optional
 from pydantic import Field
 from pydantic_settings import BaseSettings, SettingsConfigDict
 
 
 class Settings(BaseSettings):
     model_config = SettingsConfigDict(
         env_file=".env",
         env_file_encoding="utf-8",
         case_sensitive=False,
         extra="ignore",
     )
 
     # Application
     APP_NAME: str = "RAVEN"
     APP_VERSION: str = "0.1.0"
     DEBUG: bool = False
     LOG_LEVEL: str = "INFO"
     API_HOST: str = "0.0.0.0"
     API_PORT: int = 8000
 
     # Database
     DATABASE_URL: str = "postgresql+asyncpg://raven:raven@localhost:5432/raven"
     DATABASE_POOL_SIZE: int = 10
     DATABASE_MAX_OVERFLOW: int = 20
 
     # Redis
     REDIS_URL: str = "redis://localhost:6379/0"
     REDIS_MAX_CONNECTIONS: int = 50
 
     # Security
     SECRET_KEY: str = Field(default="change-me-in-production-min-32-chars", min_length=32)
     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
     REFRESH_TOKEN_EXPIRE_DAYS: int = 7
     ALGORITHM: str = "HS256"
     BCRYPT_ROUNDS: int = 12
 
     # CORS
     CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
 
     # Ollama
     OLLAMA_BASE_URL: str = "http://localhost:11434"
     OLLAMA_MODEL: str = "llama3.1:8b"
     OLLAMA_TIMEOUT: int = 120
     OLLAMA_TEMPERATURE: float = 0.1
     OLLAMA_NUM_CTX: int = 4096
     OLLAMA_NUM_GPU: int = -1
 
     # External Tools
     NMAP_PATH: str = "nmap"
     ZAP_API_URL: str = "http://localhost:8080"
     ZAP_API_KEY: Optional[str] = None
     HTTPX_TIMEOUT: int = 30
 
     # Vulnerability Intelligence
     NVD_API_KEY: Optional[str] = None
     EPSS_API_URL: str = "https://api.first.org/data/v1/epss"
     CISA_KEV_URL: str = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
     MITRE_ATTACK_URL: str = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
     INTEL_CACHE_TTL_HOURS: int = 24
     INTEL_REFRESH_INTERVAL_HOURS: int = 6
 
     # Celery
     CELERY_BROKER_URL: str = "redis://localhost:6379/0"
     CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
     CELERY_TASK_TRACK_STARTED: bool = True
     CELERY_TASK_TIME_LIMIT: int = 3600
     CELERY_WORKER_CONCURRENCY: int = 4
     CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
 
     # Policy Engine
     DEFAULT_EXECUTION_LEVEL: str = "L2_CONTROLLED"
     MAX_CONCURRENT_ASSESSMENTS: int = 5
     ASSESSMENT_TIMEOUT_HOURS: int = 24
     RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
     RATE_LIMIT_BURST: int = 10
 
     # Evidence
     EVIDENCE_STORAGE_PATH: str = "./evidence"
     EVIDENCE_MAX_SIZE_MB: int = 100
     EVIDENCE_RETENTION_DAYS: int = 365
 
     # Reporting
     REPORT_OUTPUT_PATH: str = "./reports"
     REPORT_TEMPLATES_PATH: str = "./templates"
 
     # Health Checks
     HEALTH_CHECK_INTERVAL_SECONDS: int = 30
     READINESS_TIMEOUT_SECONDS: int = 10
 
 
 @lru_cache()
 def get_settings() -> Settings:
     return Settings()
 
 
 settings = get_settings()
