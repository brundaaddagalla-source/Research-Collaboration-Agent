/**
 * Presentation-only helper: converts an existing, already-computed
 * match/collaboration score (0-100 scale, as returned by the existing
 * backend matching engines) into a simple faculty-facing label.
 *
 * This does NOT compute, adjust, or replace any score - it only decides
 * how an existing score is displayed. A score of 0 / null / undefined
 * is treated as "no meaningful value" and returns null so callers can
 * hide the metric entirely instead of showing "Strength: Weak" or
 * "Score: 0".
 */
export function getStrengthLabel(score) {
  if (score === null || score === undefined) return null;
  const numeric = Number(score);
  if (!Number.isFinite(numeric) || numeric <= 0) return null;

  if (numeric >= 75) return "Strong";
  if (numeric >= 50) return "Moderate";
  return "Weak";
}