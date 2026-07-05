import { useMemo } from "react";

interface DayData {
  day: string;
  value: number;
}

interface ActivityChartProps {
  data: DayData[];
}

const CHART_HEIGHT = 144;

export function ActivityChart({ data }: ActivityChartProps) {
  const maxValue = useMemo(
    () => Math.max(...data.map((d) => d.value), 1),
    [data]
  );

  return (
    <div className="flex items-end gap-3" style={{ height: CHART_HEIGHT }}>
      {data.map((item) => {
        const pct = (item.value / maxValue) * 100;
        return (
          <div key={item.day} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
            <span className="text-caption text-neutral-500 font-medium tabular-nums">
              {item.value}
            </span>
            <div
              className="w-full bg-primary-500/80 hover:bg-primary-500 rounded-t-md transition-all duration-fast"
              style={{ height: `${pct}%`, minHeight: pct > 0 ? 4 : 0 }}
            />
            <span className="text-caption text-neutral-400">{item.day}</span>
          </div>
        );
      })}
    </div>
  );
}
