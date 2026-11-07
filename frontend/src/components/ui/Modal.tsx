import { clsx } from "clsx";
import { forwardRef } from "react";
import { X } from "lucide-react";

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

export function Modal({ isOpen, onClose, title, children, footer, size = "md", className }: ModalProps) {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
  };

  return (
    <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby={title ? "modal-title" : undefined}>
      <div className={clsx("modal", sizeClasses[size], className)} onClick={(e) => e.stopPropagation()}>
        {(title || footer) && (
          <div className="modal-header">
            {title && <h2 id="modal-title" className="text-lg font-medium text-fg-primary">{title}</h2>}
            <button
              onClick={onClose}
              className="p-1 text-fg-muted hover:text-fg-primary rounded-sm hover:bg-bg-hover"
              aria-label="Close modal"
            >
              <X size={18} />
            </button>
          </div>
        )}
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
}