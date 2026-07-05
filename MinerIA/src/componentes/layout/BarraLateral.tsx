import { useEffect, useRef } from "react";
import { NavLink } from "react-router-dom";
import { cn } from "../../utils/cn";
import { useAuth } from "../../context/useAuth";
import { useMediaQuery } from "../../hooks/usarMediaQuery";
import {
  LayoutDashboard,
  History,
  Plus,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Pickaxe,
  User,
} from "lucide-react";

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapsed: () => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/analysis/new", label: "Nuevo análisis", icon: Plus },
  { to: "/history", label: "Historial", icon: History },
];

export function Sidebar({
  collapsed,
  onToggleCollapsed,
  mobileOpen,
  onMobileClose,
}: SidebarProps) {
  const { user, logout } = useAuth();
  const isMobile = useMediaQuery("(max-width: 1023px)");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mobileOpen) {
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  useEffect(() => {
    if (isMobile && !mobileOpen) return;
    if (!isMobile && mobileOpen) onMobileClose();
  }, [isMobile, mobileOpen, onMobileClose]);

  const sidebarContent = (
    <aside
      className={cn(
        "flex flex-col bg-neutral-900 text-neutral-100 transition-all duration-200 ease-out",
        collapsed && !isMobile ? "w-16" : "w-64"
      )}
    >
      {/* Logo */}
      <div
        className={cn(
          "flex items-center border-b border-neutral-800 shrink-0",
          collapsed && !isMobile ? "justify-center px-2 py-4" : "px-4 py-4"
        )}
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-9 h-9 rounded-lg bg-primary-600 flex items-center justify-center text-white shrink-0">
            <Pickaxe className="h-5 w-5" />
          </div>
          {(!collapsed || isMobile) && (
            <div className="truncate">
              <div className="font-semibold text-sm">MinerIA</div>
              <div className="text-[11px] text-neutral-400 truncate">
                Gestión Minera
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onMobileClose}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-lg transition-all duration-fast text-caption font-medium",
                collapsed && !isMobile ? "justify-center px-2 py-2.5" : "px-3 py-2.5",
                isActive
                  ? "bg-primary-600 text-white shadow-xs"
                  : "text-neutral-300 hover:bg-neutral-800 hover:text-white"
              )
            }
          >
            <item.icon className="h-5 w-5 shrink-0" />
            {(!collapsed || isMobile) && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* User & Logout */}
      <div
        className={cn(
          "border-t border-neutral-800 py-3",
          collapsed && !isMobile ? "px-2" : "px-4"
        )}
      >
        {user && (!collapsed || isMobile) && (
          <div className="flex items-center gap-3 px-1 mb-3">
            <div className="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center shrink-0">
              <User className="h-4 w-4 text-neutral-300" />
            </div>
            <div className="truncate min-w-0">
              <div className="text-caption-bold text-neutral-200 truncate">
                {user.name ?? user.email}
              </div>
              <div className="text-caption text-neutral-400 capitalize truncate">
                {user.role}
              </div>
            </div>
          </div>
        )}

        {collapsed && !isMobile && user && (
          <div className="flex justify-center mb-3">
            <div className="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center">
              <User className="h-4 w-4 text-neutral-300" />
            </div>
          </div>
        )}

        <button
          onClick={() => { logout(); onMobileClose(); }}
          className={cn(
            "flex items-center gap-3 w-full rounded-lg text-caption font-medium transition-all duration-fast text-neutral-300 hover:bg-neutral-800 hover:text-white",
            collapsed && !isMobile ? "justify-center px-2 py-2.5" : "px-3 py-2.5"
          )}
        >
          <LogOut className="h-5 w-5 shrink-0" />
          {(!collapsed || isMobile) && <span>Cerrar sesión</span>}
        </button>
      </div>

      {/* Collapse toggle (desktop only) */}
      {!isMobile && (
        <button
          onClick={onToggleCollapsed}
          className="flex items-center justify-center h-10 border-t border-neutral-800 text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors shrink-0"
          aria-label={collapsed ? "Expandir menú" : "Colapsar menú"}
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </button>
      )}
    </aside>
  );

  if (isMobile) {
    return (
      <>
        {/* Overlay */}
        {mobileOpen && (
          <div
            ref={overlayRef}
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
            onClick={onMobileClose}
          />
        )}

        {/* Drawer */}
        <div
          className={cn(
            "fixed inset-y-0 left-0 z-50 w-64 shadow-xl transition-transform duration-200 ease-out",
            mobileOpen ? "translate-x-0" : "-translate-x-full"
          )}
        >
          {sidebarContent}
        </div>
      </>
    );
  }

  return sidebarContent;
}
