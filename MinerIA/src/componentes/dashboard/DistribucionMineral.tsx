import { cn } from "../../utils/cn";

interface MineralItem {
  name: string;
  percent: number;
  color: string;
}

interface MineralDistributionProps {
  data: MineralItem[];
}

export function MineralDistribution({ data }: MineralDistributionProps) {
  return (
    <div className="space-y-4">
      {data.map((item) => (
        <div key={item.name} className="flex items-center gap-3">
          <div
            className="w-3 h-3 rounded-full shrink-0"
            style={{ backgroundColor: item.color }}
          />
          <span className="text-small text-neutral-600 flex-1 min-w-0 truncate">
            {item.name}
          </span>
          <div className="w-28 sm:w-36 h-2 bg-neutral-100 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-slow"
              style={{
                width: `${item.percent}%`,
                backgroundColor: item.color,
              }}
            />
          </div>
          <span
            className={cn(
              "text-caption tabular-nums w-10 text-right",
              item.percent > 30
                ? "text-neutral-700 font-medium"
                : "text-neutral-400"
            )}
          >
            {item.percent}%
          </span>
        </div>
      ))}
    </div>
  );
}
