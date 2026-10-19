"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";

const TABS = ["documents", "review", "boq", "checklist", "suppliers", "exports"] as const;

/** Tabs for one tender workspace. The tender id travels as ?id=... (static export). */
export function TenderTabs() {
  const path = usePathname();
  const id = useSearchParams().get("id") ?? "";
  return (
    <div className="mb-6 flex gap-4 border-b border-slate-200 text-sm">
      {TABS.map((tab) => {
        const href = `/tenders/view/${tab}/?id=${id}`;
        const active = path.includes(`/view/${tab}`);
        return (
          <Link
            key={tab}
            href={href}
            className={`-mb-px border-b-2 px-1 pb-2 capitalize ${
              active ? "border-slate-900 text-slate-900" : "border-transparent text-slate-500"
            }`}
          >
            {tab === "boq" ? "BoQ" : tab}
          </Link>
        );
      })}
    </div>
  );
}
