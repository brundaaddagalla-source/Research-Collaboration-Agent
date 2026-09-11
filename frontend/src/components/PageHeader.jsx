export function PageHeader({ title, description }) {
  return (
    <div className="mb-6">
      <h1 className="font-display text-2xl font-bold text-navy-950">{title}</h1>
      {description && <p className="mt-1 max-w-2xl text-sm text-navy-900/55">{description}</p>}
    </div>
  );
}
