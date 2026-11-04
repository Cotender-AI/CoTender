"use client";

import { useState } from "react";
import { Check, X } from "lucide-react";
import { Ferrule } from "@/components/Ferrule";
import { StatusBadge, type ReviewStatus } from "@/components/StatusBadge";
import { Button } from "@/components/ui/button";
import { LINES, lineTotal, zar } from "@/lib/mock";

// MOCK DATA + local state. Real version (D2) calls PATCH /boq-items/{id}; only the server's approve() sets approved.
export default function ReviewPage() {
  const [status, setStatus] = useState<Record<string, ReviewStatus>>(
    Object.fromEntries(LINES.map((l) => [l.id, l.status])),
  );
  const [selected, setSelected] = useState(LINES[1].id);
  const line = LINES.find((l) => l.id === selected)!;

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_22rem]">
      <div className="overflow-x-auto rounded-2xl border border-border/70 bg-card shadow-sm">
        <table className="w-full min-w-[40rem] text-sm">
          <thead>
            <tr className="border-b border-border text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th className="w-1.5 p-0" />
              <th className="px-3 py-4 font-medium">Item</th>
              <th className="px-3 py-4 font-medium">Description</th>
              <th className="px-3 py-4 text-right font-medium">Qty</th>
              <th className="px-3 py-4 text-right font-medium">Rate</th>
              <th className="px-3 py-4 text-right font-medium">Total</th>
              <th className="px-3 py-4 font-medium">Source</th>
              <th className="px-3 py-4 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {LINES.map((l) => {
              const st = status[l.id];
              const t = lineTotal(l);
              return (
                <tr
                  key={l.id}
                  onClick={() => setSelected(l.id)}
                  className={`cursor-pointer ${selected === l.id ? "bg-muted" : "hover:bg-muted/50"} ${st === "rejected" ? "opacity-60" : ""}`}
                >
                  <td className={`w-1.5 p-0 ${st === "approved" ? "earth-stripe" : ""}`} />
                  <td className="num px-3 py-4 text-muted-foreground">{l.item}</td>
                  <td className="max-w-xs px-3 py-4">{l.description}</td>
                  <td className="num px-3 py-4 text-right">
                    {l.qty == null ? <span className="text-copper">missing</span> : l.qty}
                    {l.qty != null && <span className="ml-1 text-xs text-muted-foreground">{l.unit}</span>}
                  </td>
                  <td className="num px-3 py-4 text-right">{zar(l.rate)}</td>
                  <td className="num px-3 py-4 text-right">{zar(t)}</td>
                  <td className="px-3 py-4"><Ferrule page={l.page} /></td>
                  <td className="px-3 py-4"><StatusBadge status={st} /></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <aside className="h-fit rounded-2xl border border-border/70 bg-card shadow-sm p-4 lg:sticky lg:top-6">
        <div className="flex items-center justify-between">
          <h2 className="font-heading text-base font-semibold">Item {line.item}</h2>
          <Ferrule page={line.page} />
        </div>
        {/* Stand-in for the react-pdf page (D2). The highlighted row is the extracted line. */}
        <div className="mt-3 rounded-md border border-border bg-white p-3 text-[11px] leading-5 text-slate-500 shadow-inner">
          <div className="h-2 w-2/3 rounded bg-slate-200" />
          <div className="mt-2 h-2 w-full rounded bg-slate-100" />
          <div className="my-2 rounded border-l-4 border-copper bg-orange-50 px-2 py-1 text-slate-800">
            {line.item} {line.description} {line.qty ?? ""} {line.unit}
          </div>
          <div className="h-2 w-5/6 rounded bg-slate-100" />
          <div className="mt-2 h-2 w-3/4 rounded bg-slate-100" />
        </div>
        {line.page == null && (
          <p className="mt-3 text-sm text-copper">No source page was found, so this line can&apos;t be approved until one is added.</p>
        )}
        <p className="mt-3 text-xs text-muted-foreground">
          Extracted to support preparation. It isn&apos;t a ruling that your bid complies.
        </p>
        <div className="mt-4 flex gap-2">
          <Button
            className="flex-1"
            disabled={line.page == null}
            onClick={() => setStatus((s) => ({ ...s, [line.id]: "approved" }))}
          >
            <Check /> Approve
          </Button>
          <Button variant="outline" onClick={() => setStatus((s) => ({ ...s, [line.id]: "rejected" }))}>
            <X /> Reject
          </Button>
        </div>
      </aside>
    </div>
  );
}
