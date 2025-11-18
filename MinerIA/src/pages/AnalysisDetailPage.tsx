import { getAnalysisById } from "../api/analysis";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Sidebar } from "../components/layout/Sidebar";
import { TopBar } from "../components/layout/TopBar";
import type { AnalysisDetail } from "../api/analysis";


export function AnalysisDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<AnalysisDetail | null>(null);
  const apiBase = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
  const handleDownloadPdf = async () => {
  if (!data) return;
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Debes iniciar sesión nuevamente para descargar el reporte.");
      return;
    }

    try {
      const resp = await fetch(
        `${apiBase}/api/analysis/${data.id}/pdf`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!resp.ok) {
        throw new Error(`Error ${resp.status}`);
      }

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
  
  useEffect(() => {
    if (id) getAnalysisById(id).then(setData);
  }, [id]);

  return (
    <div className="min-h-screen flex bg-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopBar />
        <main className="flex-1 p-6">
          {!data ? (
            <p className="text-sm text-slate-500">
              Cargando detalle de análisis...
            </p>
          ) : (
            <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-4 text-sm">
              <div className="flex gap-4">
                <img
                  src={`${apiBase}${data.imageUrl}`}
                  alt="Análisis"
                  className="w-64 h-40 object-cover rounded-lg border border-slate-200"
                />
                <div className="space-y-1">
                  <h2 className="font-semibold text-slate-900">
                    {data.zone} · {data.copperGrade}
                  </h2>
                  <p className="text-xs text-slate-500">{data.date}</p>
                  <p className="text-xs text-slate-600">
                    Categoría: {data.category}
                  </p>
                  <p className="text-xs text-slate-600">
                    Riesgo: {data.riskLevel}
                  </p>
                  <p className="text-xs text-slate-600">
                    Estado: {data.status}
                  </p>
                </div>
              </div>

              <div>
                <h3 className="text-xs font-semibold text-slate-800 mb-1">
                  Resumen IA
                </h3>
                <p className="text-xs text-slate-600">{data.aiSummary}</p>
              </div>

              <div>
                <h3 className="text-xs font-semibold text-slate-800 mb-1">
                  Recomendaciones
                </h3>
                <ul className="text-xs text-slate-600 list-disc pl-4">
                  {data.recommendations.map((r) => (
                    <li key={r}>{r}</li>
                  ))}
                </ul>
                <a onClick={handleDownloadPdf} className="inline-block mt-2 text-xs text-blue-600 hover:underline" >Descargar reporte PDF</a>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
