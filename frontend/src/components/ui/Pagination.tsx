import { clsx } from "clsx";
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  showPageNumbers?: boolean;
  maxPageNumbers?: number;
  className?: string;
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  showPageNumbers = true,
  maxPageNumbers = 5,
  className,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  const pages = useMemo(() => {
    if (totalPages <= maxPageNumbers) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const half = Math.floor(maxPageNumbers / 2);
    let start = Math.max(1, currentPage - half);
    let end = Math.min(totalPages, start + maxPageNumbers - 1);

    if (end - start + 1 < maxPageNumbers) {
      start = Math.max(1, end - maxPageNumbers + 1);
    }

    const result: (number | "ellipsis")[] = [];
    if (start > 1) {
      result.push(1);
      if (start > 2) result.push("ellipsis");
    }
    for (let i = start; i <= end; i++) {
      result.push(i);
    }
    if (end < totalPages) {
      if (end < totalPages - 1) result.push("ellipsis");
      result.push(totalPages);
    }
    return result;
  }, [currentPage, totalPages, maxPageNumbers]);

  return (
    <nav className={clsx("flex items-center gap-2", className)} aria-label="Pagination">
      <button
        onClick={() => onPageChange(1)}
        disabled={currentPage === 1}
        className="btn-ghost p-1.5"
        aria-label="First page"
        aria-disabled={currentPage === 1}
      >
        <ChevronsLeft size={16} />
      </button>
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="btn-ghost p-1.5"
        aria-label="Previous page"
        aria-disabled={currentPage === 1}
      >
        <ChevronLeft size={16} />
      </button>

      {showPageNumbers && (
        <div className="flex items-center gap-1" role="navigation" aria-label="Page numbers">
          {pages.map((page, index) =>
            page === "ellipsis" ? (
              <span key={`ellipsis-${index}`} className="px-2 text-fg-muted" aria-hidden="true">
                ...
              </span>
            ) : (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={clsx(
                  "w-8 h-8 flex items-center justify-center text-sm rounded-sm transition-colors duration-0",
                  page === currentPage
                    ? "bg-sev-info text-white"
                    : "text-fg-secondary hover:bg-bg-hover hover:text-fg-primary"
                )}
                aria-label={`Page ${page}`}
                aria-current={page === currentPage ? "page" : undefined}
              >
                {page}
              </button>
            )
          )}
        </div>
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="btn-ghost p-1.5"
        aria-label="Next page"
        aria-disabled={currentPage === totalPages}
      >
        <ChevronRight size={16} />
      </button>
      <button
        onClick={() => onPageChange(totalPages)}
        disabled={currentPage === totalPages}
        className="btn-ghost p-1.5"
        aria-label="Last page"
        aria-disabled={currentPage === totalPages}
      >
        <ChevronsRight size={16} />
      </button>
    </nav>
  );
}

import { useMemo } from "react";