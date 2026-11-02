"use client";

import { useEffect, useState } from "react";
import { api } from "@/api/client";

// Calls GET /health through the generated client so the shell shows whether the API is reachable.
export function ApiHealth() {
  const [ok, setOk] = useState<boolean | null>(null);

  useEffect(() => {
    api.GET("/health").then(({ error }) => setOk(!error)).catch(() => setOk(false));
  }, []);

  const label = ok === null ? "Checking API…" : ok ? "API online" : "API offline (using mock data)";
  const dot = ok === null ? "bg-slate-400" : ok ? "bg-earth-green" : "bg-earth-yellow";
  return (
    <div className="mt-auto flex items-center gap-2 px-2.5 text-xs text-muted-foreground" role="status">
      <span className={`size-2 rounded-full ${dot}`} />
      {label}
    </div>
  );
}
