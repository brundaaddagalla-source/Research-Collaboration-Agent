export function KpiCard({ label, value, icon: Icon, accent = "navy" }) {
  const accentMap = {
    navy: "text-navy-700 bg-sky-100",
    active: "text-signal-active bg-signal-active/10",
    dormant: "text-signal-dormant bg-signal-dormant/10",
  };

  return (
    <div className="flex items-center gap-4 rounded-xl border border-navy-900/5 bg-white p-4 shadow-panel">
      <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${accentMap[accent]}`}>
        <Icon className="h-5 w-5" />
      </div>
      <div className="min-w-0">
        <p className="font-display text-xl font-bold leading-none text-navy-950">{value}</p>
        <p className="mt-1 truncate text-xs text-navy-900/55">{label}</p>
      </div>
    </div>
  );
}
