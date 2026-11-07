import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Settings,
  Shield,
  Database,
  Server,
  Cpu,
  Network,
  Key,
  Bell,
  User,
  Lock,
  Save,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  CheckCircle,
  XCircle,
  Info,
  ExternalLink,
  Github,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Form, FormField, Input, Select, Textarea } from "@/components/ui/Form";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import clsx from "clsx";
import type { Scope, PaginatedResponse } from "@/types/api";

const scopeSchema = z.object({
  name: z.string().min(1, "Name is required").max(255),
  description: z.string().optional(),
  targets: z.array(z.string()).min(1, "At least one target required"),
  excluded_targets: z.array(z.string()).optional(),
  allowed_ports: z.array(z.number()).optional(),
  allowed_protocols: z.array(z.string()).optional(),
  max_rate_limit: z.number().optional(),
});

type ScopeFormData = z.infer<typeof scopeSchema>;

export function Settings() {
  const [activeTab, setActiveTab] = useState("general");`n`n  const openExternalLink = (url: string) => {`n    window.open(url, "_blank", "noopener,noreferrer");`n  };
  const [isScopeModalOpen, setIsScopeModalOpen] = useState(false);
  const [editingScope, setEditingScope] = useState<Scope | null>(null);

  const { data: scopesData, isLoading: scopesLoading } = useQuery({
    queryKey: ["scopes"],
    queryFn: () => api.get<PaginatedResponse<Scope>>("/scopes", { page_size: 100 }),
  });

  const scopeForm = useForm<ScopeFormData>({
    resolver: zodResolver(scopeSchema),
    defaultValues: {
      targets: [""],
      excluded_targets: [""],
      allowed_ports: [],
      allowed_protocols: [],
    },
  });

  const handleScopeSubmit = (data: ScopeFormData) => {
    const targets = data.targets.filter((t) => t.trim());
    const excluded = data.excluded_targets.filter((t) => t.trim());
    // TODO: Call create/update scope API
    console.log("Scope data:", { ...data, targets, excluded_targets: excluded });
    setIsScopeModalOpen(false);
    setEditingScope(null);
    scopeForm.reset();
  };

  if (editingScope) {
    scopeForm.reset({
      name: editingScope.name,
      description: editingScope.description || "",
      targets: editingScope.targets,
      excluded_targets: editingScope.excluded_targets,
      allowed_ports: editingScope.allowed_ports || [],
      allowed_protocols: editingScope.allowed_protocols || [],
      max_rate_limit: editingScope.max_rate_limit,
    });
  }

  return (
    <div className="p-4 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-fg-primary">Settings</h1>
        <p className="text-sm text-fg-muted">Configure RAVEN application settings</p>
      </div>

      <Tabs
        tabs={[
          { id: "general", label: "General", icon: Settings },
          { id: "scopes", label: "Scopes", icon: Shield },
          { id: "policy", label: "Policy Engine", icon: Shield },
          { id: "integrations", label: "Integrations", icon: Cpu },
          { id: "database", label: "Database", icon: Database },
          { id: "about", label: "About", icon: Info },
        ]}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      <TabPanel id="general" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">General Settings</h2>
          </CardHeader>
          <CardBody className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-fg-secondary">Application</h3>
                <FormField control={{} as any} name="app_name" label="Application Name">
                  {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value="RAVEN" disabled />}
                </FormField>
                <FormField control={{} as any} name="version" label="Version">
                  {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value="0.1.0" disabled />}
                </FormField>
                <FormField control={{} as any} name="environment" label="Environment">
                  {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value="development" options={[{ value: "development", label: "Development" }, { value: "production", label: "Production" }]} />}
                </FormField>
              </div>
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-fg-secondary">Default Policy Level</h3>
                <FormField control={{} as any} name="default_policy" label="Default Execution Level">
                  {({ onChange, onBlur, value, ref }) => <Select ref={ref} onChange={onChange} onBlur={onBlur} value="L2_CONTROLLED" options={[
                    { value: "L1_PASSIVE", label: "L1 - Passive" },
                    { value: "L2_CONTROLLED", label: "L2 - Controlled" },
                    { value: "L3_INTRUSIVE", label: "L3 - Intrusive" },
                  ]} />}
                </FormField>
              </div>
            </div>
            <div className="pt-4 border-t border-border flex justify-end">
              <button className="btn-primary"><Save size={16} /> Save Changes</button>
            </div>
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="scopes" activeTab={activeTab}>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div>
            <h2 className="text-lg font-medium text-fg-primary">Assessment Scopes</h2>
            <p className="text-sm text-fg-muted">Define authorized target scopes for assessments</p>
          </div>
          <button className="btn-primary" onClick={() => { setEditingScope(null); setIsScopeModalOpen(true); }}>
            <Plus size={16} /> New Scope
          </button>
        </div>

        <Card>
          <CardBody>
            {scopesLoading ? (
              <div className="flex items-center justify-center h-48">
                <LoadingSpinner size="lg" />
              </div>
            ) : scopesData?.items.length === 0 ? (
              <EmptyState
                icon={<Shield size={48} />}
                title="No scopes defined"
                description="Create a scope to define authorized targets for assessments."
              />
            ) : (
              <Table
                columns={[
                  { key: "name", header: "Name", render: (s: Scope) => <p className="font-medium text-fg-primary">{s.name}</p> },
                  { key: "targets", header: "Targets", render: (s: Scope) => <span className="mono text-fg-secondary">{s.targets.join(", ")}</span> },
                  { key: "excluded_targets", header: "Excluded", render: (s: Scope) => <span className="mono text-fg-muted">{s.excluded_targets.join(", ") || "â€”"}</span> },
                  { key: "is_active", header: "Status", render: (s: Scope) => <Badge variant={s.is_active ? "success" : "default"}>{s.is_active ? "Active" : "Inactive"}</Badge> },
                  { key: "actions", header: "Actions", render: (s: Scope) => (
                    <Dropdown trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>} items={[
                      { label: "Edit", onClick: () => { setEditingScope(s); setIsScopeModalOpen(true); } },
                      { label: "Delete", onClick: () => {}, danger: true },
                    ]} align="right" />
                  )},
                ]}
                data={scopesData.items}
                keyExtractor={(s: Scope) => s.id}
              />
            )}
          </CardBody>
        </Card>

        <Modal isOpen={isScopeModalOpen} onClose={() => { setIsScopeModalOpen(false); setEditingScope(null); scopeForm.reset(); }} title={editingScope ? "Edit Scope" : "Create Scope"} size="lg">
          <form onSubmit={scopeForm.handleSubmit(handleScopeSubmit)} className="space-y-4">
            <FormField control={scopeForm.control} name="name" label="Name" required error={scopeForm.formState.errors.name?.message}>
              {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Scope name" />}
            </FormField>
            <FormField control={scopeForm.control} name="description" label="Description">
              {({ onChange, onBlur, value, ref }) => <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} placeholder="Optional description" rows={2} />}
            </FormField>
            <FormField control={scopeForm.control} name="targets" label="Allowed Targets (one per line)" required error={scopeForm.formState.errors.targets?.message}>
              {({ onChange, onBlur, value, ref }) => <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={(value as string[]).join("\n")} placeholder="example.com\n192.168.1.0/24\n10.0.0.0/8" rows={4} />}
            </FormField>
            <FormField control={scopeForm.control} name="excluded_targets" label="Excluded Targets (one per line)">
              {({ onChange, onBlur, value, ref }) => <Textarea ref={ref} onChange={onChange} onBlur={onBlur} value={(value as string[]).join("\n")} placeholder="excluded.example.com" rows={2} />}
            </FormField>
            <div className="grid grid-cols-2 gap-4">
              <FormField control={scopeForm.control} name="allowed_ports" label="Allowed Ports (comma-separated)">
                {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={(value as number[]).join(",")} placeholder="80,443,8080" />}
              </FormField>
              <FormField control={scopeForm.control} name="allowed_protocols" label="Allowed Protocols (comma-separated)">
                {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={(value as string[]).join(",")} placeholder="tcp,udp" />}
              </FormField>
            </div>
            <FormField control={scopeForm.control} name="max_rate_limit" label="Max Rate Limit (req/s)">
              {({ onChange, onBlur, value, ref }) => <Input ref={ref} onChange={onChange} onBlur={onBlur} value={value as string} type="number" placeholder="100" />}
            </FormField>
            <div className="flex justify-end gap-2 pt-4 border-t border-border">
              <button type="button" className="btn-secondary" onClick={() => { setIsScopeModalOpen(false); setEditingScope(null); scopeForm.reset(); }}>Cancel</button>
              <button type="submit" className="btn-primary">{editingScope ? "Update Scope" : "Create Scope"}</button>
            </div>
          </form>
        </Modal>
      </TabPanel>

      <TabPanel id="policy" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">Policy Engine Configuration</h2>
          </CardHeader>
          <CardBody className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-fg-secondary">Execution Levels</h3>
                <div className="space-y-3">
                  {[
                    { level: "L1_PASSIVE", name: "L1 - Passive", desc: "Passive intelligence gathering, offline analysis, asset correlation" },
                    { level: "L2_CONTROLLED", name: "L2 - Controlled", desc: "Port scanning, service enumeration, non-destructive validation" },
                    { level: "L3_INTRUSIVE", name: "L3 - Intrusive", desc: "Actions that may alter system state, requires explicit approval" },
                  ].map((l) => (
                    <div key={l.level} className="p-3 bg-bg-base border border-border rounded-sm">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-fg-primary">{l.name}</p>
                          <p className="text-sm text-fg-muted">{l.desc}</p>
                        </div>
                        <Badge variant={l.level === "L1_PASSIVE" ? "info" : l.level === "L2_CONTROLLED" ? "warning" : "critical"}>{l.level}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-fg-secondary">Policy Rules</h3>
                <div className="space-y-3 text-sm">
                  <p className="text-fg-secondary">â€¢ All actions must pass through Policy Engine</p>
                  <p className="text-fg-secondary">â€¢ L3 actions require human approval</p>
                  <p className="text-fg-secondary">â€¢ Rate limits enforced per assessment</p>
                  <p className="text-fg-secondary">â€¢ Emergency stop available globally</p>
                  <p className="text-fg-secondary">â€¢ Scope validation before execution</p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="integrations" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">Tool Integrations</h2>
          </CardHeader>
          <CardBody className="space-y-4">
            {[
              { name: "Nmap", status: "configured", desc: "Network scanning and service enumeration" },
              { name: "OWASP ZAP", status: "configured", desc: "Web application security scanning" },
              { name: "httpx", status: "configured", desc: "Fast HTTP probing and discovery" },
              { name: "Ollama", status: "not_configured", desc: "Local LLM inference for AI reasoning" },
              { name: "NVD API", status: "configured", desc: "CVE vulnerability data" },
              { name: "CISA KEV", status: "configured", desc: "Known Exploited Vulnerabilities catalog" },
              { name: "EPSS", status: "configured", desc: "Exploit Prediction Scoring System" },
              { name: "MITRE ATT&CK", status: "configured", desc: "Adversary tactics and techniques" },
            ].map((tool) => (
              <div key={tool.name} className="flex items-center justify-between p-3 bg-bg-base border border-border rounded-sm">
                <div className="flex items-center gap-3">
                  <div className={clsx("w-2 h-2 rounded-full", tool.status === "configured" ? "bg-status-success" : "bg-status-warning")} />
                  <div>
                    <p className="font-medium text-fg-primary">{tool.name}</p>
                    <p className="text-sm text-fg-muted">{tool.desc}</p>
                  </div>
                </div>
                <Badge variant={tool.status === "configured" ? "success" : "warning"}>
                  {tool.status === "configured" ? "Configured" : "Not Configured"}
                </Badge>
              </div>
            ))}
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="database" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">Database</h2>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-fg-secondary">Connection</h3>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-status-success" />
                  <p className="text-fg-primary">PostgreSQL Connected</p>
                </div>
              </div>
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-fg-secondary">Migrations</h3>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-status-success" />
                  <p className="text-fg-primary">Up to date</p>
                </div>
              </div>
            </div>
            <div className="pt-4 border-t border-border">
              <button className="btn-secondary"><RefreshCw size={16} /> Check Connection</button>
            </div>
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="about" activeTab={activeTab}>
        <div className="max-w-2xl">
          <Card>
            <CardBody className="text-center py-8">
              <h1 className="text-3xl font-bold text-fg-primary font-mono mb-2">RAVEN</h1>
              <p className="text-fg-secondary mb-4">Risk-Aware Autonomous Vulnerability Exploration Network</p>
              <p className="text-sm text-fg-muted mb-6">Version 0.1.0</p>
              <div className="flex justify-center gap-4 mb-6">
                <button onClick={() => openExternalLink("https://www.linkedin.com/in/nandanamin")} className="btn-secondary">
                  <LinkedIn size={18} /> LinkedIn
                </button>
                <button onClick={() => openExternalLink("https://www.instagram.com/nandanverse/")} className="btn-secondary">
                  <Instagram size={18} /> Instagram
                </button>
              </div>
              <div className="text-sm text-fg-muted space-y-1">
                <p>Created and developed by Nandan Amin</p>
                <p>MIT License</p>
              </div>
            </CardBody>
          </Card>

          <Card className="mt-4">
            <CardHeader>
              <h2 className="text-lg font-medium text-fg-primary">Technology Stack</h2>
            </CardHeader>
            <CardBody>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { name: "FastAPI", category: "Backend" },
                  { name: "PostgreSQL", category: "Database" },
                  { name: "React", category: "Frontend" },
                  { name: "TypeScript", category: "Language" },
                  { name: "Tailwind CSS", category: "Styling" },
                  { name: "Ollama", category: "AI/ML" },
                  { name: "Nmap", category: "Security" },
                  { name: "OWASP ZAP", category: "Security" },
                  { name: "Cytoscape.js", category: "Visualization" },
                  { name: "Plotly", category: "Charts" },
                  { name: "Docker", category: "Infrastructure" },
                  { name: "Alembic", category: "Migrations" },
                ].map((tech) => (
                  <div key={tech.name} className="p-3 bg-bg-base border border-border rounded-sm">
                    <p className="font-medium text-fg-primary">{tech.name}</p>
                    <p className="text-xs text-fg-muted">{tech.category}</p>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>
      </TabPanel>
    </div>
  );
}

import { Plus, MoreHorizontal, Shield, Save, RefreshCw, Settings, Database, Server, Cpu, Network, Key, Bell, User, Lock, Info, ExternalLink, Github, LinkedIn, Instagram } from "lucide-react";