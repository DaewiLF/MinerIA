import { cn } from "../../utils/cn";

const variantStyles = {
  primary: "bg-primary-50 text-primary-700",
  success: "bg-success-50 text-success-600",
  warning: "bg-warning-50 text-warning-600",
  danger: "bg-danger-50 text-danger-600",
  info: "bg-info-50 text-info-600",
  neutral: "bg-neutral-100 text-neutral-600",
};

const sizeStyles = {
  sm: "px-2 py-0.5 text-caption-bold",
  md: "px-2.5 py-1 text-caption-bold",
};

interface BadgeProps {
  variant?: keyof typeof variantStyles;
  size?: keyof typeof sizeStyles;
  dot?: boolean;
  children: React.ReactNode;
}

export function Badge({
  variant = "neutral",
  size = "md",
  dot = false,
  children,
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium",
        variantStyles[variant],
        sizeStyles[size]
      )}
    >
      {dot && <StatusDot variant={variant as keyof typeof dotVariantMap} size="sm" />}
      {children}
    </span>
  );
}

const dotVariantMap = {
  primary: "bg-primary-500",
  success: "bg-success-500",
  warning: "bg-warning-500",
  danger: "bg-danger-500",
  info: "bg-info-500",
  neutral: "bg-neutral-400",
} as const;

interface StatusDotProps {
  variant?: keyof typeof dotVariantMap;
  size?: "sm" | "md";
  pulse?: boolean;
}

export function StatusDot({
  variant = "neutral",
  size = "md",
  pulse = false,
}: StatusDotProps) {
  return (
    <span
      className={cn(
        "inline-block rounded-full shrink-0",
        dotVariantMap[variant],
        size === "sm" ? "h-1.5 w-1.5" : "h-2 w-2",
        pulse && "animate-pulse"
      )}
      aria-hidden="true"
    />
  );
}
