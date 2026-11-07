import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Plus,
  Search,
  Filter,
  Play,
  Pause,
  Square,
  X,
  Edit,
  Trash2,
  MoreHorizontal,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Table, Column } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Modal } from "@/components/ui/Modal";
import { Form, FormField, Input, Textarea, Select } from "@/components/ui/Form";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Tooltip } from "@/components/ui/Tooltip";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import clsx from "clsx";
import type { Assessment, AssessmentStatus, AssessmentCreate, AssessmentUpdate, Scope, PaginatedResponse } from "@/types/api";

const assessmentSchema = z.object({
  name: z.string().min(1, "Name is required").max(255),
  description: z.string().optional(),
  scope_id: z.string().uuid().optional().nullable(),
  policy_level: z.enum(["L1_PASSIVE", "L2_CONTROLLED", "L3_INTRUSIVE"]),
});

type AssessmentFormData = z.infer<typeof assessmentSchema>;

const statusColors: Record<AssessmentStatus, string> = {
  DRAFT: "default",
  RUNNING: "info",
  PAUSED: "warning",
  COMPLETED: "success",
  FAILED: "error",
  CANCELLED: "default",
};

const statusLabels: Record<AssessmentStatus, string> = {
  DRAFT: "Draft",
  RUNNING: "Running",
  PAUSED: "Paused",
  COMPLETED: "Completed",
  FAILED: "Failed",
  CANCELLED: "Cancelled",
};

export function Assessments() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [statusFilter, setStatusFilter] = useState<AssessmentStatus | "">("");
  const [search, setSearch] = useState("");
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingAssessment, setEditingAssessment] = useState<Assessment | null>(null);
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);

  const { data: assessmentsData, isLoading, error } = useQuery({
    queryKey: ["assessments", page, pageSize, statusFilter, search],
    queryFn: () =>
      api.get<PaginatedResponse<Assessment>>("/assessments", {
        page,
        page_size: pageSize,
        status: statusFilter || undefined,
      }),
  });

  const { data: scopesData } = useQuery({
    queryKey: ["scopes"],
    queryFn: () => api.get<PaginatedResponse<Scope>>("/scopes", { page_size: 100 }),
  });

  const createMutation = useMutation({
    mutationFn: (data: AssessmentCreate) => api.post<Assessment>("/assessments", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
      setIsCreateModalOpen(false);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: AssessmentUpdate }) =>
      api.patch<Assessment>(`/assessments/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
      setEditingAssessment(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/assessments/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
    },
  });

  const startMutation = useMutation({
    mutationFn: (id: string) => api.post<Assessment>(`/assessments/${id}/start`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assessments"] }),
  });

  const pauseMutation = useMutation({
    mutationFn: (id: string) => api.post<Assessment>(`/assessments/${id}/pause`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assessments"] }),
  });

  const resumeMutation = useMutation({
    mutationFn: (id: string) => api.post<Assessment>(`/assessments/${id}/resume`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assessments"] }),
  });

  const cancelMutation = useMutation({
    mutationFn: (id: string) => api.post<Assessment>(`/assessments/${id}/cancel`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assessments"] }),
  });

  const columns: Column<Assessment>[] = [
    {
      key: "name",
      header: "Name",
      render: (a) => (
        <div>
          <p className="font-medium text-fg-primary">{a.name}</p>
          {a.description && <p className="text-sm text-fg-muted truncate max-w-xs">{a.description}</p>}
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (a) => (
        <Badge variant={statusColors[a.status]}>{statusLabels[a.status]}</Badge>
      ),
    },
    {
      key: "policy_level",
      header: "Policy Level",
      render: (a) => <span className="mono">{a.policy_level}</span>,
    },
    {
      key: "scope_id",
      header: "Scope",
      render: (a) =>
        a.scope_id ? (
          <span className="mono text-fg-secondary">{a.scope_id.slice(0, 8)}...</span>
        ) : (
          <span className="text-fg-muted">—</span>
        ),
    },
    {
      key: "created_at",
      header: "Created",
      render: (a) => <span className="mono text-fg-secondary">{new Date(a.created_at).toLocaleDateString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (a) => (
        <div className="flex items-center gap-2">
          <Dropdown
            trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
            items={[
              {
                label: a.status === "DRAFT" ? "Start" : a.status === "RUNNING" ? "Pause" : "Resume",
                onClick: () => {
                  if (a.status === "DRAFT") startMutation.mutate(a.id);
                  else if (a.status === "RUNNING") pauseMutation.mutate(a.id);
                  else if (a.status === "PAUSED") resumeMutation.mutate(a.id);
                },
                disabled: ["COMPLETED", "CANCELLED", "FAILED"].includes(a.status),
              },
              {
                label: "Cancel",
                onClick: () => cancelMutation.mutate(a.id),
                disabled: ["COMPLETED", "CANCELLED", "FAILED"].includes(a.status),
                danger: true,
              },
              { label: "divider" },
              {
                label: "Edit",
                onClick: () => setEditingAssessment(a),
              },
              {
                label: "Delete",
                onClick: () => deleteMutation.mutate(a.id),
                danger: true,
                disabled: a.status === "RUNNING",
              },
            ]}
            align="right"
          />
        </div>
      ),
    },
  ];

  const handleCreateSubmit = (data: AssessmentFormData) => {
    createMutation.mutate({
      name: data.name,
      description: data.description,
      scope_id: data.scope_id || undefined,
      policy_level: data.policy_level,
    });
  };

  const handleEditSubmit = (data: AssessmentFormData) => {
    if (editingAssessment) {
      updateMutation.mutate({
        id: editingAssessment.id,
        data: {
          name: data.name,
          description: data.description,
          scope_id: data.scope_id || undefined,
          policy_level: data.policy_level,
        },
      });
    }
  };

  const createForm = useForm<AssessmentFormData>({
    resolver: zodResolver(assessmentSchema),
    defaultValues: { name: "", policy_level: "L2_CONTROLLED" },
  });

  const editForm = useForm<AssessmentFormData>({
    resolver: zodResolver(assessmentSchema),
    defaultValues: { name: "", policy_level: "L2_CONTROLLED" },
  });

  if (editingAssessment) {
    editForm.reset({
      name: editingAssessment.name,
      description: editingAssessment.description || "",
      scope_id: editingAssessment.scope_id || "",
      policy_level: editingAssessment.policy_level,
    });
  }

  const scopeOptions = [
    { value: "", label: "No scope" },
    ...(scopesData?.items?.filter((s) => s.is_active).map((s) => ({ value: s.id, label: s.name })) || []),
  ];

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Assessments</h1>
          <p className="text-sm text-fg-muted">Manage security assessments</p>
        </div>
        <button className="btn-primary" onClick={() => setIsCreateModalOpen(true)}>
          <Plus size={16} /> New Assessment
        </button>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-2">
            <label htmlFor="status-filter" className="text-sm text-fg-secondary">Filter:</label>
            <Select
              id="status-filter"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as AssessmentStatus)}
              options={[
                { value: "", label: "All Statuses" },
                { value: "DRAFT", label: "Draft" },
                { value: "RUNNING", label: "Running" },
                { value: "PAUSED", label: "Paused" },
                { value: "COMPLETED", label: "Completed" },
                { value: "FAILED", label: "Failed" },
                { value: "CANCELLED", label: "Cancelled" },
              ]}
              className="w-[180px]"
            />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search assessments..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input w-[250px]"
            />
            <select
              value={pageSize}
              onChange={(e) => { setPageSize(Number(e.target.value)); setPage(1); }}
              className="input w-[80px]"
            >
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </div>
        </CardHeader>
        <CardBody>
          {isLoading ? (
            <Table columns={columns} data={[]} keyExtractor={(a) => a.id} isLoading />
          ) : error ? (
            <EmptyState
              icon={<AlertCircle size={48} />}
              title="Failed to load assessments"
              description={error.message}
            />
          ) : assessmentsData?.items.length === 0 ? (
            <EmptyState
              icon={<ClipboardList size={48} />}
              title="No assessments found"
              description="Create your first assessment to get started."
            />
          ) : (
            <>
              <Table
                columns={columns}
                data={assessmentsData.items}
                keyExtractor={(a) => a.id}
                sortBy=""
              />
              <Pagination
                currentPage={page}
                totalPages={assessmentsData.total_pages}
                onPageChange={setPage}
              />
            </>
          )}
        </CardBody>
      </Card>

      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => { setIsCreateModalOpen(false); createForm.reset(); }}
        title="Create Assessment"
        size="md"
      >
        <form onSubmit={createForm.handleSubmit(handleCreateSubmit)} className="space-y-4">
          <FormField
            control={createForm.control}
            name="name"
            label="Name"
            required
            error={createForm.formState.errors.name?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Assessment name" />
            )}
          </FormField>
          <FormField
            control={createForm.control}
            name="description"
            label="Description"
          >
            {({ onChange, onBlur, value, ref }) => (
              <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Optional description" rows={3} />
            )}
          </FormField>
          <FormField
            control={createForm.control}
            name="scope_id"
            label="Scope"
            error={createForm.formState.errors.scope_id?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={scopeOptions} placeholder="Select scope (optional)" />
            )}
          </FormField>
          <FormField
            control={createForm.control}
            name="policy_level"
            label="Policy Level"
            required
            error={createForm.formState.errors.policy_level?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Select
                ref={ref}
                onChange={onChange}
                onBlur={onBlur}
                value={value as string}
                options={[
                  { value: "L1_PASSIVE", label: "L1 - Passive (Reconnaissance only)" },
                  { value: "L2_CONTROLLED", label: "L2 - Controlled (Scanning, enumeration)" },
                  { value: "L3_INTRUSIVE", label: "L3 - Intrusive (Requires approval)" },
                ]}
              />
            )}
          </FormField>
          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <button type="button" className="btn-secondary" onClick={() => { setIsCreateModalOpen(false); createForm.reset(); }}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={createMutation.isPending}>
              {createMutation.isPending ? <LoadingSpinner size="sm" /> : "Create Assessment"}
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={!!editingAssessment}
        onClose={() => { setEditingAssessment(null); editForm.reset(); }}
        title="Edit Assessment"
        size="md"
      >
        <form onSubmit={editForm.handleSubmit(handleEditSubmit)} className="space-y-4">
          <FormField
            control={editForm.control}
            name="name"
            label="Name"
            required
            error={editForm.formState.errors.name?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Assessment name" />
            )}
          </FormField>
          <FormField
            control={editForm.control}
            name="description"
            label="Description"
          >
            {({ onChange, onBlur, value, ref }) => (
              <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Optional description" rows={3} />
            )}
          </FormField>
          <FormField
            control={editForm.control}
            name="scope_id"
            label="Scope"
            error={editForm.formState.errors.scope_id?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={scopeOptions} placeholder="Select scope (optional)" />
            )}
          </FormField>
          <FormField
            control={editForm.control}
            name="policy_level"
            label="Policy Level"
            required
            error={editForm.formState.errors.policy_level?.message}
          >
            {({ onChange, onBlur, value, ref }) => (
              <Select
                ref={ref}
                onChange={onChange}
                onBlur={onBlur}
                value={value as string}
                options={[
                  { value: "L1_PASSIVE", label: "L1 - Passive (Reconnaissance only)" },
                  { value: "L2_CONTROLLED", label: "L2 - Controlled (Scanning, enumeration)" },
                  { value: "L3_INTRUSIVE", label: "L3 - Intrusive (Requires approval)" },
                ]}
              />
            )}
          </FormField>
          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <button type="button" className="btn-secondary" onClick={() => { setEditingAssessment(null); editForm.reset(); }}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={updateMutation.isPending}>
              {updateMutation.isPending ? <LoadingSpinner size="sm" /> : "Save Changes"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

import { AlertCircle, ClipboardList, MoreHorizontal } from "lucide-react";