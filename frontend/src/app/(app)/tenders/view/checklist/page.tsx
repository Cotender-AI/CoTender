"use client";

import { useMemo, useState } from "react";
import { ArrowRight, Check, Paperclip, RotateCcw } from "lucide-react";
import { Ferrule } from "@/components/Ferrule";
import { Button } from "@/components/ui/button";
import {
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";
import { CATEGORIES, CHECKLIST, type ChecklistItem } from "@/lib/checklist-mock";

// MOCK DATA + local state. Real version: PATCH /requirements/{id}; files go through the documents endpoint.
const isRequired = (i: ChecklistItem) => i.mandatory === "mandatory";
const isFinished = (i: ChecklistItem) => i.status === "done" || i.status === "not_applicable";

export default function ChecklistPage() {
  const [items, setItems] = useState(CHECKLIST);
  const [reviewOpen, setReviewOpen] = useState(false);

  const update = (id: string, patch: Partial<ChecklistItem>) =>
    setItems((all) => all.map((i) => (i.id === id ? { ...i, ...patch } : i)));

  const required = items.filter(isRequired);
  const requiredDone = required.filter(isFinished).length;
  const outstanding = items.filter((i) => i.mandatory !== "optional" && !isFinished(i));
  const next = outstanding.find((i) => i.mandatory === "mandatory") ?? outstanding[0];
  const allClear = outstanding.length === 0;
  const pct = Math.round((requiredDone / required.length) * 100);

  const grouped = useMemo(
    () => CATEGORIES.map((c) => ({ category: c, rows: items.filter((i) => i.category === c) })),
    [items],
  );

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      {/* Tender buddy: always says what to do next. */}
      <section className="rounded-2xl border border-border/70 bg-card p-6 shadow-sm">
        <p className="num text-xs uppercase tracking-widest text-muted-foreground">Your next step</p>
        {next ? (
          <>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight">{next.text}</h2>
            {next.hint && <p className="mt-1 text-muted-foreground">{next.hint}</p>}
            <div className="mt-4 flex flex-wrap items-center gap-3">
              <Ferrule page={next.page} />
              <span className="text-sm text-muted-foreground">Due {next.due} · {next.assignee}</span>
            </div>
            <div className="mt-5 flex gap-2">
              {next.needsFile ? (
                <label className="inline-flex h-9 cursor-pointer items-center gap-2 rounded-lg bg-primary px-4 text-sm font-medium text-primary-foreground hover:bg-primary/90">
                  <Paperclip className="size-4" /> Attach file
                  <input type="file" className="sr-only" onChange={(e) => e.target.files?.[0] && update(next.id, { file: e.target.files[0].name, status: "done" })} />
                </label>
              ) : (
                <Button onClick={() => update(next.id, { status: "done" })}><Check /> Mark done</Button>
              )}
              {next.mandatory === "conditional" && (
                <Button variant="outline" onClick={() => update(next.id, { status: "not_applicable" })}>Doesn&apos;t apply to us</Button>
              )}
            </div>
          </>
        ) : (
          <h2 className="mt-2 text-2xl font-semibold tracking-tight">Everything is ticked off. Time for the final review.</h2>
        )}

        <div className="mt-6">
          <div className="flex items-baseline justify-between text-sm">
            <span><span className="num font-medium">{requiredDone}</span> of <span className="num">{required.length}</span> required items done</span>
            <span className="num text-muted-foreground">{pct}%</span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
            <div className="h-full rounded-full bg-earth-green transition-[width] duration-300" style={{ width: `${pct}%` }} />
          </div>
        </div>
      </section>

      {grouped.map(({ category, rows }) => (
        <section key={category}>
          <h3 className="mb-3 text-lg font-semibold">
            {category} <span className="num ml-1 text-sm font-normal text-muted-foreground">{rows.filter(isFinished).length}/{rows.length}</span>
          </h3>
          <ul className="divide-y divide-border overflow-hidden rounded-2xl border border-border/70 bg-card shadow-sm">
            {rows.map((i) => {
              const done = isFinished(i);
              return (
                <li key={i.id} className="flex items-start gap-4 p-5">
                  <button
                    type="button"
                    aria-label={done ? `Reopen: ${i.text}` : `Mark done: ${i.text}`}
                    onClick={() => update(i.id, { status: done ? "open" : "done" })}
                    className={`mt-0.5 grid size-6 shrink-0 place-items-center rounded-full border transition-colors ${
                      done ? "border-earth-green bg-earth-green text-white" : "border-border hover:border-copper"
                    }`}
                  >
                    {done && <Check className="size-3.5" />}
                  </button>
                  <div className="min-w-0 flex-1">
                    <p className={done ? "text-muted-foreground line-through decoration-border" : "font-medium"}>{i.text}</p>
                    <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted-foreground">
                      <Ferrule page={i.page} />
                      <span className={i.mandatory === "mandatory" ? "font-medium text-foreground" : ""}>
                        {i.mandatory === "mandatory" ? "Required" : i.mandatory === "conditional" ? "Only if it applies" : "For information"}
                      </span>
                      {i.status === "not_applicable" && <span>Doesn&apos;t apply</span>}
                      {i.flag && <span className="text-copper">{i.flag}</span>}
                      {i.mandatory !== "optional" && <span>Due {i.due} · {i.assignee}</span>}
                    </div>
                    {i.hint && !done && <p className="mt-2 text-sm text-muted-foreground">{i.hint}</p>}
                    {i.file && (
                      <p className="mt-2 inline-flex items-center gap-1.5 rounded-md bg-muted px-2 py-1 text-xs">
                        <Paperclip className="size-3" /> {i.file}
                        <button type="button" className="ml-1 text-muted-foreground hover:text-foreground" aria-label="Remove file" onClick={() => update(i.id, { file: undefined, status: "open" })}>
                          <RotateCcw className="size-3" />
                        </button>
                      </p>
                    )}
                  </div>
                  {i.needsFile && !i.file && !done && (
                    <label className="inline-flex h-8 shrink-0 cursor-pointer items-center gap-1.5 rounded-lg border border-border px-3 text-sm hover:bg-muted">
                      <Paperclip className="size-3.5" /> Attach
                      <input type="file" className="sr-only" onChange={(e) => e.target.files?.[0] && update(i.id, { file: e.target.files[0].name, status: "done" })} />
                    </label>
                  )}
                </li>
              );
            })}
          </ul>
        </section>
      ))}

      <div className="flex items-center justify-between rounded-2xl bg-muted/60 p-6">
        <div>
          <p className="font-semibold">Final review</p>
          <p className="text-sm text-muted-foreground">
            {allClear ? "Everything required is ticked off." : `${outstanding.length} items still need your attention.`}
          </p>
        </div>
        <Button onClick={() => setReviewOpen(true)}>Review checklist <ArrowRight /></Button>
      </div>

      <Dialog open={reviewOpen} onOpenChange={setReviewOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>{allClear ? "Ready to export" : "Not ready yet"}</DialogTitle>
            <DialogDescription>
              {allClear
                ? "Every required item is done. You can export the checklist and prepare your submission."
                : "These items are still open. Finish them, or mark conditional ones as not applicable."}
            </DialogDescription>
          </DialogHeader>
          {!allClear && (
            <ul className="max-h-64 space-y-2 overflow-y-auto text-sm">
              {outstanding.map((i) => (
                <li key={i.id} className="flex gap-2">
                  <Ferrule page={i.page} /> <span>{i.text}</span>
                </li>
              ))}
            </ul>
          )}
          <p className="text-xs text-muted-foreground">
            This checklist is extracted to support your preparation. It is not a ruling that your bid complies.
          </p>
          <DialogFooter>
            <Button disabled={!allClear} onClick={() => setReviewOpen(false)}>Continue to export</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
