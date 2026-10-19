# IntelTPS — Intelligent Tender Preparation System

Group project (4 developers), 16 Oct to 16 Nov 2026. Full spec: `docs/spec/IntelTPS_spec.pdf`.
Visual references (open in a browser): `docs/visuals/inteltps-architecture.html` (clickable system map, ERD, FR/NFR tables), `docs/visuals/inteltps-build-map.html` (build order per developer, contracts, gates), `docs/visuals/rfq-workflow.html` (user journey + user stories).
Detailed tables: `docs/architecture.md` (FRs, API, NFRs, business rules) and `docs/build-plan.md` (blocks per developer).

## What we are building

A multi-tenant SaaS for **electrical subcontractors** in South Africa. A contractor uploads a tender pack (RFQ/BoQ). The system extracts BoQ lines and tender requirements with source page references, a person reviews and approves them, then the app calculates totals with `Decimal`, matches supplier quotes, tracks a compliance checklist and exports approved Excel/PDF.

**AI suggests, people approve.** Nothing extracted is "verified" until a user approves it. The AI never prices totals, approves data or submits bids.

**MVP must work end to end by 8 Nov:** login → create tender → upload → background extraction → review/approve with source page → Decimal totals → supplier match confirm → checklist → approved Excel export. Deployed on Azure with tests and an AI accuracy report.

**Out of scope:** auto bid submission, tender scraping, accounting, scheduling, payment integration (record plan limits only), microservices, Celery/Redis.

## Stack

- Backend: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL 16
- Worker: same codebase, `python -m app.worker`; PyMuPDF, pdfplumber, openpyxl, pandas, python-docx, python-magic
- OCR: Azure AI Document Intelligence (Layout, F0), Tesseract fallback
- LLM: Azure OpenAI small model (gpt-4o-mini class) with JSON-schema structured output, behind an `LLMClient` interface with a fallback provider (student subscriptions often have zero OpenAI quota)
- Matching: rapidfuzz + unit normalisation + spec tokens (mm², cores, rating)
- Exports: openpyxl (Excel), WeasyPrint (PDF)
- Auth: JWT in httpOnly/Secure/SameSite=Lax cookies (30 min access, 7 day refresh), argon2id, role checks in dependencies, slowapi rate limits
- Frontend: Next.js (App Router) + TypeScript, static export, Tailwind, shadcn/ui, TanStack Table, react-pdf; typed client generated from FastAPI's OpenAPI
- Infra (Azure for Students, $100 credit): Static Web Apps (free), Container Apps consumption scale-to-zero (API app + queue-triggered worker Job), PostgreSQL Flexible Server B1ms, Blob Storage (private, SAS links), Storage Queue, Application Insights. Images on GHCR. CI/CD on GitHub Actions with OIDC login to Azure.
- Local: docker-compose with postgres, azurite (blob + queue), api, worker, frontend

## Repo layout

```
backend/
  app/
    main.py                 # FastAPI app
    worker.py               # queue consumer entrypoint
    core/                   # config, db session, security, errors, OrgScopedRepository, storage client, audit hook
    modules/<module>/       # router.py, schemas.py, service.py, repository.py (+ models in core/models or per module)
      auth, tenders, documents, jobs, checklist, boq, suppliers, exports, audit, usage, notifications
    processing/             # file extractors: pdf, xlsx, csv, docx, ocr (no AI here)
    ai/                     # LLMClient, prompts, candidate schemas, extractors, validators (no DB here)
  alembic/
  tests/  unit/ integration/ security/ ai_eval/
  Dockerfile
frontend/                   # Next.js
samples/                    # tender packs + verified expected answers
docs/  infra/  docker-compose.yml  .env.example  .github/workflows/
```

## Architecture rules (do not break)

1. **Layers:** Router = HTTP only (validate, role check, call one service, return schema). Service = business rules, transactions, audit. Repository = all SQL. Routers never touch the DB; services never build SQL.
2. **Tenant isolation:** `organisation_id` comes only from the verified JWT. Every repository inherits `OrgScopedRepository`, which adds `WHERE organisation_id = :org` to every select/update/delete. Cross-org access returns **404**, not 403. Blob keys are prefixed `org/{organisation_id}/...`.
3. **Money:** `numeric(14,2)` money, `numeric(14,3)` quantities, Python `Decimal`, `ROUND_HALF_UP` to 2 places at line level. Never float. Never let the LLM compute totals. VAT mode is an org setting (default ZAR, 15%).
4. **Null vs zero:** `quantity IS NULL` = missing; `0` = zero. UI shows them differently.
5. **Originals kept:** every extracted field has an `original_*` copy; edits change the live column and add a `field_revisions` row.
6. **Review lifecycle (Postgres enum):** extracted → corrected → approved | rejected; any → stale when a newer document version is uploaded. Only `approve()` sets approved (stamps user + time). Exports and totals use approved rows only; draft exports are watermarked.
7. **Jobs:** queued → running → succeeded | failed. Max 3 retries with backoff. `extraction_jobs.idempotency_key` = document id + checksum + job type, unique index. Worker replaces its own previous candidates in the same transaction so retries never duplicate.
8. **Upload path:** sniff MIME from bytes (ignore extension), 20 MB / 50 page cap, check usage quota, stream to Blob, insert document + job in one transaction, put job id on queue, return **202** in under 5 s. No parsing in the request.
9. **AI safety:** document text wrapped in delimiters and declared as data; model has no tools/DB/network; output must validate against the Pydantic candidate schema or is rejected; only needed pages are sent; AI output can only create `extracted` items; every item needs `source_document_id` + `source_page` (else flag `no_source`, cannot be approved).
10. **Supplier matching:** suggestions carry evidence (text, unit, spec, price, validity). Low score or unit/spec conflict stays `suggested`. Never auto-select the cheapest. Only confirmed matches feed prices.
11. **Errors:** `{"error": {"code": "...", "message": "...", "details": {...}}}`; 422 validation, 402 quota, 404 not found/other org, 409 conflict, 429 rate limit.
12. **Logs:** structured JSON with ids only; never tokens, secrets or document text.
13. **Compliance wording:** checklist/register/exports say the content is extracted to support preparation, not a ruling that a bid complies.

## Roles

Admin (manage workspace, members, defaults, audit), Estimator (upload, review, estimate, quotes, export), Project manager (deadlines, assign, tasks, exports; can assign requirements but not edit them), Reviewer (read only). Platform admin is a flag on `users`, not an org role.

## Data model (20 tables)

organisations, users, memberships, invites, tenders, documents, document_pages, extraction_jobs, tender_requirements, boq_items, field_revisions, suppliers, supplier_quotations, supplier_quotation_items, quote_matches, tasks, exports, audit_events, notifications, usage_counters. UUID keys; composite index `(organisation_id, tender_id)` on child tables. Full ERD in `docs/architecture.md`.

## API (all under /api/v1)

auth: `POST /auth/register|login|logout`, `GET /me`, `POST /invites`, `PATCH /members/{id}` ·
tenders: `POST/GET /tenders`, `GET/PATCH /tenders/{id}`, `POST /tenders/{id}/archive`, `GET /dashboard` ·
documents: `POST /tenders/{id}/documents`, `GET /documents/{id}`, `GET /documents/{id}/download` (5-min SAS), `POST /documents/{id}/process` ·
jobs: `GET /jobs/{id}`, `POST /jobs/{id}/retry` ·
checklist: `GET /tenders/{id}/requirements`, `PATCH /requirements/{id}`, `GET /tenders/{id}/checklist`, `POST /tasks`, `PATCH /tasks/{id}` ·
boq: `GET /tenders/{id}/boq`, `PATCH /boq-items/{id}`, `POST /tenders/{id}/boq/approve` ·
suppliers: `POST/GET /suppliers`, `POST /quotations`, `GET /tenders/{id}/comparisons`, `PATCH /matches/{id}` ·
exports: `POST /tenders/{id}/exports`, `GET /exports/{id}/download` ·
other: `GET /audit`, `GET /usage`, `GET/PATCH /organisation`, `GET /notifications`.
Role matrix in `docs/architecture.md`.

## Build order

Foundation (whole team, 16–19 Oct): F1 repo + compose + CI → F2 schema + migration 001 + seed → F3 API/JSON contracts (Pydantic schemas, stubbed routers, openapi.json, generated TS client) → F4 Azure setup + day-1 checks (OpenAI quota!).
MVP spine (20–26 Oct): A1 core + auth → A2 upload + staging deploy; B1 queue + worker skeleton (PyMuPDF text only); C1 tenders + seed data; D1 app shell, login, upload. **Gate G1 26 Oct:** upload travels end to end on staging.
Parallel tracks (27 Oct – 8 Nov): A3 versions/downloads, A4 audit + usage limits, A5 tenant tests + reminders; B2 extractors + OCR, B3 LLM extractors, B4 validators + eval set; C2 BoQ + Decimal pricing, C3 review + checklist, C4 supplier matching; D2 review screen, D3 BoQ editor, D4 checklist + comparison. **Gate G2 8 Nov:** real tender pack → approved priced data.
Combine (9–11 Nov): A6 hardening + prod deploy, B5 AI accuracy report, C5 Excel/PDF exports, D5 E2E tests. **Gate G3 11 Nov:** pilot release. 12–16 Nov pilot, docs, demo, submit.

Contracts frozen 19 Oct: DB schema (changes only via new Alembic migrations), OpenAPI (additive only), candidate JSON schemas, job status values, approved-only rule, one image + one `.env.example`.

## Definition of done (per feature)

Validated input, permissions enforced on the server, tests passing (incl. a cross-tenant test for any new resource), errors handled with the standard format, deployed to staging.

## Commands (once scaffolded)

`docker compose up` · `docker compose exec api alembic upgrade head` · `docker compose exec api python -m scripts.seed` · `docker compose exec api pytest` · `cd frontend && npm run dev` · `npm run gen:api` (regenerate TS client from openapi.json)
