import { useState } from "react";
import {
  LinkedIn,
  Instagram,
  Github,
  ExternalLink,
  Shield,
  Brain,
  Network,
  Database,
  Code,
  FileText,
  ChevronDown,
  ChevronUp,
  Info,
  AlertCircle,
  CheckCircle,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import clsx from "clsx";

export function About() {
  const [activeTab, setActiveTab] = useState("overview");

  const openExternalLink = (url: string) => {
    window.open(url, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="p-4 space-y-6 max-w-4xl">
      <div className="text-center py-8">
        <h1 className="text-4xl font-bold text-fg-primary font-mono mb-4">RAVEN</h1>
        <p className="text-xl text-fg-secondary mb-2">Risk-Aware Autonomous Vulnerability Exploration Network</p>
        <p className="text-lg text-fg-muted mb-6">Version 0.1.0</p>

        <div className="flex justify-center gap-4">
          <button
            onClick={() => openExternalLink("https://www.linkedin.com/in/nandanamin")}
            className="btn-secondary flex items-center gap-2"
            aria-label="LinkedIn Profile"
          >
            <LinkedIn size={20} />
            <span>LinkedIn</span>
            <ExternalLink size={14} />
          </button>
          <button
            onClick={() => openExternalLink("https://www.instagram.com/nandanverse/")}
            className="btn-secondary flex items-center gap-2"
            aria-label="Instagram Profile"
          >
            <Instagram size={20} />
            <span>Instagram</span>
            <ExternalLink size={14} />
          </button>
        </div>
      </div>

      <Card>
        <CardBody className="space-y-6">
          <div className="border-b border-border pb-6">
            <h2 className="text-lg font-medium text-fg-primary mb-3">Project Description</h2>
            <p className="text-fg-secondary leading-relaxed">
              RAVEN is an independently developed cybersecurity research and engineering project focused on autonomous security assessment,
              vulnerability intelligence, controlled validation, attack-path analysis, and local LLM-assisted security reasoning.
              The project is designed to explore how automation and AI can improve authorized security testing while maintaining human oversight and execution controls.
            </p>
          </div>

          <div className="border-b border-border pb-6">
            <h2 className="text-lg font-medium text-fg-primary mb-3">Core Principles</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { icon: Shield, title: "Authorization First", desc: "Explicit target authorization required before any assessment activity" },
                { icon: Brain, title: "AI with Guardrails", desc: "Local LLM proposes actions; Policy Engine validates every execution" },
                { icon: Network, title: "Three Execution Levels", desc: "L1 Passive, L2 Controlled, L3 Intrusive with approval gates" },
                { icon: Database, title: "Evidence-Based", desc: "All findings backed by cryptographic evidence with SHA-256 integrity" },
                { icon: Code, title: "Free & Open Source", desc: "No paid APIs, no cloud dependencies, fully self-hosted" },
                { icon: FileText, title: "Transparent Reporting", desc: "Distinguishes discovered, suspected, scanner-reported, validated, and demonstrated findings" },
              ].map((item) => (
                <div key={item.title} className="flex items-start gap-3 p-3 bg-bg-base border border-border rounded-sm">
                  <item.icon size={20} className="text-sev-info flex-shrink-0" />
                  <div>
                    <p className="font-medium text-fg-primary">{item.title}</p>
                    <p className="text-sm text-fg-muted">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="border-b border-border pb-6">
            <h2 className="text-lg font-medium text-fg-primary mb-3">Project Owner</h2>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-sev-info/20 flex items-center justify-center">
                <Shield size={32} className="text-sev-info" />
              </div>
              <div>
                <p className="font-medium text-fg-primary text-lg">Nandan Amin</p>
                <p className="text-sm text-fg-muted">Cybersecurity Engineer & Researcher</p>
                <div className="flex items-center gap-3 mt-2">
                  <button onClick={() => openExternalLink("https://www.linkedin.com/in/nandanamin")} className="text-sev-info hover:underline text-sm flex items-center gap-1">
                    <LinkedIn size={14} /> LinkedIn
                  </button>
                  <button onClick={() => openExternalLink("https://www.instagram.com/nandanverse/")} className="text-sev-info hover:underline text-sm flex items-center gap-1">
                    <Instagram size={14} /> Instagram
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-medium text-fg-primary mb-3">License</h2>
            <p className="text-fg-secondary">MIT License - Free for personal and commercial use.</p>
          </div>
        </CardBody>
      </Card>

      <Tabs
        tabs={[
          { id: "architecture", label: "Architecture" },
          { id: "modules", label: "Modules" },
          { id: "tech", label: "Tech Stack" },
        ]}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      <TabPanel id="architecture" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">System Architecture</h2>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="font-mono text-sm text-fg-secondary space-y-1">
              <p>┌─────────────────────────────────────────────────────────────┐</p>
              <p>│                     Frontend (React + TypeScript)           │</p>
              <p>│  Overview │ Assessments │ Assets │ Recon │ Intel │ Findings │</p>
              <p>│  Graph    │ AI Analysis │ Analytics │ Reports │ Settings   │</p>
              <p>└──────────────────────────┬──────────────────────────────┘</p>
              <p>                           │ REST API + WebSocket</p>
              <p>┌──────────────────────────▼──────────────────────────────┐</p>
              <p>│                    Backend (FastAPI + Python)                │</p>
              <p>│  Auth │ Policy Engine │ ReconCore │ SurfaceMapper          │</p>
              <p>│  VulnIntel │ RavenBrain │ TestExecutor │ EvidenceVault      │</p>
              <p>│  AttackGraph │ RiskEngine │ AnalyticsEngine │ ReportForge   │</p>
              <p>└──────────────────────────┬──────────────────────────────┘</p>
              <p>                           │ SQLAlchemy</p>
              <p>┌──────────────────────────▼──────────────────────────────┐</p>
              <p>│              PostgreSQL (Primary Database)                  │</p>
              <p>│  Users │ Assessments │ Scopes │ Assets │ Services          │</p>
              <p>│  Vulnerabilities │ Findings │ Evidence │ Jobs │ Policies  │</p>
              <p>│  AI Proposals │ Graph Nodes/Edges │ Attack Paths │ Reports │</p>
              <p>└──────────────────────────┬──────────────────────────────┘</p>
              <p>                           │ Async Tasks</p>
              <p>┌──────────────────────────▼──────────────────────────────┐</p>
              <p>│                   Celery Workers + Redis                      │</p>
              <p>│  Nmap Scans │ ZAP Scans │ Intel Sync │ Report Generation    │</p>
              <p>└──────────────────────────┬──────────────────────────────┘</p>
              <p>                           │ Local Services</p>
              <p>┌──────────────────────────▼──────────────────────────────┐</p>
              <p>│  Ollama (LLM) │ Nmap │ OWASP ZAP │ httpx │ NVD/KEV/EPSS    │</p>
              <p>└─────────────────────────────────────────────────────────────┘</p>
            </div>
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="modules" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">Application Modules</h2>
          </CardHeader>
          <CardBody className="space-y-3">
            {[
              { id: "A", name: "ReconCore", desc: "Authorized target discovery, host discovery, port scanning, service identification, technology fingerprinting, HTTP endpoint discovery, asset normalization, scan history" },
              { id: "B", name: "SurfaceMapper", desc: "Hosts, IPs, domains, web apps, APIs, ports, services, technologies, relationships, searchable asset inventory" },
              { id: "C", name: "VulnIntel", desc: "CVE lookup, CVSS enrichment, EPSS enrichment, CISA KEV matching, MITRE ATT&CK mapping, software correlation, confidence scoring" },
              { id: "D", name: "RavenBrain", desc: "Local LLM via Ollama, structured proposals, reasoning summaries, missing info identification, action prioritization" },
              { id: "E", name: "PolicyEngine", desc: "Scope validation, allowlists, rate limits, timeouts, L1/L2/L3 execution levels, human approval, emergency stop" },
              { id: "F", name: "TestExecutor", desc: "Execution queue, tool availability, command validation, timeouts, rate limits, standardized results, evidence collection" },
              { id: "G", name: "EvidenceVault", desc: "Finding details, HTTP evidence, tool output, timestamps, integrity hashes, secret redaction, traceability" },
              { id: "H", name: "AttackGraph", desc: "Assets, services, vulnerabilities, relationships, attack paths, Cytoscape.js visualization, evidence-backed edges" },
              { id: "I", name: "RiskEngine", desc: "Contextual risk: CVSS, EPSS, KEV, exposure, criticality, validation confidence, attack paths, transparent scoring" },
              { id: "J", name: "AnalyticsEngine", desc: "Real metrics: assets, ports, vuln distribution, validation rates, critical exposure, path depth, remediation progress" },
              { id: "K", name: "ReportForge", desc: "PDF, HTML, JSON reports: scope, methodology, executive summary, findings, evidence, risk analysis, remediation" },
            ].map((module) => (
              <div key={module.id} className="p-3 bg-bg-base border border-border rounded-sm">
                <div className="flex items-start gap-3">
                  <span className="w-6 h-6 flex items-center justify-center bg-sev-info/20 text-sev-info rounded-sm font-mono font-bold text-sm flex-shrink-0">{module.id}</span>
                  <div className="flex-1">
                    <p className="font-medium text-fg-primary">{module.name}</p>
                    <p className="text-sm text-fg-muted">{module.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </CardBody>
        </Card>
      </TabPanel>

      <TabPanel id="tech" activeTab={activeTab}>
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium text-fg-primary">Technology Stack</h2>
          </CardHeader>
          <CardBody className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { category: "Backend", items: ["Python 3.12+", "FastAPI", "Pydantic", "SQLAlchemy", "Alembic", "Celery", "Redis", "PostgreSQL"] },
                { category: "Frontend", items: ["React 18", "TypeScript", "Vite", "Tailwind CSS", "TanStack Query", "Zustand", "React Router", "Cytoscape.js", "Plotly.js"] },
                { category: "AI & Intelligence", items: ["Ollama", "Llama 3.1 / Mistral", "LangGraph", "Structured JSON Output", "RAG (planned)"] },
                { category: "Security Tools", items: ["Nmap", "OWASP ZAP", "httpx", "Python HTTP utils", "NVD API", "CISA KEV", "EPSS API", "MITRE ATT&CK"] },
                { category: "Infrastructure", items: ["Docker", "Docker Compose", "PostgreSQL", "Redis", "Nginx (prod)"] },
                { category: "Testing & Quality", items: ["Pytest", "Vitest", "Playwright", "MyPy", "Ruff", "ESLint", "Prettier"] },
              ].map((cat) => (
                <div key={cat.category} className="p-4 bg-bg-base border border-border rounded-sm">
                  <h3 className="font-medium text-fg-primary mb-3 flex items-center gap-2">
                    <Badge variant="info">{cat.category}</Badge>
                  </h3>
                  <ul className="space-y-1">
                    {cat.items.map((item) => (
                      <li key={item} className="text-sm text-fg-secondary flex items-center gap-2">
                        <CheckCircle size={12} className="text-sev-low" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      </TabPanel>
    </div>
  );
}