import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import { LoginPage } from "./paginas/PaginaInicioSesion";
import { DashboardPage } from "./paginas/PaginaPanel";
import { HistoryPage } from "./paginas/PaginaHistorial";
import { AnalysisDetailPage } from "./paginas/PaginaDetalleAnalisis";
import { NewAnalysisPage } from "./paginas/PaginaNuevoAnalisis";
import { NotFoundPage } from "./paginas/PaginaNoEncontrada";

import { AuthProvider } from "./context/AuthProvider"; 
import { useAuth } from "./context/useAuth";
import { Layout } from "./componentes/layout/Disposicion";
import { ToastProvider } from "./componentes/ui/Notificacion";
import type { JSX } from "react";

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <AuthProvider>
        <BrowserRouter>
          <ToastProvider>
          <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route element={<Layout />}>
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <DashboardPage />
                </PrivateRoute>
              }
            />

            <Route
              path="/history"
              element={
                <PrivateRoute>
                  <HistoryPage />
                </PrivateRoute>
              }
            />

            <Route
              path="/analysis/new"
              element={
                <PrivateRoute>
                  <NewAnalysisPage />
                </PrivateRoute>
              }
            />

            <Route
              path="/analysis/:id"
              element={
                <PrivateRoute>
                  <AnalysisDetailPage />
                </PrivateRoute>
              }
            />
          </Route>

          {/* fallback */}
          <Route path="*" element={<NotFoundPage />} />
          </Routes>
          </ToastProvider>
        </BrowserRouter>
    </AuthProvider>
  );
}
