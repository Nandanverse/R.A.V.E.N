 """Initial migration
 
 Revision ID: 0001
 Revises: 
 Create Date: 2026-11-06
 
 """
 from typing import Sequence, Union
 
 from alembic import op
 import sqlalchemy as sa
 from sqlalchemy.dialects import postgresql
 
 # revision identifiers, used by Alembic.
 revision: str = "0001"
 down_revision: Union[str, None] = None
 branch_labels: Union[str, Sequence[str], None] = None
 depends_on: Union[str, Sequence[str], None] = None
 
 
 def upgrade() -> None:
     # Create enum types
     op.execute("CREATE TYPE executionlevel AS ENUM ('L1_PASSIVE', 'L2_CONTROLLED', 'L3_INTRUSIVE')")
     op.execute("CREATE TYPE assessmentstatus AS ENUM ('DRAFT', 'RUNNING', 'PAUSED', 'COMPLETED', 'FAILED', 'CANCELLED')")
     op.execute("CREATE TYPE assettype AS ENUM ('HOST', 'IP_ADDRESS', 'DOMAIN', 'WEB_APP', 'API', 'SERVICE', 'TECHNOLOGY', 'NETWORK')")
     op.execute("CREATE TYPE findingstatus AS ENUM ('DISCOVERED', 'SUSPECTED', 'SCANNER_REPORTED', 'VALIDATED', 'FALSE_POSITIVE', 'DEMONSTRATED')")
     op.execute("CREATE TYPE severity AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')")
     op.execute("CREATE TYPE policydecision AS ENUM ('ALLOWED', 'REJECTED', 'REQUIRES_APPROVAL')")
     op.execute("CREATE TYPE jobstatus AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED')")
     op.execute("CREATE TYPE reportformat AS ENUM ('PDF', 'HTML', 'JSON')")
 
     # users table
     op.create_table(
         "users",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("username", sa.String(64), unique=True, nullable=False, index=True),
         sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
         sa.Column("hashed_password", sa.String(255), nullable=False),
         sa.Column("full_name", sa.String(128), nullable=True),
         sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
         sa.Column("is_superuser", sa.Boolean(), default=False, nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
         sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
     )
 
     # api_keys table
     op.create_table(
         "api_keys",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("name", sa.String(128), nullable=False),
         sa.Column("key_hash", sa.String(255), nullable=False),
         sa.Column("key_prefix", sa.String(16), nullable=False),
         sa.Column("owner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
         sa.Column("scopes", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
         sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
     )
 
     # scopes table
     op.create_table(
         "scopes",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("name", sa.String(255), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("targets", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("excluded_targets", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("allowed_ports", postgresql.JSONB(), default=list, nullable=True),
         sa.Column("allowed_protocols", postgresql.JSONB(), default=list, nullable=True),
         sa.Column("max_rate_limit", sa.Integer(), nullable=True),
         sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_scopes_is_active", "scopes", ["is_active"])
 
     # assessments table
     op.create_table(
         "assessments",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("name", sa.String(255), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("status", sa.Enum("DRAFT", "RUNNING", "PAUSED", "COMPLETED", "FAILED", "CANCELLED", name="assessmentstatus"), default="DRAFT", nullable=False),
         sa.Column("owner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
         sa.Column("scope_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scopes.id", ondelete="SET NULL"), nullable=True),
         sa.Column("policy_level", sa.Enum("L1_PASSIVE", "L2_CONTROLLED", "L3_INTRUSIVE", name="executionlevel"), default="L2_CONTROLLED", nullable=False),
         sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_assessments_owner_status", "assessments", ["owner_id", "status"])
     op.create_index("ix_assessments_created_at", "assessments", ["created_at"])
 
     # assets table
     op.create_table(
         "assets",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("type", sa.Enum("HOST", "IP_ADDRESS", "DOMAIN", "WEB_APP", "API", "SERVICE", "TECHNOLOGY", "NETWORK", name="assettype"), nullable=False),
         sa.Column("identifier", sa.String(512), nullable=False),
         sa.Column("display_name", sa.String(512), nullable=True),
         sa.Column("metadata", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("discovered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
         sa.Column("confidence", sa.Float(), default=1.0, nullable=False),
         sa.Column("source", sa.String(128), nullable=False),
     )
     op.create_unique_constraint("uq_asset_assessment_type_identifier", "assets", ["assessment_id", "type", "identifier"])
     op.create_index("ix_assets_assessment_type", "assets", ["assessment_id", "type"])
     op.create_index("ix_assets_identifier", "assets", ["identifier"])
 
     # services table
     op.create_table(
         "services",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
         sa.Column("port", sa.Integer(), nullable=False),
         sa.Column("protocol", sa.String(16), nullable=False),
         sa.Column("name", sa.String(128), nullable=True),
         sa.Column("version", sa.String(128), nullable=True),
         sa.Column("banner", sa.Text(), nullable=True),
         sa.Column("technology", sa.String(255), nullable=True),
         sa.Column("cpe", sa.String(255), nullable=True),
         sa.Column("state", sa.String(32), default="open", nullable=False),
         sa.Column("discovered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
         sa.Column("source", sa.String(128), nullable=False),
         sa.Column("metadata", postgresql.JSONB(), default=dict, nullable=False),
     )
     op.create_unique_constraint("uq_service_asset_port_protocol", "services", ["asset_id", "port", "protocol"])
     op.create_index("ix_services_asset_port", "services", ["asset_id", "port"])
     op.create_index("ix_services_technology", "services", ["technology"])
 
     # vulnerabilities table
     op.create_table(
         "vulnerabilities",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("cve_id", sa.String(32), nullable=True, index=True),
         sa.Column("title", sa.String(512), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("cvss_score", sa.Float(), nullable=True),
         sa.Column("cvss_vector", sa.String(128), nullable=True),
         sa.Column("cvss_version", sa.String(8), nullable=True),
         sa.Column("epss_score", sa.Float(), nullable=True),
         sa.Column("epss_percentile", sa.Float(), nullable=True),
         sa.Column("cisa_kev", sa.Boolean(), default=False, nullable=False),
         sa.Column("cisa_kev_date", sa.DateTime(timezone=True), nullable=True),
         sa.Column("mitre_techniques", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("affected_software", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("references", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("source", sa.String(64), nullable=False),
         sa.Column("source_url", sa.String(512), nullable=True),
         sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
         sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="SET NULL"), nullable=True),
     )
     op.create_index("ix_vulnerabilities_cvss_score", "vulnerabilities", ["cvss_score"])
     op.create_index("ix_vulnerabilities_epss_score", "vulnerabilities", ["epss_score"])
     op.create_index("ix_vulnerabilities_cisa_kev", "vulnerabilities", ["cisa_kev"])
 
     # findings table
     op.create_table(
         "findings",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
         sa.Column("vulnerability_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vulnerabilities.id", ondelete="SET NULL"), nullable=True),
         sa.Column("title", sa.String(512), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("severity", sa.Enum("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", name="severity"), nullable=False),
         sa.Column("status", sa.Enum("DISCOVERED", "SUSPECTED", "SCANNER_REPORTED", "VALIDATED", "FALSE_POSITIVE", "DEMONSTRATED", name="findingstatus"), default="DISCOVERED", nullable=False),
         sa.Column("cvss_score", sa.Float(), nullable=True),
         sa.Column("cvss_vector", sa.String(128), nullable=True),
         sa.Column("risk_score", sa.Float(), nullable=True),
         sa.Column("evidence_ids", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("remediation", sa.Text(), nullable=True),
         sa.Column("references", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("tags", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("discovered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("validated_by", postgresql.UUID(as_uuid=True), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_findings_assessment_status", "findings", ["assessment_id", "status"])
     op.create_index("ix_findings_severity", "findings", ["severity"])
     op.create_index("ix_findings_vulnerability", "findings", ["vulnerability_id"])
 
     # evidence table
     op.create_table(
         "evidence",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("finding_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("findings.id", ondelete="CASCADE"), nullable=True),
         sa.Column("job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("execution_jobs.id", ondelete="SET NULL"), nullable=True),
         sa.Column("type", sa.String(64), nullable=False),
         sa.Column("title", sa.String(255), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("content", postgresql.BYTEA(), nullable=True),
         sa.Column("content_hash", sa.String(64), nullable=False),
         sa.Column("content_type", sa.String(128), nullable=True),
         sa.Column("size_bytes", sa.Integer(), default=0, nullable=False),
         sa.Column("redacted", sa.Boolean(), default=False, nullable=False),
         sa.Column("metadata", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
     )
     op.create_index("ix_evidence_finding", "evidence", ["finding_id"])
     op.create_index("ix_evidence_job", "evidence", ["job_id"])
     op.create_index("ix_evidence_content_hash", "evidence", ["content_hash"])
 
     # execution_jobs table
     op.create_table(
         "execution_jobs",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("name", sa.String(255), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("tool", sa.String(64), nullable=False),
         sa.Column("command", sa.Text(), nullable=False),
         sa.Column("args", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("status", sa.Enum("PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", name="jobstatus"), default="PENDING", nullable=False),
         sa.Column("execution_level", sa.Enum("L1_PASSIVE", "L2_CONTROLLED", "L3_INTRUSIVE", name="executionlevel"), nullable=False),
         sa.Column("policy_decision_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("policy_decisions.id", ondelete="SET NULL"), nullable=True),
         sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("duration_ms", sa.Integer(), nullable=True),
         sa.Column("exit_code", sa.Integer(), nullable=True),
         sa.Column("stdout", sa.Text(), nullable=True),
         sa.Column("stderr", sa.Text(), nullable=True),
         sa.Column("error", sa.Text(), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_jobs_assessment_status", "execution_jobs", ["assessment_id", "status"])
     op.create_index("ix_jobs_tool", "execution_jobs", ["tool"])
     op.create_index("ix_jobs_policy_decision", "execution_jobs", ["policy_decision_id"])
 
     # policy_decisions table
     op.create_table(
         "policy_decisions",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("action", sa.String(128), nullable=False),
         sa.Column("target", sa.String(512), nullable=False),
         sa.Column("execution_level", sa.Enum("L1_PASSIVE", "L2_CONTROLLED", "L3_INTRUSIVE", name="executionlevel"), nullable=False),
         sa.Column("decision", sa.Enum("ALLOWED", "REJECTED", "REQUIRES_APPROVAL", name="policydecision"), nullable=False),
         sa.Column("reason", sa.Text(), nullable=True),
         sa.Column("conditions", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("approved_by", postgresql.UUID(as_uuid=True), nullable=True),
         sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("metadata", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
     )
     op.create_index("ix_policy_decisions_assessment", "policy_decisions", ["assessment_id"])
     op.create_index("ix_policy_decisions_decision", "policy_decisions", ["decision"])
 
     # ai_proposals table
     op.create_table(
         "ai_proposals",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("action", sa.String(128), nullable=False),
         sa.Column("target", sa.String(512), nullable=False),
         sa.Column("reason", sa.Text(), nullable=False),
         sa.Column("required_evidence", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("risk_level", sa.String(32), nullable=False),
         sa.Column("confidence", sa.Float(), default=0.0, nullable=False),
         sa.Column("raw_response", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("policy_decision_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("policy_decisions.id", ondelete="SET NULL"), nullable=True),
         sa.Column("status", sa.String(32), default="pending", nullable=False),
         sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
     )
     op.create_index("ix_ai_proposals_assessment", "ai_proposals", ["assessment_id"])
     op.create_index("ix_ai_proposals_status", "ai_proposals", ["status"])
 
     # graph_nodes table
     op.create_table(
         "graph_nodes",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="SET NULL"), nullable=True),
         sa.Column("node_type", sa.String(64), nullable=False),
         sa.Column("label", sa.String(255), nullable=False),
         sa.Column("data", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("x", sa.Float(), nullable=True),
         sa.Column("y", sa.Float(), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_graph_nodes_assessment", "graph_nodes", ["assessment_id"])
     op.create_index("ix_graph_nodes_type", "graph_nodes", ["node_type"])
 
     # graph_edges table
     op.create_table(
         "graph_edges",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("graph_nodes.id", ondelete="CASCADE"), nullable=False),
         sa.Column("target_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("graph_nodes.id", ondelete="CASCADE"), nullable=False),
         sa.Column("edge_type", sa.String(64), nullable=False),
         sa.Column("label", sa.String(255), nullable=True),
         sa.Column("weight", sa.Float(), default=1.0, nullable=False),
         sa.Column("evidence_ids", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("data", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
     )
     op.create_index("ix_graph_edges_assessment", "graph_edges", ["assessment_id"])
     op.create_index("ix_graph_edges_source_target", "graph_edges", ["source_id", "target_id"])
 
     # attack_paths table
     op.create_table(
         "attack_paths",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("name", sa.String(255), nullable=False),
         sa.Column("description", sa.Text(), nullable=True),
         sa.Column("node_ids", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("edge_ids", postgresql.JSONB(), default=list, nullable=False),
         sa.Column("risk_score", sa.Float(), default=0.0, nullable=False),
         sa.Column("max_severity", sa.Enum("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", name="severity"), default="INFO", nullable=False),
         sa.Column("is_validated", sa.Boolean(), default=False, nullable=False),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
     )
     op.create_index("ix_attack_paths_assessment", "attack_paths", ["assessment_id"])
     op.create_index("ix_attack_paths_risk_score", "attack_paths", ["risk_score"])
 
     # reports table
     op.create_table(
         "reports",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
         sa.Column("name", sa.String(255), nullable=False),
         sa.Column("format", sa.Enum("PDF", "HTML", "JSON", name="reportformat"), nullable=False),
         sa.Column("content", postgresql.BYTEA(), nullable=True),
         sa.Column("file_path", sa.String(512), nullable=True),
         sa.Column("size_bytes", sa.Integer(), default=0, nullable=False),
         sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
         sa.Column("generated_by", postgresql.UUID(as_uuid=True), nullable=False),
     )
     op.create_index("ix_reports_assessment", "reports", ["assessment_id"])
 
     # audit_events table
     op.create_table(
         "audit_events",
         sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
         sa.Column("assessment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True),
         sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
         sa.Column("action", sa.String(128), nullable=False),
         sa.Column("resource_type", sa.String(64), nullable=False),
         sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
         sa.Column("details", postgresql.JSONB(), default=dict, nullable=False),
         sa.Column("ip_address", sa.String(45), nullable=True),
         sa.Column("user_agent", sa.String(512), nullable=True),
         sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
     )
     op.create_index("ix_audit_events_assessment", "audit_events", ["assessment_id"])
     op.create_index("ix_audit_events_user", "audit_events", ["user_id"])
     op.create_index("ix_audit_events_action", "audit_events", ["action"])
     op.create_index("ix_audit_events_created_at", "audit_events", ["created_at"])
 
 
 def downgrade() -> None:
     op.drop_table("audit_events")
     op.drop_table("reports")
     op.drop_table("attack_paths")
     op.drop_table("graph_edges")
     op.drop_table("graph_nodes")
     op.drop_table("ai_proposals")
     op.drop_table("policy_decisions")
     op.drop_table("execution_jobs")
     op.drop_table("evidence")
     op.drop_table("findings")
     op.drop_table("vulnerabilities")
     op.drop_table("services")
     op.drop_table("assets")
     op.drop_table("assessments")
     op.drop_table("scopes")
     op.drop_table("api_keys")
     op.drop_table("users")
 
     op.execute("DROP TYPE reportformat")
     op.execute("DROP TYPE jobstatus")
     op.execute("DROP TYPE policydecision")
     op.execute("DROP TYPE severity")
     op.execute("DROP TYPE findingstatus")
     op.execute("DROP TYPE assettype")
     op.execute("DROP TYPE assessmentstatus")
     op.execute("DROP TYPE executionlevel")
