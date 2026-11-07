import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  FileText,
  Download,
  ChevronDown,
  ChevronUp,
  Filter,
  Search,
  Trash2,
  MoreHorizontal,
  Clock,
  AlertCircle,
  CheckCircle,
  XCircle,
  Loader2,
  FileType,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Table, Column } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Modal } from "@/components/ui/Modal";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Form, FormField, Select, Input, Textarea } from "@/components/ui/Form";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import clsx from "clsx";
import type { Report, ReportFormat, Assessment, PaginatedResponse } from "@/types/api";

const reportGenerateSchema = z.object({
  assessment_id: z.string().uuid("Select an assessment"),
  name: z.string().min(1, "Report name is required").max(255),
  format: z.enum(["PDF", "HTML", "JSON"]).default("HTML"),
  template: z.string().optional(),
});

type ReportGenerateFormData = z.infer<typeof reportGenerateSchema>;

const formatIcons: Record<ReportFormat, React.ComponentType<{ size?: number }>> = {
  PDF: FileType,
  HTML: FileText,
  JSON: FileText,
};

const formatColors: Record<ReportFormat, string> = {
  PDF: "sev-critical",
  HTML: "sev-info",
  JSON: "sev-warning",
};

export function Reports() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [assessmentFilter, setAssessmentFilter] = useState<string>("");
  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);
  const [generatingReport, setGeneratingReport] = useState<Report | null>(null);

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-list"],
    queryFn: () => api.get<PaginatedResponse<Assessment>>("/assessments", { page_size: 100 }),
  });

  const { data: reportsData, isLoading, error } = useQuery({
    queryKey: ["reports", page, pageSize, assessmentFilter],
    queryFn: () =>
      api.get<PaginatedResponse<Report>>("/reports", {
        page,
        page_size: pageSize,
        assessment_id: assessmentFilter || undefined,
      }),
  });

  const generateMutation = useMutation({
    mutationFn: (data: ReportGenerateFormData) => api.post<Report>("/reports/generate", data),
    onSuccess: (report) => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
      setGeneratingReport(report);
      setIsGenerateModalOpen(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/reports/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
    },
  });

  const downloadMutation = useMutation({
    mutationFn: (report: Report) => api.download(`/reports/${report.id}/download`, `${report.name}.${report.format.toLowerCase()}`),
  });

  const assessmentOptions = [
    { value: "", label: "All Assessments" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const generateForm = useForm<ReportGenerateFormData>({
    resolver: zodResolver(reportGenerateSchema),
    defaultValues: { format: "HTML" },
  });

  const formatOptions = [
    { value: "HTML", label: "HTML" },
    { value: "PDF", label: "PDF" },
    { value: "JSON", label: "JSON" },
  ];

  const columns: Column<Report>[] = [
    {
      key: "name",
      header: "Name",
      render: (r) => (
        <div className="flex items-center gap-2">
          <FileType size={16} className={clsx("text-fg-secondary", formatColors[r.format])} />
          <div>
            <p className="font-medium text-fg-primary">{r.name}</p>
            <p className="text-xs text-fg-muted mono">{r.assessment_id.slice(0, 8)}...</p>
          </div>
        </div>
      ),
    },
    {
      key: "format",
      header: "Format",
      render: (r) => <Badge variant={formatColors[r.format] as any}>{r.format}</Badge>,
    },
    {
      key: "size_bytes",
      header: "Size",
      render: (r) => <span className="mono text-fg-secondary">{formatBytes(r.size_bytes)}</span>,
    },
    {
      key: "generated_at",
      header: "Generated",
      render: (r) => <span className="mono text-fg-secondary">{new Date(r.generated_at).toLocaleString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            {
              label: "Download",
              onClick: () => downloadMutation.mutate(r),
              disabled: r.size_bytes === 0,
            },
            { label: "divider" },
            {
              label: "Delete",
              onClick: () => deleteMutation.mutate(r.id),
              danger: true,
            },
          ]}
          align="right"
        />
      ),
    },
  ];

  function formatBytes(bytes: number): string {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  }

  const handleGenerateSubmit = (data: ReportGenerateFormData) => {
    generateMutation.mutate(data);
  };

  if (isLoading) {
    return (
      <div className="p-4 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-fg-primary">Reports</h1>
            <p className="text-sm text-fg-muted">Generated assessment reports</p>
          </div>
        </div>
        <Table columns={columns} data={[]} keyExtractor={(r) => r.id} isLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Reports</h1>
        </div>
        <EmptyState
          icon={<AlertCircle size={48} />}
          title="Failed to load reports"
          description={error.message}
        />
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Reports</h1>
          <p className="text-sm text-fg-muted">Generated assessment reports</p>
        </div>
        <button className="btn-primary" onClick={() => setIsGenerateModalOpen(true)}>
          <FileText size={16} /> Generate Report
        </button>
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
          {reportsData?.items.length === 0 ? (
            <EmptyState
              icon={<FileText size={48} />}
              title="No reports found"
              description="Generate a report from a completed assessment."
            />
          ) : (
            <>
              <Table columns={columns} data={reportsData.items} keyExtractor={(r) => r.id} />
              <Pagination currentPage={page} totalPages={reportsData.total_pages} onPageChange={setPage} />
            </>
          )}
        </CardBody>
      </Card>

      <Modal isOpen={isGenerateModalOpen} onClose={() => { setIsGenerateModalOpen(false); generateForm.reset(); }} title="Generate Report" size="md">
        <form onSubmit={generateForm.handleSubmit(handleGenerateSubmit)} className="space-y-4">
          <FormField control={generateForm.control} name="assessment_id" label="Assessment" required error={generateForm.formState.errors.assessment_id?.message}>
            {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={assessmentOptions.filter((o) => o.value)} placeholder="Select assessment" />}
          </FormField>
          <FormField control={generateForm.control} name="name" label="Report Name" required error={generateForm.formState.errors.name?.message}>
            {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="e.g., Q1 2024 Security Assessment" />}
          </FormField>
          <FormField control={generateForm.control} name="format" label="Format" required error={generateForm.formState.errors.format?.message}>
            {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={formatOptions} />}
          </FormField>
          <FormField control={generateForm.control} name="template" label="Template (optional)">
            {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Custom template name" />}
          </FormField>
          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <button type="button" className="btn-secondary" onClick={() => { setIsGenerateModalOpen(false); generateForm.reset(); }}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={generateMutation.isPending}>{generateMutation.isPending ? <LoadingSpinner size="sm" /> : "Generate Report"}</button>
          </div>
        </form>
      </Modal>

      {generatingReport && (
        <Modal isOpen={true} onClose={() => setGeneratingReport(null)} title="Report Generated" size="md">
          <div className="space-y-4 text-center">
            <FileType size={48} className={clsx("mx-auto", formatColors[generatingReport.format])} />
            <h3 className="text-lg font-medium text-fg-primary">Report Generated</h3>
            <p className="text-fg-secondary">{generatingReport.name}</p>
            <p className="text-sm text-fg-muted mono">{generatingReport.format} • {formatBytes(generatingReport.size_bytes)}</p>
            <div className="flex justify-center gap-2">
              <button className="btn-primary" onClick={() => { downloadMutation.mutate(generatingReport); setGeneratingReport(null); }}>
                <Download size={16} /> Download
              </button>
              <button className="btn-secondary" onClick={() => setGeneratingReport(null)}>Close</button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

import { FileText, Download, MoreHorizontal, AlertCircle, FileType, FileText as FileTextIcon, Loader2 } from "lucide-react";