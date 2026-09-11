import { getExternalResearchers } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function ExternalResearchers() {
  const { data, status, error } = useApiData(getExternalResearchers);

  if (status === "loading") return <LoadingView label="Loading external researchers" />;
  if (status === "error") return <ErrorView message={error} />;

  const researchers = data?.external_researchers || [];
  if (researchers.length === 0) return <EmptyView message="No external researcher candidates yet." />;

  return (
    <div>
      <PageHeader
        title="External Researchers"
        description="Candidates outside the institution whose expertise fits current research areas. Mock data - discovery and fit-scoring logic will be added later."
      />

      <div className="overflow-hidden rounded-xl border border-navy-900/5 bg-white shadow-panel">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-navy-900/5 bg-sky-50/60 text-xs uppercase tracking-wide text-navy-900/45">
              <th className="px-5 py-3 font-medium">Researcher</th>
              <th className="px-5 py-3 font-medium">Institution</th>
              <th className="px-5 py-3 font-medium">Country</th>
              <th className="px-5 py-3 font-medium">Research Area</th>
              <th className="px-5 py-3 font-medium">Fit</th>
              <th className="px-5 py-3 font-medium">Reachability</th>
              <th className="px-5 py-3 font-medium">Overall</th>
            </tr>
          </thead>
          <tbody>
            {researchers.map((r) => (
              <tr key={r.id} className="border-b border-navy-900/5 last:border-0 hover:bg-sky-50/50">
                <td className="px-5 py-3 font-medium text-navy-950">{r.name}</td>
                <td className="px-5 py-3 text-navy-900/70">{r.institution}</td>
                <td className="px-5 py-3 text-navy-900/70">{r.country}</td>
                <td className="px-5 py-3 text-navy-700">{r.research_area}</td>
                <td className="px-5 py-3 text-navy-900/70">{r.research_fit}%</td>
                <td className="px-5 py-3"><StatusBadge status={r.network_reachability} /></td>
                <td className="px-5 py-3 font-display font-semibold text-navy-950">{r.overall_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
