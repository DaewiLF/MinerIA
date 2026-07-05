import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  Upload, CheckCircle2, AlertCircle, Loader2,
  ArrowLeft, ArrowRight, MapPin, Crosshair,
  User, Users, X, Eye, List, FileText, Cpu,
} from "lucide-react";
import { Card, Heading, Button, Input, Select, Badge } from "../componentes/ui";
import { Skeleton } from "../componentes/ui/Esqueleto";
import { cn } from "../utils/cn";
import { toAbsoluteUrl } from "../utils/url";
import { extraerCoordenadasDeImagen } from "../utils/extraerCoordenadas";
import { MapaSelector } from "../componentes/MapaSelector";
import {
  getAnalysisModels,
  uploadAnalysis,
  type AnalysisDetail,
  type AnalysisModelOption,
} from "../api/analysis";

const STEPS = ["Seleccionar", "Configurar", "Resultados"];

const RISK_OPTIONS = [
  { value: "Bajo", label: "Bajo" },
  { value: "Medio", label: "Medio" },
  { value: "Alto", label: "Alto" },
];

const CATEGORY_OPTIONS = [
  { value: "exploracion", label: "Exploración" },
  { value: "produccion", label: "Producción" },
  { value: "control_calidad", label: "Control de calidad" },
  { value: "otro", label: "Otro" },
];

const riskVariant: Record<string, "success" | "warning" | "danger"> = {
  Bajo: "success",
  Medio: "warning",
  Alto: "danger",
};

export function NewAnalysisPage() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [models, setModels] = useState<AnalysisModelOption[]>([]);
  const [modelId, setModelId] = useState("copper");
  const [form, setForm] = useState({
    location: "",
    category: "",
    riskLevel: "Bajo",
    coordinates: "",
    responsible: "",
    personnel: "",
  });
  const [modelsLoading, setModelsLoading] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [coordFuente, setCoordFuente] = useState<"" | "exif" | "mapa" | "manual">("");
  const [mapaAbierto, setMapaAbierto] = useState(false);

  useEffect(() => {
    setModelsLoading(true);
    getAnalysisModels()
      .then((models) => {
        setModels(models);
        if (models.length > 0) setModelId(models[0].id);
      })
      .catch(() => {})
      .finally(() => setModelsLoading(false));
  }, []);

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleFileSelect = (f: File) => {
    if (!["image/jpeg", "image/png"].includes(f.type)) {
      setError("Solo se aceptan imágenes PNG o JPEG");
      return;
    }
    setError(null);
    setFile(f);
    setPreview(URL.createObjectURL(f));
    extraerCoordenadasDeImagen(f).then((exif) => {
      if (exif && !form.coordinates) {
        setForm((prev) => ({ ...prev, coordinates: exif.texto }));
        setCoordFuente("exif");
      }
    });
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f) handleFileSelect(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const res = await uploadAnalysis(file, form, modelId);
      setResult(res);
      setStep(3);
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail || err?.message || "Error al procesar la imagen";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const confidence = result?.metadata?.confianza_porcentaje as number | undefined;

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div>
        <Heading level={1} size="lg">Nuevo análisis</Heading>
        <p className="text-neutral-500 mt-1">
          Selecciona una imagen y configura los parámetros para el análisis
        </p>
      </div>

      {/* Step indicator */}
      <div className="flex items-center">
        {STEPS.map((label, i) => {
          const num = i + 1;
          const active = num === step;
          const done = num < step;
          return (
            <div key={label} className="flex items-center flex-1">
              <div className="flex items-center gap-2">
                <div
                  className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center text-small font-semibold transition-colors shrink-0",
                    done || active
                      ? "bg-primary-600 text-white"
                      : "bg-neutral-100 text-neutral-400"
                  )}
                >
                  {done ? <CheckCircle2 className="h-4 w-4" /> : num}
                </div>
                <span
                  className={cn(
                    "text-small font-medium hidden sm:inline",
                    active
                      ? "text-primary-700"
                      : done
                        ? "text-neutral-600"
                        : "text-neutral-400"
                  )}
                >
                  {label}
                </span>
              </div>
              {i < STEPS.length - 1 && (
                <div
                  className={cn(
                    "flex-1 h-0.5 mx-3",
                    done ? "bg-primary-500" : "bg-neutral-200"
                  )}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Error banner */}
      {error && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-danger-50 text-danger-700 text-small">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Step 1: Select file + model */}
      {step === 1 && (
        <Card padding="lg" variant="elevated">
          <Card.Body className="space-y-6">
            <div>
              <Heading level={3} size="md" className="mb-3">
                Imagen a analizar
              </Heading>
              <div
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
                onClick={() => fileInputRef.current?.click()}
                className={cn(
                  "border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors",
                  "hover:border-primary-400 hover:bg-primary-50/30",
                  file
                    ? "border-primary-400 bg-primary-50/20"
                    : "border-neutral-300"
                )}
              >
                {preview ? (
                  <div className="inline-flex flex-col items-center gap-3">
                    <div className="relative">
                      <img
                        src={preview}
                        alt="Vista previa"
                        className="max-h-48 rounded-lg object-contain border border-neutral-200"
                      />
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setFile(null);
                          setPreview(null);
                        }}
                        className="absolute -top-2 -right-2 p-1 bg-white rounded-full shadow-sm border border-neutral-200 hover:bg-neutral-100 transition-colors"
                      >
                        <X className="h-3.5 w-3.5 text-neutral-500" />
                      </button>
                    </div>
                    <p className="text-small text-neutral-500">{file?.name}</p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-2 py-4">
                    <Upload className="h-10 w-10 text-neutral-300" />
                    <p className="text-body text-neutral-500">
                      Arrastra una imagen o haz clic para seleccionar
                    </p>
                    <p className="text-caption text-neutral-400">
                      PNG o JPEG · Máximo 10MB
                    </p>
                  </div>
                )}
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg"
                className="hidden"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) handleFileSelect(f);
                }}
              />
            </div>

            <div>
              <Heading level={3} size="md" className="mb-3">
                Modelo de IA
              </Heading>
              {modelsLoading ? (
                <div className="space-y-2">
                  <Skeleton variant="rect" className="h-12 w-full" />
                  <Skeleton variant="text" className="w-3/4" />
                </div>
              ) : (
                <>
                  <Select
                    label="Modelo"
                    options={models.map((m) => ({ value: m.id, label: m.name }))}
                    value={modelId}
                    onChange={(e) => setModelId(e.target.value)}
                    selectSize="lg"
                  />
                  {(() => {
                    const model = models.find((m) => m.id === modelId);
                    return model ? (
                      <p className="text-caption text-neutral-400 mt-1.5">
                        {model.description}
                      </p>
                    ) : null;
                  })()}
                </>
              )}
            </div>
          </Card.Body>
        </Card>
      )}

      {/* Step 2: Configure or Processing */}
      {step === 2 && (
        loading ? (
          <Card padding="lg" variant="elevated">
            <Card.Body className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-10 w-10 text-primary-500 animate-spin mb-4" />
              <Heading level={3} size="md" className="mb-1">
                Analizando imagen
              </Heading>
              <p className="text-small text-neutral-500 text-center max-w-sm">
                El modelo de IA está procesando la imagen. Esto puede tomar unos segundos.
              </p>
            </Card.Body>
          </Card>
        ) : (
          <Card padding="lg" variant="elevated">
            <Card.Body className="space-y-5">
              <Heading level={3} size="md">
                Parámetros del análisis
              </Heading>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Ubicación / Zona"
                  placeholder="Ej: Mina Norte - Zona A3"
                  value={form.location}
                  onChange={(e) => setForm({ ...form, location: e.target.value })}
                  iconPrefix={<MapPin className="h-4 w-4" />}
                />
                <Select
                  label="Categoría"
                  options={CATEGORY_OPTIONS}
                  placeholder="Seleccionar"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                />
                <Select
                  label="Nivel de riesgo"
                  options={RISK_OPTIONS}
                  value={form.riskLevel}
                  onChange={(e) => setForm({ ...form, riskLevel: e.target.value })}
                />
              <div className="space-y-1.5">
                <Input
                  label="Coordenadas (opcional)"
                  placeholder="Ej: -23.456, -69.123"
                  value={form.coordinates}
                  onChange={(e) => {
                    setForm({ ...form, coordinates: e.target.value });
                    setCoordFuente(e.target.value ? "manual" : "");
                  }}
                  iconPrefix={<Crosshair className="h-4 w-4" />}
                />
                <div className="flex items-center gap-2">
                  {coordFuente === "exif" && (
                    <span className="inline-flex items-center gap-1 text-caption text-success-600">
                      <span className="h-1.5 w-1.5 rounded-full bg-success-500" />
                      Obtenidas desde EXIF
                    </span>
                  )}
                  {coordFuente === "mapa" && (
                    <span className="inline-flex items-center gap-1 text-caption text-primary-600">
                      <span className="h-1.5 w-1.5 rounded-full bg-primary-500" />
                      Seleccionadas en mapa
                    </span>
                  )}
                  {!form.coordinates && (
                    <button
                      type="button"
                      onClick={() => setMapaAbierto(true)}
                      className="text-caption font-medium text-primary-600 hover:text-primary-700 hover:underline transition-colors"
                    >
                      Seleccionar en mapa
                    </button>
                  )}
                </div>
              </div>
                <Input
                  label="Responsable (opcional)"
                  placeholder="Nombre del responsable"
                  value={form.responsible}
                  onChange={(e) => setForm({ ...form, responsible: e.target.value })}
                  iconPrefix={<User className="h-4 w-4" />}
                />
                <Input
                  label="Personal involucrado (opcional)"
                  placeholder="Ej: Juan, María, Pedro"
                  value={form.personnel}
                  onChange={(e) => setForm({ ...form, personnel: e.target.value })}
                  iconPrefix={<Users className="h-4 w-4" />}
                />
              </div>
            </Card.Body>
          </Card>
        )
      )}

      {/* Step 3: Results */}
      {step === 3 && result && (
        <div className="space-y-5">
          {/* Success header + key data */}
          <Card padding="lg" variant="elevated">
            <Card.Body className="space-y-5">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-full bg-success-100 flex items-center justify-center shrink-0">
                  <CheckCircle2 className="h-5 w-5 text-success-600" />
                </div>
                <div>
                  <Heading level={3} size="md">
                    Análisis completado
                  </Heading>
                  <p className="text-small text-neutral-500">{result.date}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {result.imageUrl && (
                  <img
                    src={toAbsoluteUrl(result.imageUrl)}
                    alt="Imagen analizada"
                    className="rounded-lg border border-neutral-200 object-contain max-h-40"
                  />
                )}
                <div className="grid grid-cols-2 gap-3 content-start">
                  <div className="p-3 rounded-lg bg-neutral-50">
                    <p className="text-caption text-neutral-500">Confianza</p>
                    <p className="text-heading-md font-semibold text-neutral-800">
                      {confidence != null ? `${confidence.toFixed(1)}%` : "—"}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-neutral-50">
                    <p className="text-caption text-neutral-500">Riesgo</p>
                    <Badge
                      variant={riskVariant[result.riskLevel] ?? "neutral"}
                      size="sm"
                      dot
                    >
                      {result.riskLevel}
                    </Badge>
                  </div>
                  <div className="p-3 rounded-lg bg-neutral-50">
                    <p className="text-caption text-neutral-500">Zona</p>
                    <p className="text-body font-medium text-neutral-700 truncate">
                      {result.zone}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-neutral-50">
                    <p className="text-caption text-neutral-500">Estado</p>
                    <p className="text-body font-medium text-neutral-700 capitalize">
                      {result.status === "con_cobre"
                        ? "Con cobre"
                        : result.status === "sin_cobre"
                          ? "Sin cobre"
                          : result.status}
                    </p>
                  </div>
                </div>
              </div>
            </Card.Body>
          </Card>

          {/* AI Summary */}
          <Card padding="lg" variant="elevated">
            <Card.Header>
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4 text-neutral-400" />
                <Heading level={3} size="md">
                  Resumen del análisis
                </Heading>
              </div>
            </Card.Header>
            <Card.Body>
              <p className="text-body text-neutral-700 leading-relaxed">
                {result.aiSummary}
              </p>
            </Card.Body>
          </Card>

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <Card padding="lg" variant="elevated">
              <Card.Header>
                <div className="flex items-center gap-2">
                  <List className="h-4 w-4 text-neutral-400" />
                  <Heading level={3} size="md">
                    Recomendaciones
                  </Heading>
                </div>
              </Card.Header>
              <Card.Body>
                <ul className="space-y-2">
                  {result.recommendations.map((rec, i) => (
                    <li
                      key={i}
                      className="flex items-start gap-2 text-body text-neutral-700"
                    >
                      <span className="text-primary-500 font-semibold mt-0.5">
                        {i + 1}.
                      </span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </Card.Body>
            </Card>
          )}
        </div>
      )}

      {/* Navigation */}
      <div className="flex items-center justify-between pt-2">
        <Button
          variant="ghost"
          onClick={() => {
            if (step === 1) navigate("/");
            else setStep(step - 1);
          }}
          disabled={loading}
          iconLeft={<ArrowLeft className="h-4 w-4" />}
        >
          {step === 1 ? "Volver al panel" : "Atrás"}
        </Button>

        {step < 3 ? (
          <Button
            size="lg"
            disabled={step === 1 ? !file || !modelId : false}
            loading={loading}
            onClick={() => {
              if (step === 1) setStep(2);
              else if (step === 2) handleUpload();
            }}
            iconRight={step === 1 ? <ArrowRight className="h-4 w-4" /> : undefined}
          >
            {step === 1 ? "Continuar" : "Analizar imagen"}
          </Button>
        ) : (
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              onClick={() => navigate(`/analysis/${result?.id}`)}
              iconLeft={<Eye className="h-4 w-4" />}
            >
              Ver detalle
            </Button>
            <Button size="lg" onClick={() => navigate("/")}>
              Volver al panel
            </Button>
          </div>
        )}
      </div>

      <MapaSelector
        abierto={mapaAbierto}
        onCerrar={() => setMapaAbierto(false)}
        onConfirmar={(texto) => {
          setForm((prev) => ({ ...prev, coordinates: texto }));
          setCoordFuente("mapa");
        }}
        inicial={form.coordinates || undefined}
      />
    </div>
  );
}
