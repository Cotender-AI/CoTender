import { cn } from "@/lib/utils";

// Review lifecycle from the Postgres enum: extracted -> corrected -> approved | rejected; any -> stale.
export type ReviewStatus = "extracted" | "corrected" | "approved" | "rejected" | "stale";

export const STATUS_STYLES: Record<ReviewStatus, { label: string; dot: string; text: string }> = {
  extracted: { label: "Extracted", dot: "bg-phase-blue", text: "text-phase-blue" },
  corrected: { label: "Corrected", dot: "bg-earth-yellow", text: "text-amber-800" },
  approved: { label: "Approved", dot: "bg-earth-green", text: "text-earth-green" },
  rejected: { label: "Rejected", dot: "bg-phase-red", text: "text-phase-red" },
  stale: { label: "Stale", dot: "bg-muted-foreground", text: "text-muted-foreground" },
};

export function StatusBadge({ status, className }: { status: ReviewStatus; className?: string }) {
  const s = STATUS_STYLES[status];
  return (
    <span className={cn("inline-flex items-center gap-1.5 text-xs font-medium", s.text, className)}>
      <span className={cn("size-2 rounded-full", s.dot)} />
      {s.label}
    </span>
  );
}
