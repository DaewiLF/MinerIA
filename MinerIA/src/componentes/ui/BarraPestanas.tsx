import { cn } from "../../utils/cn";

interface Tab {
  id: string;
  label: string;
  badge?: string | number;
}

interface TabBarProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (tabId: string) => void;
  className?: string;
}

export function TabBar({
  tabs,
  activeTab,
  onChange,
  className,
}: TabBarProps) {
  return (
    <div
      role="tablist"
      className={cn(
        "inline-flex items-center border border-neutral-200 rounded-lg p-1 bg-neutral-50 gap-0.5",
        className
      )}
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={activeTab === tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            "inline-flex items-center gap-2 px-4 py-2 text-caption font-medium rounded-md transition-all duration-fast",
            "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500",
            activeTab === tab.id
              ? "bg-white text-neutral-800 shadow-xs"
              : "text-neutral-500 hover:text-neutral-700"
          )}
        >
          {tab.label}
          {tab.badge != null && (
            <span className="inline-flex items-center justify-center min-w-[20px] h-5 px-1.5 text-caption-bold rounded-full bg-neutral-200 text-neutral-600">
              {tab.badge}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
