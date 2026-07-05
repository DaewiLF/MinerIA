import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";
import { cn } from "../../utils/cn";
import { Pagination } from "./Paginacion";

export interface Column<T> {
  key: string;
  label: string;
  sortable?: boolean;
  render?: (row: T) => React.ReactNode;
  className?: string;
  width?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (row: T) => string | number;
  sortKey?: string;
  sortDirection?: "asc" | "desc";
  onSort?: (key: string) => void;
  page?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  isLoading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  onRowClick?: (row: T) => void;
  className?: string;
}

/* eslint-disable @typescript-eslint/no-explicit-any */
export function DataTable<T extends Record<string, any>>({
  columns,
  data,
  keyExtractor,
  sortKey,
  sortDirection,
  onSort,
  page,
  totalPages,
  onPageChange,
  isLoading = false,
  emptyTitle = "Sin datos",
  emptyDescription,
  onRowClick,
  className,
}: DataTableProps<T>) {
  const renderSortIcon = (col: Column<T>) => {
    if (!col.sortable) return null;
    if (sortKey !== col.key) {
      return <ChevronsUpDown className="h-3.5 w-3.5 text-neutral-400" />;
    }
    return sortDirection === "asc" ? (
      <ChevronUp className="h-3.5 w-3.5 text-primary-600" />
    ) : (
      <ChevronDown className="h-3.5 w-3.5 text-primary-600" />
    );
  };

  if (isLoading) {
    return (
      <div className={cn("border border-neutral-200 rounded-xl overflow-hidden", className)}>
        <div className="animate-pulse">
          <div className="flex gap-4 px-4 py-3 bg-neutral-50 border-b border-neutral-200">
            {columns.map((col) => (
              <div
                key={col.key}
                className="h-4 bg-neutral-200 rounded"
                style={{ width: col.width ?? `${100 / columns.length}%` }}
              />
            ))}
          </div>
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="flex gap-4 px-4 py-3 border-b border-neutral-100 last:border-0"
            >
              {columns.map((col) => (
                <div
                  key={col.key}
                  className="h-3 bg-neutral-100 rounded"
                  style={{ width: col.width ?? `${100 / columns.length}%` }}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className={cn("border border-neutral-200 rounded-xl", className)}>
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <p className="text-body-bold text-neutral-600">{emptyTitle}</p>
          {emptyDescription && (
            <p className="mt-1 text-small text-neutral-400">{emptyDescription}</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={cn("space-y-3", className)}>
      <div className="border border-neutral-200 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-neutral-50 border-b border-neutral-200">
                {columns.map((col) => (
                  <th
                    key={col.key}
                    scope="col"
                    className={cn(
                      "px-4 py-3 text-left text-caption-bold text-neutral-500",
                      col.sortable && "cursor-pointer select-none hover:text-neutral-700",
                      col.className
                    )}
                    style={{ width: col.width }}
                    onClick={() => col.sortable && onSort?.(col.key)}
                  >
                    <span className="inline-flex items-center gap-1.5">
                      {col.label}
                      {renderSortIcon(col)}
                    </span>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="divide-y divide-neutral-100">
              {data.map((row) => (
                <tr
                  key={keyExtractor(row)}
                  onClick={() => onRowClick?.(row)}
                  className={cn(
                    "transition-colors duration-fast",
                    onRowClick
                      ? "cursor-pointer hover:bg-neutral-50"
                      : "hover:bg-neutral-50/50"
                  )}
                >
                  {columns.map((col) => (
                    <td
                      key={col.key}
                      className={cn(
                        "px-4 py-3 text-body text-neutral-700",
                        col.className
                      )}
                    >
                      {col.render
                        ? col.render(row)
                        : (row[col.key] as React.ReactNode) ?? "—"}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {page != null && totalPages != null && onPageChange && (
        <Pagination
          currentPage={page}
          totalPages={totalPages}
          onPageChange={onPageChange}
        />
      )}
    </div>
  );
}
