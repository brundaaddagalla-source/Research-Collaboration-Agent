import { CircleDot } from "lucide-react";

export function Topbar() {
  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-navy-900/8 bg-sky-50/80 px-6 py-4 backdrop-blur lg:px-8">
      <div>
        <p className="text-[11px] uppercase tracking-wide text-navy-900/40">CSE · Agentic AI Platform</p>
        <p className="font-display text-sm font-semibold text-navy-950">Vignan's Institution</p>
      </div>
      <div className="flex items-center gap-2 rounded-full bg-white px-3 py-1.5 text-xs text-navy-900/60 shadow-panel">
        <CircleDot className="h-3.5 w-3.5 text-signal-active" />
        API connected · localhost:8000
      </div>
    </header>
  );
}
