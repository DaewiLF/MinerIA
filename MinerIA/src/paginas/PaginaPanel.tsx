import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, BarChart3, Gauge, ShieldAlert, Clock, Cpu, TrendingUp, AlertCircle } from "lucide-react";
import { KpiCard, ActivityChart, MineralDistribution, RecentAnalyses, SystemAlerts } from "../componentes/dashboard";
import { Card } from "../componentes/ui/Tarjeta";
import { Heading } from "../componentes/ui/Encabezado";
import { Button } from "../componentes/ui/Boton";
import { Skeleton } from "../componentes/ui/Esqueleto";
import { EmptyState } from "../componentes/ui/EstadoVacio";
import { useToast } from "../componentes/ui/Notificacion";
import { getDashboardStats, type DashboardStats } from "../api/analysis";

const DAY_NAMES: Record<string, string> = {
  Mon: "Lun", Tue: "Mar", Wed: "Mié", Thu: "Jue", Fri: "Vie", Sat: "Sáb", Sun: "Dom",
};

function toDayName(isoDate: string): string {
  const [y, m, d] = isoDate.split("-").map(Number);
  const date = new Date(y, m - 1, d);
  const short = date.toLocaleDateString("en-US", { weekday: "short" });
  return DAY_NAMES[short] ?? isoDate;
}

const MINERAL_COLORS: Record<string, string> = {
  con_cobre: "#2563EB",
  sin_cobre: "#94A3B8",
};

const MINERAL_LABELS: Record<string, string> = {
  con_cobre: "Con cobre",
  sin_cobre: "Sin cobre",
};

export function DashboardPage() {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchStats = useCallback(() => {
    setLoading(true);
    setError(false);
    getDashboardStats()
      .then(setStats)
      .catch(() => {
        setStats(null);
        setError(true);
        addToast("error", "No se pudieron cargar las estadísticas del panel");
      })
      .finally(() => setLoading(false));
  }, [addToast]);

  useEffect(() => { fetchStats(); }, [fetchStats]);

  if (loading) {
    return (
      <div className="space-y-6">
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white border border-neutral-200 rounded-xl p-4 space-y-3">
              <Skeleton variant="circle" className="h-5 w-5" />
              <Skeleton variant="title" className="w-16" />
              <Skeleton variant="text" className="w-24" />
            </div>
          ))}
        </section>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-white border border-neutral-200 rounded-xl p-4 space-y-4">
              <Skeleton variant="title" className="w-40" />
              <Skeleton variant="rect" className="h-32 w-full" />
            </div>
          ))}
        </div>
        <div className="flex gap-3">
          <Skeleton variant="rect" className="h-12 w-40" />
          <Skeleton variant="rect" className="h-12 w-48" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <EmptyState
        icon={<AlertCircle className="h-12 w-12" />}
        title="Error al cargar el panel"
        description="No se pudieron obtener las estadísticas. Verifica la conexión con el backend."
        action={<Button onClick={fetchStats}>Reintentar</Button>}
      />
    );
  }

  const isEmpty = stats && stats.analisis_hoy === 0 && stats.analisis_semana === 0 && stats.ultimos_analisis.length === 0;

  const totalMineral = stats?.distribucion_mineral.reduce((s, m) => s + m.total, 0) ?? 1;

  const kpiData = [
    { icon: <BarChart3 className="h-5 w-5" />, label: "Análisis realizados hoy", value: (stats?.analisis_hoy ?? 0).toString() },
    { icon: <Gauge className="h-5 w-5" />, label: "Confianza promedio", value: `${stats?.confianza_promedio ?? 0}%` },
    { icon: <TrendingUp className="h-5 w-5" />, label: "Análisis esta semana", value: (stats?.analisis_semana ?? 0).toString() },
    { icon: <ShieldAlert className="h-5 w-5" />, label: "Alertas críticas", value: (stats?.alertas_criticas ?? 0).toString(), variant: "danger" as const },
    { icon: <Clock className="h-5 w-5" />, label: "En cola de procesamiento", value: (stats?.en_cola ?? 0).toString(), variant: "warning" as const },
    { icon: <Cpu className="h-5 w-5" />, label: "Modelos activos", value: (stats?.modelos_activos ?? 0).toString() },
  ];

  const activityData = (stats?.actividad_semanal ?? []).map((d) => ({
    day: toDayName(d.fecha),
    value: d.total,
  }));

  const mineralData = (stats?.distribucion_mineral ?? []).map((m) => ({
    name: MINERAL_LABELS[m.nombre] ?? m.nombre,
    percent: Math.round((m.total / totalMineral) * 100),
    color: MINERAL_COLORS[m.nombre] ?? "#94A3B8",
  }));

  const recentAnalyses = (stats?.ultimos_analisis ?? []).map((a) => ({
    id: a.id,
    zone: a.zone,
    copperGrade: a.copperGrade,
    confidence: `${a.confidence}%`,
    riskLevel: a.riskLevel,
    date: a.date,
  }));

  const systemAlerts = [
    { id: "model-cobre", label: "Modelo cobre (detección binaria)", value: "12h online", status: "success" as const },
    { id: "model-minerales", label: "Modelo minerales (clasificación)", value: "8h online", status: "success" as const },
    { id: "gpu", label: "GPU (NVIDIA A100)", value: "45% uso", status: "info" as const },
    { id: "cola", label: "Cola de procesamiento", value: `${stats?.en_cola ?? 0} pendientes`, status: "warning" as const },
  ];

  if (isEmpty) {
    return (
      <EmptyState
        title="Bienvenido a MinerIA"
        description="Aún no tienes análisis realizados. Carga tu primera imagen para comenzar."
        action={
          <Button
            size="lg"
            onClick={() => navigate("/analysis/new")}
            iconLeft={<Plus className="h-5 w-5" />}
          >
            Primer análisis
          </Button>
        }
      />
    );
  }

  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {kpiData.map((kpi) => (
          <KpiCard key={kpi.label} {...kpi} />
        ))}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <Card.Header>
            <Heading level={3} size="md">Actividad reciente</Heading>
          </Card.Header>
          <Card.Body>
            <ActivityChart data={activityData} />
          </Card.Body>
        </Card>

        <Card>
          <Card.Header>
            <Heading level={3} size="md">Distribución de minerales</Heading>
          </Card.Header>
          <Card.Body>
            <MineralDistribution data={mineralData} />
          </Card.Body>
        </Card>

        <Card>
          <Card.Header>
            <Heading level={3} size="md">Últimos análisis</Heading>
          </Card.Header>
          <Card.Body>
            <RecentAnalyses items={recentAnalyses} />
          </Card.Body>
        </Card>

        <Card>
          <Card.Header>
            <Heading level={3} size="md">Estado del sistema</Heading>
          </Card.Header>
          <Card.Body>
            <SystemAlerts items={systemAlerts} />
          </Card.Body>
        </Card>
      </div>

      <div className="flex items-center gap-3 pt-2">
        <Button
          size="lg"
          onClick={() => navigate("/analysis/new")}
          iconLeft={<Plus className="h-5 w-5" />}
        >
          Nuevo análisis
        </Button>
        <Button
          variant="outline"
          size="lg"
          onClick={() => navigate("/history")}
        >
          Ver historial completo
        </Button>
      </div>
    </div>
  );
}
