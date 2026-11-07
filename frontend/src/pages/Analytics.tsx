import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  BarChart2,
  PieChart,
  TrendingUp,
  ChevronDown,
  ChevronUp,
  Filter,
  Calendar,
  Download,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Select } from "@/components/ui/Form";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import Plot from "react-plotly.js";
import clsx from "clsx";
import type { OverviewStats, FindingDistribution, AssetTypeDistribution, JobStats, TimelinePoint, PaginatedResponse } from "@/types/api";

const severityColors = {
  CRITICAL: "#dc2626",
  HIGH: "#ea580c",
  MEDIUM: "#ca8a04",
  LOW: "#16a34a",
  INFO: "#3b82f6",
};

const layout = {
  paper_bgcolor: "#0d0d0d",
  plot_bgcolor: "#141414",
  font: { color: "#e8e8e8", family: "system-ui, sans-serif" },
  margin: { t: 10, r: 10, b: 40, l: 50 },
  xaxis: { gridcolor: "#2a2a2a", zerolinecolor: "#2a2a2a" },
  yaxis: { gridcolor: "#2a2a2a", zerolinecolor: "#2a2a2a" },
  hoverlabel: { bgcolor: "#1a1a1a", bordercolor: "#2a2a2a", font: { color: "#e8e8e8" } },
};

export function Analytics() {
  const [timeRange, setTimeRange] = useState(30);
  const [assessmentFilter, setAssessmentFilter] = useState<string>("");

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-list"],
    queryFn: () => api.get<PaginatedResponse<{ id: string; name: string }>>("/assessments", { page_size: 100 }),
  });

  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ["analytics-overview"],
    queryFn: () => api.get<OverviewStats>("/analytics/overview"),
  });

  const { data: findingDist, isLoading: distLoading } = useQuery({
    queryKey: ["analytics-finding-dist", assessmentFilter],
    queryFn: () => api.get<FindingDistribution[]>("/analytics/findings/distribution", { assessment_id: assessmentFilter || undefined }),
  });

  const { data: assetDist, isLoading: assetDistLoading } = useQuery({
    queryKey: ["analytics-asset-dist", assessmentFilter],
    queryFn: () => api.get<AssetTypeDistribution[]>("/analytics/assets/distribution", { assessment_id: assessmentFilter || undefined }),
  });

  const { data: jobStats, isLoading: jobStatsLoading } = useQuery({
    queryKey: ["analytics-job-stats", assessmentFilter, timeRange],
    queryFn: () => api.get<JobStats[]>("/analytics/jobs/stats", { assessment_id: assessmentFilter || undefined, days: timeRange }),
  });

  const { data: timeline, isLoading: timelineLoading } = useQuery({
    queryKey: ["analytics-timeline", timeRange],
    queryFn: () => api.get<TimelinePoint[]>("/analytics/timeline", { days: timeRange }),
  });

  const assessmentOptions = [
    { value: "", label: "All Assessments" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const timeRangeOptions = [
    { value: 7, label: "Last 7 days" },
    { value: 30, label: "Last 30 days" },
    { value: 90, label: "Last 90 days" },
    { value: 365, label: "Last year" },
  ];

  if (overviewLoading) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Analytics</h1>
          <p className="text-sm text-fg-muted">Assessment metrics and trends</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <Card key={i}>
              <CardBody className="flex items-center justify-center h-24">
                <LoadingSpinner size="lg" />
              </CardBody>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const statCards = [
    { label: "Total Assessments", value: overview?.total_assessments ?? 0, icon: BarChart2, color: "text-fg-primary" },
    { label: "Running", value: overview?.running_assessments ?? 0, icon: TrendingUp, color: "text-sev-info" },
    { label: "Completed", value: overview?.completed_assessments ?? 0, icon: CheckCircle, color: "text-sev-low" },
    { label: "Total Assets", value: overview?.total_assets ?? 0, icon: PieChart, color: "text-fg-primary" },
    { label: "Total Findings", value: overview?.total_findings ?? 0, icon: AlertTriangle, color: "text-sev-high" },
  ];

  const findingSeverityChart = findingDist && findingDist.length > 0 ? {
    data: [{
      type: "bar",
      x: findingDist.map((d) => d.severity),
      y: findingDist.map((d) => d.count),
      marker: { color: findingDist.map((d) => severityColors[d.severity as keyof typeof severityColors] || "#6a6a6a") },
      text: findingDist.map((d) => `${d.percentage.toFixed(1)}%`),
      textposition: "auto",
      hovertemplate: "%{x}: %{y} (%{text})<extra></extra>",
    }],
    layout: { ...layout, title: { text: "Findings by Severity", font: { size: 14 } }, showlegend: false },
  } : null;

  const assetTypeChart = assetDist && assetDist.length > 0 ? {
    data: [{
      type: "pie",
      labels: assetDist.map((d) => d.type),
      values: assetDist.map((d) => d.count),
      marker: { colors: ["#3b82f6", "#06b6d4", "#8b5cf6", "#10b981", "#f59e0b", "#6366f1", "#ec4899", "#ef4444"] },
      hole: 0.4,
      textinfo: "label+percent",
      hovertemplate: "%{label}: %{value} (%{percent})<extra></extra>",
    }],
    layout: { ...layout, title: { text: "Assets by Type", font: { size: 14 } }, showlegend: true },
  } : null;

  const jobStatsChart = jobStats && jobStats.length > 0 ? {
    data: [
      {
        type: "bar",
        name: "Jobs",
        x: jobStats.map((d) => d.tool),
        y: jobStats.map((d) => d.count),
        marker: { color: "#3b82f6" },
        yaxis: "y",
        hovertemplate: "%{x}: %{y} jobs<extra></extra>",
      },
      {
        type: "scatter",
        name: "Success Rate",
        x: jobStats.map((d) => d.tool),
        y: jobStats.map((d) => d.success_rate),
        mode: "lines+markers",
        line: { color: "#16a34a", width: 2 },
        marker: { color: "#16a34a", size: 8 },
        yaxis: "y2",
        hovertemplate: "%{x}: %{y}% success<extra></extra>",
      },
    ],
    layout: {
      ...layout,
      title: { text: "Tool Execution Statistics", font: { size: 14 } },
      xaxis: { ...layout.xaxis, title: "Tool" },
      yaxis: { ...layout.yaxis, title: "Job Count", side: "left" },
      yaxis2: { ...layout.yaxis, title: "Success Rate (%)", side: "right", overlaying: "y", range: [0, 100] },
      legend: { orientation: "h", y: -0.2 },
    },
  } : null;

  const timelineChart = timeline && timeline.length > 0 ? {
    data: [
      {
        type: "scatter",
        name: "Assessments",
        x: timeline.map((d) => d.date),
        y: timeline.map((d) => d.assessments),
        mode: "lines+markers",
        line: { color: "#3b82f6", width: 2 },
        marker: { color: "#3b82f6", size: 6 },
        hovertemplate: "%{x}: %{y} assessments<extra></extra>",
      },
      {
        type: "scatter",
        name: "Findings",
        x: timeline.map((d) => d.date),
        y: timeline.map((d) => d.findings),
        mode: "lines+markers",
        line: { color: "#ef4444", width: 2 },
        marker: { color: "#ef4444", size: 6 },
        hovertemplate: "%{x}: %{y} findings<extra></extra>",
      },
    ],
    layout: {
      ...layout,
      title: { text: "Assessment Timeline", font: { size: 14 } },
      xaxis: { ...layout.xaxis, title: "Date" },
      yaxis: { ...layout.yaxis, title: "Count" },
      legend: { orientation: "h", y: -0.2 },
    },
  } : null;

  return (
    <div className="p-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Analytics</h1>
          <p className="text-sm text-fg-muted">Assessment metrics and trends</p>
        </div>
        <div className="flex items-center gap-2">
          <Select value={timeRange} onChange={(e) => setTimeRange(Number(e.target.value))} options={timeRangeOptions} className="w-[160px]" />
          <Select value={assessmentFilter} onChange={(e) => setAssessmentFilter(e.target.value)} options={assessmentOptions} className="w-[250px]" />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardBody className="flex items-center gap-4">
              <div className={clsx("p-3 rounded-sm bg-bg-base", stat.color)}>
                <stat.icon size={24} aria-hidden="true" />
              </div>
              <div>
                <p className="text-sm text-fg-secondary">{stat.label}</p>
                <p className="text-2xl font-bold text-fg-primary font-mono">{stat.value}</p>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      <Tabs tabs={[
        { id: "overview", label: "Overview" },
        { id: "findings", label: "Findings" },
        { id: "assets", label: "Assets" },
        { id: "jobs", label: "Jobs" },
        { id: "timeline", label: "Timeline" },
      ]} activeTab={activeTab} onChange={setActiveTab} />
    </div>
  );
}

import { AlertTriangle, CheckCircle, TrendingUp, PieChart, BarChart2 } from "lucide-react";
const [activeTab, setActiveTab] = useState("overview");