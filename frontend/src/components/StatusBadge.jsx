// const STYLE_MAP = {
//   Active: "bg-signal-active/10 text-signal-active",
//   Underutilized: "bg-signal-underutilized/10 text-signal-underutilized",
//   Dormant: "bg-signal-dormant/10 text-signal-dormant",
//   Suggested: "bg-navy-700/10 text-navy-700",
//   "Under Review": "bg-signal-underutilized/10 text-signal-underutilized",
//   High: "bg-signal-active/10 text-signal-active",
//   Medium: "bg-signal-underutilized/10 text-signal-underutilized",
//   Low: "bg-signal-dormant/10 text-signal-dormant",
//   Strong: "bg-signal-active/10 text-signal-active",
//   Moderate: "bg-signal-underutilized/10 text-signal-underutilized",
//   Weak: "bg-signal-dormant/10 text-signal-dormant",
// };

// export function StatusBadge({ status }) {
//   const style = STYLE_MAP[status] || "bg-navy-900/10 text-navy-900/70";
//   return (
//     <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${style}`}>
//       {status}
//     </span>
//   );
// }

const STYLE_MAP = {
  Active: "bg-soft-green text-signal-active",
  Underutilized: "bg-soft-orange text-signal-underutilized",
  Dormant: "bg-signal-dormant/10 text-signal-dormant",

  Suggested: "bg-soft-blue text-blue",
  "Under Review": "bg-soft-orange text-signal-underutilized",

  High: "bg-soft-green text-signal-active",
  Medium: "bg-soft-orange text-signal-underutilized",
  Low: "bg-signal-dormant/10 text-signal-dormant",

  Strong: "bg-soft-green text-signal-active",
  Moderate: "bg-soft-orange text-signal-underutilized",
  Weak: "bg-signal-dormant/10 text-signal-dormant",

  Accepted: "bg-soft-green text-signal-active",
};

export function StatusBadge({ status }) {
  const style =
    STYLE_MAP[status] || "bg-sky-100 text-surface-muted";

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ${style}`}
    >
      {status}
    </span>
  );
}