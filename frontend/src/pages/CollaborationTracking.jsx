import { Check, Activity } from "lucide-react";
import { getTracking } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function CollaborationTracking() {
  const { data, status, error } = useApiData(getTracking);

  if (status === "loading") return <LoadingView label="Loading tracking pipeline" />;
  if (status === "error") return <ErrorView message={error} />;

  const stages = data?.stages || [];
  const records = data?.records || [];
  if (records.length === 0) return <EmptyView message="No collaborations are being tracked yet." />;

  return (
    <div>
      <PageHeader
        icon={Activity}
        title="Collaboration Tracking"
        description="Follows each suggested collaboration from first recommendation through to publication. Mock records - outcome tracking automation will be added later."
      />

      <div className="space-y-4">
        {records.map((rec) => {
          const currentIndex = stages.indexOf(rec.current_stage);
          return (
            <div key={rec.id} className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="font-display text-sm font-semibold text-navy-950">
                  {rec.faculty_a} &harr; {rec.faculty_b}
                </p>
                <span className="text-xs text-navy-900/45">Updated {rec.last_updated}</span>
              </div>
              <p className="mt-1 text-sm text-navy-900/70">{rec.topic}</p>

              {/* Pipeline */}
              <div className="mt-4 flex items-center">
                {stages.map((stage, i) => {
                  const done = i <= currentIndex;
                  const isCurrent = i === currentIndex;
                  return (
                    <div key={stage} className="flex flex-1 items-center last:flex-none">
                      <div className="flex flex-col items-center gap-1">
                        <div
                          className={`flex h-7 w-7 items-center justify-center rounded-full border-2 text-xs font-semibold ${
                            done
                              ? "border-navy-700 bg-navy-700 text-white"
                              : "border-navy-900/15 bg-white text-navy-900/30"
                          } ${isCurrent ? "ring-4 ring-navy-700/15" : ""}`}
                        >
                          {done ? <Check className="h-3.5 w-3.5" /> : i + 1}
                        </div>
                        <span
                          className={`w-20 text-center text-[10px] leading-tight ${
                            done ? "font-medium text-navy-950" : "text-navy-900/40"
                          }`}
                        >
                          {stage}
                        </span>
                      </div>
                      {i < stages.length - 1 && (
                        <div className={`mx-1 h-0.5 flex-1 ${i < currentIndex ? "bg-navy-700" : "bg-navy-900/10"}`} />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}