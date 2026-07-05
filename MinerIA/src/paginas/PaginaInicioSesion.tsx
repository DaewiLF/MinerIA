import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Pickaxe, LogIn } from "lucide-react";
import type { LoginPayload } from "../api/auth";
import { loginApi } from "../api/auth";
import { useAuth } from "../context/useAuth";
import { Button } from "../componentes/ui/Boton";
import { Input } from "../componentes/ui/Entrada";
import { Select } from "../componentes/ui/Seleccion";

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
    } catch {
      setError("Error al iniciar sesión.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-neutral-900 relative overflow-hidden">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-20">
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
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-neutral-200">
          {/* Logo */}
          <div className="flex flex-col items-center mb-8">
            <div className="w-14 h-14 rounded-2xl bg-primary-600 flex items-center justify-center text-white mb-3">
              <Pickaxe className="h-7 w-7" />
            </div>
            <h1 className="text-heading-lg text-neutral-900">MinerIA</h1>
            <p className="text-small text-neutral-500">
              Sistema de Gestión Inteligente
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Select
              label="Rol de usuario"
              name="role"
              value={form.role}
              onChange={handleChange}
              options={[
                { value: "admin", label: "Administrador" },
                { value: "analyst", label: "Analista / Regulador" },
              ]}
              selectSize="md"
            />

            <Input
              label="Correo electrónico"
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="usuario@mineria.com"
              inputSize="md"
              required
            />

            <Input
              label="Contraseña"
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="••••••••"
              inputSize="md"
              required
            />

            {error && (
              <p className="text-caption text-danger-600 text-center">{error}</p>
            )}

            <Button
              type="submit"
              variant="primary"
              loading={loading}
              iconLeft={!loading ? <LogIn className="h-4 w-4" /> : undefined}
              className="w-full"
            >
              {loading ? "Ingresando..." : "Iniciar sesión"}
            </Button>

            <p className="text-caption text-neutral-400 text-center">
              © 2026 MinerIA. Todos los derechos reservados.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
