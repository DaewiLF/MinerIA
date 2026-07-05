import { forwardRef, useId } from "react";
import { cn } from "../../utils/cn";

const sizeStyles = {
  sm: "h-8 px-2.5 text-caption rounded-md",
  md: "h-10 px-3 text-body rounded-lg",
  lg: "h-12 px-4 text-body rounded-lg",
};

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  iconPrefix?: React.ReactNode;
  inputSize?: keyof typeof sizeStyles;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      iconPrefix,
      inputSize = "md",
      className,
      id: externalId,
      ...props
    },
    ref
  ) => {
    const autoId = useId();
    const inputId = externalId ?? autoId;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    return (
      <div className="space-y-1">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-caption font-medium text-neutral-600"
          >
            {label}
          </label>
        )}

        <div className="relative">
          {iconPrefix && (
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400 pointer-events-none">
              {iconPrefix}
            </span>
          )}

          <input
            ref={ref}
            id={inputId}
            aria-invalid={!!error}
            aria-describedby={
              error ? errorId : helperText ? helperId : undefined
            }
            className={cn(
              "w-full border border-neutral-300 bg-white text-neutral-800",
              "placeholder:text-neutral-400",
              "transition-all duration-fast",
              "focus:border-primary-500 focus:ring-2 focus:ring-primary-100 focus:outline-none",
              "disabled:cursor-not-allowed disabled:bg-neutral-50 disabled:text-neutral-400",
              iconPrefix && "pl-10",
              error &&
                "border-danger-500 focus:border-danger-500 focus:ring-danger-100",
              sizeStyles[inputSize],
              className
            )}
            {...props}
          />
        </div>

        {error && (
          <p id={errorId} className="text-caption text-danger-600" role="alert">
            {error}
          </p>
        )}

        {helperText && !error && (
          <p id={helperId} className="text-caption text-neutral-400">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
