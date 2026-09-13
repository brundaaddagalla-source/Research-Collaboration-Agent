import { useMemo } from "react";
import { Users } from "lucide-react";
import { getCollaborations } from "../services/api";
import { useApiData } from "../services/useApiData";
import { getStoredFaculty } from "../services/auth";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function MyCollaborations() {
  const stored = getStoredFaculty();
  const { data, status, error } = useApiData(getCollaborations);

  const myName = (stored?.name || "").trim().toLowerCase();
  const collaborations = data?.collaborations || [];

  const mine = useMemo(
    () =>
      collaborations.filter(
        (c) =>
          (c.faculty_a || "").trim().toLowerCase() === myName ||
          (c.faculty_b || "").trim().toLowerCase() === myName
      ),
    [collaborations, myName]
  );

  if (status === "loading") return <LoadingView label="Loading your collaborations" />;
  if (status === "error") return <ErrorView message={error} />;

  return (
    <div>
      <PageHeader
        icon={Users}
        title="My Collaborations"
        description="Existing collaborations involving you, from the collaboration record."
      />

      {mine.length === 0 ? (
        <EmptyView message="No collaborations recorded for you yet." />
      ) : (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {mine.map((c) => {
            const other = (c.faculty_a || "").trim().toLowerCase() === myName ? c.faculty_b : c.faculty_a;
            return (
              <div key={c.id} className="rounded-xl border border-surface-line bg-white p-5 shadow-panel">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-display text-sm font-semibold text-navy-800">{other}</p>
                    <p className="text-xs text-surface-muted">{c.department}</p>
                  </div>
                  <StatusBadge status={c.collaboration_strength} />
                </div>

                <p className="mt-3 text-xs font-medium text-blue">
                  {(c.research_areas || []).join(", ")}
                </p>

                <p className="mt-2 text-sm text-surface-muted">{c.collaboration_type}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}