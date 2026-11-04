import type { ReviewStatus } from "./StatusBadge";
import { STATUS_STYLES } from "./StatusBadge";

const ORDER: ReviewStatus[] = ["approved", "corrected", "extracted", "rejected", "stale"];

/** Segmented bar of review status counts; same colours as StatusBadge. */
export function ProgressBar({ counts }: { counts: Record<ReviewStatus, number> }) {
  const total = ORDER.reduce((n, k) => n + counts[k], 0);
  if (total === 0) {
    return <div className="h-2 rounded-full bg-muted" aria-label="Nothing extracted yet" />;
  }
  return (
    <div
      className="flex h-2 overflow-hidden rounded-full bg-muted"
      role="img"
      aria-label={ORDER.filter((k) => counts[k]).map((k) => `${counts[k]} ${k}`).join(", ")}
    >
      {ORDER.map((k) =>
        counts[k] ? <div key={k} className={STATUS_STYLES[k].dot} style={{ width: `${(counts[k] / total) * 100}%` }} /> : null,
      )}
    </div>
  );
}
