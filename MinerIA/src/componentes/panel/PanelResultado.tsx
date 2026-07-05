import { Sparkles } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Heading } from "../ui/Encabezado";
import { LoadingSkeleton } from "../ui/Esqueleto";
import { EmptyState } from "../ui/EstadoVacio";
import type { AnalysisDetail } from "../../api/analysis";

interface ResultPanelProps {
  result: AnalysisDetail | null;
  loading: boolean;
}

export function ResultPanel({ result, loading }: ResultPanelProps) {
  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Respuesta de la IA (Imagen)
        </Heading>
      </Card.Header>

      <Card.Body>
        {!result && !loading && (
          <EmptyState
            icon={<Sparkles className="h-10 w-10" />}
            title="Sin análisis aún"
            description='Sube una imagen y presiona "Analizar con IA".'
          />
        )}

        {loading && <LoadingSkeleton lines={4} />}

        {result && (
          <div className="space-y-3 text-small">
            <div className="flex flex-wrap gap-2">
              <span className="text-body-bold text-neutral-800">
                {result.zone}
              </span>
              <span className="text-neutral-400">·</span>
              <span className="text-body-bold text-neutral-800">
                {result.copperGrade}
              </span>
              <span className="text-neutral-400">·</span>
              <span className="text-body-bold text-neutral-800">
                Riesgo {result.riskLevel}
              </span>
            </div>

            <p className="text-neutral-600">{result.aiSummary}</p>

            <ul className="list-disc pl-4 text-neutral-600 space-y-1">
              {result.recommendations.map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
