import { forwardRef } from "react";
import { Loader2 } from "lucide-react";
import { cn } from "../../utils/cn";

const variantStyles = {
  primary:
    "bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 shadow-xs",
  secondary:
    "bg-neutral-100 text-neutral-700 hover:bg-neutral-200 active:bg-neutral-300",
  outline:
    "border border-neutral-300 text-neutral-700 hover:bg-neutral-50 active:bg-neutral-100",
  ghost: "text-neutral-600 hover:bg-neutral-100 active:bg-neutral-200",
  danger:
    "bg-danger-600 text-white hover:bg-danger-700 active:bg-danger-800 shadow-xs",
};

const sizeStyles = {
  sm: "h-8 px-3 text-caption rounded-md gap-1.5",
  md: "h-10 px-4 text-body rounded-lg gap-2",
  lg: "h-12 px-6 text-body rounded-lg gap-2.5",
};

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variantStyles;
  size?: keyof typeof sizeStyles;
  loading?: boolean;
  iconLeft?: React.ReactNode;
  iconRight?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = "primary",
      size = "md",
      loading = false,
      iconLeft,
      iconRight,
      className,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          "inline-flex items-center justify-center font-medium transition-all duration-fast",
          "disabled:pointer-events-none disabled:opacity-50",
          "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500",
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin shrink-0" />
        ) : iconLeft ? (
          <span className="shrink-0">{iconLeft}</span>
        ) : null}
        {children && <span>{children}</span>}
        {!loading && iconRight && (
          <span className="shrink-0">{iconRight}</span>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
