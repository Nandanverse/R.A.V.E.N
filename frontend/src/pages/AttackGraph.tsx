import { useState, useEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Search,
  Filter,
  Target,
  GitBranch,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Download,
  ChevronDown,
  ChevronUp,
  MoreHorizontal,
  AlertTriangle,
  CheckCircle,
  Shield,
  Server,
  Database,
  Globe,
  Network,
  Code,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Select } from "@/components/ui/Form";
import clsx from "clsx";
import type { GraphNode, GraphEdge, AttackPath, PaginatedResponse, GraphData } from "@/types/api";
import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";
import dagre from "cytoscape-dagre";

cytoscape.use(coseBilkent);
cytoscape.use(dagre);

const nodeTypeIcons: Record<string, React.ComponentType<{ size?: number }>> = {
  HOST: Server,
  IP_ADDRESS: Server,
  DOMAIN: Globe,
  WEB_APP: Database,
  API: Code,
  SERVICE: Network,
  TECHNOLOGY: Code,
  NETWORK: Network,
  VULNERABILITY: Shield,
  FINDING: AlertTriangle,
  ATTACK_PATH: Target,
};

const nodeTypeColors: Record<string, string> = {
  HOST: "#3b82f6",
  IP_ADDRESS: "#3b82f6",
  DOMAIN: "#06b6d4",
  WEB_APP: "#8b5cf6",
  API: "#8b5cf6",
  SERVICE: "#10b981",
  TECHNOLOGY: "#f59e0b",
  NETWORK: "#6366f1",
  VULNERABILITY: "#ef4444",
  FINDING: "#f97316",
  ATTACK_PATH: "#ec4899",
};

export function AttackGraph() {
  const [assessmentId, setAssessmentId] = useState<string>("");
  const [layout, setLayout] = useState<"cose-bilkent" | "dagre">("cose-bilkent");
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);
  const [showPaths, setShowPaths] = useState(false);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-list"],
    queryFn: () => api.get<PaginatedResponse<{ id: string; name: string }>>("/assessments", { page_size: 100 }),
  });

  const { data: graphData, isLoading, error } = useQuery({
    queryKey: ["attack-graph", assessmentId],
    queryFn: () => api.get<GraphData>(`/graph/assessments/${assessmentId}/graph`),
    enabled: !!assessmentId,
  });

  const { data: pathsData } = useQuery({
    queryKey: ["attack-paths", assessmentId],
    queryFn: () => api.get<PaginatedResponse<AttackPath>>(`/graph/assessments/${assessmentId}/paths`),
    enabled: !!assessmentId && showPaths,
  });

  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements: [
        ...graphData.nodes.map((n) => ({
          data: {
            id: n.id,
            label: n.label,
            type: n.node_type,
            ...n.data,
          },
          classes: n.node_type.toLowerCase(),
        })),
        ...graphData.edges.map((e) => ({
          data: {
            id: e.id,
            source: e.source_id,
            target: e.target_id,
            label: e.label,
            type: e.edge_type,
            weight: e.weight,
            ...e.data,
          },
        })),
      ],
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "font-size": "11px",
            "font-family": "JetBrains Mono, monospace",
            "text-valign": "bottom",
            "text-halign": "center",
            "text-margin-y": 10,
            "background-color": (ele: cytoscape.NodeSingular) => nodeTypeColors[ele.data("type")] || "#6a6a6a",
            "border-width": 2,
            "border-color": "#0d0d0d",
            width: 40,
            height: 40,
            "overlay-padding": 6,
            "z-index": 10,
          },
        },
        {
          selector: "node:selected",
          style: {
            "border-color": "#3b82f6",
            "border-width": 3,
            "z-index": 20,
          },
        },
        {
          selector: "edge",
          style: {
            width: (ele: cytoscape.EdgeSingular) => Math.max(1, ele.data("weight") * 2),
            "line-color": "#2a2a2a",
            "target-arrow-color": "#2a2a2a",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "font-size": "9px",
            "font-family": "JetBrains Mono, monospace",
            label: "data(label)",
            "text-rotation": "autorotate",
            "text-margin-y": -8,
            "color": "#a0a0a0",
          },
        },
        {
          selector "edge:selected",
          style: {
            "line-color": "#3b82f6",
            "target-arrow-color": "#3b82f6",
            width: 3,
            "z-index": 20,
          },
        },
        {
          selector: ".vulnerability",
          style: {
            shape: "diamond",
          },
        },
        {
          selector: ".finding",
          style: {
            shape: "hexagon",
          },
        },
        {
          selector: ".attack_path",
          style: {
            shape: "star",
          },
        },
      ],
      layout: {
        name: layout,
        animate: false,
        fit: true,
        padding: 50,
        ...(layout === "dagre" ? { rankDir: "LR" } : {}),
      },
      minZoom: 0.1,
      maxZoom: 3,
      wheelSensitivity: 0.1,
    });

    cyRef.current = cy;

    cy.on("tap", (event) => {
      if (event.target === cy) {
        setSelectedNode(null);
        setSelectedEdge(null);
      }
    });

    cy.on("tap", "node", (event) => {
      const node = event.target;
      const nodeData = graphData.nodes.find((n) => n.id === node.id());
      if (nodeData) setSelectedNode(nodeData);
      setSelectedEdge(null);
    });

    cy.on("tap", "edge", (event) => {
      const edge = event.target;
      const edgeData = graphData.edges.find((e) => e.id === edge.id());
      if (edgeData) setSelectedEdge(edgeData);
      setSelectedNode(null);
    });

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [graphData, layout, assessmentId]);

  const handleLayoutChange = (newLayout: "cose-bilkent" | "dagre") => {
    setLayout(newLayout);
    if (cyRef.current) {
      cyRef.current.layout({ name: newLayout, animate: false, fit: true, padding: 50, ...(newLayout === "dagre" ? { rankDir: "LR" } : {}) }).run();
    }
  };

  const fitToScreen = () => {
    cyRef.current?.fit(50);
  };

  const resetZoom = () => {
    cyRef.current?.zoom(1);
    cyRef.current?.pan({ x: 0, y: 0 });
  };

  const assessmentOptions = [
    { value: "", label: "Select Assessment" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  if (!assessmentId) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Attack Graph</h1>
          <p className="text-sm text-fg-muted">Visualize asset relationships and attack paths</p>
        </div>
        <Card>
          <CardBody className="flex flex-col items-center justify-center py-12">
            <EmptyState
              icon={<GitBranch size={48} />}
              title="Select an assessment"
              description="Choose an assessment from the dropdown to visualize its attack graph."
            />
          </CardBody>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6 h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Attack Graph</h1>
          <p className="text-sm text-fg-muted">Visualize asset relationships and attack paths</p>
        </div>
        <div className="flex items-center gap-2">
          <Select
            value={assessmentId}
            onChange={(e) => setAssessmentId(e.target.value)}
            options={assessmentOptions}
            className="w-[300px]"
          />
          {graphData && (
            <>
              <span className="text-sm text-fg-muted">
                {graphData.nodes.length} nodes, {graphData.edges.length} edges
              </span>
            </>
          )}
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden min-h-0">
        <div className="flex-1 relative" ref={containerRef} style={{ minWidth: 0, minHeight: 0 }} />

        <div className="w-80 bg-bg-elevated border-l border-border flex flex-col">
          <div className="p-3 border-b border-border flex items-center justify-between">
            <h3 className="font-medium text-fg-primary">Controls</h3>
          </div>
          <div className="p-3 border-b border-border">
            <label className="text-sm text-fg-secondary block mb-2">Layout</label>
            <div className="flex gap-2">
              <button
                className={clsx("btn-secondary flex-1 text-xs", layout === "cose-bilkent" && "bg-sev-info/10 border-sev-info")}
                onClick={() => handleLayoutChange("cose-bilkent")}
              >
                Cose-Bilkent
              </button>
              <button
                className={clsx("btn-secondary flex-1 text-xs", layout === "dagre" && "bg-sev-info/10 border-sev-info")}
                onClick={() => handleLayoutChange("dagre")}
              >
                Dagre (LR)
              </button>
            </div>
          </div>
          <div className="p-3 border-b border-border">
            <div className="flex gap-2">
              <button className="btn-secondary flex-1 text-xs" onClick={fitToScreen} title="Fit to screen">
                <ZoomIn size={14} />
              </button>
              <button className="btn-secondary flex-1 text-xs" onClick={resetZoom} title="Reset zoom">
                <ZoomOut size={14} />
              </button>
              <button className="btn-secondary flex-1 text-xs" onClick={() => cyRef.current?.layout({ name: layout, animate: false, fit: true, padding: 50 }).run()} title="Relayout">
                <RotateCcw size={14} />
              </button>
            </div>
          </div>
          <div className="p-3 border-b border-border">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={showPaths}
                onChange={(e) => setShowPaths(e.target.checked)}
                className="w-4 h-4 rounded border-border bg-bg-base text-sev-info focus:ring-sev-info"
              />
              <span className="text-fg-primary">Show Attack Paths</span>
            </label>
          </div>
          <div className="p-3 flex-1 overflow-y-auto">
            {selectedNode && (
              <NodeDetailsPanel node={selectedNode} graphData={graphData} onClose={() => { setSelectedNode(null); cyRef.current?.$(`#${selectedNode.id}`).unselect(); }} />
            )}
            {selectedEdge && !selectedNode && (
              <EdgeDetailsPanel edge={selectedEdge} onClose={() => { setSelectedEdge(null); cyRef.current?.$(`#${selectedEdge.id}`).unselect(); }} />
            )}
            {!selectedNode && !selectedEdge && (
              <EmptyState
                icon={<GitBranch size={32} />}
                title="Select a node or edge"
                description="Click on a graph element to view details."
                className="py-8"
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

interface NodeDetailsPanelProps {
  node: GraphNode;
  graphData: GraphData;
  onClose: () => void;
}

function NodeDetailsPanel({ node, graphData, onClose }: NodeDetailsPanelProps) {
  const connectedEdges = graphData.edges.filter((e) => e.source_id === node.id || e.target_id === node.id);
  const connectedNodes = connectedEdges.map((e) =>
    graphData.nodes.find((n) => n.id === (e.source_id === node.id ? e.target_id : e.source_id))
  ).filter(Boolean);

  const Icon = nodeTypeIcons[node.node_type] || Server;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon size={20} className="text-sev-info" />
          <div>
            <p className="font-medium text-fg-primary">{node.label}</p>
            <p className="text-xs text-fg-muted mono">{node.node_type}</p>
          </div>
        </div>
        <button className="btn-ghost p-1" onClick={onClose}><X size={16} /></button>
      </div>

      <div className="border-t border-border pt-3 space-y-2">
        <div className="grid grid-cols-2 gap-2 text-sm">
          <span className="text-fg-muted">ID</span>
          <span className="mono text-fg-primary truncate">{node.id}</span>
          <span className="text-fg-muted">Type</span>
          <span className="text-fg-primary">{node.node_type}</span>
          <span className="text-fg-muted">Asset ID</span>
          <span className="mono text-fg-primary">{node.asset_id || "—"}</span>
        </div>
      </div>

      {Object.keys(node.data).length > 0 && (
        <div className="border-t border-border pt-3">
          <h4 className="text-sm font-medium text-fg-secondary mb-2">Data</h4>
          <div className="text-xs text-fg-primary font-mono max-h-40 overflow-y-auto">
            <pre>{JSON.stringify(node.data, null, 2)}</pre>
          </div>
        </div>
      )}

      {connectedEdges.length > 0 && (
        <div className="border-t border-border pt-3">
          <h4 className="text-sm font-medium text-fg-secondary mb-2">Connections ({connectedEdges.length})</h4>
          <div className="space-y-1 max-h-40 overflow-y-auto">
            {connectedEdges.map((e) => (
              <div key={e.id} className="text-xs flex items-center gap-1 text-fg-secondary">
                <span className="mono">{e.edge_type}</span>
                <span>{e.source_id === node.id ? "→" : "←"}</span>
                <span className="truncate">{connectedNodes.find((n) => n?.id === (e.source_id === node.id ? e.target_id : e.source_id))?.label || e.source_id === node.id ? e.target_id : e.source_id}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

interface EdgeDetailsPanelProps {
  edge: GraphEdge;
  onClose: () => void;
}

function EdgeDetailsPanel({ edge, onClose }: EdgeDetailsPanelProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium text-fg-primary">{edge.edge_type}</p>
          <p className="text-xs text-fg-muted mono">{edge.label || "No label"}</p>
        </div>
        <button className="btn-ghost p-1" onClick={onClose}><X size={16} /></button>
      </div>

      <div className="border-t border-border pt-3 space-y-2 text-sm">
        <div className="grid grid-cols-2 gap-2">
          <span className="text-fg-muted">ID</span>
          <span className="mono text-fg-primary truncate">{edge.id}</span>
          <span className="text-fg-muted">Source</span>
          <span className="mono text-fg-primary truncate">{edge.source_id}</span>
          <span className="text-fg-muted">Target</span>
          <span className="mono text-fg-primary truncate">{edge.target_id}</span>
          <span className="text-fg-muted">Weight</span>
          <span className="text-fg-primary">{edge.weight}</span>
        </div>
      </div>

      {edge.evidence_ids.length > 0 && (
        <div className="border-t border-border pt-3">
          <h4 className="text-sm font-medium text-fg-secondary mb-2">Evidence ({edge.evidence_ids.length})</h4>
          <div className="flex flex-wrap gap-1">
            {edge.evidence_ids.map((eid) => (
              <span key={eid} className="code text-xs">{eid.slice(0, 8)}...</span>
            ))}
          </div>
        </div>
      )}

      {Object.keys(edge.data).length > 0 && (
        <div className="border-t border-border pt-3">
          <h4 className="text-sm font-medium text-fg-secondary mb-2">Data</h4>
          <div className="text-xs text-fg-primary font-mono max-h-40 overflow-y-auto">
            <pre>{JSON.stringify(edge.data, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

import { X } from "lucide-react";