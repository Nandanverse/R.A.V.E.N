import { clsx } from "clsx";
import { forwardRef } from "react";
import { Controller, ControllerProps, FieldPath, FieldValues, UseFormRegister } from "react-hook-form";

export interface FormFieldProps<T extends FieldValues> extends Omit<ControllerProps<T>, "name" | "control" | "render"> {
  name: FieldPath<T>;
  control: ReturnType<UseFormRegister<T>>["control"];
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  children: (field: { onChange: (value: unknown) => void; onBlur: () => void; value: unknown; ref: React.RefCallback<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement> }) => React.ReactNode;
}

export function FormField<T extends FieldValues>({
  name,
  control,
  label,
  error,
  hint,
  required,
  children,
  ...props
}: FormFieldProps<T>) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field: { onChange, onBlur, value, ref }, fieldState: { error: fieldError } }) => (
        <div className="form-group" {...props}>
          <label className="form-label">
            {label}
            {required && <span className="text-sev-critical ml-1" aria-hidden="true">*</span>}
          </label>
          {children({ onChange, onBlur, value, ref })}
          {(error || fieldError?.message) && (
            <p className="form-error" role="alert">{error || fieldError?.message}</p>
          )}
          {hint && !error && !fieldError?.message && <p className="form-hint">{hint}</p>}
        </div>
      )}
    />
  );
}

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={clsx(error ? "input-error" : "input", className)}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: boolean;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={clsx(error ? "input-error" : "input", "resize-y min-h-[80px]", className)}
        {...props}
      />
    );
  }
);

Textarea.displayName = "Textarea";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  options: SelectOption[];
  placeholder?: string;
  error?: boolean;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, options, placeholder, error, ...props }, ref) => {
    return (
      <select
        ref={ref}
        className={clsx(error ? "input-error" : "input", className)}
        {...props}
      >
        {placeholder && <option value="" disabled>{placeholder}</option>}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} disabled={opt.disabled}>
            {opt.label}
          </option>
        ))}
      </select>
    );
  }
);

Select.displayName = "Select";