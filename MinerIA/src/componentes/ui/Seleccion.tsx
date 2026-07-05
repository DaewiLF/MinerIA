import { forwardRef, useId } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "../../utils/cn";

const sizeStyles = {
  sm: "h-8 px-2.5 text-caption rounded-md",
  md: "h-10 px-3 text-body rounded-lg",
  lg: "h-12 px-4 text-body rounded-lg",
};

interface Option {
  value: string;
  label: string;
}

interface SelectProps
  extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "children"> {
  label?: string;
  error?: string;
  options: Option[];
  placeholder?: string;
  selectSize?: keyof typeof sizeStyles;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      label,
      error,
      options,
      placeholder = "Seleccionar",
      selectSize = "md",
      className,
      id: externalId,
      ...props
    },
    ref
  ) => {
    const autoId = useId();
    const selectId = externalId ?? autoId;
    const errorId = `${selectId}-error`;

    return (
      <div className="space-y-1">
        {label && (
          <label
            htmlFor={selectId}
            className="block text-caption font-medium text-neutral-600"
          >
            {label}
          </label>
        )}

        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            aria-invalid={!!error}
            aria-describedby={error ? errorId : undefined}
            className={cn(
              "w-full appearance-none border border-neutral-300 bg-white text-neutral-800",
              "transition-all duration-fast",
              "focus:border-primary-500 focus:ring-2 focus:ring-primary-100 focus:outline-none",
              "disabled:cursor-not-allowed disabled:bg-neutral-50 disabled:text-neutral-400",
              "pr-10",
              error &&
                "border-danger-500 focus:border-danger-500 focus:ring-danger-100",
              sizeStyles[selectSize],
              className
            )}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>

          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 pointer-events-none">
            <ChevronDown className="h-4 w-4" />
          </span>
        </div>

        {error && (
          <p id={errorId} className="text-caption text-danger-600" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = "Select";
