import { createElement } from "react";
import { cn } from "../../utils/cn";

const sizeClasses = {
  xl: "text-heading-xl",
  lg: "text-heading-lg",
  md: "text-heading-md",
};

type Tag = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";

const levelMap: Record<number, Tag> = {
  1: "h1",
  2: "h2",
  3: "h3",
  4: "h4",
  5: "h5",
  6: "h6",
};

interface HeadingProps {
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  size?: keyof typeof sizeClasses;
  className?: string;
  children: React.ReactNode;
}

export function Heading({
  level = 2,
  size,
  className,
  children,
}: HeadingProps) {
  const tag = levelMap[level] ?? "h2";
  const visualSize = size ?? (level <= 1 ? "xl" : level === 2 ? "lg" : "md");

  return createElement(
    tag,
    {
      className: cn(
        "text-neutral-800 font-semibold",
        sizeClasses[visualSize],
        className
      ),
    },
    children
  );
}
