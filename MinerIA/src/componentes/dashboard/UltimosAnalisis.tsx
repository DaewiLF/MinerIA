import { Eye } from "lucide-react";
import { Link } from "react-router-dom";
import { Badge } from "../ui/Insignia";

interface AnalysisItem {
  id: number;
  zone: string;
  copperGrade: string;
  confidence: string;
  riskLevel: string;
  date: string;
}

interface RecentAnalysesProps {
  items: AnalysisItem[];
}

const riskVariant: Record<string, "success" | "warning" | "danger"> = {
  Bajo: "success",
  Medio: "warning",
  Alto: "danger",
};

export function RecentAnalyses({ items }: RecentAnalysesProps) {
  if (items.length === 0) {
    return (
      <p className="text-small text-neutral-400 text-center py-6">
        No hay análisis recientes. Crea tu primer análisis.
      </p>
    );
  }

  return (
    <div className="space-y-1">
      {items.map((item) => (
        <div
          key={item.id}
          className="flex items-center gap-3 py-2.5 px-3 -mx-3 rounded-lg hover:bg-neutral-50 transition-colors"
        >
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-body font-medium text-neutral-800 truncate">
                {item.zone}
              </span>
              <span className="text-caption text-neutral-300">·</span>
              <span className="text-body text-neutral-600">{item.copperGrade}</span>
            </div>
            <p className="text-caption text-neutral-400">{item.date}</p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="text-caption text-neutral-500">{item.confidence}</span>
            <Badge variant={riskVariant[item.riskLevel] ?? "neutral"} size="sm" dot>
              {item.riskLevel}
            </Badge>
            <Link
              to={`/analysis/${item.id}`}
              className="p-1.5 rounded-md text-neutral-400 hover:text-primary-600 hover:bg-primary-50 transition-colors"
              aria-label="Ver detalle"
            >
              <Eye className="h-4 w-4" />
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
}
