export function TopBar() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
      <div>
        <h1 className="text-lg font-semibold text-slate-900">
          Panel de Control
        </h1>
        <p className="text-xs text-slate-500">
          Monitoreo en tiempo real de operaciones mineras de cobre
        </p>
      </div>
      <span className="text-xs text-slate-400">
        MinerIA · Versión demo frontend
      </span>
    </header>
  );
}
