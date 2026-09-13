import { useState } from "react";
import { Inbox, Check, X, Loader2 } from "lucide-react";
import { getSentRequests, getReceivedRequests, respondToRequestAsFaculty } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";
import { getStrengthLabel } from "../utils/strength";

const STAGE_LABELS = {
  REQUESTED: "Pending",
  FACULTY_REJECTED: "Rejected",
  ACCEPTED: "Accepted",
  // Kept for any already-existing requests stored under the old stage
  // name before it was renamed to ACCEPTED.
  AUTHORITY_REVIEW: "Accepted",
  AUTHORITY_REJECTED: "Rejected by Authority",
  ACTIVE: "Active Collaboration",
};

function stageLabel(stage) {
  return STAGE_LABELS[stage] || stage;
}

function SentRequestRow({ request }) {
  const strength = getStrengthLabel(request.matching_score);
  return (
    <div className="flex items-center justify-between gap-3 border-b border-surface-line py-3 last:border-0">
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-navy-800">{request.faculty.name}</p>
        <p className="text-xs text-surface-muted">{request.topic}</p>
        {strength && <p className="text-[11px] text-surface-muted">Strength: {strength}</p>}
      </div>
      <StatusBadge status={stageLabel(request.stage)} />
    </div>
  );
}

function ReceivedRequestCard({ request, onResponded }) {
  const [comments, setComments] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const canRespond = request.stage === "REQUESTED" && request.faculty_status === "PENDING";

  async function respond(status) {
    setBusy(true);
    setError("");
    try {
      await respondToRequestAsFaculty(request.id, status, comments);
      onResponded();
    } catch (err) {
      setError(err.message || "Could not submit your response.");
    } finally {
      setBusy(false);
    }
  }

  const evidence = request.matching_evidence || {};
  const strength = getStrengthLabel(request.matching_score);

  return (
    <div className="rounded-xl border border-surface-line bg-white p-4">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-navy-800">{request.requester.name}</p>
          <p className="text-xs text-surface-muted">{request.requester.department}</p>
        </div>
        <StatusBadge status={stageLabel(request.stage)} />
      </div>

      <p className="mt-3 text-sm font-semibold text-navy-800">{request.topic}</p>
      {strength && <p className="text-xs text-surface-muted">Strength: {strength}</p>}

      {request.reason && (
        <p className="mt-2 text-sm text-surface-muted">
          <span className="font-medium text-navy-800">Reason: </span>
          {request.reason}
        </p>
      )}
      {request.proposal && (
        <p className="mt-1 text-sm text-surface-muted">
          <span className="font-medium text-navy-800">Proposal: </span>
          {request.proposal}
        </p>
      )}
      {request.university_benefit && (
        <p className="mt-1 text-sm text-surface-muted">
          <span className="font-medium text-navy-800">University benefit: </span>
          {request.university_benefit}
        </p>
      )}

      {evidence.matching_expertise?.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {evidence.matching_expertise.map((e) => (
            <span key={e} className="rounded-full bg-soft-blue px-2.5 py-1 text-xs font-medium text-blue">
              {e}
            </span>
          ))}
        </div>
      )}

      {canRespond ? (
        <div className="mt-4 space-y-2">
          <textarea
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            rows={2}
            placeholder="Optional comments..."
            className="w-full rounded-lg border border-surface-line bg-white px-3 py-2 text-sm text-navy-800 outline-none focus:border-blue focus:ring-2 focus:ring-blue/15"
          />
          {error && <p className="text-xs text-signal-dormant">{error}</p>}
          <div className="flex gap-2">
            <button
              onClick={() => respond("approved")}
              disabled={busy}
              className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-blue px-3 py-2 text-sm font-medium text-white transition hover:bg-blue-2 disabled:opacity-70"
            >
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4" />}
              Accept
            </button>
            <button
              onClick={() => respond("rejected")}
              disabled={busy}
              className="flex flex-1 items-center justify-center gap-2 rounded-lg border border-surface-line bg-white px-3 py-2 text-sm font-medium text-navy-800 transition hover:bg-signal-dormant/5 hover:text-signal-dormant disabled:opacity-70"
            >
              <X className="h-4 w-4" />
              Reject
            </button>
          </div>
        </div>
      ) : (
        request.faculty_comments && (
          <p className="mt-3 text-xs text-surface-muted">Your response: {request.faculty_comments}</p>
        )
      )}
    </div>
  );
}

export default function MyRequests() {
  const [refreshKey, setRefreshKey] = useState(0);
  const { data: sentData, status: sentStatus, error: sentError } = useApiData(getSentRequests, [refreshKey]);
  const { data: receivedData, status: receivedStatus, error: receivedError } = useApiData(
    getReceivedRequests,
    [refreshKey]
  );

  const reload = () => setRefreshKey((k) => k + 1);

  const sent = sentData?.requests || [];
  const received = receivedData?.requests || [];

  return (
    <div>
      <PageHeader
        icon={Inbox}
        title="My Requests"
        description="Collaboration requests you've sent, and requests waiting on your response."
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-800">Sent Requests</h2>
          {sentStatus === "loading" ? (
            <LoadingView label="Loading sent requests" />
          ) : sentStatus === "error" ? (
            <ErrorView message={sentError} />
          ) : sent.length === 0 ? (
            <EmptyView message="No sent requests found." />
          ) : (
            <div className="mt-2">
              {sent.map((r) => (
                <SentRequestRow key={r.id} request={r} />
              ))}
            </div>
          )}
        </div>

        <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-800">Received Requests</h2>
          {receivedStatus === "loading" ? (
            <LoadingView label="Loading received requests" />
          ) : receivedStatus === "error" ? (
            <ErrorView message={receivedError} />
          ) : received.length === 0 ? (
            <EmptyView message="No received requests found." />
          ) : (
            <div className="mt-2 space-y-3">
              {received.map((r) => (
                <ReceivedRequestCard key={r.id} request={r} onResponded={reload} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}