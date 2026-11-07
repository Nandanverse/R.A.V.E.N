import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Brain,
  Search,
  Filter,
  CheckCircle,
  XCircle,
  Clock,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  MoreHorizontal,
  RefreshCw,
  Zap,
  FileText,
  MessageSquare,
  Shield,
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
import type { AIProposal, OllamaStatus, Assessment, PolicyDecision, PaginatedResponse, EvaluateResponse } from "@/types/api";

const proposalStatusColors: Record<string, string> = {
  pending: "warning",
  approved: "success",
  rejected: "error",
  executed: "info",
  failed: "error",
};

export function AIAnalysis() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [assessmentFilter, setAssessmentFilter] = useState<string>("");
  const [selectedProposal, setSelectedProposal] = useState<AIProposal | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [isEvaluateModalOpen, setIsEvaluateModalOpen] = useState(false);
  const [evaluateResult, setEvaluateResult] = useState<EvaluateResponse | null>(null);

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-running"],
    queryFn: () => api.get<PaginatedResponse<Assessment>>("/assessments", { status: "RUNNING", page_size: 100 }),
  });

  const { data: proposalsData, isLoading, error } = useQuery({
    queryKey: ["ai-proposals", page, pageSize, statusFilter, assessmentFilter],
    queryFn: () =>
      api.get<PaginatedResponse<AIProposal>>("/brain/proposals", {
        page,
        page_size: pageSize,
        status: statusFilter || undefined,
        assessment_id: assessmentFilter || undefined,
      }),
  });

  const { data: ollamaStatus } = useQuery({
    queryKey: ["ollama-status"],
    queryFn: () => api.get<OllamaStatus>("/brain/ollama/status"),
    refetchInterval: 30000,
  });

  const generateMutation = useMutation({
    mutationFn: (assessmentId: string) => api.post<AIProposal>("/brain/propose", { assessment_id: assessmentId, context: {} }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-proposals"] });
    },
  });

  const evaluateMutation = useMutation({
    mutationFn: (proposalId: string) => api.post<{ allowed: boolean; decision: string; reason: string; conditions: string[]; requires_approval: boolean; policy_decision_id?: string }>(`/brain/proposals/${proposalId}/evaluate`),
    onSuccess: (result) => {
      setEvaluateResult(result as EvaluateResponse);
      setIsEvaluateModalOpen(true);
      queryClient.invalidateQueries({ queryKey: ["ai-proposals"] });
    },
  });

  const assessmentOptions = [
    { value: "", label: "All Assessments" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const columns: Column<AIProposal>[] = [
    {
      key: "action",
      header: "Action",
      render: (p) => (
        <div>
          <p className="font-medium text-fg-primary mono">{p.action}</p>
          <p className="text-sm text-fg-muted truncate max-w-xs">{p.target}</p>
        </div>
      ),
    },
    {
      key: "reason",
      header: "Reason",
      render: (p) => <p className="text-sm text-fg-secondary truncate max-w-md">{p.reason}</p>,
    },
    {
      key: "risk_level",
      header: "Risk",
      render: (p) => <Badge variant={p.risk_level as any}>{p.risk_level}</Badge>,
    },
    {
      key: "confidence",
      header: "Confidence",
      render: (p) => (
        <div className="flex items-center gap-2">
          <div className="w-24 h-2 bg-bg-base border border-border rounded-full overflow-hidden">
            <div className="h-full bg-sev-info" style={{ width: `${Math.round(p.confidence * 100)}%` }} />
          </div>
          <span className="mono text-sm">{Math.round(p.confidence * 100)}%</span>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (p) => <Badge variant={proposalStatusColors[p.status] || "default"}>{p.status}</Badge>,
    },
    {
      key: "created_at",
      header: "Created",
      render: (p) => <span className="mono text-fg-secondary">{new Date(p.created_at).toLocaleString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (p) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            { label: "View Details", onClick: () => { setSelectedProposal(p); setIsDetailModalOpen(true); } },
            { label: "divider" },
            {
              label: "Evaluate Policy",
              onClick: () => evaluateMutation.mutate(p.id),
              disabled: p.status !== "pending",
            },
            {
              label: "View Policy Decision",
              onClick: () => {},
              disabled: !p.policy_decision_id,
            },
          ]}
          align="right"
        />
      ),
    },
  ];

  if (isLoading) {
    return (
      <div className="p-4 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-fg-primary">AI Analysis</h1>
            <p className="text-sm text-fg-muted">LLM-generated assessment proposals and policy evaluation</p>
          </div>
        </div>
        <Table columns={columns} data={[]} keyExtractor={(p) => p.id} isLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">AI Analysis</h1>
        </div>
        <EmptyState
          icon={<AlertTriangle size={48} />}
          title="Failed to load proposals"
          description={error.message}
        />
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">AI Analysis</h1>
          <p className="text-sm text-fg-muted">LLM-generated assessment proposals and policy evaluation</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className={clsx("w-2 h-2 rounded-full", ollamaStatus?.available ? "bg-status-success" : "bg-status-error")} />
            <span className="text-sm text-fg-secondary">
              {ollamaStatus?.available ? "Ollama Connected" : "Ollama Unavailable"}
            </span>
          </div>
          <button className="btn-secondary" onClick={() => generateMutation.mutate(assessmentFilter)} disabled={!assessmentFilter || generateMutation.isPending}>
            <Zap size={16} /> Generate Proposal
          </button>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Select
              value={assessmentFilter}
              onChange={(e) => { setAssessmentFilter(e.target.value); setPage(1); }}
              options={assessmentOptions}
              className="w-[250px]"
            />
            <Select
              value={statusFilter}
              onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
              options={[
                { value: "", label: "All Statuses" },
                { value: "pending", label: "Pending" },
                { value: "approved", label: "Approved" },
                { value: "rejected", label: "Rejected" },
                { value: "executed", label: "Executed" },
                { value: "failed", label: "Failed" },
              ]}
              className="w-[160px]"
            />
          </div>
          <select
            value={pageSize}
            onChange={(e) => { setPageSize(Number(e.target.value)); setPage(1); }}
            className="input w-[80px]"
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
          </select>
        </CardHeader>
        <CardBody>
          {proposalsData?.items.length === 0 ? (
            <EmptyState
              icon={<Brain size={48} />}
              title="No AI proposals found"
              description="Select a running assessment and generate proposals using the local LLM."
            />
          ) : (
            <>
              <Table
                columns={columns}
                data={proposalsData.items}
                keyExtractor={(p) => p.id}
              />
              <Pagination currentPage={page} totalPages={proposalsData.total_pages} onPageChange={setPage} />
            </>
          )}
        </CardBody>
      </Card>

      <Modal isOpen={isDetailModalOpen} onClose={() => { setIsDetailModalOpen(false); setSelectedProposal(null); }} title={selectedProposal?.action || "Proposal Details"} size="lg">
        {selectedProposal && (
          <div className="space-y-4">
            <div className="flex flex-wrap items-center gap-3">
              <Badge variant={proposalStatusColors[selectedProposal.status] || "default"}>{selectedProposal.status}</Badge>
              <Badge variant={selectedProposal.risk_level as any}>{selectedProposal.risk_level}</Badge>
              <Badge variant="info">Confidence: {Math.round(selectedProposal.confidence * 100)}%</Badge>
            </div>

            <div>
              <h4 className="text-sm font-medium text-fg-secondary mb-1">Target</h4>
              <p className="mono text-fg-primary">{selectedProposal.target}</p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-fg-secondary mb-1">Reasoning</h4>
              <p className="text-fg-primary">{selectedProposal.reason}</p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-fg-secondary mb-1">Required Evidence</h4>
              <ul className="space-y-1">
                {selectedProposal.required_evidence.map((e, i) => (
                  <li key={i} className="text-sm text-fg-primary flex items-center gap-2">
                    <Shield size={14} className="text-sev-info" />
                    {e}
                  </li>
                ))}
              </ul>
            </div>

            {selectedProposal.policy_decision_id && (
              <div className="border-t border-border pt-4">
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Policy Decision</h4>
                <p className="mono text-xs text-fg-muted">{selectedProposal.policy_decision_id}</p>
              </div>
            )}

            {selectedProposal.raw_response && Object.keys(selectedProposal.raw_response).length > 0 && (
              <div className="border-t border-border pt-4">
                <h4 className="text-sm font-medium text-fg-secondary mb-2">Raw LLM Response</h4>
                <div className="text-xs text-fg-primary font-mono max-h-60 overflow-y-auto bg-bg-base p-3 rounded-sm border border-border">
                  <pre>{JSON.stringify(selectedProposal.raw_response, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>

      <Modal isOpen={isEvaluateModalOpen} onClose={() => { setIsEvaluateModalOpen(false); setEvaluateResult(null); }} title="Policy Evaluation Result" size="md">
        {evaluateResult && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-4 rounded-sm bg-bg-base">
              <div className={clsx("w-10 h-10 rounded-full flex items-center justify-center", evaluateResult.allowed ? "bg-status-success/20" : "bg-sev-critical/20")}>
                {evaluateResult.allowed ? (
                  <CheckCircle size={24} className="text-status-success" />
                ) : (
                  <XCircle size={24} className="text-sev-critical" />
                )}
              </div>
              <div>
                <p className="font-medium text-fg-primary">{evaluateResult.allowed ? "Allowed" : "Rejected"}</p>
                <p className="text-sm text-fg-secondary">{evaluateResult.decision}</p>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-fg-secondary mb-1">Reason</h4>
              <p className="text-fg-primary">{evaluateResult.reason}</p>
            </div>

            {evaluateResult.conditions.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-fg-secondary mb-1">Conditions</h4>
                <ul className="space-y-1">
                  {evaluateResult.conditions.map((c, i) => (
                    <li key={i} className="text-sm text-fg-primary flex items-center gap-2">
                      <Shield size={14} className="text-sev-info" />
                      {c}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {evaluateResult.requires_approval && (
              <div className="p-3 bg-sev-warning/10 border border-sev-warning/30 rounded-sm">
                <p className="text-sm text-sev-warning flex items-center gap-2">
                  <AlertTriangle size={16} />
                  This action requires human approval before execution.
                </p>
              </div>
            )}

            <div className="flex justify-end pt-4 border-t border-border">
              <button className="btn-primary" onClick={() => { setIsEvaluateModalOpen(false); setEvaluateResult(null); }}>
                Close
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

import { CheckCircle, XCircle, AlertTriangle, Shield, MoreHorizontal, Zap, Brain, RefreshCw } from "lucide-react";