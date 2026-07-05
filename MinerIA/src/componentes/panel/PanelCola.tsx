import { Clock, Loader2 } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Heading } from "../ui/Encabezado";
import { Badge, StatusDot } from "../ui/Insignia";
import type { QueueItem } from "../../api/analysis";

interface QueuePanelProps {
  items: QueueItem[];
}

const statusConfig: Record<
  string,
  { variant: "warning" | "info" | "danger"; label: string }
> = {
  pendiente: { variant: "warning", label: "Pendiente" },
  procesando: { variant: "info", label: "Procesando" },
  error: { variant: "danger", label: "Error" },
};

export function QueuePanel({ items }: QueuePanelProps) {
  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Cola de procesamiento
        </Heading>
      </Card.Header>

      <Card.Body>
        {items.length === 0 ? (
          <div className="flex items-center gap-2 text-small text-neutral-400">
            <Clock className="h-4 w-4" />
            <span>No hay elementos en cola.</span>
          </div>
        ) : (
          <div className="space-y-2 max-h-48 overflow-y-auto text-small">
            {items.map((item) => {
              const config = statusConfig[item.estado] ?? statusConfig.error;
              return (
                <div
                  key={item.id}
                  className="flex items-center justify-between py-1.5 border-b border-neutral-100 last:border-0"
                >
                  <span className="text-neutral-600 font-medium">
                    #{item.id}
                  </span>

                  <Badge variant={config.variant} size="sm" dot>
                    {config.label}
                  </Badge>

                  {item.error && (
                    <span className="text-danger-500 truncate ml-2 max-w-[120px]">
                      {item.error}
                    </span>
                  )}

                  {item.estado === "procesando" && (
                    <Loader2 className="h-3.5 w-3.5 animate-spin text-info-600 shrink-0" />
                  )}

                  {item.estado === "pendiente" && (
                    <StatusDot variant="warning" pulse size="sm" />
                  )}
                </div>
              );
            })}
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
