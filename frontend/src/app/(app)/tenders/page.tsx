"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Plus } from "lucide-react";
import { api, errorMessage } from "@/api/client";
import type { Schemas } from "@/api/types";
import { TenderSheetIllustration } from "@/components/Illustration";
import { buttonVariants } from "@/components/ui/button";

type Tender = Schemas["Tender"];
type Load = { state: "loading" } | { state: "error"; message: string } | { state: "ready"; items: Tender[] };

const STATUS_LABEL: Record<Tender["status"], string> = {
  draft: "Draft",
  in_progress: "In progress",
  ready: "Ready",
  submitted: "Submitted",
  archived: "Archived",
};

const dateFmt = new Intl.DateTimeFormat("en-ZA", { day: "numeric", month: "short", year: "numeric" });

function daysLeft(closingAt: string) {
  return Math.ceil((new Date(closingAt).getTime() - Date.now()) / 86_400_000);
}

function TenderTable() {
  const q = useSearchParams().get("q") ?? "";
  const [load, setLoad] = useState<Load>({ state: "loading" });

  useEffect(() => {
    let cancelled = false;
    setLoad({ state: "loading" });
    api
      .GET("/api/v1/tenders", { params: { query: { q: q || undefined } } })
      .then(({ data, error }) => {
        if (cancelled) return;
        setLoad(error || !data ? { state: "error", message: errorMessage(error) } : { state: "ready", items: data.items });
      })
      .catch(() => !cancelled && setLoad({ state: "error", message: "Can't reach the API. Check that the backend is running on port 8000." }));
    return () => {
      cancelled = true;
    };
  }, [q]);

  if (load.state === "loading") return <p className="mt-6 text-sm text-muted-foreground">Loading tenders…</p>;
  if (load.state === "error")
    return (
      <p role="alert" className="mt-6 rounded-lg border border-phase-red/30 bg-phase-red/5 p-4 text-sm text-phase-red">
        {load.message}
      </p>
    );
  if (load.items.length === 0)
    return (
      <div className="mt-8 rounded-2xl border border-dashed border-border p-12 text-center">
        <TenderSheetIllustration className="mx-auto mb-4 w-40" />
        <p className="font-medium">{q ? `No tenders match "${q}"` : "No tenders yet"}</p>
        <p className="mt-1 text-sm text-muted-foreground">
          {q ? "Try a different title, client or reference." : "Create your first tender to start uploading documents."}
        </p>
      </div>
    );

  return (
    <div className="mt-6 overflow-x-auto rounded-2xl border border-border/70 bg-card shadow-sm">
      <table className="w-full min-w-[40rem] text-sm">
        <thead>
          <tr className="border-b border-border text-left text-xs uppercase tracking-wider text-muted-foreground">
            <th className="px-5 py-4 font-medium">Tender</th>
            <th className="px-5 py-4 font-medium">Closes</th>
            <th className="px-5 py-4 font-medium">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {load.items.map((t) => {
            const left = daysLeft(t.closing_at);
            return (
              <tr key={t.id} className="hover:bg-muted/50">
                <td className="px-5 py-4">
                  <Link href={`/tenders/view/documents/?id=${t.id}`} className="font-medium hover:underline">
                    {t.title}
                  </Link>
                  <div className="text-xs text-muted-foreground">
                    {t.client_name} · <span className="num">{t.reference_number}</span>
                  </div>
                </td>
                <td className="px-5 py-4">
                  <div>{dateFmt.format(new Date(t.closing_at))}</div>
                  <div className={`num text-xs ${left < 0 ? "text-phase-red" : left <= 7 ? "text-copper" : "text-muted-foreground"}`}>
                    {left < 0 ? `closed ${-left} days ago` : `${left} days left`}
                  </div>
                </td>
                <td className="px-5 py-4">{STATUS_LABEL[t.status]}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function TendersPage() {
  return (
    <div className="mx-auto max-w-5xl">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="num text-xs uppercase tracking-widest text-muted-foreground">Tenders</p>
          <h1 className="mt-1 text-4xl font-semibold tracking-tight">All tenders</h1>
        </div>
        <Link href="/tenders/new/" className={buttonVariants()}>
          <Plus /> New tender
        </Link>
      </div>
      <Suspense>
        <TenderTable />
      </Suspense>
    </div>
  );
}
