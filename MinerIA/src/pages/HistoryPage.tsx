import { useEffect, useState } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { TopBar } from "../components/layout/TopBar";
import { Link } from "react-router-dom";

// IMPORTS CORRECTOS
import type { AnalysisSummary } from "../api/analysis";
import { getAnalysisHistory } from "../api/analysis";

export function HistoryPage() {
  const [rows, setRows] = useState<AnalysisSummary[]>([]);

  useEffect(() => {
    getAnalysisHistory().then(setRows);
  }, []);

  return (
    <div className="min-h-screen flex bg-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopBar />
        <main className="flex-1 p-6">
          <div className="bg-white rounded-xl border border-slate-200 p-4">
            <h2 className="text-sm font-semibold text-slate-900 mb-4">
              Historial de análisis
            </h2>

            <table className="w-full text-xs text-left">
              <thead className="border-b border-slate-200 text-slate-500">
                <tr>
                  <th className="py-2">Fecha</th>
                  <th>Zona</th>
                  <th>Categoría</th>
                  <th>Riesgo</th>
                  <th>Ley Cu</th>
                  <th>Estado</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>
                {rows.map((r) => (
                  <tr key={r.id} className="border-b border-slate-100">
                    <td className="py-2">{r.date}</td>
                    <td>{r.zone}</td>
                    <td>{r.category}</td>
                    <td>{r.riskLevel}</td>
                    <td>{r.copperGrade}</td>
                    <td>{r.status}</td>
                    <td>
                      <Link
                        to={`/analysis/${r.id}`}
                        className="text-blue-600 hover:underline"
                      >
                        Ver detalle
                      </Link>
                    </td>
                  </tr>
                ))}

                {rows.length === 0 && (
                  <tr>
                    <td
                      colSpan={7}
                      className="py-4 text-center text-slate-400"
                    >
                      No hay análisis registrados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
}
