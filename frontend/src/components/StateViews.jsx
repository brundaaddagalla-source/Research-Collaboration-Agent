// import { Loader2, AlertTriangle, Inbox } from "lucide-react";

// export function LoadingView({ label = "Loading data" }) {
//   return (
//     <div className="flex flex-col items-center justify-center gap-3 py-20 text-navy-700/70">
//       <Loader2 className="h-6 w-6 animate-spin" />
//       <p className="font-body text-sm">{label}...</p>
//     </div>
//   );
// }

// export function ErrorView({ message, onRetry }) {
//   return (
//     <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-signal-dormant/20 bg-signal-dormant/5 py-16 text-center">
//       <AlertTriangle className="h-6 w-6 text-signal-dormant" />
//       <p className="font-display text-sm font-semibold text-navy-900">
//         Couldn't load data from the API
//       </p>
//       <p className="max-w-sm text-xs text-navy-900/60">{message}</p>
//       {onRetry && (
//         <button
//           onClick={onRetry}
//           className="mt-2 rounded-lg bg-navy-700 px-4 py-1.5 text-xs font-medium text-white hover:bg-navy-600"
//         >
//           Try again
//         </button>
//       )}
//     </div>
//   );
// }

// export function EmptyView({ message = "No records yet." }) {
//   return (
//     <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-navy-900/15 py-16 text-center text-navy-900/50">
//       <Inbox className="h-5 w-5" />
//       <p className="text-sm">{message}</p>
//     </div>
//   );
// }

import { Loader2, AlertTriangle, Inbox } from "lucide-react";

export function LoadingView({ label = "Loading data" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-20 text-surface-muted">
      <Loader2 className="h-6 w-6 animate-spin text-blue" />

      <p className="font-body text-sm">
        {label}...
      </p>
    </div>
  );
}

export function ErrorView({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-panel border border-signal-dormant/20 bg-signal-dormant/5 py-16 text-center">
      <AlertTriangle className="h-6 w-6 text-signal-dormant" />

      <p className="font-display text-sm font-semibold text-navy-800">
        Couldn't load data from the API
      </p>

      <p className="max-w-sm text-xs text-surface-muted">
        {message}
      </p>

      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 rounded-lg bg-blue px-4 py-1.5 text-xs font-medium text-white transition hover:bg-blue-2"
        >
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyView({ message = "No records yet." }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-panel border border-dashed border-surface-line bg-white py-16 text-center text-surface-muted">
      <Inbox className="h-5 w-5" />

      <p className="text-sm">
        {message}
      </p>
    </div>
  );
}
