import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";
import { cn } from "../../utils/cn";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  showFirstLast?: boolean;
  className?: string;
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  showFirstLast = true,
  className,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  const getVisiblePages = () => {
    const pages: (number | "ellipsis")[] = [];
    const delta = 1;
    const left = Math.max(2, currentPage - delta);
    const right = Math.min(totalPages - 1, currentPage + delta);

    pages.push(1);
    if (left > 2) pages.push("ellipsis");
    for (let i = left; i <= right; i++) pages.push(i);
    if (right < totalPages - 1) pages.push("ellipsis");
    if (totalPages > 1) pages.push(totalPages);

    return pages;
  };

  const btnBase =
    "inline-flex items-center justify-center h-8 min-w-[32px] px-2 text-caption font-medium rounded-md transition-all duration-fast";

  return (
    <nav
      aria-label="Paginación"
      className={cn("flex items-center gap-1", className)}
    >
      {showFirstLast && (
        <button
          onClick={() => onPageChange(1)}
          disabled={currentPage === 1}
          aria-label="Primera página"
          className={cn(
            btnBase,
            "text-neutral-400 hover:text-neutral-600 disabled:opacity-30 disabled:pointer-events-none"
          )}
        >
          <ChevronsLeft className="h-4 w-4" />
        </button>
      )}

      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Página anterior"
        className={cn(
          btnBase,
          "text-neutral-400 hover:text-neutral-600 disabled:opacity-30 disabled:pointer-events-none"
        )}
      >
        <ChevronLeft className="h-4 w-4" />
      </button>

      {getVisiblePages().map((page, idx) =>
        page === "ellipsis" ? (
          <span key={`ellipsis-${idx}`} className="px-1 text-neutral-400 text-caption">
            ...
          </span>
        ) : (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            aria-current={page === currentPage ? "page" : undefined}
            className={cn(
              btnBase,
              page === currentPage
                ? "bg-primary-600 text-white shadow-xs"
                : "text-neutral-600 hover:bg-neutral-100"
            )}
          >
            {page}
          </button>
        )
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Página siguiente"
        className={cn(
          btnBase,
          "text-neutral-400 hover:text-neutral-600 disabled:opacity-30 disabled:pointer-events-none"
        )}
      >
        <ChevronRight className="h-4 w-4" />
      </button>

      {showFirstLast && (
        <button
          onClick={() => onPageChange(totalPages)}
          disabled={currentPage === totalPages}
          aria-label="Última página"
          className={cn(
            btnBase,
            "text-neutral-400 hover:text-neutral-600 disabled:opacity-30 disabled:pointer-events-none"
          )}
        >
          <ChevronsRight className="h-4 w-4" />
        </button>
      )}
    </nav>
  );
}
