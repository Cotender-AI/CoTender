"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { Check } from "lucide-react";

// The order is real: each step needs the one before it. Where you are comes from the tab you're on.
// MOCK: which steps count as done will come from the tender's data (documents processed, items approved, ...).
const STEPS = [
  { tab: "documents", label: "Upload the pack", help: "Add the zip or PDFs" },
  { tab: "review", label: "Check what we found", help: "Approve each line" },
  { tab: "checklist", label: "Complete the checklist", help: "Forms and certificates" },
  { tab: "boq", label: "Price it", help: "Rates and totals" },
  { tab: "exports", label: "Final check and export", help: "Review, then download" },
] as const;

export function TenderJourney() {
  const path = usePathname();
  const id = useSearchParams().get("id") ?? "";
  const current = Math.max(0, STEPS.findIndex((s) => path.includes(`/view/${s.tab}`)));

  return (
    <nav aria-label="Tender progress" className="mb-6">
      <ol className="grid grid-cols-2 gap-2 sm:grid-cols-5">
        {STEPS.map((s, i) => {
          const done = i < current;
          const active = i === current;
          return (
            <li key={s.tab}>
              <Link
                href={`/tenders/view/${s.tab}/?id=${id}`}
                aria-current={active ? "step" : undefined}
                className={`flex h-full items-start gap-3 rounded-xl border p-3 transition-colors ${
                  active ? "border-copper bg-card shadow-sm" : "border-border/70 bg-card/60 hover:bg-card"
                }`}
              >
                <span
                  className={`num grid size-6 shrink-0 place-items-center rounded-full text-xs ${
                    done ? "bg-earth-green text-white" : active ? "bg-copper text-white" : "bg-muted text-muted-foreground"
                  }`}
                >
                  {done ? <Check className="size-3.5" /> : i + 1}
                </span>
                <span className="min-w-0">
                  <span className={`block text-sm leading-tight ${active ? "font-semibold" : "font-medium"}`}>{s.label}</span>
                  <span className="block text-xs text-muted-foreground">{s.help}</span>
                </span>
              </Link>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
