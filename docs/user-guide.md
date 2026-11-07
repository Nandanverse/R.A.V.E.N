# User Guide

This guide covers using RAVEN for authorized security assessments.

## Getting Started

### 1. Access the Application

Open your browser to `http://localhost:5173` (or your configured frontend URL).

### 2. Create Your First Assessment

1. Click **Assessments** in the sidebar
2. Click **New Assessment**
3. Fill in:
   - **Name**: Descriptive name (e.g., "Juice Shop Lab Assessment")
   - **Description**: Optional details about scope and goals
   - **Targets**: Add authorized targets from the allowlist
   - **Execution Level**: L1 (Passive), L2 (Controlled), or L3 (Intrusive)
4. Click **Create Assessment**

### 3. Run Reconnaissance

1. Navigate to **Reconnaissance**
2. Select your assessment from the dropdown
3. Choose scan types:
   - **Host Discovery**: Find live hosts (ping, ARP, TCP SYN)
   - **Port Scan**: Scan ports (top 100, top 1000, or custom range)
   - **Service Enumeration**: Detect service versions
   - **HTTP Discovery**: Find web endpoints, APIs, technologies
4. Click **Start Scan**
5. Monitor progress in the scan list
6. Click **View Results** when complete

### 4. Explore Discovered Assets

1. Navigate to **Asset Inventory**
2. Filter by: assessment, asset type, criticality
3. Click an asset to see:
   - Associated services and ports
   - Discovered technologies
   - Related vulnerabilities
   - Scan history

### 5. Review Vulnerability Intelligence

1. Navigate to **Vulnerability Intelligence**
2. Search CVEs by: ID, keyword, severity, EPSS score
3. View CVE details:
   - CVSS vector and scores
   - EPSS exploit probability
   - CISA KEV status
   - MITRE ATT&CK techniques
   - Affected software versions
4. Correlate with your assets using the **Correlate** button

### 6. Analyze Findings

1. Navigate to **Findings**
2. Filter by: severity, validation status, asset, assessment
3. Click a finding to view:
   - Evidence (HTTP requests/responses, tool output)
   - Validation status and confidence
   - Remediation guidance
   - Related attack paths

### 7. Use AI Analysis

1. Navigate to **AI Analysis**
2. Check **Ollama Status**: Should show "Connected" with model name
3. Click **Analyze Assessment** to generate proposals
4. Review proposals:
   - **Action**: What test to run
   - **Target**: Which asset/endpoint
   - **Reason**: Why this test is relevant
   - **Required Evidence**: What proof is needed
   - **Risk Level**: L1/L2/L3 classification
5. Click **Approve** or **Reject** on each proposal
6. Approved proposals are queued for execution
7. View results in **Execution History**

### 8. Explore Attack Graph

1. Navigate to **Attack Graph**
2. Select an assessment
3. Graph shows:
   - **Nodes**: Assets (blue), Services (green), Vulnerabilities (red/orange/yellow), Findings (purple)
   - **Edges**: Relationships (exposes, runs, enables, validated)
4. Click a node to inspect:
   - Details and metadata
   - Connected edges with evidence
   - Attack paths from this node
5. Use layout controls: Hierarchical, Organic, Circular
6. Export as PNG or SVG

### 9. View Analytics

1. Navigate to **Analytics**
2. Dashboards show real data from your assessments:
   - **Asset Summary**: Total, by type, by criticality
   - **Vulnerability Distribution**: By severity, validation status
   - **Exposure Analysis**: Internet-facing vs internal
   - **Tool Performance**: Success rates, duration, errors
   - **Remediation Progress**: Open vs resolved findings
3. All charts use actual database data (no mock data)

### 10. Generate Reports

1. Navigate to **Reports**
2. Click **Generate Report**
3. Select:
   - Assessment(s) to include
   - Format: PDF, HTML, JSON
   - Sections: Executive summary, methodology, assets, findings, risk analysis, remediation, limitations
4. Click **Generate**
5. Download when ready

## Page Reference

### Overview

Dashboard with real-time summary:
- Active assessments count
- Total assets discovered
- Critical/High findings requiring attention
- Recent scan activity
- AI reasoning status
- Quick actions

### Assessments

List and manage assessments:
- Create, edit, clone, delete
- Start, pause, stop, resume
- View assessment timeline
- Configure scope, credentials, execution level
- Archive completed assessments

### Asset Inventory

Searchable asset database:
- Filters: assessment, type (host, domain, web app, API), criticality, tags
- Columns: name, IP, type, criticality, services count, vulnerabilities count, last scanned
- Bulk actions: tag, export, delete
- Detail view: services, technologies, vulnerabilities, scan history, evidence

### Reconnaissance

Scan management:
- Scan types: Host Discovery, Port Scan, Service Enum, HTTP Discovery, Full Recon
- Scan configuration: ports, timing, scripts, rate limits
- Scan history with differential comparison
- Raw Nmap XML output download
- Scan scheduling (future)

### Vulnerability Intelligence

CVE knowledge base:
- Search: CVE ID, keyword, CWE, product, vendor
- Filters: severity, EPSS range, KEV status, ATT&CK technique
- CVE detail: CVSS, EPSS, KEV, ATT&CK, references, affected versions
- Correlation: Match CVEs to discovered services
- Feed management: Refresh NVD, EPSS, KEV, ATT&CK
- Local cache status and size

### Findings

Validated vulnerability tracking:
- Filters: severity, status (validated/suspected/rejected/pending), asset, assessment, date
- Validation workflow: Suspected → Validated/Rejected
- Evidence viewer: HTTP request/response, tool output, screenshots
- Remediation tracking: status, assignee, due date, verification
- False positive marking with reason
- Export: CSV, JSON

### Attack Graph

Relationship visualization:
- Graph built from findings and evidence
- Nodes: Asset, Service, Vulnerability, Finding
- Edges: exposes, runs, enables, validated (with evidence count)
- Path finding: Source → Target with max depth
- Evidence-backed only (no speculative paths)
- Interactive: pan, zoom, select, inspect
- Layouts: dagre (hierarchical), cose-bilkent (organic)
- Export: PNG (3x), SVG, JSON (Cytoscape.js format)

### AI Analysis

LLM-assisted reasoning:
- Ollama connection status and model info
- Proposal history with reasoning
- Policy approval/rejection with reasons
- Execution results linked to proposals
- Manual proposal creation (for testing)
- Context retrieval: relevant CVEs, ATT&CK, evidence
- Offline mode indicator when Ollama unavailable

### Analytics

Real metrics dashboards:
- Asset metrics: count, type distribution, criticality, exposure
- Vulnerability metrics: severity distribution, validation rate, FP rate, KEV coverage
- Scan metrics: success rate, duration percentiles, error categories
- Finding metrics: remediation velocity, SLA compliance, recurrence
- Risk metrics: score distribution, trend, top risk assets
- Time range selector: 7d, 30d, 90d, custom
- Empty states when no data

### Reports

Report generation and management:
- Templates: Executive, Technical, Compliance, Custom
- Formats: PDF (WeasyPrint), HTML, JSON
- Sections: configurable per template
- Scheduled generation (future)
- Report history with download links
- Version comparison

### Settings

Application configuration:
- **General**: App name, timezone, date format, theme
- **Assessment**: Default timeout, execution level, concurrent limits
- **Scanning**: Nmap defaults, ZAP config, rate limits
- **AI**: Ollama URL, model, temperature, timeout
- **Intelligence**: Feed refresh intervals, cache TTL
- **Storage**: Evidence path, retention, max file size
- **Security**: Session timeout, password policy, audit log retention
- **Notifications**: Email, webhook (future)

### About

Project information:
- RAVEN name, version, description
- Author: Nandan Amin
- Links: LinkedIn, Instagram
- Technology stack
- License
- GitHub repository (when available)

## Best Practices

### Scope Management

- Define `ALLOWED_TARGETS` narrowly — only targets you own or have written authorization for
- Use CIDR ranges for internal networks, individual domains for external
- Review and update allowlist regularly

### Assessment Workflow

1. Start with L1 (Passive) reconnaissance
2. Review assets, expand scope if authorized
3. Run L2 (Controlled) service enumeration
4. Correlate with vulnerability intelligence
5. Use AI Analysis for test proposals
6. Approve L2 tests incrementally
7. Only request L3 (Intrusive) for specific, documented needs
8. Document all approvals and rationale

### Evidence Handling

- Evidence is automatically collected for all executed tests
- Review evidence before marking findings as Validated
- Redact sensitive data manually if auto-redaction misses something
- Export evidence packages for ticketing systems

### AI Reasoning

- Treat AI proposals as suggestions, not commands
- Always review reasoning before approving
- The policy engine is the final gate — AI cannot bypass it
- When Ollama is unavailable, continue with manual assessment

### Reporting

- Generate reports at assessment milestones
- Use Executive template for management, Technical for engineers
- Include limitations section honestly
- Archive reports with assessment records

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + K` | Global search |
| `Ctrl/Cmd + /` | Focus search input |
| `Esc` | Close modal/drawer |
| `Tab` / `Shift+Tab` | Navigate focusable elements |
| `Enter` / `Space` | Activate button/link |
| `Arrow keys` | Navigate tables, graphs |

## Accessibility

- All pages keyboard navigable
- Screen reader labels on all interactive elements
- High contrast mode supported (OS-level)
- Reduced motion respected (OS-level)
- Focus indicators visible
- ARIA live regions for status updates

---

*User guide version: 1.0*
*Last updated: 2026-11-06*
