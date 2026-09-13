import { useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";
import { searchCollaborators } from "../services/api";
import { OpportunityCard } from "./OpportunityCard";
import { RequestCollaborationModal } from "./RequestCollaborationModal";
import { EmptyView, ErrorView } from "./StateViews";

const SUGGESTIONS = [
  "AI + Healthcare",
  "Computer Vision",
  "Remote Sensing",
  "Machine Learning",
];

/**
 * Identity (who is searching, and who gets excluded from their own
 * results) is entirely determined server-side from the JWT - this
 * component only ever sends the free-text research topic.
 */
export function CollaborationAssistant({ topK = 8, compact = false }) {
  const [keyword, setKeyword] = useState("");
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [error, setError] = useState("");
  const [results, setResults] = useState([]);
  const [activeRequest, setActiveRequest] = useState(null);
  const filteredResults = results.filter((op) => {
    if (op.result_type === "external") {
      return (
        op.matching_expertise?.length > 0 &&
        (
          op.skills?.length > 0 ||
          op.research_area ||
          op.funding_opportunities?.length > 0 ||
          op.mou_opportunities?.length > 0
        )
      );
    }

    return (
      op.matching_expertise?.length > 0 &&
      (
        op.relevant_publications?.length > 0 ||
        op.relevant_projects?.length > 0 ||
        op.relevant_research_work?.length > 0
      )
    );
  });

  async function handleSearch(event) {
    event?.preventDefault();
    if (!keyword.trim()) return;

    setStatus("loading");
    setError("");

    try {
      const data = await searchCollaborators(keyword, topK);
      setResults(data.results || []);
      setStatus("success");
    } catch (err) {
      setError(err.message || "Could not reach the collaboration matching API.");
      setStatus("error");
    }
  }

  return (
    <div className={compact ? "" : "rounded-panel border border-surface-line bg-white p-6 shadow-panel"}>
      {!compact && (
        <div className="mb-5">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-blue" />
            <h2 className="font-display text-lg font-bold text-navy-800">
              Collaboration Assistant
            </h2>
          </div>
          <p className="mt-1 text-sm text-surface-muted">
            Find researchers whose expertise complements your research.
          </p>
        </div>
      )}

      <form onSubmit={handleSearch} className="space-y-3">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="What research area do you want to collaborate on?"
          className="w-full rounded-lg border border-surface-line bg-white px-3.5 py-2.5 text-sm text-navy-800 outline-none transition focus:border-blue focus:ring-2 focus:ring-blue/15"
        />

        <div className="flex flex-wrap gap-1.5">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => setKeyword(s)}
              className="rounded-full bg-soft-blue px-2.5 py-1 text-xs font-medium text-blue transition hover:bg-blue/15"
            //              flex w-full items-center justify-center gap-2 rounded-lg bg-accent-blue px-4 py-2.5 text-sm font-medium text-white transition hover:bg-navy-700 disabled:cursor-not-allowed disabled:opacity-70
            >
              {s}
            </button>
          ))}
        </div>

        <button
          type="submit"
          disabled={status === "loading"}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-accent-blue px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-2 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {status === "loading" && <Loader2 className="h-4 w-4 animate-spin" />}
          Find Collaborators
        </button>
      </form>

      <div className="mt-5">
        {status === "loading" && (
          <p className="py-6 text-center text-sm text-surface-muted">
            Finding potential collaborators...
          </p>
        )}

        {status === "error" && <ErrorView message={error} />}

        {status === "success" && filteredResults.length === 0 && (
          <EmptyView message="No collaboration opportunities found for that topic yet." />
        )}

        {status === "success" && filteredResults.length > 0 && (
          <div className="space-y-4">
            {filteredResults.map((op) => (
              <OpportunityCard
                key={
                  op.result_type === "external"
                    ? `external-${op.researcher?.id}`
                    : `internal-${op.faculty?.faculty_id}`
                }
                opportunity={op}
                onRequestCollaboration={(opp) =>
                  setActiveRequest({ ...opp, query: keyword })
                }
              />
            ))}
          </div>
        )}
      </div>

      {activeRequest && (
        <RequestCollaborationModal
          opportunity={activeRequest}
          onClose={() => setActiveRequest(null)}
        />
      )}
    </div>
  );
}