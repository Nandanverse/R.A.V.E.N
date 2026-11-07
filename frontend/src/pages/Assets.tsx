import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Search,
  Filter,
  Server,
  Globe,
  Database,
  Cpu,
  Network,
  Code,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { Table, Column } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Dropdown, DropdownItem } from "@/components/ui/Dropdown";
import { Tooltip } from "@/components/ui/Tooltip";
import { Tabs, TabPanel } from "@/components/ui/Tabs";
import clsx from "clsx";
import type { Asset, AssetType, PaginatedResponse } from "@/types/api";

const assetTypeIcons: Record<AssetType, React.ComponentType<{ size?: number }>> = {
  HOST: Server,
  IP_ADDRESS: Server,
  DOMAIN: Globe,
  WEB_APP: Database,
  API: Cpu,
  SERVICE: Network,
  TECHNOLOGY: Code,
  NETWORK: Network,
};

const assetTypeLabels: Record<AssetType, string> = {
  HOST: "Host",
  IP_ADDRESS: "IP Address",
  DOMAIN: "Domain",
  WEB_APP: "Web App",
  API: "API",
  SERVICE: "Service",
  TECHNOLOGY: "Technology",
  NETWORK: "Network",
};

export function Assets() {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [typeFilter, setTypeFilter] = useState<AssetType | "">("");
  const [search, setSearch] = useState("");
  const [selectedAssessment, setSelectedAssessment] = useState<string | "">("");
  const [sortBy, setSortBy] = useState<string>("");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const { data: assessmentsData } = useQuery({
    queryKey: ["assessments-list"],
    queryFn: () => api.get<PaginatedResponse<{ id: string; name: string }>>("/assessments", { page_size: 100 }),
  });

  const { data: assetsData, isLoading, error } = useQuery({
    queryKey: ["assets", page, pageSize, typeFilter, search, selectedAssessment],
    queryFn: () =>
      api.get<PaginatedResponse<Asset>>("/assets", {
        page,
        page_size: pageSize,
        type: typeFilter || undefined,
        search: search || undefined,
        assessment_id: selectedAssessment || undefined,
      }),
  });

  const columns: Column<Asset>[] = [
    {
      key: "type",
      header: "Type",
      sortable: true,
      render: (a) => {
        const Icon = assetTypeIcons[a.type];
        return (
          <div className="flex items-center gap-2">
            <Icon size={16} className="text-fg-secondary" aria-hidden="true" />
            <span>{assetTypeLabels[a.type]}</span>
          </div>
        );
      },
    },
    {
      key: "identifier",
      header: "Identifier",
      sortable: true,
      render: (a) => (
        <div>
          <p className="font-mono text-fg-primary">{a.identifier}</p>
          {a.display_name && <p className="text-sm text-fg-muted">{a.display_name}</p>}
        </div>
      ),
    },
    {
      key: "confidence",
      header: "Confidence",
      sortable: true,
      render: (a) => (
        <div className="flex items-center gap-2">
          <div className="w-24 h-2 bg-bg-base border border-border rounded-full overflow-hidden">
            <div
              className="h-full bg-sev-info"
              style={{ width: `${Math.round(a.confidence * 100)}%` }}
            />
          </div>
          <span className="mono text-sm">{Math.round(a.confidence * 100)}%</span>
        </div>
      ),
    },
    {
      key: "source",
      header: "Source",
      sortable: true,
      render: (a) => <span className="mono text-fg-secondary">{a.source}</span>,
    },
    {
      key: "discovered_at",
      header: "Discovered",
      sortable: true,
      render: (a) => <span className="mono text-fg-secondary">{new Date(a.discovered_at).toLocaleString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      render: (a) => (
        <Dropdown
          trigger={<button className="btn-ghost p-1.5"><MoreHorizontal size={16} /></button>}
          items={[
            { label: "View Details", onClick: () => {} },
            { label: "View Services", onClick: () => {} },
            { label: "View Findings", onClick: () => {} },
          ]}
          align="right"
        />
      ),
    },
  ];

  const assessmentOptions = [
    { value: "", label: "All Assessments" },
    ...(assessmentsData?.items?.map((a) => ({ value: a.id, label: a.name })) || []),
  ];

  const typeOptions = [
    { value: "", label: "All Types" },
    ...Object.entries(assetTypeLabels).map(([value, label]) => ({ value, label })),
  ];

  if (isLoading) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Asset Inventory</h1>
          <p className="text-sm text-fg-muted">Discovered assets across assessments</p>
        </div>
        <Table columns={columns} data={[]} keyExtractor={(a) => a.id} isLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-fg-primary">Asset Inventory</h1>
        </div>
        <EmptyState
          icon={<AlertCircle size={48} />}
          title="Failed to load assets"
          description={error.message}
        />
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-fg-primary">Asset Inventory</h1>
        <p className="text-sm text-fg-muted">Discovered assets across assessments</p>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Select
              value={selectedAssessment}
              onChange={(e) => { setSelectedAssessment(e.target.value); setPage(1); }}
              options={assessmentOptions}
              className="w-[200px]"
            />
            <Select
              value={typeFilter}
              onChange={(e) => { setTypeFilter(e.target.value as AssetType); setPage(1); }}
              options={typeOptions}
              className="w-[180px]"
            />
            <input
              type="text"
              placeholder="Search identifier..."
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
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </CardHeader>
        <CardBody>
          {assetsData?.items.length === 0 ? (
            <EmptyState
              icon={<Server size={48} />}
              title="No assets found"
              description="Run reconnaissance to discover assets."
            />
          ) : (
            <>
              <Table
                columns={columns}
                data={assetsData.items}
                keyExtractor={(a) => a.id}
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
              <Pagination
                currentPage={page}
                totalPages={assetsData.total_pages}
                onPageChange={setPage}
              />
            </>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

import { MoreHorizontal, AlertCircle, Server } from "lucide-react";