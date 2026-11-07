 import enum
 from datetime import datetime
 from typing import Optional
 from uuid import UUID, uuid4
 
 from sqlalchemy import (
     JSON,
     DateTime,
     Enum,
     ForeignKey,
     Index,
     String,
     Text,
     UniqueConstraint,
     func,
 )
 from sqlalchemy.dialects.postgresql import INET, UUID as PG_UUID
 from sqlalchemy.orm import Mapped, mapped_column, relationship
 
 from app.db.session import Base
 
 
 class ExecutionLevel(str, enum.Enum):
     L1_PASSIVE = "L1_PASSIVE"
     L2_CONTROLLED = "L2_CONTROLLED"
     L3_INTRUSIVE = "L3_INTRUSIVE"
 
 
 class AssessmentStatus(str, enum.Enum):
     DRAFT = "DRAFT"
     RUNNING = "RUNNING"
     PAUSED = "PAUSED"
     COMPLETED = "COMPLETED"
     FAILED = "FAILED"
     CANCELLED = "CANCELLED"
 
 
 class AssetType(str, enum.Enum):
     HOST = "HOST"
     IP_ADDRESS = "IP_ADDRESS"
     DOMAIN = "DOMAIN"
     WEB_APP = "WEB_APP"
     API = "API"
     SERVICE = "SERVICE"
     TECHNOLOGY = "TECHNOLOGY"
     NETWORK = "NETWORK"
 
 
 class FindingStatus(str, enum.Enum):
     DISCOVERED = "DISCOVERED"
     SUSPECTED = "SUSPECTED"
     SCANNER_REPORTED = "SCANNER_REPORTED"
     VALIDATED = "VALIDATED"
     FALSE_POSITIVE = "FALSE_POSITIVE"
     DEMONSTRATED = "DEMONSTRATED"
 
 
 class Severity(str, enum.Enum):
     CRITICAL = "CRITICAL"
     HIGH = "HIGH"
     MEDIUM = "MEDIUM"
     LOW = "LOW"
     INFO = "INFO"
 
 
 class PolicyDecision(str, enum.Enum):
     ALLOWED = "ALLOWED"
     REJECTED = "REJECTED"
     REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
 
 
 class JobStatus(str, enum.Enum):
     PENDING = "PENDING"
     RUNNING = "RUNNING"
     COMPLETED = "COMPLETED"
     FAILED = "FAILED"
     CANCELLED = "CANCELLED"
 
 
 class ReportFormat(str, enum.Enum):
     PDF = "PDF"
     HTML = "HTML"
     JSON = "JSON"
 
 
 class User(Base):
     __tablename__ = "users"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
     email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
     hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
     full_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
     is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
     last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
 
     assessments = relationship("Assessment", back_populates="owner")
     api_keys = relationship("APIKey", back_populates="owner")
 
 
 class APIKey(Base):
     __tablename__ = "api_keys"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     name: Mapped[str] = mapped_column(String(128), nullable=False)
     key_hash: Mapped[str] = mapped_column(String(255), nullable=False)
     key_prefix: Mapped[str] = mapped_column(String(16), nullable=False)
     owner_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
     scopes: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
     expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
 
     owner = relationship("User", back_populates="api_keys")
 
 
 class Assessment(Base):
     __tablename__ = "assessments"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     name: Mapped[str] = mapped_column(String(255), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     status: Mapped[AssessmentStatus] = mapped_column(Enum(AssessmentStatus), default=AssessmentStatus.DRAFT, nullable=False)
     owner_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
     scope_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("scopes.id", ondelete="SET NULL"), nullable=True)
     policy_level: Mapped[ExecutionLevel] = mapped_column(Enum(ExecutionLevel), default=ExecutionLevel.L2_CONTROLLED, nullable=False)
     started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     owner = relationship("User", back_populates="assessments")
     scope = relationship("Scope", back_populates="assessments")
     assets = relationship("Asset", back_populates="assessment")
     findings = relationship("Finding", back_populates="assessment")
     jobs = relationship("ExecutionJob", back_populates="assessment")
     ai_proposals = relationship("AIProposal", back_populates="assessment")
     reports = relationship("Report", back_populates="assessment")
     audit_events = relationship("AuditEvent", back_populates="assessment")
 
     __table_args__ = (
         Index("ix_assessments_owner_status", "owner_id", "status"),
         Index("ix_assessments_created_at", "created_at"),
     )
 
 
 class Scope(Base):
     __tablename__ = "scopes"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     name: Mapped[str] = mapped_column(String(255), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     targets: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     excluded_targets: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     allowed_ports: Mapped[Optional[list[int]]] = mapped_column(JSON, default=list, nullable=True)
     allowed_protocols: Mapped[Optional[list[str]]] = mapped_column(JSON, default=list, nullable=True)
     max_rate_limit: Mapped[Optional[int]] = mapped_column(nullable=True)
     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     assessments = relationship("Assessment", back_populates="scope")
 
     __table_args__ = (
         Index("ix_scopes_is_active", "is_active"),
     )
 
 
 class Asset(Base):
     __tablename__ = "assets"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     type: Mapped[AssetType] = mapped_column(Enum(AssetType), nullable=False)
     identifier: Mapped[str] = mapped_column(String(512), nullable=False)
     display_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
     metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
     discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
     confidence: Mapped[float] = mapped_column(default=1.0, nullable=False)
     source: Mapped[str] = mapped_column(String(128), nullable=False)
 
     assessment = relationship("Assessment", back_populates="assets")
     services = relationship("Service", back_populates="asset")
     findings = relationship("Finding", back_populates="asset")
     graph_nodes = relationship("GraphNode", back_populates="asset")
 
     __table_args__ = (
         UniqueConstraint("assessment_id", "type", "identifier", name="uq_asset_assessment_type_identifier"),
         Index("ix_assets_assessment_type", "assessment_id", "type"),
         Index("ix_assets_identifier", "identifier"),
     )
 
 
 class Service(Base):
     __tablename__ = "services"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     asset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
     port: Mapped[int] = mapped_column(nullable=False)
     protocol: Mapped[str] = mapped_column(String(16), nullable=False)
     name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     version: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     banner: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     technology: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
     cpe: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
     state: Mapped[str] = mapped_column(String(32), default="open", nullable=False)
     discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
     source: Mapped[str] = mapped_column(String(128), nullable=False)
     metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
 
     asset = relationship("Asset", back_populates="services")
     vulnerabilities = relationship("Vulnerability", back_populates="service")
 
     __table_args__ = (
         UniqueConstraint("asset_id", "port", "protocol", name="uq_service_asset_port_protocol"),
         Index("ix_services_asset_port", "asset_id", "port"),
         Index("ix_services_technology", "technology"),
     )
 
 
 class Vulnerability(Base):
     __tablename__ = "vulnerabilities"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     cve_id: Mapped[Optional[str]] = mapped_column(String(32), index=True, nullable=True)
     title: Mapped[str] = mapped_column(String(512), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     cvss_score: Mapped[Optional[float]] = mapped_column(nullable=True)
     cvss_vector: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     cvss_version: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
     epss_score: Mapped[Optional[float]] = mapped_column(nullable=True)
     epss_percentile: Mapped[Optional[float]] = mapped_column(nullable=True)
     cisa_kev: Mapped[bool] = mapped_column(default=False, nullable=False)
     cisa_kev_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     mitre_techniques: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     affected_software: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
     references: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     source: Mapped[str] = mapped_column(String(64), nullable=False)
     source_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
     published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
     fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     service_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("services.id", ondelete="SET NULL"), nullable=True)
     service = relationship("Service", back_populates="vulnerabilities")
     findings = relationship("Finding", back_populates="vulnerability")
 
     __table_args__ = (
         Index("ix_vulnerabilities_cve_id", "cve_id"),
         Index("ix_vulnerabilities_cvss_score", "cvss_score"),
         Index("ix_vulnerabilities_epss_score", "epss_score"),
         Index("ix_vulnerabilities_cisa_kev", "cisa_kev"),
     )
 
 
 class Finding(Base):
     __tablename__ = "findings"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     asset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
     vulnerability_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("vulnerabilities.id", ondelete="SET NULL"), nullable=True)
     title: Mapped[str] = mapped_column(String(512), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=False)
     status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.DISCOVERED, nullable=False)
     cvss_score: Mapped[Optional[float]] = mapped_column(nullable=True)
     cvss_vector: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     risk_score: Mapped[Optional[float]] = mapped_column(nullable=True)
     evidence_ids: Mapped[list[UUID]] = mapped_column(JSON, default=list, nullable=False)
     remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     references: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     validated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     validated_by: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     assessment = relationship("Assessment", back_populates="findings")
     asset = relationship("Asset", back_populates="findings")
     vulnerability = relationship("Vulnerability", back_populates="findings")
     evidence = relationship("Evidence", back_populates="finding")
 
     __table_args__ = (
         Index("ix_findings_assessment_status", "assessment_id", "status"),
         Index("ix_findings_severity", "severity"),
         Index("ix_findings_vulnerability", "vulnerability_id"),
     )
 
 
 class Evidence(Base):
     __tablename__ = "evidence"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     finding_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("findings.id", ondelete="CASCADE"), nullable=True)
     job_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("execution_jobs.id", ondelete="SET NULL"), nullable=True)
     type: Mapped[str] = mapped_column(String(64), nullable=False)
     title: Mapped[str] = mapped_column(String(255), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     content: Mapped[Optional[bytes]] = mapped_column(nullable=True)
     content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
     content_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
     size_bytes: Mapped[int] = mapped_column(default=0, nullable=False)
     redacted: Mapped[bool] = mapped_column(default=False, nullable=False)
     metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
     collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     finding = relationship("Finding", back_populates="evidence")
     job = relationship("ExecutionJob", back_populates="evidence")
 
     __table_args__ = (
         Index("ix_evidence_finding", "finding_id"),
         Index("ix_evidence_job", "job_id"),
         Index("ix_evidence_content_hash", "content_hash"),
     )
 
 
 class ExecutionJob(Base):
     __tablename__ = "execution_jobs"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     name: Mapped[str] = mapped_column(String(255), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     tool: Mapped[str] = mapped_column(String(64), nullable=False)
     command: Mapped[str] = mapped_column(Text, nullable=False)
     args: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
     status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
     execution_level: Mapped[ExecutionLevel] = mapped_column(Enum(ExecutionLevel), nullable=False)
     policy_decision_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("policy_decisions.id", ondelete="SET NULL"), nullable=True)
     started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     duration_ms: Mapped[Optional[int]] = mapped_column(nullable=True)
     exit_code: Mapped[Optional[int]] = mapped_column(nullable=True)
     stdout: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     stderr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     assessment = relationship("Assessment", back_populates="jobs")
     policy_decision = relationship("PolicyDecision", back_populates="jobs")
     evidence = relationship("Evidence", back_populates="job")
 
     __table_args__ = (
         Index("ix_jobs_assessment_status", "assessment_id", "status"),
         Index("ix_jobs_tool", "tool"),
         Index("ix_jobs_policy_decision", "policy_decision_id"),
     )
 
 
 class PolicyDecision(Base):
     __tablename__ = "policy_decisions"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     action: Mapped[str] = mapped_column(String(128), nullable=False)
     target: Mapped[str] = mapped_column(String(512), nullable=False)
     execution_level: Mapped[ExecutionLevel] = mapped_column(Enum(ExecutionLevel), nullable=False)
     decision: Mapped[PolicyDecision] = mapped_column(Enum(PolicyDecision), nullable=False)
     reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     conditions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     approved_by: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
     approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     jobs = relationship("ExecutionJob", back_populates="policy_decision")
 
     __table_args__ = (
         Index("ix_policy_decisions_assessment", "assessment_id"),
         Index("ix_policy_decisions_decision", "decision"),
     )
 
 
 class AIProposal(Base):
     __tablename__ = "ai_proposals"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     action: Mapped[str] = mapped_column(String(128), nullable=False)
     target: Mapped[str] = mapped_column(String(512), nullable=False)
     reason: Mapped[str] = mapped_column(Text, nullable=False)
     required_evidence: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
     risk_level: Mapped[str] = mapped_column(String(32), nullable=False)
     confidence: Mapped[float] = mapped_column(default=0.0, nullable=False)
     raw_response: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
     policy_decision_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("policy_decisions.id", ondelete="SET NULL"), nullable=True)
     status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
     executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     assessment = relationship("Assessment", back_populates="ai_proposals")
     policy_decision = relationship("PolicyDecision")
 
     __table_args__ = (
         Index("ix_ai_proposals_assessment", "assessment_id"),
         Index("ix_ai_proposals_status", "status"),
     )
 
 
 class GraphNode(Base):
     __tablename__ = "graph_nodes"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     asset_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
     node_type: Mapped[str] = mapped_column(String(64), nullable=False)
     label: Mapped[str] = mapped_column(String(255), nullable=False)
     data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
     x: Mapped[Optional[float]] = mapped_column(nullable=True)
     y: Mapped[Optional[float]] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     asset = relationship("Asset", back_populates="graph_nodes")
     edges_from = relationship("GraphEdge", foreign_keys="GraphEdge.source_id", back_populates="source")
     edges_to = relationship("GraphEdge", foreign_keys="GraphEdge.target_id", back_populates="target")
 
     __table_args__ = (
         Index("ix_graph_nodes_assessment", "assessment_id"),
         Index("ix_graph_nodes_type", "node_type"),
     )
 
 
 class GraphEdge(Base):
     __tablename__ = "graph_edges"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     source_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("graph_nodes.id", ondelete="CASCADE"), nullable=False)
     target_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("graph_nodes.id", ondelete="CASCADE"), nullable=False)
     edge_type: Mapped[str] = mapped_column(String(64), nullable=False)
     label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
     weight: Mapped[float] = mapped_column(default=1.0, nullable=False)
     evidence_ids: Mapped[list[UUID]] = mapped_column(JSON, default=list, nullable=False)
     data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     source = relationship("GraphNode", foreign_keys=[source_id], back_populates="edges_from")
     target = relationship("GraphNode", foreign_keys=[target_id], back_populates="edges_to")
 
     __table_args__ = (
         Index("ix_graph_edges_assessment", "assessment_id"),
         Index("ix_graph_edges_source_target", "source_id", "target_id"),
     )
 
 
 class AttackPath(Base):
     __tablename__ = "attack_paths"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     name: Mapped[str] = mapped_column(String(255), nullable=False)
     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
     node_ids: Mapped[list[UUID]] = mapped_column(JSON, default=list, nullable=False)
     edge_ids: Mapped[list[UUID]] = mapped_column(JSON, default=list, nullable=False)
     risk_score: Mapped[float] = mapped_column(default=0.0, nullable=False)
     max_severity: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.INFO, nullable=False)
     is_validated: Mapped[bool] = mapped_column(default=False, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
     __table_args__ = (
         Index("ix_attack_paths_assessment", "assessment_id"),
         Index("ix_attack_paths_risk_score", "risk_score"),
     )
 
 
 class Report(Base):
     __tablename__ = "reports"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
     name: Mapped[str] = mapped_column(String(255), nullable=False)
     format: Mapped[ReportFormat] = mapped_column(Enum(ReportFormat), nullable=False)
     content: Mapped[Optional[bytes]] = mapped_column(nullable=True)
     file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
     size_bytes: Mapped[int] = mapped_column(default=0, nullable=False)
     generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     generated_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
 
     assessment = relationship("Assessment", back_populates="reports")
 
     __table_args__ = (
         Index("ix_reports_assessment", "assessment_id"),
     )
 
 
 class AuditEvent(Base):
     __tablename__ = "audit_events"
 
     id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
     assessment_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True)
     user_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
     action: Mapped[str] = mapped_column(String(128), nullable=False)
     resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
     resource_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
     details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
     ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
     user_agent: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
     assessment = relationship("Assessment", back_populates="audit_events")
 
     __table_args__ = (
         Index("ix_audit_events_assessment", "assessment_id"),
         Index("ix_audit_events_user", "user_id"),
         Index("ix_audit_events_action", "action"),
         Index("ix_audit_events_created_at", "created_at"),
     )
