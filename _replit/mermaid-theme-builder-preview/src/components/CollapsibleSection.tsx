import { useState } from "react";

interface CollapsibleSectionProps {
  title: string;
  id: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export default function CollapsibleSection({ title, id, children, defaultOpen = false }: CollapsibleSectionProps) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div
      className="border border-border/50 rounded-lg bg-card overflow-hidden"
      data-testid={`collapsible-${id}`}
    >
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-muted/30 transition-colors group"
        aria-expanded={open}
        aria-controls={`collapsible-content-${id}`}
        data-testid={`collapsible-toggle-${id}`}
      >
        <span className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
          {title}
        </span>
        <svg
          viewBox="0 0 24 24"
          className={`w-4 h-4 text-muted-foreground transition-transform duration-200 flex-shrink-0 ${open ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {open && (
        <div
          id={`collapsible-content-${id}`}
          className="px-5 pb-5 pt-1 border-t border-border/30"
          data-testid={`collapsible-content-${id}`}
        >
          {children}
        </div>
      )}
    </div>
  );
}
