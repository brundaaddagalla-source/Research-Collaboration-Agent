import { useEffect, useRef, useState } from "react";

import { CheckCircle2, Loader2, X, XCircle } from "lucide-react";

import { createCollaborationRequest } from "../services/api";

/**
 * No manual form. The faculty already saw everything on the
 * OpportunityCard before clicking "Request Collaboration".
 *
 * The modal reuses that exact result data to create the request
 * automatically.
 *
 * Internal faculty requests use:
 *   target_faculty_id
 *
 * External researcher requests use:
 *   target_external_researcher_id
 */

export function RequestCollaborationModal({ opportunity, onClose }) {
  const op = opportunity;

  const isExternal = op.result_type === "external";

  const faculty = op.faculty || {};
  const researcher = op.researcher || {};

  const targetName = isExternal
    ? researcher.name
    : faculty.name;

  const targetOrganization = isExternal
    ? [researcher.institution, researcher.country]
        .filter(Boolean)
        .join(" · ")
    : [faculty.department, faculty.designation]
        .filter(Boolean)
        .join(" · ");

  const [status, setStatus] = useState("sending");
  const [error, setError] = useState("");

  const firedRef = useRef(false);

  useEffect(() => {
    if (firedRef.current) return;

    firedRef.current = true;

    // Reuse the exact same fields already produced by the
    // existing search result.
    const topic = (
      op.query ||
      op.matching_expertise?.[0] ||
      ""
    ).trim();

    if (!topic) {
      setStatus("error");
      setError(
        "This result has no research topic to attach to the request."
      );
      return;
    }

    const payload = {
      topic,
      proposal: null,
      reason: op.reason || null,
      fundingId: op.funding_opportunities?.[0]?.id ?? null,
      mouId: op.mou_opportunities?.[0]?.id ?? null,
      universityBenefit: null,
    };

    // Internal faculty
    if (!isExternal) {
      payload.targetFacultyId = faculty.faculty_id;
    }

    // External researcher
    if (isExternal) {
      payload.targetExternalResearcherId = researcher.id;
    }

    createCollaborationRequest(payload)
      .then(() => setStatus("sent"))
      .catch((err) => {
        setStatus("error");
        setError(
          err.message ||
            "Could not send the collaboration request."
        );
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-navy-950/40 px-4">
      <div className="w-full max-w-md rounded-panel border border-surface-line bg-white p-6 text-center shadow-panel">
        <div className="flex items-start justify-between">
          <h2 className="font-display text-lg font-bold text-navy-800">
            Request Collaboration
          </h2>

          <button
            onClick={onClose}
            className="rounded-lg p-1 text-surface-muted transition hover:bg-sky-50 hover:text-navy-800"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <p className="mt-1 text-sm text-surface-muted">
          {targetName}
          {targetOrganization
            ? ` · ${targetOrganization}`
            : ""}
        </p>

        <div className="mt-6">
          {status === "sending" && (
            <>
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-blue" />

              <p className="mt-3 text-sm text-surface-muted">
                Sending your collaboration request...
              </p>
            </>
          )}

          {status === "sent" && (
            <>
              <CheckCircle2 className="mx-auto h-8 w-8 text-signal-active" />

              <p className="mt-3 rounded-lg bg-soft-green px-3 py-2.5 text-sm text-signal-active">
                Collaboration request sent successfully.
              </p>
            </>
          )}

          {status === "error" && (
            <>
              <XCircle className="mx-auto h-8 w-8 text-signal-dormant" />

              <p className="mt-3 rounded-lg bg-signal-dormant/5 px-3 py-2.5 text-sm text-signal-dormant">
                {error}
              </p>
            </>
          )}
        </div>

        <button
          onClick={onClose}
          disabled={status === "sending"}
          className="mt-6 w-full rounded-lg bg-blue px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-2 disabled:cursor-not-allowed disabled:opacity-70"
        >
          Close
        </button>
      </div>
    </div>
  );
}