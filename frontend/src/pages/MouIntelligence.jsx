import { getMous } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function MouIntelligence() {
  const { data, status, error } = useApiData(getMous);

  if (status === "loading") return <LoadingView label="Loading MoU records" />;
  if (status === "error") return <ErrorView message={error} />;

  const mous = data?.mous || [];
  if (mous.length === 0) return <EmptyView message="No MoUs recorded yet." />;

  return (
    <div>
      <PageHeader
        title="MoU Intelligence"
        description="Institutional partnerships and their usage status. Mock classifications - dormancy detection logic will be added in a later phase."
      />

      <div className="overflow-hidden rounded-xl border border-navy-900/5 bg-white shadow-panel">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-navy-900/5 bg-sky-50/60 text-xs uppercase tracking-wide text-navy-900/45">
              <th className="px-5 py-3 font-medium">Institution</th>
              <th className="px-5 py-3 font-medium">Country</th>
              <th className="px-5 py-3 font-medium">Research Area</th>
              <th className="px-5 py-3 font-medium">Signed</th>
              <th className="px-5 py-3 font-medium">Last Activity</th>
              <th className="px-5 py-3 font-medium">Publications</th>
              <th className="px-5 py-3 font-medium">Projects</th>
              <th className="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {mous.map((m) => (
              <tr key={m.id} className="border-b border-navy-900/5 last:border-0 hover:bg-sky-50/50">
                <td className="px-5 py-3 font-medium text-navy-950">{m.institution}</td>
                <td className="px-5 py-3 text-navy-900/70">{m.country}</td>
                <td className="px-5 py-3 text-navy-700">{m.research_area}</td>
                <td className="px-5 py-3 text-navy-900/70">{m.signed_date}</td>
                <td className="px-5 py-3 text-navy-900/70">{m.last_activity}</td>
                <td className="px-5 py-3 text-navy-900/70">{m.joint_publications}</td>
                <td className="px-5 py-3 text-navy-900/70">{m.joint_projects}</td>
                <td className="px-5 py-3"><StatusBadge status={m.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
