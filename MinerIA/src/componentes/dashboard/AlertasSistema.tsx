import { CheckCircle2, AlertTriangle, Cpu } from "lucide-react";
import { cn } from "../../utils/cn";
import { StatusDot } from "../ui/Insignia";

interface AlertItem {
  id: string;
  label: string;
  value: string;
  status: "success" | "warning" | "danger" | "info";
}

interface SystemAlertsProps {
  items: AlertItem[];
}

const statusIcon = {
  success: CheckCircle2,
  warning: AlertTriangle,
  danger: AlertTriangle,
  info: Cpu,
};

const statusColor = {
  success: "text-success-600",
  warning: "text-warning-600",
  danger: "text-danger-600",
  info: "text-info-600",
};

export function SystemAlerts({ items }: SystemAlertsProps) {
  return (
    <div className="space-y-0">
      {items.map((item) => {
        const Icon = statusIcon[item.status];
        return (
          <div
            key={item.id}
            className="flex items-center gap-3 py-2.5 border-b border-neutral-100 last:border-0"
          >
            <Icon className={cn("h-4 w-4 shrink-0", statusColor[item.status])} />
            <div className="flex-1 min-w-0">
              <p className="text-small text-neutral-700 truncate">{item.label}</p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <StatusDot variant={item.status} size="sm" />
              <span className="text-caption font-medium text-neutral-500">
                {item.value}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
