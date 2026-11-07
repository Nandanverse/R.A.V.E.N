import pathlib
content = """# Attack Graph

Design and implementation of the AttackGraph module for relationship modeling and attack path analysis.

## Overview

AttackGraph builds a relationship graph from assessment findings, enabling visualization and analysis of potential attack paths. The graph contains only evidence-backed relationships - no speculative paths.

## Graph Model

### Nodes

| Node Type | Source Table | Label | Key Attributes |
|-----------|--------------|-------|----------------|
| Asset | assets | IP, domain, app name | type, criticality, tags |
| Service | services | port/protocol/service | version, fingerprint |
| Vulnerability | vulnerabilities | CVE-ID | cvss, epss, kev, techniques |
| Finding | findings | title | severity, status, confidence |

### Edges

| Edge Type | Source | Target | Meaning | Evidence Required |
|-----------|--------|--------|---------|-------------------|
| exposes | Asset | Service | Asset runs this service | Scan result |
| runs | Service | Vulnerability | Service matches CVE | Correlation confidence |
| enables | Vulnerability | Finding | CVE validated as finding | Validation evidence |
| validated | Finding | Asset/Service | Finding confirmed on target | Test execution evidence |
| lateral | Asset | Asset | Network reachability | Network scan, routing |

### Graph Storage (PostgreSQL)

```sql
CREATE TABLE graph_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    node_type VARCHAR(20) NOT NULL,  -- asset, service, vulnerability, finding
    ref_id UUID NOT NULL,  -- references source table PK
    label VARCHAR(255) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, node_type, ref_id)
);

CREATE TABLE graph_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    target_id UUID NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    edge_type VARCHAR(30) NOT NULL,  -- exposes, runs, enables, validated, lateral
    evidence JSONB NOT NULL DEFAULT '[]',  -- array of evidence IDs
    weight DECIMAL(3,2) DEFAULT 1.0,  -- confidence weight
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(assessment_id, source_id, target_id, edge_type)
);

CREATE INDEX ix_graph_nodes_assessment ON graph_nodes(assessment_id);
CREATE INDEX ix_graph_nodes_type ON graph_nodes(node_type);
CREATE INDEX ix_graph_nodes_ref ON graph_nodes(ref_id);
CREATE INDEX ix_graph_edges_assessment ON graph_edges(assessment_id);
CREATE INDEX ix_graph_edges_source ON graph_edges(source_id);
CREATE INDEX ix_graph_edges_target ON graph_edges(target_id);
CREATE INDEX ix_graph_edges_type ON graph_edges(edge_type);
```

## Graph Building

### Trigger

Graph rebuild triggered on:
- Finding created/validated/rejected
- Service correlated with vulnerability
- Asset relationship discovered
- Manual rebuild via API

### Build Process

```python
class GraphBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_for_assessment(self, assessment_id: UUID) -> GraphBuildResult:
        # Clear existing graph for assessment
        await self._clear_graph(assessment_id)

        # 1. Create asset nodes
        assets = await self._get_assets(assessment_id)
        for asset in assets:
            await self._create_node(assessment_id, "asset", asset.id, asset.display_name, {
                "asset_type": asset.asset_type,
                "criticality": asset.criticality,
                "identifier": asset.identifier
            })

        # 2. Create service nodes and exposes edges
        services = await self._get_services(assessment_id)
        for service in services:
            service_node = await self._create_node(assessment_id, "service", service.id,
                f"{service.port}/{service.protocol} {service.service_name}", {
                    "port": service.port,
                    "protocol": service.protocol,
                    "version": service.version
                })
            # exposes edge: asset -> service
            asset_node = await self._get_node(assessment_id, "asset", service.asset_id)
            await self._create_edge(assessment_id, asset_node.id, service_node.id, "exposes",
                evidence=[service.scan_evidence_id])

        # 3. Create vulnerability nodes and runs edges
        correlations = await self._get_correlations(assessment_id)
        for corr in correlations:
            vuln_node = await self._create_node(assessment_id, "vulnerability", corr.vulnerability_id,
                corr.vulnerability.cve_id, {
                    "cvss": corr.vulnerability.cvss_score,
                    "epss": corr.vulnerability.epss_score,
                    "kev": corr.vulnerability.kev_listed
                })
            # runs edge: service -> vulnerability
            service_node = await self._get_node(assessment_id, "service", corr.service_id)
            await self._create_edge(assessment_id, service_node.id, vuln_node.id, "runs",
                evidence=[corr.correlation_evidence_id], weight=corr.confidence / 100.0)

        # 4. Create finding nodes and enables/validated edges
        findings = await self._get_findings(assessment_id)
        for finding in findings:
            finding_node = await self._create_node(assessment_id, "finding", finding.id, finding.title, {
                "severity": finding.severity,
                "status": finding.status,
                "confidence": finding.confidence
            })

            # enables edge: vulnerability -> finding
            if finding.vuln_id:
                vuln_node = await self._get_node(assessment_id, "vulnerability", finding.vuln_id)
                await self._create_edge(assessment_id, vuln_node.id, finding_node.id, "enables",
                    evidence=finding.evidence_ids)

            # validated edge: finding -> asset/service
            target_node = await self._get_node(assessment_id, "asset", finding.asset_id)
            await self._create_edge(assessment_id, finding_node.id, target_node.id, "validated",
                evidence=finding.evidence_ids)

        # 5. Lateral edges (network reachability)
        await self._build_lateral_edges(assessment_id)

        return GraphBuildResult(nodes_created=..., edges_created=...)
```

## Attack Path Analysis

### Path Finding Algorithm

Bounded depth-first search from entry points to high-value targets:

```python
class PathFinder:
    def __init__(self, db: AsyncSession, max_depth: int = 6):
        self.db = db
        self.max_depth = max_depth

    async def find_paths(self, assessment_id: UUID, source_types: list[str] = None,
                         target_types: list[str] = None) -> list[AttackPath]:
        \"\"\"Find all attack paths from sources to targets.\"\"\"
        # Default: entry points (internet-facing assets) to critical assets
        sources = await self._get_entry_points(assessment_id)
        targets = await self._get_high_value_targets(assessment_id)

        paths = []
        for source in sources:
            paths.extend(await self._dfs(source, targets, assessment_id, [], set()))

        return sorted(paths, key=lambda p: p.risk_score, reverse=True)

    async def _dfs(self, current: GraphNode, targets: list[GraphNode],
                   assessment_id: UUID, path: list[GraphEdge],
                   visited: set[UUID]) -> list[AttackPath]:
        if current.id in visited:
            return []  # Cycle detection

        if len(path) >= self.max_depth:
            return []

        visited.add(current.id)

        results = []

        # Check if current is a target
        if current in targets:
            results.append(AttackPath(
                nodes=[e.source_id for e in path] + [current.id],
                edges=[e.id for e in path],
                risk_score=self._calculate_path_risk(path),
                evidence=self._collect_path_evidence(path)
            ))

        # Continue traversal
        edges = await self._get_outgoing_edges(current.id)
        for edge in edges:
            if edge.weight < 0.3:  # Low confidence threshold
                continue
            next_node = await self._get_node(edge.target_id)
            results.extend(await self._dfs(next_node, targets, assessment_id,
                                           path + [edge], visited.copy()))

        return results

    def _calculate_path_risk(self, edges: list[GraphEdge]) -> float:
        \"\"\"Composite risk: product of edge weights * max node severity.\"\"\"
        if not edges:
            return 0.0
        weight_product = 1.0
        for edge in edges:
            weight_product *= edge.weight
        max_severity = max(self._severity_to_score(self._get_node(e.target_id).metadata.get("severity", "info"))
                           for e in edges)
        return weight_product * (max_severity / 10.0)
```

### Path Scoring

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Edge confidence | 0.4 | Product of edge weights |
| Max node severity | 0.3 | Critical=10, High=7.5, Medium=5, Low=2.5, Info=1 |
| KEV on path | 0.15 | Any vulnerability with KEV listed |
| EPSS > 0.5 | 0.1 | Any vulnerability with high EPSS |
| Validated findings | 0.05 | Count of validated findings on path |

## Visualization (Cytoscape.js)

### Stylesheet

```javascript
const style = [
  // Nodes
  {
    selector: 'node',
    style: {
      'background-color': '#141414',
      'border-width': 1,
      'border-color': '#2a2a2a',
      'label': 'data(label)',
      'font-size': '11px',
      'color': '#e8e8e8',
      'text-valign': 'bottom',
      'text-margin-y': 8
    }
  },
  {
    selector: 'node[type = "asset"]',
    style: { 'shape': 'rectangle', 'width': 40, 'height': 40 }
  },
  {
    selector: 'node[type = "service"]',
    style: { 'shape': 'ellipse', 'width': 32, 'height': 32 }
  },
  {
    selector: 'node[type = "vulnerability"]',
    style: { 'shape': 'triangle', 'width': 28, 'height': 28 }
  },
  {
    selector: 'node[type = "finding"]',
    style: { 'shape': 'pentagon', 'width': 24, 'height': 24 }
  },
  // Severity borders
  {
    selector: 'node[severity = "critical"]',
    style: { 'border-color': '#dc2626', 'border-width': 3 }
  },
  {
    selector: 'node[severity = "high"]',
    style: { 'border-color': '#ea580c', 'border-width': 2 }
  },
  {
    selector: 'node[severity = "medium"]',
    style: { 'border-color': '#ca8a04', 'border-width': 2 }
  },
  {
    selector: 'node[severity = "low"]',
    style: { 'border-color': '#16a34a', 'border-width': 2 }
  },
  // Validated findings
  {
    selector: 'node[validated = true]',
    style: { 'border-color': '#16a34a', 'border-width': 3, 'border-style': 'double' }
  },
  // Edges
  {
    selector: 'edge',
    style: {
      'width': 1.5,
      'line-color': '#6a6a6a',
      'target-arrow-shape': 'triangle',
      'target-arrow-color': '#6a6a6a',
      'curve-style': 'bezier',
      'label': 'data(edge_type)',
      'font-size': '9px',
      'color': '#a0a0a0',
      'text-background-color': '#141414',
      'text-background-padding': '2px'
    }
  },
  // Edge types
  {
    selector: 'edge[edge_type = "validated"]',
    style: { 'line-color': '#16a34a', 'target-arrow-color': '#16a34a', 'width': 2.5 }
  },
  {
    selector: 'edge[edge_type = "enables"]',
    style: { 'line-color': '#ea580c', 'target-arrow-color': '#ea580c' }
  },
  {
    selector: 'edge[edge_type = "runs"]',
    style: { 'line-color': '#ca8a04', 'target-arrow-color': '#ca8a04' }
  },
  {
    selector: 'edge[edge_type = "exposes"]',
    style: { 'line-color': '#2563eb', 'target-arrow-color': '#2563eb' }
  },
  // Selection
  {
    selector: ':selected',
    style: {
      'border-color': '#2563eb',
      'border-width': 3,
      'z-index': 9999
    }
  }
];
```

### Layouts

- **dagre** (hierarchical): Top-down from entry points
- **cose-bilkent** (organic): Force-directed for exploration
- **circle**: For small graphs

### Interactions

- Pan/zoom (mouse wheel, pinch)
- Node click: Show detail panel with metadata, evidence, connected edges
- Edge click: Show evidence list
- Path highlight: Select source and target, highlight shortest path
- Export: PNG (3x), SVG, JSON (Cytoscape.js format)

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | /graph/nodes | List nodes with filters |
| GET | /graph/nodes/{id} | Node detail with connected edges |
| GET | /graph/edges | List edges |
| GET | /graph/paths | Find attack paths (source, target, max_depth) |
| GET | /graph/export | Export graph (format: png, svg, json) |
| POST | /graph/rebuild | Trigger graph rebuild for assessment |

## Testing

```python
# Test graph building
result = await builder.build_for_assessment(assessment_id)
assert result.nodes_created > 0
assert result.edges_created > 0

# Verify edge types
assets = await get_nodes(assessment_id, type="asset")
services = await get_nodes(assessment_id, type="service")
edges = await get_edges(assessment_id, source_type="asset", target_type="service")
assert all(e.edge_type == "exposes" for e in edges)

# Test path finding
paths = await finder.find_paths(assessment_id)
assert len(paths) > 0
for path in paths:
    assert path.risk_score > 0
    assert len(path.evidence) > 0
    # Verify no cycles
    node_ids = set()
    for node_id in path.nodes:
        assert node_id not in node_ids
        node_ids.add(node_id)

# Test evidence-backed only
for edge in await get_all_edges(assessment_id):
    assert len(edge.evidence) > 0
    # Verify evidence exists
    for ev_id in edge.evidence:
        assert await evidence_exists(ev_id)
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `GRAPH_MAX_DEPTH` | 6 | Max path depth for traversal |
| `GRAPH_MIN_EDGE_WEIGHT` | 0.3 | Minimum edge confidence to traverse |
| `GRAPH_REBUILD_ON_FINDING` | true | Auto-rebuild when findings change |
| `GRAPH_LAYOUT_DEFAULT` | dagre | Default layout algorithm |
| `GRAPH_EXPORT_DPI` | 300 | PNG export resolution |

## Future Enhancements

- **Attack Simulation**: Monte Carlo simulation of attack success probability
- **Mitigation Analysis**: What-if analysis for remediation impact
- **Temporal Graphs**: Graph evolution over assessment timeline
- **Multi-Assessment Graphs**: Cross-assessment relationship mapping
- **MITRE ATT&CK Overlay**: Map paths to ATT&CK tactics/techniques

---

*Attack graph version: 1.0*
*Last updated: 2026-11-06*
"""
pathlib.Path("C:/Users/nanda/OneDrive/Desktop/RAVEN/docs/attack-graph.md").write_text(content, encoding="utf-8")
print("done")
