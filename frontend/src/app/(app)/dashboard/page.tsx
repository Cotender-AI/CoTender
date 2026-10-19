"use client";

import { useEffect, useState } from "react";
import { api, errorMessage } from "@/api/client";
import type { Schemas } from "@/api/types";
import { Placeholder } from "@/components/Placeholder";

// Wiring example: a typed call to the (stubbed) API. FE-03 turns this into the real dashboard.
export default function DashboardPage() {
  const [data, setData] = useState<Schemas["Dashboard"] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.GET("/api/v1/dashboard").then(({ data, error }) => {
      if (error) setError(errorMessage(error));
      else setData(data);
    }).catch(() => setError("Cannot reach the API. Is `docker compose up` running?"));
  }, []);

  return (
    <Placeholder title="Dashboard" issue="FE-03">
      {error && <p className="text-red-700">{error}</p>}
      {!data && !error && <p>Loading…</p>}
      {data && (
        <ul className="space-y-1">
          {data.closing_soon.map((t) => (
            <li key={t.id}>
              {t.reference_number}: {t.title} closes in {t.days_left} days
            </li>
          ))}
        </ul>
      )}
    </Placeholder>
  );
}
