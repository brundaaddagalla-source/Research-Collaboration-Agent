import { useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { CheckCircle2, XCircle, Clock, Ban, Radar } from "lucide-react";
import { respondViaEmailToken } from "../services/api";

const RESULT_STYLES = {
  success: { icon: CheckCircle2, color: "text-signal-active" },
  used: { icon: Ban, color: "text-signal-underutilized" },
  expired: { icon: Clock, color: "text-signal-underutilized" },
  already_processed: { icon: Ban, color: "text-signal-underutilized" },
  invalid: { icon: XCircle, color: "text-signal-dormant" },
};

export default function CollaborationResponse() {
  const { token } = useParams();
  const [state, setState] = useState({ status: "loading" }); // loading | done | error

  // This is a one-time-use token: the GET below actually consumes it on
  // the backend. React 18's StrictMode (and any other double-mount) runs
  // this effect twice in development, which - without a guard - fires
  // the request twice. The first call would succeed and process the
  // acceptance, but the second would then hit the token as already used,
  // and that second ("already used") response is what ends up on screen
  // even though the request itself was accepted. hasFiredRef makes sure
  // the request is only ever sent once per token, no matter how many
  // times this effect runs.
  const hasFiredRef = useRef(false);

  useEffect(() => {
    if (hasFiredRef.current) return;

    hasFiredRef.current = true;

    respondViaEmailToken(token)
      .then((data) => {
        setState({
          status: "done",
          result: data.result,
          message: data.message,
        });
      })
      .catch((err) => {
        setState({
          status: "error",
          message: err.message,
        });
      });
  }, [token]);

  const resultStyle = RESULT_STYLES[state.result] || RESULT_STYLES.invalid;
  const Icon = resultStyle.icon;

  return (
    <div className="flex min-h-screen items-center justify-center bg-sky-50 px-4">
      <div className="w-full max-w-md rounded-panel border border-surface-line bg-white p-8 text-center shadow-panel">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-soft-blue ring-1 ring-blue/10">
          <Radar className="h-6 w-6 text-blue" />
        </div>
        <p className="text-[11px] font-semibold uppercase tracking-wider text-blue">
          Agent 24 Research Collaboration
        </p>

        {state.status === "loading" && (
          <p className="mt-6 text-sm text-surface-muted">Processing your response...</p>
        )}

        {state.status === "error" && (
          <>
            <XCircle className="mx-auto mt-6 h-8 w-8 text-signal-dormant" />
            <p className="mt-3 text-sm font-medium text-navy-800">{state.message}</p>
          </>
        )}

        {state.status === "done" && (
          <>
            <Icon className={`mx-auto mt-6 h-8 w-8 ${resultStyle.color}`} />
            <p className="mt-3 text-sm font-medium text-navy-800">{state.message}</p>
          </>
        )}

        <Link
          to="/login"
          className="mt-6 inline-block rounded-lg bg-accent-blue px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-2"
        >
          Go to Faculty Login
        </Link>
      </div>
    </div>
  );
}