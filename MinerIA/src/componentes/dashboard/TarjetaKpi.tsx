import { cn } from "../../utils/cn";

interface KpiCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  change?: { value: string; positive: boolean };
  variant?: "default" | "warning" | "danger";
}

const variantBorder = {
  default: "border-l-primary-500",
  warning: "border-l-warning-500",
  danger: "border-l-danger-500",
};

export function KpiCard({ icon, label, value, change, variant = "default" }: KpiCardProps) {
  return (
    <div
      className={cn(
        "bg-white border border-neutral-200 rounded-xl p-4 border-l-4 transition-all duration-fast hover:shadow-sm hover:border-neutral-300",
        variantBorder[variant]
      )}
    >
      <div className="flex items-start justify-between mb-2">
        <span className="text-neutral-400">{icon}</span>
        {change && (
          <span
            className={cn(
              "text-caption font-medium",
              change.positive ? "text-success-600" : "text-danger-600"
            )}
          >
            {change.positive ? "↑" : "↓"} {change.value}
          </span>
        )}
      </div>
      <p className="text-heading-md text-neutral-800 font-semibold">{value}</p>
      <p className="text-caption text-neutral-500 mt-0.5">{label}</p>
    </div>
  );
}
