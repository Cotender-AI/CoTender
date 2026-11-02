import Link from "next/link";
import { ProgressBar } from "@/components/ProgressBar";
import { TENDERS } from "@/lib/mock";

// MOCK DATA: wire to GET /api/v1/dashboard in FE-03.
export default function DashboardPage() {
  const open = TENDERS.filter((t) => t.daysLeft >= 0).sort((a, b) => a.daysLeft - b.daysLeft);
  const waiting = open.reduce((n, t) => n + t.counts.extracted + t.counts.corrected, 0);

  return (
    <div className="mx-auto max-w-5xl">
      <p className="num text-xs uppercase tracking-widest text-muted-foreground">Closing board</p>
      <h1 className="mt-1 text-4xl font-semibold tracking-tight">
        {open.length} tenders open, {waiting} lines waiting for a person to check them
      </h1>

      <ul className="mt-8 divide-y divide-border overflow-hidden rounded-2xl border border-border/70 bg-card shadow-sm">
        {open.map((t) => (
          <li key={t.id}>
            <Link
              href={`/tenders/view/review/?id=${t.id}`}
              className="grid grid-cols-[4.5rem_1fr] items-center gap-x-5 gap-y-3 p-4 transition-colors hover:bg-muted/50 sm:grid-cols-[5.5rem_1fr_14rem] sm:p-5"
            >
              <div className="text-center">
                <div className={`num text-4xl font-medium leading-none ${t.daysLeft <= 7 ? "text-copper" : ""}`}>{t.daysLeft}</div>
                <div className="mt-1 text-[11px] uppercase tracking-wider text-muted-foreground">days left</div>
              </div>
              <div className="min-w-0">
                <div className="truncate font-heading text-lg font-semibold">{t.title}</div>
                <div className="truncate text-sm text-muted-foreground">
                  {t.client} · <span className="num">{t.reference}</span> · closes {t.closes}
                </div>
              </div>
              <div className="col-span-2 sm:col-span-1">
                <ProgressBar counts={t.counts} />
                <div className="num mt-1.5 text-xs text-muted-foreground">
                  {t.counts.approved} approved · {t.counts.extracted + t.counts.corrected} to review
                </div>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
