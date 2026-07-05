import { Monitor, FileText } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Button } from "../ui/Boton";
import { Heading } from "../ui/Encabezado";
import { LoadingSkeleton } from "../ui/Esqueleto";
import { EmptyState } from "../ui/EstadoVacio";
import type { VideoAnalysisResponse } from "../../api/analysis";

const backendBaseUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

interface VideoResultPanelProps {
  result: VideoAnalysisResponse | null;
  loading: boolean;
  error: string | null;
  onDownloadPdf: (id: number) => void;
}

export function VideoResultPanel({
  result,
  loading,
  error,
  onDownloadPdf,
}: VideoResultPanelProps) {
  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Respuesta de la IA (Video)
        </Heading>
      </Card.Header>

      <Card.Body>
        {!result && !loading && !error && (
          <EmptyState
            icon={<Monitor className="h-10 w-10" />}
            title="Sin análisis de video"
            description='Selecciona un video y presiona "Analizar video con IA".'
          />
        )}

        {loading && <LoadingSkeleton lines={3} />}

        {error && (
          <p className="text-small text-danger-600">{error}</p>
        )}

        {result && (
          <div className="space-y-3 text-small text-neutral-700">
            <p className="text-body-bold text-neutral-800">
              Hallazgos: {result.total_hallazgos} · Duración:{" "}
              {result.duracion_total_segundos}s
            </p>

            {result.reporte_pdf && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDownloadPdf(result.id_video)}
                iconLeft={<FileText className="h-4 w-4" />}
              >
                Descargar informe PDF
              </Button>
            )}

            <p className="text-neutral-600 truncate">
              Video: {result.ruta_video_original}
            </p>

            {result.detalle_hallazgos.length > 0 ? (
              <ul className="list-disc pl-4 text-neutral-600 space-y-1">
                {result.detalle_hallazgos.map((h) => (
                  <li key={`${result.video_id}-${h.segundo}`}>
                    {h.timestamp} · {h.confianza}% ·{" "}
                    <a
                      className="text-primary-600 hover:underline"
                      href={`${backendBaseUrl}${h.frame_url}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      ver frame
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-small text-neutral-500">Sin hallazgos positivos.</p>
            )}

            <p className="text-caption text-neutral-400 pt-1">
              <a href="/history" className="text-primary-600 hover:underline">
                Ir al historial
              </a>{" "}
              para ver todos los análisis de video.
            </p>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
