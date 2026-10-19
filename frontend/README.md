# CoTender frontend

Next.js (App Router) + TypeScript + Tailwind, built as a static export for Azure Static Web Apps.

```bash
npm install
npm run dev        # http://localhost:3000 (API expected on http://localhost:8000)
npm run gen:api    # regenerate src/api/schema.d.ts after docs/openapi.json changes
npm run build      # static site in out/
```

- Call the backend only through `src/api/client.ts` (typed from the OpenAPI contract).
- Tender pages live under `/tenders/view/<tab>/?id=<tender id>`. Static export can't do
  `[id]` routes without knowing every id at build time, so ids go in the query string.
- Each page marked "To build in issue …" is a placeholder; replace it when you take the issue.
