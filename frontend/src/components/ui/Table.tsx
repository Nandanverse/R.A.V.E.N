import { useMemo, useState } from "react";
import { clsx } from "clsx";
import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T, index: number) => React.ReactNode;
  sortable?: boolean;
  className?: string;
  width?: string;
}

export interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string;
  isLoading?: boolean;
  emptyMessage?: string;
  emptyIcon?: React.ReactNode;
  onRowClick?: (item: T) => void;
  sortBy?: string;
  sortOrder?: "asc" | "desc";
  onSort?: (key: string) => void;
  className?: string;
  striped?: boolean;
  hoverable?: boolean;
}

export function Table<T>({
  columns,
  data,
  keyExtractor,
  isLoading = false,
  emptyMessage = "No data available",
  emptyIcon,
  onRowClick,
  sortBy,
  sortOrder,
  onSort,
  className,
  striped = true,
  hoverable = true,
}: TableProps<T>) {
  if (isLoading) {
    return (
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key} className={clsx(col.className)} style={{ width: col.width }}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3].map((i) => (
              <tr key={i}>
                {columns.map((col) => (
                  <td key={col.key} className={clsx(col.className)}>
                    <LoadingSpinner size="sm" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key} className={clsx(col.className)} style={{ width: col.width }}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={columns.length} className="py-8 text-center">
                <EmptyState icon={emptyIcon} title={emptyMessage} />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }

  const sortedData = useMemo(() => {
    if (!sortBy || !onSort) return data;
    return [...data].sort((a, b) => {
      const aVal = (a as Record<string, unknown>)[sortBy];
      const bVal = (b as Record<string, unknown>)[sortBy];
      if (aVal === bVal) return 0;
      const direction = sortOrder === "asc" ? 1 : -1;
      return aVal > bVal ? direction : -direction;
    });
  }, [data, sortBy, sortOrder, onSort]);

  return (
    <div className={clsx("table-container", className)}>
      <table className="table" role="grid">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={clsx(
                  col.className,
                  col.sortable && "cursor-pointer select-none hover:bg-bg-hover"
                )}
                style={{ width: col.width }}
                onClick={col.sortable && onSort ? () => onSort(col.key) : undefined}
                aria-sort={sortBy === col.key ? (sortOrder === "asc" ? "ascending" : "descending") : "none"}
              >
                <div className="flex items-center gap-1">
                  <span>{col.header}</span>
                  {col.sortable && onSort && (
                    <span className="flex flex-col">
                      {sortBy === col.key ? (
                        sortOrder === "asc" ? (
                          <ChevronUp size={10} className="text-fg-primary" />
                        ) : (
                          <ChevronDown size={10} className="text-fg-primary" />
                        )
                      ) : (
                        <ChevronsUpDown size={10} className="text-fg-muted" />
                      )}
                    </span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((item, index) => (
            <tr
              key={keyExtractor(item)}
              className={clsx(
                onRowClick && "cursor-pointer",
                hoverable && "hover:bg-bg-hover",
                striped && index % 2 === 1 && "bg-bg-base/50"
              )}
              onClick={onRowClick ? () => onRowClick(item) : undefined}
              tabIndex={onRowClick ? 0 : undefined}
              onKeyDown={onRowClick ? (e) => { if (e.key === "Enter" || e.key === " ") onRowClick(item); } : undefined}
            >
              {columns.map((col) => (
                <td key={col.key} className={clsx(col.className)}>
                  {col.render ? col.render(item, index) : String((item as Record<string, unknown>)[col.key] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { EmptyState } from "@/components/ui/EmptyState";