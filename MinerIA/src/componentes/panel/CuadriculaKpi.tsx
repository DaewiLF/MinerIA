import { cn } from "../../utils/cn";

interface Kpi {
  label: string;
  value: string;
  change: string;
  trend: "up" | "down" | "neutral";
}

interface KpiGridProps {
  items: Kpi[];
  className?: string;
}

const trendColors = {
  up: "text-success-600",
  down: "text-danger-600",
  neutral: "text-info-600",
};

export function KpiGrid({ items, className }: KpiGridProps) {
  return (
    <section
      className={cn(
        "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
        className
      )}
    >
      {items.map((kpi) => (
        <div
          key={kpi.label}
          className="bg-white border border-neutral-200 rounded-xl p-4 transition-all duration-fast hover:shadow-sm hover:border-neutral-300"
        >
          <p className="text-caption text-neutral-500">{kpi.label}</p>
          <p className="text-heading-md text-neutral-800 mt-1">{kpi.value}</p>
          <p className={cn("text-caption mt-1", trendColors[kpi.trend])}>
            {kpi.change}
          </p>
        </div>
      ))}
    </section>
  );
}
