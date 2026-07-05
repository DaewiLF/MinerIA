import { useLocation } from "react-router-dom";
import { Menu, ChevronRight } from "lucide-react";
import { cn } from "../../utils/cn";

const routeTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/history": "Historial de análisis",
};

export function TopBar({
  onMenuClick,
}: {
  onMenuClick: () => void;
}) {
  const location = useLocation();
  const currentTitle = routeTitles[location.pathname] ?? "MinerIA";

  const breadcrumbs: { label: string; path?: string }[] = [
    { label: "MinerIA" },
  ];

  if (location.pathname.startsWith("/analysis/")) {
    breadcrumbs.push({ label: "Historial", path: "/history" });
    breadcrumbs.push({ label: "Detalle de análisis" });
  } else if (currentTitle !== "Dashboard") {
    breadcrumbs.push({ label: currentTitle });
  }

  return (
    <header className="h-16 bg-white border-b border-neutral-200 flex items-center justify-between px-4 lg:px-6 shrink-0">
      <div className="flex items-center gap-3">
        {/* Mobile hamburger */}
        <button
          onClick={onMenuClick}
          className="lg:hidden p-2 rounded-lg text-neutral-500 hover:bg-neutral-100 hover:text-neutral-700 transition-colors"
          aria-label="Abrir menú"
        >
          <Menu className="h-5 w-5" />
        </button>

        {/* Breadcrumb */}
        <nav aria-label="Breadcrumb" className="hidden sm:flex items-center gap-1.5 text-caption text-neutral-400">
          {breadcrumbs.map((crumb, idx) => (
            <span key={idx} className="flex items-center gap-1.5">
              {idx > 0 && <ChevronRight className="h-3.5 w-3.5" />}
              {crumb.path ? (
                <a
                  href={crumb.path}
                  className="hover:text-neutral-600 transition-colors"
                >
                  {crumb.label}
                </a>
              ) : (
                <span
                  className={cn(
                    idx === breadcrumbs.length - 1
                      ? "text-neutral-700 font-medium"
                      : ""
                  )}
                >
                  {crumb.label}
                </span>
              )}
            </span>
          ))}
        </nav>

        {/* Page title (mobile only, no breadcrumbs) */}
        <h1 className="sm:hidden text-body-bold text-neutral-800 truncate">
          {currentTitle}
        </h1>
      </div>

      <div className="flex items-center gap-3">
        <span className="text-caption text-neutral-400 hidden sm:block">
          MinerIA · v1.0
        </span>
      </div>
    </header>
  );
}
