import { Outlet } from "react-router-dom";
import { Sidebar } from "./BarraLateral";
import { TopBar } from "./BarraSuperior";
import { useSidebar } from "../../hooks/usarSidebar";

export function Layout() {
  const { collapsed, mobileOpen, toggleCollapsed, openMobile, closeMobile } =
    useSidebar();

  return (
    <div className="h-screen flex bg-neutral-50 overflow-hidden">
      <Sidebar
        collapsed={collapsed}
        onToggleCollapsed={toggleCollapsed}
        mobileOpen={mobileOpen}
        onMobileClose={closeMobile}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar onMenuClick={openMobile} />

        <main className="flex-1 p-4 lg:p-6 overflow-auto animate-[fadeIn_0.25s_ease-out]">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
