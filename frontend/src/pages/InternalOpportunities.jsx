import { getOpportunities } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { ScoreBar } from "../components/ScoreBar";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function InternalOpportunities() {
  const { data, status, error } = useApiData(getOpportunities);

  if (status === "loading") return <LoadingView label="Loading opportunities" />;
  if (status === "error") return <ErrorView message={error} />;

  const opportunities = data?.opportunities || [];
  if (opportunities.length === 0) return <EmptyView message="No collaboration opportunities suggested yet." />;

  return (
    <div>
      <PageHeader
        title="Internal Opportunities"
        description="Suggested faculty pairings based on complementary, non-overlapping expertise. Mock data - scoring logic is not implemented in Phase 1."
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {opportunities.map((op) => (
          <div key={op.id} className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
            <div className="flex items-start justify-between gap-2">
              <div>
                <p className="font-display text-sm font-semibold text-navy-950">{op.faculty_a}</p>
                <p className="text-xs text-navy-900/50">{op.department_a}</p>
              </div>
              <StatusBadge status={op.status} />
            </div>

            <div className="my-2 flex items-center gap-2 text-navy-900/30">
              <span className="h-px flex-1 bg-navy-900/10" />
              <span className="text-xs">&harr;</span>
              <span className="h-px flex-1 bg-navy-900/10" />
            </div>

            <div>
              <p className="font-display text-sm font-semibold text-navy-950">{op.faculty_b}</p>
              <p className="text-xs text-navy-900/50">{op.department_b}</p>
            </div>

            <p className="mt-3 text-xs font-medium text-navy-700">{op.research_areas.join(" + ")}</p>
            <p className="mt-2 text-sm text-navy-900/75">{op.reason}</p>

            <div className="mt-4 grid grid-cols-2 gap-4">
              <ScoreBar score={op.compatibility_score} label="Compatibility" />
              <ScoreBar score={op.complementarity_score} label="Complementarity" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
