import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Search,
  Filter,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Shield,
  FileText,
  ChevronDown,
  ChevronUp,
  MoreHorizontal,
  Eye,
  Edit,
  Trash2,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Table, Column } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Modal } from "@/components/ui/Modal";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Form, FormField, Select, Textarea } from "@/components/ui/Form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import clsx from "clsx";
import type { Finding, FindingStatus, Severity, FindingUpdate, Evidence, PaginatedResponse } from "@/types/api";

const findingUpdateSchema = z.object({
  status: z.enum(["DISCOVERED", "SUSPECTED", "SCANNER_REPORTED", "VALIDATED", "FALSE_POSITIVE", "DEMONSTRATED"]).optional(),
  severity: z.enum(["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]).optional(),
  risk_score: z.number().min(0).max(100).optional(),
  remediation: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

type FindingUpdateFormData = z.infer<typeof findingUpdateSchema>;

const statusColors: Record<FindingStatus, string> = {
  DISCOVERED: "default",
  SUSPECTED: "warning",
  SCANNER_REPORTED: "info",
  VALIDATED: "success",
  FALSE_POSITIVE: "error",
  DEMONSTRATED: "critical",
};

const statusLabels: Record<FindingStatus, string> = {
  DISCOVERED: "Discovered",
  SUSPECTED: "Suspected",
  SCANNER_REPORTED: "Scanner Reported",
  VALIDATED: "Validated",
  FALSE_POSITIVE: "False Positive",
  DEMONSTRATED: "Demonstrated",
};

const severityColors: Record<Severity, string> = {
  CRITICAL: "critical",
  HIGH: "high",
  MEDIUM: "medium",
  LOW: "low",
  INFO: "info",
};

export function Findings() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [statusFilter, setStatusFilter] = useState<FindingStatus | "">("");
  const [severityFilter, setSeverityFilter] = useState<Severity | "">("");
  const [assessmentFilter, setAssessmentFilter] = useState<string>("");  const [search, setSearch] = useState("");
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [sortBy, setSortBy] = useState<string>("");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-list"],
    queryFn: () => api.get<PaginatedResponse<{ id: string; name: string }>>("/assessments", { page_size: 100 }),
  });

  const { data: findingsData, isLoading, error } = useQuery({
    queryKey: ["findings", page, pageSize, statusFilter, severityFilter, assessmentFilter, search],
    queryFn: () =>
      api.get<PaginatedResponse<Finding>>("/findings", {
        page,
        page_size: pageSize,
        status: statusFilter || undefined,
        severity: severityFilter || undefined,
        assessment_id: assessmentFilter || undefined,
      }),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: FindingUpdate }) =>
      api.patch<Finding>(`/findings/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["findings"] });
      setIsEditModalOpen(false);
    },
  });

  const editForm = useForm<FindingUpdateFormData>({
    resolver: zodResolver(findingUpdateSchema),
    defaultValues: {},
  });

  const assessmentOptions = [
    { value: "", label: "All Assessments" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const columns: Column<Finding>[] = [
    {
      key: "title",
      header: "Title",
      sortable: true,
      render: (f) => (
        <div>
          <p className="font-medium text-fg-primary truncate max-w-md">{f.title}</p>
          {f.description && <p className="text-sm text-fg-muted truncate max-w-md">{f.description}</p>}
        </div>
      ),
    },
    {
      key: "severity",
      header: "Severity",
      sortable: true,
      render: (f) => <Badge variant={severityColors[f.severity]}>{f.severity}</Badge>,
    },
    {
      key: "status",
      header: "Status",
      sortable: true,
      render: (f) => <Badge variant={statusColors[f.status]}>{statusLabels[f.status]}</Badge>,
    },
    {
      key: "risk_score",
      header: "Risk Score",
      sortable: true,
      render: (f) => f.risk_score !== null && f.risk_score !== undefined ? (
        <span className="mono font-medium">{f.risk_score.toFixed(1)}</span>
      ) : (
        <span className="text-fg-muted">—</span>
      ),
    },
    {
      key: "cvss_score",
      header: "CVSS",
      sortable: true,
      render: (f) => f.cvss_score !== null && f.cvss_score !== undefined ? (
        <Badge variant={severityColors[getSeverityFromCvss(f.cvss_score)] || "default"}>
          {f.cvss_score.toFixed(1)}
        </Badge>
      ) : (
        <span className="text-fg-muted">—</span>
      ),
    },
    {
      key: "discovered_at",
      header: "Discovered",
      sortable: true,
      render: (f) => <span className="mono text-fg-secondary">{new Date(f.discovered_at).toLocaleDateString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (f) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            { label: "View Details", onClick: () => { setSelectedFinding(f); setIsDetailModalOpen(true); } },
            { label: "View Evidence", onClick: () => {} },
            { label: "divider" },
            { label: "Edit", onClick: () => { setSelectedFinding(f); setIsEditModalOpen(true); } },
            { label: "divider" },
            {
              label: "Mark Validated",
              onClick: () => updateMutation.mutate({ id: f.id, data: { status: "VALIDATED" } }),
              disabled: f.status === "VALIDATED",
            },
            {
              label: "Mark False Positive",
              onClick: () => updateMutation.mutate({ id: f.id, data: { status: "FALSE_POSITIVE" } }),
              disabled: f.status === "FALSE_POSITIVE",
              danger: true,
            },
          ]}
          align="right"
        />
      ),
    },
  ];

  function getSeverityFromCvss(score: number): Severity {
    if (score >= 9.0) return "CRITICAL";
    if (score >= 7.0) return "HIGH";
    if (score >= 4.0) return "MEDIUM";
    if (score > 0) return "LOW";
    return "INFO";
  }

  const handleEditSubmit = (data: FindingUpdateFormData) => {
    if (selectedFinding) {
      updateMutation.mutate({ id: selectedFinding.id, data });
    }
  };

  if (isLoading) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Findings</h1>
          <p className="text-sm text-fg-muted">Vulnerability findings with validation status</p>
        </div>
        <Table columns={columns} data={[]} keyExtractor={(f) => f.id} isLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Findings</h1>
        </div>
        <EmptyState
          icon={<AlertCircle size={48} />}
          title="Failed to load findings"
          description={error.message}
        />
      </div>
    );
  }

  if (selectedFinding) {
    editForm.reset({
      status: selectedFinding.status,
      severity: selectedFinding.severity,
      risk_score: selectedFinding.risk_score,
      remediation: selectedFinding.remediation || "",
      tags: selectedFinding.tags,
    });
  }

  return (
    <div className="p-4 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-fg-primary">Findings</h1>
        <p className="text-sm text-fg-muted">Vulnerability findings with validation status</p>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Select
              value={assessmentFilter}
              onChange={(e) => { setAssessmentFilter(e.target.value); setPage(1); }}
              options={assessmentOptions}
              className="w-[200px]"
            />
            <Select
              value={statusFilter}
              onChange={(e) => { setStatusFilter(e.target.value as FindingStatus); setPage(1); }}
              options={[
                { value: "", label: "All Statuses" },
                { value: "DISCOVERED", label: "Discovered" },
                { value: "SUSPECTED", label: "Suspected" },
                { value: "SCANNER_REPORTED", label: "Scanner Reported" },
                { value: "VALIDATED", label: "Validated" },
                { value: "FALSE_POSITIVE", label: "False Positive" },
                { value: "DEMONSTRATED", label: "Demonstrated" },
              ]}
              className="w-[180px]"
            />
            <Select
              value={severityFilter}
              onChange={(e) => { setSeverityFilter(e.target.value as Severity); setPage(1); }}
              options={[
                { value: "", label: "All Severities" },
                { value: "CRITICAL", label: "Critical" },
                { value: "HIGH", label: "High" },
                { value: "MEDIUM", label: "Medium" },
                { value: "LOW", label: "Low" },
                { value: "INFO", label: "Info" },
              ]}
              className="w-[160px]"
            />
            <input
              type="text"
              placeholder="Search findings..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="input w-[250px]"
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
          </select>
        </CardHeader>
        <CardBody>
          {findingsData?.items.length === 0 ? (
            <EmptyState
              icon={<AlertTriangle size={48} />}
              title="No findings found"
              description="Run assessments and scans to discover vulnerabilities."
            />
          ) : (
            <>
              <Table
                columns={columns}
                data={findingsData.items}
                keyExtractor={(f) => f.id}
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
              <Pagination currentPage={page} totalPages={findingsData.total_pages} onPageChange={setPage} />
            </>
          )}
        </CardBody>
      </Card>

      <Modal isOpen={isDetailModalOpen} onClose={() => { setIsDetailModalOpen(false); setSelectedFinding(null); }} title={selectedFinding?.title || "Finding Details"} size="xl">
        {selectedFinding && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center gap-3">
              <Badge variant={severityColors[selectedFinding.severity]}>{selectedFinding.severity}</Badge>
              <Badge variant={statusColors[selectedFinding.status]}>{statusLabels[selectedFinding.status]}</Badge>
              {selectedFinding.risk_score !== null && selectedFinding.risk_score !== undefined && (
                <Badge variant="info">Risk: {selectedFinding.risk_score.toFixed(1)}</Badge>
              )}
              {selectedFinding.cvss_score !== null && selectedFinding.cvss_score !== undefined && (
                <Badge variant={severityColors[getSeverityFromCvss(selectedFinding.cvss_score)] || "default"}>CVSS: {selectedFinding.cvss_score.toFixed(1)}</Badge>
              )}
              {selectedFinding.vulnerability_id && <Badge variant="default">CVE Linked</Badge>}
            </div>

            {selectedFinding.description && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Description</h4>
                <p className="text-fg-primary">{selectedFinding.description}</p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Remediation</h4>
                <p className="text-fg-primary">{selectedFinding.remediation || "No remediation provided"}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Tags</h4>
                <div className="flex flex-wrap gap-1">
                  {selectedFinding.tags.length > 0 ? (
                    selectedFinding.tags.map((t) => <span key={t} className="code text-xs">{t}</span>)
                  ) : (
                    <span className="text-fg-muted">None</span>
                  )}
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-fg-secondary mb-2">Timeline</h4>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-fg-muted">Discovered</p>
                  <p className="mono text-fg-primary">{new Date(selectedFinding.discovered_at).toLocaleString()}</p>
                </div>
                {selectedFinding.validated_at && (
                  <div>
                    <p className="text-fg-muted">Validated</p>
                    <p className="mono text-fg-primary">{new Date(selectedFinding.validated_at).toLocaleString()}</p>
                  </div>
                )}
                <div>
                  <p className="text-fg-muted">Created</p>
                  <p className="mono text-fg-primary">{new Date(selectedFinding.created_at).toLocaleString()}</p>
                </div>
              </div>
            </div>

            {selectedFinding.evidence_ids.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Evidence ({selectedFinding.evidence_ids.length})</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedFinding.evidence_ids.map((eid) => (
                    <span key={eid} className="code text-xs">{eid.slice(0, 8)}...</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>

      <Modal isOpen={isEditModalOpen} onClose={() => { setIsEditModalOpen(false); setSelectedFinding(null); editForm.reset(); }} title="Edit Finding" size="md">
        {selectedFinding && (
          <form onSubmit={editForm.handleSubmit(handleEditSubmit)} className="space-y-4">
            <FormField control={editForm.control} name="status" label="Status">
              {({ onChange, onBlur, value, ref }) => (
                <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={[
                  { value: "DISCOVERED", label: "Discovered" },
                  { value: "SUSPECTED", label: "Suspected" },
                  { value: "SCANNER_REPORTED", label: "Scanner Reported" },
                  { value: "VALIDATED", label: "Validated" },
                  { value: "FALSE_POSITIVE", label: "False Positive" },
                  { value: "DEMONSTRATED", label: "Demonstrated" },
                ]} />
              )}
            </FormField>
            <FormField control={editForm.control} name="severity" label="Severity">
              {({ onChange, onBlur, value, ref }) => (
                <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={[
                  { value: "CRITICAL", label: "Critical" },
                  { value: "HIGH", label: "High" },
                  { value: "MEDIUM", label: "Medium" },
                  { value: "LOW", label: "Low" },
                  { value: "INFO", label: "Info" },
                ]} />
              )}
            </FormField>
            <FormField control={editForm.control} name="risk_score" label="Risk Score (0-100)">
              {({ onChange, onBlur, value, ref }) => (
                <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} type="number" min="0" max="100" step="0.1" placeholder="Risk score" />
              )}
            </FormField>
            <FormField control={editForm.control} name="remediation" label="Remediation">
              {({ onChange, onBlur, value, ref }) => (
                <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Remediation steps" rows={4} />
              )}
            </FormField>
            <div className="flex justify-end gap-2 pt-4 border-t border-border">
              <button type="button" className="btn-secondary" onClick={() => { setIsEditModalOpen(false); setSelectedFinding(null); editForm.reset(); }}>Cancel</button>
              <button type="submit" className="btn-primary" disabled={updateMutation.isPending}>{updateMutation.isPending ? <LoadingSpinner size="sm" /> : "Save Changes"}</button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}

import { AlertCircle, AlertTriangle, CheckCircle, XCircle, Clock, Shield, FileText, MoreHorizontal } from "lucide-react";