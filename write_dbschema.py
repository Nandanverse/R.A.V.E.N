import pathlib
content = """# Database Schema

Complete PostgreSQL schema for RAVEN.

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   users     │       │ assessments │       │   scopes    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ id (PK)     │──────►│ id (PK)     │
│ username    │       │ name        │       │ assessment_id│
│ email       │       │ description │       │ target_type │
│ password_hash       │ status      │       │ target_value│
│ role        │       │ exec_level  │       │ description │
│ created_at  │       │ created_at  │       │ created_at  │
│ updated_at  │       │ updated_at  │       └─────────────┘
│ last_login  │       │ started_at  │
│ is_active   │       │ completed_at│
└─────────────┘       │ timeout_min │       ┌─────────────┐
                     │ created_by  │       │   assets    │
                     └──────┬──────┘       ├─────────────┤
                            │              │ id (PK)     │
                     ┌──────▼──────┐       │ assessment_id│
                     │ scan_history│       │ host_id     │
                     ├─────────────┤       │ asset_type  │
                     │ id (PK)     │       │ identifier  │
                     │ assessment_id│       │ display_name│
                     │ scan_type   │       │ criticality │
                     │ status      │       │ tags        │
                     │ started_at  │       │ created_at  │
                     │ completed_at│       │ updated_at  │
                     │ config      │       └──────┬──────┘
                     │ statistics  │              │
                     └─────────────┘       ┌──────▼──────┐
                                         │  services   │
                     ┌─────────────┐     ├─────────────┤
                     │vulnerabilities│     │ id (PK)     │
                     ├─────────────┤     │ asset_id    │
                     │ id (PK)     │     │ port        │
                     │ cve_id      │     │ protocol    │
                     │ cvss_vector │     │ service_name│
                     │ cvss_score  │     │ version     │
                     │ epss_score  │     │ fingerprint │
                     │ kev_listed  │     │ tls_info    │
                     │ attack_techs│     │ created_at  │
                     │ description │     │ updated_at  │
                     │ references  │     └──────┬──────┘
                     │ fetched_at  │            │
                     └──────┬──────┘       ┌──────▼──────┐
                            │              │  findings   │
                     ┌──────▼──────┐       ├─────────────┤
                     │  evidence   │       │ id (PK)     │
                     ├─────────────┤       │ assessment_id│
                     │ id (PK)     │       │ asset_id    │
                     │ finding_id  │       │ service_id  │
                     │ type        │       │ vuln_id     │
                     │ content     │       │ title       │
                     │ hash        │       │ description │
                     │ metadata    │       │ severity    │
                     │ created_at  │       │ status      │
                     └─────────────┘       │ confidence  │
                                           │ remediation │
                     ┌─────────────┐       │ created_at  │
                     │  proposals  │       │ updated_at  │
                     ├─────────────┤       └──────┬──────┘
                     │ id (PK)     │              │
                     │ assessment_id│       ┌──────▼──────┐
                     │ action_type │       │graph_nodes  │
                     │ target_ref  │       ├─────────────┤
                     │ reasoning   │       │ id (PK)     │
                     │ required_ev │       │ assessment_id│
                     │ risk_level  │       │ node_type   │
                     │ status      │       │ ref_id      │
                     │ llm_response│       │ label       │
                     │ created_at  │       │ metadata    │
                     └──────┬──────┘       │ created_at  │
                            │              └──────┬──────┘
                     ┌──────▼──────┐              │
                     │policy_decisions        ┌────▼────┐
                     ├─────────────┤          │graph_edges│
                     │ id (PK)     │          ├───────────┤
                     │ proposal_id │          │ id (PK)   │
                     │ decision    │          │ source_id │
                     │ reason      │          │ target_id │
                     │ reviewer    │          │ edge_type │
                     │ expires_at  │          │ evidence  │
                     │ created_at  │          │ created_at│
                     └─────────────┘          └───────────┘
                                              ┌─────────────┐
                                              │ risk_scores │
                                              ├─────────────┤
                                              │ id (PK)     │
                                              │ finding_id  │
                                              │ base_score  │
                                              │ contextual  │
                                              │ factors     │
                                              │ explanation │
                                              │ calculated_at│
                                              └─────────────┘
                                              ┌─────────────┐
                                              │  reports    │
                                              ├─────────────┤
                                              │ id (PK)     │
                                              │ assessment_id│
                                              │ title       │
                                              │ format      │
                                              │ file_path   │
                                              │ generated_by│
                                              │ created_at  │
                                              └─────────────┘
                                              ┌─────────────┐
                                              │audit_events │
                                              ├─────────────┤
                                              │ id (PK)     │
                                              │ timestamp   │
                                              │ event_type  │
                                              │ actor       │
                                              │ resource    │
                                              │ action      │
                                              │ outcome     │
                                              │ details     │
                                              │ ip_address  │
                                              └─────────────┘
```

## Table Definitions

### users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'analyst',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX ix_users_username ON users(username);
CREATE INDEX ix_users_email ON users(email);
```

### assessments

```sql
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    execution_level VARCHAR(20) NOT NULL DEFAULT 'L1',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    timeout_minutes INTEGER NOT NULL DEFAULT 120,
    created_by UUID REFERENCES users(id),
    config JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX ix_assessments_status ON assessments(status);
CREATE INDEX ix_assessments_created_by ON assessments(created_by);
CREATE INDEX ix_assessments_created_at ON assessments(created_at DESC);
```

### scopes

```sql
CREATE TABLE scopes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL,  -- domain, ip, cidr
    target_value VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, target_type, target_value)
);

CREATE INDEX ix_scopes_assessment ON scopes(assessment_id);
CREATE INDEX ix_scopes_target ON scopes(target_type, target_value);
```

### assets

```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    host_id UUID REFERENCES assets(id),  -- self-ref for host relationship
    asset_type VARCHAR(30) NOT NULL,  -- host, domain, web_app, api, network
    identifier VARCHAR(255) NOT NULL,  -- IP, domain, URL
    display_name VARCHAR(255),
    criticality VARCHAR(20) NOT NULL DEFAULT 'medium',  -- critical, high, medium, low
    tags JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, asset_type, identifier)
);

CREATE INDEX ix_assets_assessment ON assets(assessment_id);
CREATE INDEX ix_assets_type ON assets(asset_type);
CREATE INDEX ix_assets_criticality ON assets(criticality);
CREATE INDEX ix_assets_host ON assets(host_id);
CREATE INDEX ix_assets_identifier ON assets(identifier);
```

### services

```sql
CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    port INTEGER NOT NULL,
    protocol VARCHAR(10) NOT NULL DEFAULT 'tcp',  -- tcp, udp
    service_name VARCHAR(100),
    version VARCHAR(100),
    fingerprint JSONB NOT NULL DEFAULT '{}',  -- banners, SSL certs, HTTP headers
    tls_info JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(asset_id, port, protocol)
);

CREATE INDEX ix_services_asset ON services(asset_id);
CREATE INDEX ix_services_port ON services(port);
CREATE INDEX ix_services_name ON services(service_name);
CREATE INDEX ix_services_fingerprint_gin ON services USING GIN(fingerprint);
```

### vulnerabilities

```sql
CREATE TABLE vulnerabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cve_id VARCHAR(20) NOT NULL UNIQUE,  -- CVE-YYYY-NNNNN
    cvss_vector VARCHAR(200),
    cvss_score DECIMAL(3,1),
    cvss_version VARCHAR(10) DEFAULT '3.1',
    epss_score DECIMAL(4,3),  -- 0.000 to 1.000
    epss_percentile DECIMAL(5,2),
    kev_listed BOOLEAN NOT NULL DEFAULT FALSE,
    kev_date DATE,
    attack_techniques JSONB NOT NULL DEFAULT '[]',  -- ATT&CK technique IDs
    description TEXT,
    references JSONB NOT NULL DEFAULT '[]',
    affected_products JSONB NOT NULL DEFAULT '[]',  -- CPE matches
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_vuln_cve ON vulnerabilities(cve_id);
CREATE INDEX ix_vuln_cvss ON vulnerabilities(cvss_score DESC);
CREATE INDEX ix_vuln_epss ON vulnerabilities(epss_score DESC);
CREATE INDEX ix_vuln_kev ON vulnerabilities(kev_listed) WHERE kev_listed;
CREATE INDEX ix_vuln_techniques_gin ON vulnerabilities USING GIN(attack_techniques);
CREATE INDEX ix_vuln_products_gin ON vulnerabilities USING GIN(affected_products);
```

### findings

```sql
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    service_id UUID REFERENCES services(id) ON DELETE SET NULL,
    vuln_id UUID REFERENCES vulnerabilities(id) ON DELETE SET NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,  -- critical, high, medium, low, info
    status VARCHAR(20) NOT NULL DEFAULT 'suspected',  -- suspected, validated, rejected, pending
    confidence INTEGER NOT NULL DEFAULT 50,  -- 0-100
    remediation TEXT,
    remediation_status VARCHAR(20) DEFAULT 'open',  -- open, in_progress, resolved, verified
    remediation_assignee UUID REFERENCES users(id),
    remediation_due TIMESTAMPTZ,
    false_positive_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    validated_at TIMESTAMPTZ,
    validated_by UUID REFERENCES users(id)
);

CREATE INDEX ix_findings_assessment ON findings(assessment_id);
CREATE INDEX ix_findings_asset ON findings(asset_id);
CREATE INDEX ix_findings_severity ON findings(severity);
CREATE INDEX ix_findings_status ON findings(status);
CREATE INDEX ix_findings_vuln ON findings(vuln_id);
CREATE INDEX ix_findings_assessment_status ON findings(assessment_id, status);
```

### evidence

```sql
CREATE TABLE evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    finding_id UUID NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    type VARCHAR(30) NOT NULL,  -- http_request, http_response, tool_output, screenshot, log
    content BYTEA NOT NULL,
    hash CHAR(64) NOT NULL,  -- SHA-256 hex
    metadata JSONB NOT NULL DEFAULT '{}',  -- headers, method, url, status_code, tool, etc.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_evidence_finding ON evidence(finding_id);
CREATE INDEX ix_evidence_hash ON evidence(hash);
CREATE INDEX ix_evidence_type ON evidence(type);
```

### scan_history

```sql
CREATE TABLE scan_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    scan_type VARCHAR(30) NOT NULL,  -- host_discovery, port_scan, service_enum, http_discovery
    status VARCHAR(20) NOT NULL,  -- running, completed, failed, cancelled
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    config JSONB NOT NULL DEFAULT '{}',
    statistics JSONB NOT NULL DEFAULT '{}',  -- hosts_up, ports_open, services_found, etc.
    error TEXT,
    raw_output_path VARCHAR(500)  -- path to Nmap XML
);

CREATE INDEX ix_scan_history_assessment ON scan_history(assessment_id);
CREATE INDEX ix_scan_history_status ON scan_history(status);
CREATE INDEX ix_scan_history_started ON scan_history(started_at DESC);
```

### proposals

```sql
CREATE TABLE proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,  -- test_header_analysis, test_api_authz, zap_scan, etc.
    target_ref JSONB NOT NULL,  -- {asset_id, service_id, url, params}
    reasoning TEXT NOT NULL,
    required_evidence JSONB NOT NULL DEFAULT '[]',
    risk_level VARCHAR(20) NOT NULL,  -- L1, L2, L3
    status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, approved, rejected, executed
    llm_response JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    decided_at TIMESTAMPTZ,
    decided_by UUID REFERENCES users(id)
);

CREATE INDEX ix_proposals_assessment ON proposals(assessment_id);
CREATE INDEX ix_proposals_status ON proposals(status);
CREATE INDEX ix_proposals_risk ON proposals(risk_level);
```

### policy_decisions

```sql
CREATE TABLE policy_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proposal_id UUID NOT NULL REFERENCES proposals(id) ON DELETE CASCADE,
    decision VARCHAR(20) NOT NULL,  -- approved, rejected, requires_approval
    reason TEXT NOT NULL,
    reviewer UUID REFERENCES users(id),
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(proposal_id)
);

CREATE INDEX ix_policy_proposal ON policy_decisions(proposal_id);
CREATE INDEX ix_policy_decision ON policy_decisions(decision);
```

### graph_nodes

```sql
CREATE TABLE graph_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    node_type VARCHAR(20) NOT NULL,  -- asset, service, vulnerability, finding
    ref_id UUID NOT NULL,  -- references assets.id, services.id, etc.
    label VARCHAR(255) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, node_type, ref_id)
);

CREATE INDEX ix_graph_nodes_assessment ON graph_nodes(assessment_id);
CREATE INDEX ix_graph_nodes_type ON graph_nodes(node_type);
CREATE INDEX ix_graph_nodes_ref ON graph_nodes(ref_id);
```

### graph_edges

```sql
CREATE TABLE graph_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    target_id UUID NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    edge_type VARCHAR(30) NOT NULL,  -- exposes, runs, enables, validated
    evidence JSONB NOT NULL DEFAULT '[]',  -- array of evidence IDs
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, source_id, target_id, edge_type)
);

CREATE INDEX ix_graph_edges_assessment ON graph_edges(assessment_id);
CREATE INDEX ix_graph_edges_source ON graph_edges(source_id);
CREATE INDEX ix_graph_edges_target ON graph_edges(target_id);
CREATE INDEX ix_graph_edges_type ON graph_edges(edge_type);
```

### risk_scores

```sql
CREATE TABLE risk_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    finding_id UUID NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    base_score DECIMAL(3,1) NOT NULL,  -- CVSS base
    contextual_score DECIMAL(3,1) NOT NULL,  -- 0.0-10.0
    factors JSONB NOT NULL DEFAULT '{}',  -- {cvss, epss, kev, exposure, criticality, validation, path}
    explanation TEXT NOT NULL,
    calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(finding_id)
);

CREATE INDEX ix_risk_finding ON risk_scores(finding_id);
CREATE INDEX ix_risk_contextual ON risk_scores(contextual_score DESC);
```

### reports

```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    format VARCHAR(20) NOT NULL,  -- pdf, html, json
    file_path VARCHAR(500) NOT NULL,
    template VARCHAR(100),
    generated_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    file_size BIGINT,
    checksum CHAR(64)  -- SHA-256
);

CREATE INDEX ix_reports_assessment ON reports(assessment_id);
CREATE INDEX ix_reports_created ON reports(created_at DESC);
```

### audit_events

```sql
CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type VARCHAR(50) NOT NULL,  -- assessment_created, scan_started, finding_validated, etc.
    actor VARCHAR(255) NOT NULL,  -- user ID or 'system'
    resource_type VARCHAR(50),  -- assessment, finding, proposal, etc.
    resource_id UUID,
    action VARCHAR(50) NOT NULL,  -- create, read, update, delete, execute, approve
    outcome VARCHAR(20) NOT NULL,  -- success, failure, denied
    details JSONB NOT NULL DEFAULT '{}',
    ip_address INET
);

CREATE INDEX ix_audit_timestamp ON audit_events(timestamp DESC);
CREATE INDEX ix_audit_actor ON audit_events(actor);
CREATE INDEX ix_audit_resource ON audit_events(resource_type, resource_id);
CREATE INDEX ix_audit_event_type ON audit_events(event_type);
```

## Migration Strategy

All schema changes managed via Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Current revision
alembic current

# History
alembic history
```

## Soft Deletes

Tables with soft deletes use `deleted_at TIMESTAMPTZ` column:
- `assessments`, `assets`, `services`, `findings`, `proposals`, `graph_nodes`, `graph_edges`

Queries must filter: `WHERE deleted_at IS NULL`

## Partitioning (Future)

Large tables candidates for partitioning:
- `audit_events` — by month (timestamp)
- `evidence` — by month (created_at)
- `scan_history` — by month (started_at)

---

*Database schema version: 1.0*
*Last updated: 2026-11-06*
"""
pathlib.Path("C:/Users/nanda/OneDrive/Desktop/RAVEN/docs/database-schema.md").write_text(content, encoding="utf-8")
print("done")
