import { forwardRef, useId } from "react";
import { cn } from "../../utils/cn";

interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    { label, error, helperText, className, id: externalId, ...props },
    ref
  ) => {
    const autoId = useId();
    const textareaId = externalId ?? autoId;
    const errorId = `${textareaId}-error`;
    const helperId = `${textareaId}-helper`;

    return (
      <div className="space-y-1">
        {label && (
          <label
            htmlFor={textareaId}
            className="block text-caption font-medium text-neutral-600"
          >
            {label}
          </label>
        )}

        <textarea
          ref={ref}
          id={textareaId}
          aria-invalid={!!error}
          aria-describedby={
            error ? errorId : helperText ? helperId : undefined
          }
          className={cn(
            "w-full border border-neutral-300 bg-white text-neutral-800 rounded-lg px-3 py-2 text-body",
            "placeholder:text-neutral-400",
            "transition-all duration-fast",
            "focus:border-primary-500 focus:ring-2 focus:ring-primary-100 focus:outline-none",
            "disabled:cursor-not-allowed disabled:bg-neutral-50 disabled:text-neutral-400",
            "resize-y min-h-[80px]",
            error &&
              "border-danger-500 focus:border-danger-500 focus:ring-danger-100",
            className
          )}
          {...props}
        />

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

Textarea.displayName = "Textarea";
