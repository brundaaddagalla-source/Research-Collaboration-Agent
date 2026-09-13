export function PageHeader({ title, description, icon: Icon }) {
  return (
    <div className="relative mb-6 overflow-hidden rounded-panel border border-surface-line bg-hero px-6 py-6 shadow-panel sm:px-8 sm:py-7">
      {/* Soft decorative glow */}
      <div className="pointer-events-none absolute -right-12 -top-16 h-48 w-48 rounded-full bg-blue/10 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-20 left-1/4 h-40 w-40 rounded-full bg-accent-purple/10 blur-3xl" />

      <div className="relative flex items-start gap-3">
        {Icon && (
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white ring-1 ring-blue/10 shadow-sm">
            <Icon className="h-5 w-5 text-blue" />
          </div>
        )}

        <div className="min-w-0">
          <p className="mb-1 text-[11px] font-semibold uppercase tracking-wider text-blue">
            Agent 24 · Research Collaboration
          </p>

          <h1 className="font-display text-xl font-bold text-navy-800 sm:text-2xl">
            {title}
          </h1>

          {description && (
            <p className="mt-1 max-w-2xl text-sm leading-6 text-surface-muted">
              {description}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}