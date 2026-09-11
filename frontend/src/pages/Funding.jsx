import { CheckCircle2, XCircle } from "lucide-react";
import { getFunding } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

function Flag({ ok, label }) {
  return (
    <span className={`flex items-center gap-1.5 text-xs ${ok ? "text-signal-active" : "text-navy-900/40"}`}>
      {ok ? <CheckCircle2 className="h-3.5 w-3.5" /> : <XCircle className="h-3.5 w-3.5" />}
      {label}
    </span>
  );
}

export default function Funding() {
  const { data, status, error } = useApiData(getFunding);

  if (status === "loading") return <LoadingView label="Loading funding opportunities" />;
  if (status === "error") return <ErrorView message={error} />;

  const funding = data?.funding_opportunities || [];
  if (funding.length === 0) return <EmptyView message="No funding calls available yet." />;

  return (
    <div>
      <PageHeader
        title="Funding & Consortiums"
        description="Open funding calls matched to faculty research areas. Mock data - live funding-call ingestion (Agent 22) will be integrated later."
      />

      <div className="space-y-4">
        {funding.map((f) => (
          <div key={f.id} className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="font-display text-sm font-semibold text-navy-950">{f.title}</p>
                <p className="mt-0.5 text-xs text-navy-900/50">{f.organization}</p>
              </div>
              <span className="whitespace-nowrap rounded-full bg-navy-900/5 px-3 py-1 text-xs font-medium text-navy-900/70">
                Deadline: {f.deadline}
              </span>
            </div>

            <p className="mt-3 text-xs font-medium text-navy-700">{f.research_areas.join(", ")}</p>

            <div className="mt-3 flex flex-wrap gap-4">
              <Flag ok={f.consortium_requirement} label="Consortium required" />
              <Flag ok={f.international_partner_required} label="International partner" />
              <Flag ok={f.industry_partner_required} label="Industry partner" />
            </div>

            <div className="mt-3 flex flex-wrap gap-2">
              {f.matching_faculty.map((name) => (
                <span key={name} className="rounded-full bg-sky-100 px-2.5 py-1 text-xs text-navy-700">
                  {name}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
