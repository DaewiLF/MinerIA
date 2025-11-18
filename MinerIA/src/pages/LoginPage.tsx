import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { LoginPayload } from "../api/auth";
import { loginApi } from "../api/auth";
import { useAuth } from "../context/useAuth";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState<LoginPayload>({
    email: "",
    password: "",
    role: "admin",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const resp = await loginApi(form);
      login(resp);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Error al iniciar sesión.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-slate-900 relative overflow-hidden">
      <div className="absolute inset-0 opacity-30">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "linear-gradient(30deg, #1e293b 12%, transparent 12.5%, transparent 87%, #1e293b 87.5%, #1e293b), linear-gradient(150deg, #1e293b 12%, transparent 12.5%, transparent 87%, #1e293b 87.5%, #1e293b)",
            backgroundSize: "80px 140px",
            backgroundPosition: "0 0, 40px 70px",
          }}
        />
      </div>

      <div className="relative z-10 w-full max-w-md px-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 border border-slate-200">
          <div className="flex flex-col items-center mb-8">
            <div className="w-14 h-14 rounded-2xl bg-blue-600 flex items-center justify-center text-white text-2xl mb-3">
              ⛏
            </div>
            <h1 className="text-xl font-semibold text-slate-900">MinerIA</h1>
            <p className="text-sm text-slate-500">
              Sistema de Gestión Inteligente
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 text-sm">
            <div className="space-y-1">
              <label className="text-slate-700 text-xs">Rol de usuario</label>
              <select
                name="role"
                value={form.role}
                onChange={handleChange}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 bg-slate-50 text-sm"
              >
                <option value="admin">Administrador</option>
                <option value="analyst">Analista / Regulador</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-slate-700 text-xs">
                Correo electrónico
              </label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="usuario@mineria.com"
                className="w-full border border-slate-300 rounded-lg px-3 py-2 bg-slate-50 text-sm"
                required
              />
            </div>

            <div className="space-y-1">
              <label className="text-slate-700 text-xs">Contraseña</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full border border-slate-300 rounded-lg px-3 py-2 bg-slate-50 text-sm"
                required
              />
            </div>

            {error && (
              <p className="text-xs text-red-600 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 text-sm font-medium shadow-md transition"
            >
              {loading ? "Ingresando..." : "Iniciar sesión"}
            </button>

            <p className="text-[11px] text-slate-400 text-center mt-4">
              © 2025 MinerIA. Todos los derechos reservados.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
