import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Play,
  Pause,
  Square,
  Search,
  Target,
  Wifi,
  Globe,
  Database,
  Cpu,
  Network,
  Code,
  Loader2,
  AlertCircle,
  CheckCircle,
  XCircle,
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
import { Form, FormField, Input, Select, Textarea } from "@/components/ui/Form";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import clsx from "clsx";
import type { Assessment, ScanRequest, ScanResponse, DiscoveryRequest, ExecutionJob, JobStatus, PaginatedResponse } from "@/types/api";

const scanSchema = z.object({
  assessment_id: z.string().uuid("Select an assessment"),
  targets: z.string().min(1, "At least one target required"),
  scan_type: z.enum(["tcp_connect", "tcp_syn", "udp"]).default("tcp_connect"),
  ports: z.string().default("1-1000"),
  timing_template: z.enum(["T0", "T1", "T2", "T3", "T4", "T5"]).default("T4"),
});

type ScanFormData = z.infer<typeof scanSchema>;

const discoverySchema = z.object({
  assessment_id: z.string().uuid("Select an assessment"),
  target: z.string().min(1, "Target required"),
  methods: z.array(z.string()).min(1, "Select at least one method"),
});

type DiscoveryFormData = z.infer<typeof discoverySchema>;

const jobStatusColors: Record<JobStatus, string> = {
  PENDING: "default",
  RUNNING: "info",
  COMPLETED: "success",
  FAILED: "error",
  CANCELLED: "default",
};

export function Recon() {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState("scan");
  const [scanPage, setScanPage] = useState(1);
  const [discoveryPage, setDiscoveryPage] = useState(1);
  const [selectedAssessment, setSelectedAssessment] = useState<string>("");
  const [isScanModalOpen, setIsScanModalOpen] = useState(false);
  const [isDiscoveryModalOpen, setIsDiscoveryModalOpen] = useState(false);

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-running"],
    queryFn: () => api.get<PaginatedResponse<Assessment>>("/assessments", { status: "RUNNING", page_size: 100 }),
  });

  const { data: scanJobsData, isLoading: scanLoading } = useQuery({
    queryKey: ["scan-jobs", scanPage, selectedAssessment],
    queryFn: () =>
      api.get<PaginatedResponse<ExecutionJob>>("/executor/jobs", {
        page: scanPage,
        page_size: 20,
        assessment_id: selectedAssessment || undefined,
      }),
    enabled: activeTab === "scan",
  });

  const { data: discoveryJobsData, isLoading: discoveryLoading } = useQuery({
    queryKey: ["discovery-jobs", discoveryPage, selectedAssessment],
    queryFn: () =>
      api.get<PaginatedResponse<ExecutionJob>>("/executor/jobs", {
        page: discoveryPage,
        page_size: 20,
        assessment_id: selectedAssessment || undefined,
      }),
    enabled: activeTab === "discovery",
  });

  const scanMutation = useMutation({
    mutationFn: (data: ScanRequest) => api.post<ScanResponse>("/recon/scan", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scan-jobs"] });
      setIsScanModalOpen(false);
    },
  });

  const discoveryMutation = useMutation({
    mutationFn: (data: DiscoveryRequest) => api.post<ScanResponse>("/recon/discover", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["discovery-jobs"] });
      setIsDiscoveryModalOpen(false);
    },
  });

  const scanForm = useForm<ScanFormData>({
    resolver: zodResolver(scanSchema),
    defaultValues: {
      scan_type: "tcp_connect",
      ports: "1-1000",
      timing_template: "T4",
    },
  });

  const discoveryForm = useForm<DiscoveryFormData>({
    resolver: zodResolver(discoverySchema),
    defaultValues: {
      methods: ["dns", "http", "certificates"],
    },
  });

  const assessmentOptions = [
    { value: "", label: "Select assessment" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const scanTypeOptions = [
    { value: "tcp_connect", label: "TCP Connect Scan" },
    { value: "tcp_syn", label: "TCP SYN Scan (requires root)" },
    { value: "udp", label: "UDP Scan" },
  ];

  const timingOptions = [
    { value: "T0", label: "T0 - Paranoid" },
    { value: "T1", label: "T1 - Sneaky" },
    { value: "T2", label: "T2 - Polite" },
    { value: "T3", label: "T3 - Normal" },
    { value: "T4", label: "T4 - Aggressive" },
    { value: "T5", label: "T5 - Insane" },
  ];

  const discoveryMethodOptions = [
    { value: "dns", label: "DNS Enumeration" },
    { value: "http", label: "HTTP Discovery" },
    { value: "certificates", label: "SSL Certificates" },
    { value: "subdomains", label: "Subdomain Enumeration" },
  ];

  const scanColumns: Column<ExecutionJob>[] = [
    {
      key: "name",
      header: "Name",
      render: (j) => (
        <div>
          <p className="font-medium text-fg-primary">{j.name}</p>
          <p className="text-sm text-fg-muted mono">{j.tool}</p>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (j) => <Badge variant={jobStatusColors[j.status]}>{j.status}</Badge>,
    },
    {
      key: "execution_level",
      header: "Level",
      render: (j) => <span className="mono text-fg-secondary">{j.execution_level}</span>,
    },
    {
      key: "started_at",
      header: "Started",
      render: (j) => j.started_at ? <span className="mono text-fg-secondary">{new Date(j.started_at).toLocaleString()}</span> : <span className="text-fg-muted">—</span>,
    },
    {
      key: "duration_ms",
      header: "Duration",
      render: (j) => j.duration_ms ? <span className="mono text-fg-secondary">{j.duration_ms}ms</span> : <span className="text-fg-muted">—</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (j) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            { label: "View Output", onClick: () => {} },
            { label: "View Evidence", onClick: () => {} },
            { label: "divider" },
            {
              label: "Cancel",
              onClick: () => {},
              disabled: j.status !== "PENDING" && j.status !== "RUNNING",
              danger: true,
            },
          ]}
          align="right"
        />
      ),
    },
  ];

  const handleScanSubmit = (data: ScanFormData) => {
    const targets = data.targets.split(",").map((t) => t.trim()).filter(Boolean);
    scanMutation.mutate({
      assessment_id: data.assessment_id,
      targets,
      scan_type: data.scan_type,
      ports: data.ports,
      timing_template: data.timing_template,
    });
  };

  const handleDiscoverySubmit = (data: DiscoveryFormData) => {
    discoveryMutation.mutate({
      assessment_id: data.assessment_id,
      target: data.target,
      methods: data.methods,
    });
  };

  return (
    <div className="p-4 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-fg-primary">Reconnaissance</h1>
        <p className="text-sm text-fg-muted">Network scanning and asset discovery</p>
      </div>

      <Card>
        <CardHeader>
          <Tabs tabs={[
            { id: "scan", label: "Port Scanning" },
            { id: "discovery", label: "Asset Discovery" },
          ]} activeTab={activeTab} onChange={setActiveTab} />
        </CardHeader>
        <CardBody>
          <TabPanel id="scan" activeTab={activeTab}>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <Select
                value={selectedAssessment}
                onChange={(e) => { setSelectedAssessment(e.target.value); setScanPage(1); }}
                options={assessmentOptions}
                className="w-[250px]"
              />
              <button className="btn-primary" onClick={() => setIsScanModalOpen(true)} disabled={!selectedAssessment || scanMutation.isPending}>
                <Play size={16} /> New Scan
              </button>
            </div>

            {scanLoading ? (
              <Table columns={scanColumns} data={[]} keyExtractor={(j) => j.id} isLoading />
            ) : scanJobsData?.items.length === 0 ? (
              <EmptyState
                icon={<Target size={48} />}
                title="No scans found"
                description="Select a running assessment and start a port scan."
              />
            ) : (
              <>
                <Table columns={scanColumns} data={scanJobsData.items} keyExtractor={(j) => j.id} />
                <Pagination currentPage={scanPage} totalPages={scanJobsData.total_pages} onPageChange={setScanPage} />
              </>
            )}
          </TabPanel>

          <TabPanel id="discovery" activeTab={activeTab}>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <Select
                value={selectedAssessment}
                onChange={(e) => { setSelectedAssessment(e.target.value); setDiscoveryPage(1); }}
                options={assessmentOptions}
                className="w-[250px]"
              />
              <button className="btn-primary" onClick={() => setIsDiscoveryModalOpen(true)} disabled={!selectedAssessment || discoveryMutation.isPending}>
                <Search size={16} /> New Discovery
              </button>
            </div>

            {discoveryLoading ? (
              <Table columns={scanColumns} data={[]} keyExtractor={(j) => j.id} isLoading />
            ) : discoveryJobsData?.items.length === 0 ? (
              <EmptyState
                icon={<Globe size={48} />}
                title="No discovery jobs found"
                description="Select a running assessment and start asset discovery."
              />
            ) : (
              <>
                <Table columns={scanColumns} data={discoveryJobsData.items} keyExtractor={(j) => j.id} />
                <Pagination currentPage={discoveryPage} totalPages={discoveryJobsData.total_pages} onPageChange={setDiscoveryPage} />
              </>
            )}
          </TabPanel>
        </CardBody>
      </Card>

      <Modal isOpen={isScanModalOpen} onClose={() => { setIsScanModalOpen(false); scanForm.reset(); }} title="New Port Scan" size="lg">
        <form onSubmit={scanForm.handleSubmit(handleScanSubmit)} className="space-y-4">
          <FormField control={scanForm.control} name="assessment_id" label="Assessment" required error={scanForm.formState.errors.assessment_id?.message}>
            {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={assessmentOptions} placeholder="Select running assessment" />}
          </FormField>
          <FormField control={scanForm.control} name="targets" label="Targets (comma-separated)" required error={scanForm.formState.errors.targets?.message}>
            {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="192.168.1.0/24, example.com, 10.0.0.1" />}
          </FormField>
          <FormField control={scanForm.control} name="scan_type" label="Scan Type" required error={scanForm.formState.errors.scan_type?.message}>
            {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={scanTypeOptions} />}
          </FormField>
          <div className="grid grid-cols-2 gap-4">
            <FormField control={scanForm.control} name="ports" label="Ports" required error={scanForm.formState.errors.ports?.message}>
              {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="1-1000, 80,443,8080" />}
            </FormField>
            <FormField control={scanForm.control} name="timing_template" label="Timing Template" required error={scanForm.formState.errors.timing_template?.message}>
              {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={timingOptions} />}
            </FormField>
          </div>
          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <button type="button" className="btn-secondary" onClick={() => { setIsScanModalOpen(false); scanForm.reset(); }}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={scanMutation.isPending}>{scanMutation.isPending ? <LoadingSpinner size="sm" /> : "Start Scan"}</button>
          </div>
        </form>
      </Modal>

      <Modal isOpen={isDiscoveryModalOpen} onClose={() => { setIsDiscoveryModalOpen(false); discoveryForm.reset(); }} title="New Asset Discovery" size="lg">
        <form onSubmit={discoveryForm.handleSubmit(handleDiscoverySubmit)} className="space-y-4">
          <FormField control={discoveryForm.control} name="assessment_id" label="Assessment" required error={discoveryForm.formState.errors.assessment_id?.message}>
            {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} options={assessmentOptions} placeholder="Select running assessment" />}
          </FormField>
          <FormField control={discoveryForm.control} name="target" label="Target" required error={discoveryForm.formState.errors.target?.message}>
            {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="example.com or 192.168.1.0/24" />}
          </FormField>
          <FormField control={discoveryForm.control} name="methods" label="Discovery Methods" required error={discoveryForm.formState.errors.methods?.message}>
            {({ onChange, onBlur, value, ref }) => (
              <div className="flex flex-wrap gap-2">
                {discoveryMethodOptions.map((opt) => (
                  <label key={opt.value} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={(value as string[]).includes(opt.value)}
                      onChange={(e) => {
                        const arr = value as string[];
                        if (e.target.checked) onChange([...arr, opt.value]);
                        else onChange(arr.filter((v) => v !== opt.value));
                      }}
                      className="w-4 h-4 rounded border-border bg-bg-elevated text-sev-info focus:ring-sev-info"
                    />
                    <span className="text-sm">{opt.label}</span>
                  </label>
                ))}
              </div>
            )}
          </FormField>
          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <button type="button" className="btn-secondary" onClick={() => { setIsDiscoveryModalOpen(false); discoveryForm.reset(); }}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={discoveryMutation.isPending}>{discoveryMutation.isPending ? <LoadingSpinner size="sm" /> : "Start Discovery"}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

import { MoreHorizontal, AlertCircle, Target, Globe, Play, Search } from "lucide-react";