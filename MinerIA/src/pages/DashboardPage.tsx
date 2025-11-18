import { useState, useRef } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { TopBar } from "../components/layout/TopBar";
import type { AnalysisDetail } from "../api/analysis";
import { uploadAnalysis } from "../api/analysis";

export function DashboardPage() {
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [metadata, setMetadata] = useState({
    category: "",
    riskLevel: "",
    location: "",
    coordinates: "",
    responsible: "",
    personnel: 1,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisDetail | null>(null);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleMetaChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setMetadata((m) => ({
      ...m,
      [name]: name === "personnel" ? Number(value) : value,
    }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = (ev) => setFilePreview(ev.target?.result as string);
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setResult(null);

    try {
      const r = await uploadAnalysis(selectedFile, metadata);
      setResult(r);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-slate-100">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <TopBar />

        <main className="flex-1 p-6 space-y-6">
          {/* tarjetas superiores */}
          <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <p className="text-xs text-slate-500">Producción diaria</p>
              <p className="text-xl font-semibold text-slate-900 mt-1">
                8.542 ton
              </p>
              <p className="text-xs text-emerald-600 mt-1">+12% vs ayer</p>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <p className="text-xs text-slate-500">Rendimiento</p>
              <p className="text-xl font-semibold text-slate-900 mt-1">
                94.2%
              </p>
              <p className="text-xs text-emerald-600 mt-1">Óptimo</p>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <p className="text-xs text-slate-500">Ley promedio</p>
              <p className="text-xl font-semibold text-slate-900 mt-1">
                1.32% Cu
              </p>
              <p className="text-xs text-indigo-600 mt-1">Sobre meta</p>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <p className="text-xs text-slate-500">Imágenes analizadas</p>
              <p className="text-xl font-semibold text-slate-900 mt-1">
                124 hoy
              </p>
              <p className="text-xs text-amber-600 mt-1">+18 vs ayer</p>
            </div>
          </section>

          {/* formulario + upload */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* formulario metadatos */}
            <div className="lg:col-span-2 space-y-4">
              <div className="bg-white border border-slate-200 rounded-xl p-4">
                <h2 className="text-sm font-semibold text-slate-900 mb-4">
                  Cargar imagen y metadatos
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                  <div className="space-y-1">
                    <label className="text-slate-600">Categoría</label>
                    <select
                      name="category"
                      value={metadata.category}
                      onChange={handleMetaChange}
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                    >
                      <option value="">Seleccionar</option>
                      <option value="Clasificación Mineral">
                        Clasificación Mineral
                      </option>
                      <option value="Análisis de Tajo">Análisis de Tajo</option>
                      <option value="Producción Activa">
                        Producción Activa
                      </option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-slate-600">Nivel de riesgo</label>
                    <select
                      name="riskLevel"
                      value={metadata.riskLevel}
                      onChange={handleMetaChange}
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                    >
                      <option value="">Seleccionar</option>
                      <option value="Bajo">Bajo</option>
                      <option value="Medio">Medio</option>
                      <option value="Alto">Alto</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-slate-600">Ubicación</label>
                    <input
                      name="location"
                      value={metadata.location}
                      onChange={handleMetaChange}
                      placeholder="Mina Norte - Zona A3"
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-slate-600">Coordenadas GPS</label>
                    <input
                      name="coordinates"
                      value={metadata.coordinates}
                      onChange={handleMetaChange}
                      placeholder={`23°45'12"S 69°23'45"W`}
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-slate-600">
                      Responsable del registro
                    </label>
                    <input
                      name="responsible"
                      value={metadata.responsible}
                      onChange={handleMetaChange}
                      placeholder="Geólogo supervisor"
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-slate-600">
                      Personal involucrado
                    </label>
                    <input
                      type="number"
                      name="personnel"
                      value={metadata.personnel}
                      onChange={handleMetaChange}
                      className="w-full rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
                      min={1}
                    />
                  </div>
                </div>
              </div>

              {/* subida de imagen */}
              <div className="bg-white border border-slate-200 rounded-xl p-4">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleFileChange}
                />

                {!filePreview ? (
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-slate-300 rounded-xl p-10 text-center text-sm text-slate-500 hover:border-blue-500 cursor-pointer"
                  >
                    <p className="font-medium text-slate-700 mb-1">
                      Arrastra una imagen aquí
                    </p>
                    <p className="text-xs">o haz clic para seleccionar</p>
                    <p className="text-[11px] mt-3 text-slate-400">
                      Formatos soportados: JPG, PNG
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <img
                      src={filePreview}
                      alt="Imagen subida"
                      className="w-full rounded-xl border border-slate-200"
                    />

                    <div className="flex gap-2">
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="flex-1 border border-slate-300 text-slate-700 rounded-lg py-2 text-sm hover:bg-slate-50"
                      >
                        Cambiar imagen
                      </button>

                      <button
                        disabled={loading}
                        onClick={handleAnalyze}
                        className="flex-1 rounded-lg py-2 text-sm text-white bg-blue-600 hover:bg-blue-700"
                      >
                        {loading ? "Analizando..." : "Analizar con IA"}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* RESULTADO IA */}
            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <h2 className="text-sm font-semibold text-slate-900 mb-3">
                Respuesta de la IA
              </h2>

              {!result && !loading && (
                <p className="text-xs text-slate-500">
                  Sube una imagen y presiona “Analizar con IA”.
                </p>
              )}

              {loading && (
                <p className="text-xs text-slate-500">Analizando...</p>
              )}

              {result && (
                <div className="text-xs space-y-2">
                  <p className="font-semibold text-slate-800">
                    {result.zone} · {result.copperGrade} · Riesgo{" "}
                    {result.riskLevel}
                  </p>

                  <p className="text-slate-600">{result.aiSummary}</p>

                  <ul className="list-disc pl-4 text-slate-600">
                    {result.recommendations.map((r) => (
                      <li key={r}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
