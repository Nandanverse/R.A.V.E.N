import { useState, useRef, useEffect, Fragment } from "react";
import { clsx } from "clsx";
import { ChevronDown } from "lucide-react";

export interface DropdownItem {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  danger?: boolean;
  icon?: React.ReactNode;
}

export interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: "left" | "right";
  className?: string;
}

export function Dropdown({ trigger, items, align = "left", className }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className={clsx("relative inline-block", className)} ref={dropdownRef}>
      <div onClick={() => setIsOpen(!isOpen)} className="inline-flex items-center gap-1">
        {trigger}
        <ChevronDown size={14} className="text-fg-muted" aria-hidden="true" />
      </div>
      {isOpen && (
        <div
          className={clsx("dropdown", align === "right" && "right-0")}
          role="menu"
          aria-orientation="vertical"
        >
          {items.map((item, index) => (
            item.label === "divider" ? (
              <div key={`divider-${index}`} className="dropdown-divider" role="separator" />
            ) : (
              <button
                key={index}
                role="menuitem"
                tabIndex={-1}
                className={clsx(
                  "dropdown-item w-full",
                  item.disabled && "opacity-50 cursor-not-allowed",
                  item.danger && "text-sev-critical"
                )}
                onClick={() => {
                  if (!item.disabled) {
                    item.onClick();
                    setIsOpen(false);
                  }
                }}
                disabled={item.disabled}
              >
                {item.icon && <span className="flex items-center" aria-hidden="true">{item.icon}</span>}
                <span className="flex-1 text-left">{item.label}</span>
              </button>
            )
          ))}
        </div>
      )}
    </div>
  );
}