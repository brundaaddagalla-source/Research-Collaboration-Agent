import { getExpertise } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function ExpertiseMap() {
  const { data, status, error } = useApiData(getExpertise);

  if (status === "loading") return <LoadingView label="Loading expertise map" />;
  if (status === "error") return <ErrorView message={error} />;

  const areas = data?.expertise_map || [];
  if (areas.length === 0) return <EmptyView message="No research areas recorded yet." />;

  const maxCount = Math.max(...areas.map((a) => a.faculty_count));

  return (
    <div>
      <PageHeader
        title="Expertise Map"
        description="Research areas mapped by faculty count. In later phases this will be generated from faculty profiles and publication embeddings (Agent 19)."
      />

      <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
        <div className="space-y-4">
          {areas
            .sort((a, b) => b.faculty_count - a.faculty_count)
            .map((area) => (
              <div key={area.research_area}>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span className="font-medium text-navy-950">{area.research_area}</span>
                  <span className="text-navy-900/55">{area.faculty_count} faculty</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-navy-900/8">
                  <div
                    className="h-full rounded-full bg-navy-700"
                    style={{ width: `${(area.faculty_count / maxCount) * 100}%` }}
                  />
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
