export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ErrorResponse {
  detail: string;
  type: string;
  code?: string;
}

export interface SuccessResponse {
  message: string;
  data?: Record<string, unknown>;
}

// Assessment
export type AssessmentStatus = 'DRAFT' | 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
export type ExecutionLevel = 'L1_PASSIVE' | 'L2_CONTROLLED' | 'L3_INTRUSIVE';

export interface Assessment {
  id: string;
  name: string;
  description?: string;
  status: AssessmentStatus;
  scope_id?: string;
  policy_level: ExecutionLevel;
  owner_id: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface AssessmentCreate {
  name: string;
  description?: string;
  scope_id?: string;
  policy_level?: ExecutionLevel;
}

export interface AssessmentUpdate {
  name?: string;
  description?: string;
  status?: AssessmentStatus;
  policy_level?: ExecutionLevel;
}

// Scope
export interface Scope {
  id: string;
  name: string;
  description?: string;
  targets: string[];
  excluded_targets: string[];
  allowed_ports?: number[];
  allowed_protocols?: string[];
  max_rate_limit?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ScopeCreate {
  name: string;
  description?: string;
  targets: string[];
  excluded_targets?: string[];
  allowed_ports?: number[];
  allowed_protocols?: string[];
  max_rate_limit?: number;
}

// Asset
export type AssetType = 'HOST' | 'IP_ADDRESS' | 'DOMAIN' | 'WEB_APP' | 'API' | 'SERVICE' | 'TECHNOLOGY' | 'NETWORK';

export interface Asset {
  id: string;
  assessment_id: string;
  type: AssetType;
  identifier: string;
  display_name?: string;
  metadata: Record<string, unknown>;
  discovered_at: string;
  updated_at: string;
  confidence: number;
  source: string;
}

// Service
export interface Service {
  id: string;
  asset_id: string;
  port: number;
  protocol: string;
  name?: string;
  version?: string;
  banner?: string;
  technology?: string;
  cpe?: string;
  state: string;
  discovered_at: string;
  updated_at: string;
  source: string;
  metadata: Record<string, unknown>;
}

// Vulnerability
export interface Vulnerability {
  id: string;
  cve_id?: string;
  title: string;
  description?: string;
  cvss_score?: number;
  cvss_vector?: string;
  cvss_version?: string;
  epss_score?: number;
  epss_percentile?: number;
  cisa_kev: boolean;
  cisa_kev_date?: string;
  mitre_techniques: string[];
  affected_software: Record<string, unknown>[];
  references: string[];
  source: string;
  source_url?: string;
  published_at?: string;
  updated_at: string;
  fetched_at: string;
  service_id?: string;
}

// Finding
export type FindingStatus = 'DISCOVERED' | 'SUSPECTED' | 'SCANNER_REPORTED' | 'VALIDATED' | 'FALSE_POSITIVE' | 'DEMONSTRATED';
export type Severity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';

export interface Finding {
  id: string;
  assessment_id: string;
  asset_id: string;
  vulnerability_id?: string;
  title: string;
  description?: string;
  severity: Severity;
  status: FindingStatus;
  cvss_score?: number;
  cvss_vector?: string;
  risk_score?: number;
  evidence_ids: string[];
  remediation?: string;
  references: string[];
  tags: string[];
  discovered_at: string;
  validated_at?: string;
  validated_by?: string;
  created_at: string;
  updated_at: string;
}

export interface FindingUpdate {
  status?: FindingStatus;
  severity?: Severity;
  risk_score?: number;
  remediation?: string;
  tags?: string[];
}

export interface FindingRiskDetail {
  finding_id: string;
  title: string;
  severity: Severity;
  cvss_score?: number;
  epss_score?: number;
  cisa_kev: boolean;
  risk_score?: number;
  risk_factors: string[];
}

// Evidence
export interface Evidence {
  id: string;
  finding_id?: string;
  job_id?: string;
  type: string;
  title: string;
  description?: string;
  content_hash: string;
  content_type?: string;
  size_bytes: number;
  redacted: boolean;
  metadata: Record<string, unknown>;
  collected_at: string;
  created_at: string;
}

// Execution Job
export type JobStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';

export interface ExecutionJob {
  id: string;
  assessment_id: string;
  name: string;
  description?: string;
  tool: string;
  command: string;
  args: Record<string, unknown>;
  status: JobStatus;
  execution_level: ExecutionLevel;
  policy_decision_id?: string;
  started_at?: string;
  completed_at?: string;
  duration_ms?: number;
  exit_code?: number;
  stdout?: string;
  stderr?: string;
  error?: string;
  created_at: string;
  updated_at: string;
}

export interface JobCreate {
  assessment_id: string;
  name: string;
  tool: string;
  command: string;
  args?: Record<string, unknown>;
  execution_level?: ExecutionLevel;
}

// Policy
export type PolicyDecision = 'ALLOWED' | 'REJECTED' | 'REQUIRES_APPROVAL';

export interface PolicyDecisionRecord {
  id: string;
  assessment_id: string;
  action: string;
  target: string;
  execution_level: ExecutionLevel;
  decision: PolicyDecision;
  reason?: string;
  conditions: string[];
  approved_by?: string;
  approved_at?: string;
  created_at: string;
}

export interface EvaluateRequest {
  assessment_id: string;
  action: string;
  target: string;
  execution_level?: ExecutionLevel;
  context?: Record<string, unknown>;
}

export interface EvaluateResponse {
  allowed: boolean;
  decision: PolicyDecision;
  reason: string;
  conditions: string[];
  requires_approval: boolean;
  policy_decision_id?: string;
}

// AI Proposal
export interface AIProposal {
  id: string;
  assessment_id: string;
  action: string;
  target: string;
  reason: string;
  required_evidence: string[];
  risk_level: string;
  confidence: number;
  raw_response: Record<string, unknown>;
  policy_decision_id?: string;
  status: string;
  executed_at?: string;
  created_at: string;
}

export interface ProposalRequest {
  assessment_id: string;
  context?: Record<string, unknown>;
}

export interface OllamaStatus {
  available: boolean;
  model: string;
  message?: string;
}

// Graph
export interface GraphNode {
  id: string;
  assessment_id: string;
  asset_id?: string;
  node_type: string;
  label: string;
  data: Record<string, unknown>;
  x?: number;
  y?: number;
  created_at: string;
  updated_at: string;
}

export interface GraphEdge {
  id: string;
  assessment_id: string;
  source_id: string;
  target_id: string;
  edge_type: string;
  label?: string;
  weight: number;
  evidence_ids: string[];
  data: Record<string, unknown>;
  created_at: string;
}

export interface AttackPath {
  id: string;
  assessment_id: string;
  name: string;
  description?: string;
  node_ids: string[];
  edge_ids: string[];
  risk_score: number;
  max_severity: Severity;
  is_validated: boolean;
  created_at: string;
  updated_at: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// Risk
export interface RiskSummary {
  assessment_id: string;
  total_findings: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  info: number;
  validated_count: number;
  avg_risk_score?: number;
  max_risk_score?: number;
  cisa_kev_findings: number;
  epss_above_50: number;
}

// Analytics
export interface FindingDistribution {
  severity: string;
  count: number;
  percentage: number;
}

export interface AssetTypeDistribution {
  type: string;
  count: number;
}

export interface JobStats {
  tool: string;
  count: number;
  success_rate: number;
  avg_duration_ms?: number;
}

export interface TimelinePoint {
  date: string;
  assessments: number;
  findings: number;
}

export interface OverviewStats {
  total_assessments: number;
  running_assessments: number;
  completed_assessments: number;
  total_assets: number;
  total_findings: number;
  validated_findings: number;
  critical_findings: number;
  high_findings: number;
  total_evidence: number;
  total_jobs: number;
}

// Reports
export type ReportFormat = 'PDF' | 'HTML' | 'JSON';

export interface Report {
  id: string;
  assessment_id: string;
  name: string;
  format: ReportFormat;
  size_bytes: number;
  file_path?: string;
  generated_at: string;
  generated_by: string;
}

export interface ReportGenerateRequest {
  assessment_id: string;
  name: string;
  format: ReportFormat;
  template?: string;
}

// Recon
export interface ScanRequest {
  assessment_id: string;
  targets: string[];
  scan_type?: string;
  ports?: string;
  timing_template?: string;
}

export interface ScanResponse {
  job_id: string;
  status: string;
  message: string;
}

export interface DiscoveryRequest {
  assessment_id: string;
  target: string;
  methods?: string[];
}