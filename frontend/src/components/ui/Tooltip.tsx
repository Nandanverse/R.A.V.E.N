import { useState, useRef, useEffect, Fragment } from "react";
import { clsx } from "clsx";

export interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  position?: "top" | "bottom" | "left" | "right";
  delay?: number;
  className?: string;
}

export function Tooltip({ content, children, position = "top", delay = 200, className }: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef<number>();
  const childRef = useRef<HTMLElement>(null);

  const show = () => {
    timeoutRef.current = window.setTimeout(() => setIsVisible(true), delay);
  };

  const hide = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setIsVisible(false);
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  const positionClasses = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2",
  };

  const arrowClasses = {
    top: "top-full left-1/2 -translate-x-1/2 border-t-separator",
    bottom: "bottom-full left-1/2 -translate-x-1/2 border-b-separator",
    left: "left-full top-1/2 -translate-y-1/2 border-l-separator",
    right: "right-full top-1/2 -translate-y-1/2 border-r-separator",
  };

  const childWithEvents = React.cloneElement(children, {
    ref: childRef,
    onMouseEnter: show,
    onMouseLeave: hide,
    onFocus: show,
    onBlur: hide,
  });

  return (
    <Fragment>
      {childWithEvents}
      {isVisible && (
        <div
          className={clsx("tooltip", positionClasses[position], className)}
          role="tooltip"
          aria-hidden={!isVisible}
        >
          {content}
          <div className={clsx("absolute w-0 h-0 border-4 border-transparent", arrowClasses[position])} />
        </div>
      )}
    </Fragment>
  );
}