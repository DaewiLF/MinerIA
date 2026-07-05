import { cn } from "../../utils/cn";

const variants = {
  text: "h-4 rounded",
  title: "h-6 rounded-md",
  circle: "rounded-full",
  rect: "rounded-lg",
} as const;

interface SkeletonProps {
  variant?: keyof typeof variants;
  className?: string;
}

export function Skeleton({ variant = "text", className }: SkeletonProps) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "animate-pulse bg-neutral-200",
        variants[variant],
        className
      )}
    />
  );
}

interface LoadingSkeletonProps {
  lines?: number;
  className?: string;
}

export function LoadingSkeleton({
  lines = 3,
  className,
}: LoadingSkeletonProps) {
  return (
    <div className={cn("space-y-3", className)}>
      <Skeleton variant="title" className="w-3/4" />
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          variant="text"
          className={i === lines - 1 ? "w-1/2" : "w-full"}
        />
      ))}
    </div>
  );
}

LoadingSkeleton.Skeleton = Skeleton;
