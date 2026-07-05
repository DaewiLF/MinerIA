import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Download, Image as ImageIcon } from "lucide-react";
import { getAnalysisById } from "../api/analysis";
import type { AnalysisDetail } from "../api/analysis";
import { Card } from "../componentes/ui/Tarjeta";
import { Heading } from "../componentes/ui/Encabezado";
import { Button } from "../componentes/ui/Boton";
import { Badge } from "../componentes/ui/Insignia";
import { LoadingSkeleton } from "../componentes/ui/Esqueleto";

const riskVariant: Record<string, "success" | "warning" | "danger"> = {
  Bajo: "success",
  Medio: "warning",
  Alto: "danger",
};

const statusVariant: Record<string, "success" | "warning" | "danger" | "info" | "neutral"> = {
  completado: "success",
  pendiente: "warning",
  error: "danger",
  procesando: "info",
};

export function AnalysisDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [data, setData] = useState<AnalysisDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const apiBase = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getAnalysisById(id)
      .then(setData)
      .finally(() => setLoading(false));
  }, [id]);

  const handleDownloadPdf = async () => {
    if (!data) return;
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión nuevamente para descargar el reporte.");
      return;
    }
    try {
      const resp = await fetch(`${apiBase}/api/analysis/${data.id}/pdf`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!resp.ok) throw new Error(`Error ${resp.status}`);
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `reporte_${data.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("No se pudo descargar el PDF.");
    }
  };

  if (loading) {
    return (
      <Card>
        <Card.Body>
          <LoadingSkeleton lines={6} />
        </Card.Body>
      </Card>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-neutral-500">
        <p>No se encontró el análisis solicitado.</p>
        <Button variant="ghost" onClick={() => navigate("/history")} className="mt-2">
          Volver al historial
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back button */}
      <div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate("/history")}
          iconLeft={<ArrowLeft className="h-4 w-4" />}
        >
          Volver al historial
        </Button>
      </div>

      <Card variant="elevated">
        <Card.Body>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Image */}
            <div className="lg:col-span-1 space-y-4">
              <img
                src={`${apiBase}${data.imageUrl}`}
                alt="Análisis"
                className="w-full rounded-xl border border-neutral-200 object-cover max-h-64"
              />

              {data.gradcamUrl && (
                <div>
                  <p className="text-caption-bold text-neutral-500 mb-1.5 flex items-center gap-1.5">
                    <ImageIcon className="h-3.5 w-3.5" />
                    Mapa de activación (Grad-CAM)
                  </p>
                  <img
                    src={`${apiBase}${data.gradcamUrl}`}
                    alt="Grad-CAM"
                    className="w-full rounded-xl border border-neutral-200 object-cover max-h-48"
                  />
                </div>
              )}
            </div>

            {/* Info */}
            <div className="lg:col-span-2 space-y-5">
              <div>
                <div className="flex items-center gap-2 flex-wrap mb-2">
                  <Heading level={2} size="lg">
                    {data.zone}
                  </Heading>
                  <span className="text-neutral-300">·</span>
                  <span className="text-heading-md text-neutral-700">
                    {data.copperGrade}
                  </span>
                </div>
                <p className="text-small text-neutral-400">{data.date}</p>
              </div>

              <div className="flex flex-wrap gap-3">
                <div className="space-y-0.5">
                  <p className="text-caption text-neutral-400">Categoría</p>
                  <p className="text-body-bold text-neutral-700">{data.category}</p>
                </div>
                <div className="space-y-0.5">
                  <p className="text-caption text-neutral-400">Riesgo</p>
                  <Badge variant={riskVariant[data.riskLevel] ?? "neutral"} dot>
                    {data.riskLevel}
                  </Badge>
                </div>
                <div className="space-y-0.5">
                  <p className="text-caption text-neutral-400">Estado</p>
                  <Badge variant={statusVariant[data.status] ?? "neutral"}>
                    {data.status}
                  </Badge>
                </div>
              </div>

              <div>
                <Heading level={3} size="md">
                  Resumen IA
                </Heading>
                <p className="mt-1 text-body text-neutral-600 leading-relaxed">
                  {data.aiSummary}
                </p>
              </div>

              <div>
                <Heading level={3} size="md">
                  Recomendaciones
                </Heading>
                <ul className="mt-1 list-disc pl-5 text-body text-neutral-600 space-y-1">
                  {data.recommendations.map((r) => (
                    <li key={r}>{r}</li>
                  ))}
                </ul>
              </div>

              <Button
                variant="outline"
                onClick={handleDownloadPdf}
                iconLeft={<Download className="h-4 w-4" />}
              >
                Descargar reporte PDF
              </Button>
            </div>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
