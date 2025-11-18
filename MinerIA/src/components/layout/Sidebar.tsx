import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/useAuth";

export function Sidebar() {
  const { user, logout } = useAuth();

  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition ${
      isActive
        ? "bg-blue-600 text-white"
        : "text-slate-200 hover:bg-slate-700 hover:text-white"
    }`;

  return (
    <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col">
      {/* Logo */}
      <div className="px-4 py-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white text-xl">
            ⛏
          </div>
          <div>
            <div className="font-semibold">MinerIA</div>
            <div className="text-xs text-slate-400">Gestión Minera</div>
          </div>
        </div>
      </div>

      {/* navegación */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        <NavLink to="/dashboard" className={linkClasses}>
          Inicio
        </NavLink>
        <NavLink to="/history" className={linkClasses}>
          Historial
        </NavLink>
      </nav>

      {/* user info + logout */}
      <div className="px-4 py-4 border-t border-slate-800 text-xs text-slate-400 space-y-2">
        {user && (
          <div>
           <div className="font-medium text-slate-200">
             {user.email}
            </div>
            <div className="capitalize">{user.role}</div>
          </div>
        )}

        <button
          onClick={logout}
          className="w-full text-left text-slate-300 hover:text-white hover:bg-slate-800 px-3 py-2 rounded-lg text-sm transition"
        >
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
