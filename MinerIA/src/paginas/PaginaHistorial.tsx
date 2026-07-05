import { useEffect, useState, useMemo, useCallback } from "react";
import { Link } from "react-router-dom";
import { Eye, Download } from "lucide-react";
import { TabBar } from "../componentes/ui/BarraPestanas";
import { DataTable } from "../componentes/ui/TablaDatos";
import { Button } from "../componentes/ui/Boton";
import { Badge } from "../componentes/ui/Insignia";
import { Heading } from "../componentes/ui/Encabezado";
import { Card } from "../componentes/ui/Tarjeta";
import type { AnalysisSummary, VideoHistorySummary } from "../api/analysis";
import { getAnalysisHistory, getVideoHistory, downloadVideoPdf } from "../api/analysis";

type Tab = "imagenes" | "videos";

const tabs = [
  { id: "imagenes" as Tab, label: "Imágenes" },
  { id: "videos" as Tab, label: "Videos" },
];

const statusVariant: Record<string, "success" | "warning" | "danger" | "info" | "neutral"> = {
  completado: "success",
  pendiente: "warning",
  error: "danger",
  procesando: "info",
};

const riskVariant: Record<string, "success" | "warning" | "danger"> = {
  Bajo: "success",
  Medio: "warning",
  Alto: "danger",
};

const PAGE_SIZE = 10;

export function HistoryPage() {
  const [tab, setTab] = useState<Tab>("imagenes");
  const [rows, setRows] = useState<AnalysisSummary[]>([]);
  const [videos, setVideos] = useState<VideoHistorySummary[]>([]);
  const [loading, setLoading] = useState(false);

  const [sortKey, setSortKey] = useState<string>("date");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");
  const [page, setPage] = useState(1);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    setLoading(true);
    if (tab === "imagenes") {
      getAnalysisHistory().then(setRows).finally(() => setLoading(false));
    } else {
      getVideoHistory().then(setVideos).finally(() => setLoading(false));
    }
  }, [tab]);

  const handleSort = useCallback((key: string) => {
    setSortKey((prev) => {
      if (prev === key) {
        setSortDir((d) => (d === "asc" ? "desc" : "asc"));
        return prev;
      }
      setSortDir("desc");
      return key;
    });
  }, []);

  const imageColumns = [
    { key: "date", label: "Fecha", sortable: true },
    { key: "zone", label: "Zona", sortable: true },
    { key: "category", label: "Categoría", sortable: true },
    {
      key: "riskLevel",
      label: "Riesgo",
      sortable: true,
      render: (row: AnalysisSummary) => (
        <Badge
          variant={riskVariant[row.riskLevel] ?? "neutral"}
          size="sm"
          dot
        >
          {row.riskLevel}
        </Badge>
      ),
    },
    { key: "copperGrade", label: "Ley Cu", sortable: true },
    {
      key: "status",
      label: "Estado",
      sortable: true,
      render: (row: AnalysisSummary) => (
        <Badge
          variant={statusVariant[row.status] ?? "neutral"}
          size="sm"
        >
          {row.status}
        </Badge>
      ),
    },
    {
      key: "actions",
      label: "",
      width: "100px",
      render: (row: AnalysisSummary) => (
        <Link
          to={`/analysis/${row.id}`}
          className="inline-flex items-center gap-1.5 text-caption font-medium text-primary-600 hover:text-primary-700 transition-colors"
        >
          <Eye className="h-4 w-4" />
          Ver
        </Link>
      ),
    },
  ];

  const videoColumns = [
    { key: "fecha_analisis", label: "Fecha", sortable: true },
    { key: "nombre_archivo", label: "Archivo", sortable: true },
    {
      key: "duracion_segundos",
      label: "Duración",
      sortable: true,
      render: (row: VideoHistorySummary) => `${row.duracion_segundos}s`,
    },
    {
      key: "total_frames_analizados",
      label: "Frames",
      sortable: true,
    },
    {
      key: "total_hallazgos",
      label: "Hallazgos",
      sortable: true,
    },
    {
      key: "actions",
      label: "Informe",
      width: "140px",
      render: (row: VideoHistorySummary) =>
        row.reporte_pdf ? (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => downloadVideoPdf(row.id_video)}
            iconLeft={<Download className="h-4 w-4" />}
          >
            PDF
          </Button>
        ) : (
          <span className="text-caption text-neutral-400">No disponible</span>
        ),
    },
  ];

  const sortedRows = useMemo(() => {
    const data = tab === "imagenes" ? rows : videos;
    const sorted = [...data].sort((a, b) => {
      const aVal = (a as unknown as Record<string, unknown>)[sortKey];
      const bVal = (b as unknown as Record<string, unknown>)[sortKey];
      if (aVal == null) return 1;
      if (bVal == null) return -1;
      const cmp = String(aVal).localeCompare(String(bVal), "es", { numeric: true });
      return sortDir === "asc" ? cmp : -cmp;
    });
    const start = (page - 1) * PAGE_SIZE;
    return sorted.slice(start, start + PAGE_SIZE);
  }, [tab, rows, videos, sortKey, sortDir, page]);

  const totalPages = Math.ceil(
    (tab === "imagenes" ? rows.length : videos.length) / PAGE_SIZE
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Heading level={2} size="lg">
          Historial de análisis
        </Heading>
        <TabBar
          tabs={tabs}
          activeTab={tab}
          onChange={(id) => { setPage(1); setTab(id as Tab); }}
        />
      </div>

      <Card padding="none" variant="default">
        {tab === "imagenes" && (
          <DataTable
            columns={imageColumns}
            data={sortedRows as AnalysisSummary[]}
            keyExtractor={(row) => row.id}
            sortKey={sortKey}
            sortDirection={sortDir}
            onSort={handleSort}
            page={page}
            totalPages={totalPages}
            onPageChange={setPage}
            isLoading={loading}
            emptyTitle="No hay análisis registrados"
            emptyDescription="Sube una imagen desde el Dashboard para ver resultados aquí."
          />
        )}

        {tab === "videos" && (
          <DataTable
            columns={videoColumns}
            data={sortedRows as VideoHistorySummary[]}
            keyExtractor={(row) => row.id_video}
            sortKey={sortKey}
            sortDirection={sortDir}
            onSort={handleSort}
            page={page}
            totalPages={totalPages}
            onPageChange={setPage}
            isLoading={loading}
            emptyTitle="No hay análisis de video registrados"
            emptyDescription="Sube un video desde el Dashboard para ver resultados aquí."
          />
        )}
      </Card>
    </div>
  );
}
