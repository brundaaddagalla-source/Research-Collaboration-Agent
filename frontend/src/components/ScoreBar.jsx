// export function ScoreBar({ score, label = "Compatibility" }) {
//   const color =
//     score >= 85 ? "bg-signal-active" : score >= 70 ? "bg-navy-700" : "bg-signal-underutilized";

//   return (
//     <div>
//       <div className="mb-1 flex items-center justify-between text-xs text-navy-900/55">
//         <span>{label}</span>
//         <span className="font-display font-semibold text-navy-950">{score}%</span>
//       </div>
//       <div className="h-1.5 w-full overflow-hidden rounded-full bg-navy-900/8">
//         <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
//       </div>
//     </div>
//   );
// }

export function ScoreBar({ score, label = "Compatibility" }) {
  const color =
    score >= 85
      ? "bg-signal-active"
      : score >= 70
        ? "bg-blue"
        : "bg-signal-underutilized";

  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-xs">
        <span className="text-surface-muted">{label}</span>

        <span className="font-display font-semibold text-navy-800">
          {score}%
        </span>
      </div>

      <div className="h-1.5 w-full overflow-hidden rounded-full bg-sky-100">
        <div
          className={`h-full rounded-full transition-all ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}
