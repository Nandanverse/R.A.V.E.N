import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Search,
  Filter,
  RefreshCw,
  AlertTriangle,
  Shield,
  Database,
  ChevronDown,
  ChevronUp,
  MoreHorizontal,
  ExternalLink,
  FileText,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Table, Column } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Modal } from "@/components/ui/Modal";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import clsx from "clsx";
import type { Vulnerability, PaginatedResponse } from "@/types/api";

const severityColors: Record<string, string> = {
  CRITICAL: "critical",
  HIGH: "high",
  MEDIUM: "medium",
  LOW: "low",
  INFO: "info",
};

export function Intel() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [cveFilter, setCveFilter] = useState("");
  const [minCvss, setMinCvss] = useState("");
  const [maxCvss, setMaxCvss] = useState("");
  const [kevFilter, setKevFilter] = useState<boolean | "">("");
  const [selectedVuln, setSelectedVuln] = useState<Vulnerability | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [sortBy, setSortBy] = useState<string>("");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const { data: vulnsData, isLoading, error } = useQuery({
    queryKey: ["vulnerabilities", page, pageSize, cveFilter, minCvss, maxCvss, kevFilter],
    queryFn: () =>
      api.get<PaginatedResponse<Vulnerability>>("/intel/vulnerabilities", {
        page,
        page_size: pageSize,
        cve_id: cveFilter || undefined,
        min_cvss: minCvss ? parseFloat(minCvss) : undefined,
        max_cvss: maxCvss ? parseFloat(maxCvss) : undefined,
        cisa_kev: kevFilter === "true" ? true : kevFilter === "false" ? false : undefined,
      }),
  });

  const refreshMutation = useMutation({
    mutationFn: () => api.post("/intel/refresh", { sources: ["nvd", "cisa_kev", "epss", "mitre"] }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vulnerabilities"] });
    },
  });

  const columns: Column<Vulnerability>[] = [
    {
      key: "cve_id",
      header: "CVE ID",
      sortable: true,
      render: (v) => (
        <div className="flex items-center gap-2">
          {v.cve_id ? (
            <span className="mono font-medium text-fg-primary">{v.cve_id}</span>
          ) : (
            <span className="text-fg-muted">—</span>
          )}
          {v.cisa_kev && <Badge variant="critical">KEV</Badge>}
        </div>
      ),
    },
    {
      key: "title",
      header: "Title",
      sortable: true,
      render: (v) => <p className="truncate max-w-md">{v.title}</p>,
    },
    {
      key: "cvss_score",
      header: "CVSS",
      sortable: true,
      render: (v) => v.cvss_score !== null && v.cvss_score !== undefined ? (
        <Badge variant={severityColors[getSeverityFromCvss(v.cvss_score)] || "default"}>
          {v.cvss_score.toFixed(1)}
        </Badge>
      ) : (
        <span className="text-fg-muted">—</span>
      ),
    },
    {
      key: "epss_score",
      header: "EPSS",
      sortable: true,
      render: (v) => v.epss_score !== null && v.epss_score !== undefined ? (
        <span className="mono">{v.epss_score < 0.5 ? "text-fg-primary" : "text-sev-high"}{(v.epss_score * 100).toFixed(1)}%</span>
      ) : (
        <span className="text-fg-muted">—</span>
      ),
    },
    {
      key: "mitre_techniques",
      header: "MITRE ATT&CK",
      render: (v) => (
        <div className="flex flex-wrap gap-1">
          {v.mitre_techniques.slice(0, 3).map((t) => (
            <span key={t} className="code text-xs">{t}</span>
          ))}
          {v.mitre_techniques.length > 3 && (
            <span className="text-fg-muted text-xs">+{v.mitre_techniques.length - 3} more</span>
          )}
        </div>
      ),
    },
    {
      key: "source",
      header: "Source",
      sortable: true,
      render: (v) => <span className="mono text-fg-secondary">{v.source}</span>,
    },
    {
      key: "fetched_at",
      header: "Fetched",
      sortable: true,
      render: (v) => <span className="mono text-fg-secondary">{new Date(v.fetched_at).toLocaleDateString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (v) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            { label: "View Details", onClick: () => { setSelectedVuln(v); setIsDetailModalOpen(true); } },
            { label: "NVD Entry", onClick: () => v.cve_id && window.open(`https://nvd.nist.gov/vuln/detail/${v.cve_id}`, "_blank") },
            { label: "CISA KEV", onClick: () => v.cisa_kev && window.open("https://www.cisa.gov/known-exploited-vulnerabilities-catalog", "_blank") },
          ]}
          align="right"
        />
      ),
    },
  ];

  function getSeverityFromCvss(score: number): string {
    if (score >= 9.0) return "CRITICAL";
    if (score >= 7.0) return "HIGH";
    if (score >= 4.0) return "MEDIUM";
    if (score > 0) return "LOW";
    return "INFO";
  }

  if (isLoading) {
    return (
      <div className="p-4 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-fg-primary">Vulnerability Intelligence</h1>
            <p className="text-sm text-fg-muted">CVE, CVSS, EPSS, CISA KEV, and MITRE ATT&CK data</p>
          </div>
        </div>
        <Table columns={columns} data={[]} keyExtractor={(v) => v.id} isLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Vulnerability Intelligence</h1>
        </div>
        <EmptyState
          icon={<AlertCircle size={48} />}
          title="Failed to load vulnerabilities"
          description={error.message}
        />
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Vulnerability Intelligence</h1>
          <p className="text-sm text-fg-muted">CVE, CVSS, EPSS, CISA KEV, and MITRE ATT&CK data</p>
        </div>
        <button className="btn-secondary" onClick={() => refreshMutation.mutate()} disabled={refreshMutation.isPending}>
          <RefreshCw size={16} className={refreshMutation.isPending ? "animate-spin" : ""} />
          Refresh Intelligence
        </button>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <input
              type="text"
              placeholder="CVE ID (e.g., CVE-2024-1234)"
              value={cveFilter}
              onChange={(e) => { setCveFilter(e.target.value.toUpperCase()); setPage(1); }}
              className="input w-[200px]"
            />
            <input
              type="number"
              step="0.1"
              min="0"
              max="10"
              placeholder="Min CVSS"
              value={minCvss}
              onChange={(e) => { setMinCvss(e.target.value); setPage(1); }}
              className="input w-[100px]"
            />
            <input
              type="number"
              step="0.1"
              min="0"
              max="10"
              placeholder="Max CVSS"
              value={maxCvss}
              onChange={(e) => { setMaxCvss(e.target.value); setPage(1); }}
              className="input w-[100px]"
            />
            <Select
              value={kevFilter}
              onChange={(e) => { setKevFilter(e.target.value as boolean | ""); setPage(1); }}
              options={[
                { value: "", label: "All" },
                { value: "true", label: "KEV Only" },
                { value: "false", label: "Non-KEV" },
              ]}
              className="w-[140px]"
            />
          </div>
          <select
            value={pageSize}
            onChange={(e) => { setPageSize(Number(e.target.value)); setPage(1); }}
            className="input w-[80px]"
          >
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
            <option value={200}>200</option>
          </select>
        </CardHeader>
        <CardBody>
          {vulnsData?.items.length === 0 ? (
            <EmptyState
              icon={<Database size={48} />}
              title="No vulnerabilities found"
              description="Refresh intelligence to fetch latest data from NVD, CISA KEV, EPSS, and MITRE ATT&CK."
            />
          ) : (
            <>
              <Table
                columns={columns}
                data={vulnsData.items}
                keyExtractor={(v) => v.id}
                sortBy={sortBy}
                sortOrder={sortOrder}
                onSort={(key) => {
                  if (sortBy === key) {
                    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
                  } else {
                    setSortBy(key);
                    setSortOrder("asc");
                  }
                }}
              />
              <Pagination currentPage={page} totalPages={vulnsData.total_pages} onPageChange={setPage} />
            </>
          )}
        </CardBody>
      </Card>

      <Modal isOpen={isDetailModalOpen} onClose={() => { setIsDetailModalOpen(false); setSelectedVuln(null); }} title={selectedVuln?.cve_id || "Vulnerability Details"} size="lg">
        {selectedVuln && (
          <div className="space-y-4">
            <div className="flex items-center gap-4 flex-wrap">
              {selectedVuln.cve_id && <span className="mono font-medium text-lg">{selectedVuln.cve_id}</span>}
              {selectedVuln.cisa_kev && <Badge variant="critical">CISA KEV</Badge>}
              {selectedVuln.cvss_score !== null && selectedVuln.cvss_score !== undefined && (
                <Badge variant={severityColors[getSeverityFromCvss(selectedVuln.cvss_score)] || "default"}>
                  CVSS {selectedVuln.cvss_score.toFixed(1)}
                </Badge>
              )}
              {selectedVuln.epss_score !== null && selectedVuln.epss_score !== undefined && (
                <Badge variant="info">EPSS {(selectedVuln.epss_score * 100).toFixed(1)}%</Badge>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Title</h4>
                <p className="text-fg-primary">{selectedVuln.title}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Source</h4>
                <p className="text-fg-primary mono">{selectedVuln.source}</p>
              </div>
            </div>

            {selectedVuln.description && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Description</h4>
                <p className="text-fg-primary text-sm">{selectedVuln.description}</p>
              </div>
            )}

            {selectedVuln.cvss_vector && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">CVSS Vector</h4>
                <p className="text-fg-primary mono text-sm">{selectedVuln.cvss_vector}</p>
              </div>
            )}

            {selectedVuln.mitre_techniques.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">MITRE ATT&CK Techniques</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedVuln.mitre_techniques.map((t) => (
                    <span key={t} className="code text-sm">{t}</span>
                  ))}
                </div>
              </div>
            )}

            {selectedVuln.references.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">References</h4>
                <ul className="space-y-1">
                  {selectedVuln.references.map((ref, i) => (
                    <li key={i}>
                      <a href={ref} target="_blank" rel="noopener noreferrer" className="text-sev-info hover:underline text-sm flex items-center gap-1">
                        {ref}
                        <ExternalLink size={12} />
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex items-center justify-between pt-4 border-t border-border">
              <div className="text-sm text-fg-muted">
                Fetched: {new Date(selectedVuln.fetched_at).toLocaleString()}
                {selectedVuln.published_at && <span className="ml-4">Published: {new Date(selectedVuln.published_at).toLocaleDateString()}</span>}
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

import { RefreshCw, AlertCircle, Database, MoreHorizontal, ExternalLink, Shield } from "lucide-react";