export function KpiCard({ label, value, icon: Icon, accent = "blue" }) {
  const accentMap = {
    navy: { badge: "text-navy-700 bg-sky-100", bar: "bg-navy-700" },
    blue: { badge: "text-accent-blue bg-accent-blue/10", bar: "bg-accent-blue" },
    teal: { badge: "text-accent-teal bg-accent-teal/10", bar: "bg-accent-teal" },
    green: { badge: "text-accent-green bg-accent-green/10", bar: "bg-accent-green" },
    purple: { badge: "text-accent-purple bg-accent-purple/10", bar: "bg-accent-purple" },
    orange: { badge: "text-accent-orange bg-accent-orange/10", bar: "bg-accent-orange" },
    active: { badge: "text-signal-active bg-signal-active/10", bar: "bg-signal-active" },
    dormant: { badge: "text-signal-dormant bg-signal-dormant/10", bar: "bg-signal-dormant" },
  };

  const { badge, bar } = accentMap[accent] || accentMap.blue;

  return (
    <div className="group relative overflow-hidden rounded-xl border border-navy-900/5 bg-white p-4 shadow-panel">
      <div className="flex items-center gap-4">
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${badge}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="min-w-0">
          <p className="font-display text-xl font-bold leading-none text-navy-950">{value}</p>
          <p className="mt-1 truncate text-xs text-navy-900/55">{label}</p>
        </div>
      </div>
      <div className={`absolute inset-x-0 bottom-0 h-1 ${bar} opacity-70`} />
    </div>
  );
}