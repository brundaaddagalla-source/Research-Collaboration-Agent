import { StatusBadge } from "./StatusBadge";
import { getStrengthLabel } from "../utils/strength";

// Each item is one result from POST /api/collaborations/search - either:
//
// internal: {
//   result_type: "internal",
//   faculty: {
//     faculty_id,
//     name,
//     department,
//     designation
//   },
//   score,
//   matching_expertise,
//   relevant_publications,
//   relevant_projects,
//   relevant_research_work,
//   network_reachability,
//   network_score,
//   funding_opportunities,
//   mou_opportunities,
//   reason
// }
//
// external: {
//   result_type: "external",
//   researcher: {
//     id,
//     name,
//     institution,
//     country
//   },
//   score,
//   matching_expertise,
//   skills,
//   research_area,
//   funding_opportunities,
//   mou_opportunities,
//   reason
// }
//
// (see backend/services/search_orchestrator.py)

export function OpportunityCard({ opportunity, onRequestCollaboration }) {
  const op = opportunity;

  const isExternal = op.result_type === "external";

  const faculty = op.faculty || {};
  const researcher = op.researcher || {};

  const fundingLabels = (op.funding_opportunities || [])
    .map((f) => f.name)
    .filter(Boolean);

  const mouLabels = (op.mou_opportunities || [])
    .map((m) => m.institution)
    .filter(Boolean);

  // Presentation only - the underlying score from the existing matching
  // engine is never modified. A score of 0/null is treated as "no
  // meaningful value" and the Strength indicator is simply hidden.
  const strength = getStrengthLabel(op.score);

  return (
    <div className="rounded-xl border border-surface-line bg-white p-5 shadow-panel">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <span
            className={`mb-1 inline-block rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${
              isExternal
                ? "bg-amber-100 text-amber-700"
                : "bg-soft-blue text-blue"
            }`}
          >
            {isExternal ? "External Researcher" : "Internal Faculty"}
          </span>

          <p className="truncate font-display text-sm font-semibold text-navy-800">
            {isExternal ? researcher.name : faculty.name}
          </p>

          {!isExternal && faculty.designation && (
            <p className="text-xs text-surface-muted">
              {faculty.designation}
            </p>
          )}

          <p className="text-xs text-surface-muted">
            {isExternal
              ? [researcher.institution, researcher.country]
                  .filter(Boolean)
                  .join(", ")
              : faculty.department}
          </p>
        </div>
      </div>

      {strength && (
        <div className="mt-4 flex items-center justify-between">
          <span className="text-xs font-medium text-surface-muted">
            Strength
          </span>
          <StatusBadge status={strength} />
        </div>
      )}

      {!isExternal && op.network_reachability && (
        <p className="mt-2 text-xs text-surface-muted">
          Network:{" "}
          <span className="font-medium text-navy-800">
            {op.network_reachability}
          </span>
        </p>
      )}

      {op.matching_expertise?.length > 0 && (
        <div className="mt-4">
          <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
            Matching Expertise
          </p>

          <div className="mt-1.5 flex flex-wrap gap-1.5">
            {op.matching_expertise.map((topic) => (
              <span
                key={topic}
                className="rounded-full bg-soft-blue px-2.5 py-1 text-xs font-medium text-blue"
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 grid grid-cols-2 gap-x-4 gap-y-3">
        {!isExternal && (
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
              Relevant Publications
            </p>

            <p className="mt-1 text-sm text-navy-800">
              {op.relevant_publications?.length > 0
                ? op.relevant_publications.join(", ")
                : "None on file"}
            </p>
          </div>
        )}

        {!isExternal && (
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
              Relevant Projects
            </p>

            <p className="mt-1 text-sm text-navy-800">
              {op.relevant_projects?.length > 0
                ? op.relevant_projects.join(", ")
                : "None on file"}
            </p>
          </div>
        )}

        {!isExternal && op.relevant_research_work?.length > 0 && (
          <div className="col-span-2">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
              Relevant Uploaded Research
            </p>

            <p className="mt-1 text-sm text-navy-800">
              {op.relevant_research_work.join(", ")}
            </p>
          </div>
        )}

        {isExternal && op.skills?.length > 0 && (
          <div className="col-span-2">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
              Skills
            </p>

            <p className="mt-1 text-sm text-navy-800">
              {op.skills.join(", ")}
            </p>
          </div>
        )}

        {isExternal && researcher.research_area && (
          <div className="col-span-2">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
              Research Area
            </p>

            <p className="mt-1 text-sm text-navy-800">
              {researcher.research_area}
            </p>
          </div>
        )}

        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
            Existing MoU
          </p>

          <p className="mt-1 text-sm text-navy-800">
            {mouLabels.length > 0 ? mouLabels.join(", ") : "None"}
          </p>
        </div>

        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wide text-surface-muted">
            Funding Opportunities
          </p>

          <p className="mt-1 text-sm text-navy-800">
            {fundingLabels.length > 0 ? fundingLabels.join(", ") : "None"}
          </p>
        </div>
      </div>

      {op.reason && (
        <p className="mt-4 rounded-lg bg-sky-50 p-3 text-xs leading-5 text-surface-muted">
          {op.reason}
        </p>
      )}

      {/* Both internal faculty and external researchers can now receive
          collaboration requests. The backend decides whether the request
          targets target_faculty_id or target_external_researcher_id. */}
      <button
        onClick={() => onRequestCollaboration(op)}
        className="mt-4 w-full rounded-lg bg-accent-blue px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-2"
      >
        Request Collaboration
      </button>
    </div>
  );
}