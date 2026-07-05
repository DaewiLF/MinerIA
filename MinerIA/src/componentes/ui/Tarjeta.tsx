import { cn } from "../../utils/cn";

const variantStyles = {
  default: "bg-white border border-neutral-200",
  elevated: "bg-white border border-neutral-200 shadow-sm",
  flat: "bg-neutral-50",
};

const paddingStyles = {
  none: "",
  sm: "p-3",
  md: "p-4",
  lg: "p-6",
};

interface CardProps {
  variant?: keyof typeof variantStyles;
  padding?: keyof typeof paddingStyles;
  className?: string;
  children: React.ReactNode;
}

export function Card({
  variant = "default",
  padding = "md",
  className,
  children,
}: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl transition-all duration-fast",
        variantStyles[variant],
        paddingStyles[padding],
        variant === "elevated" && "hover:shadow-md",
        className
      )}
    >
      {children}
    </div>
  );
}

Card.Header = function CardHeader({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={cn("mb-4", className)}>
      {children}
    </div>
  );
};

Card.Body = function CardBody({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("", className)}>{children}</div>;
};

Card.Footer = function CardFooter({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "mt-4 pt-4 border-t border-neutral-200",
        className
      )}
    >
      {children}
    </div>
  );
};
