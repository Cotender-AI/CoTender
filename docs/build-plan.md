# IntelTPS build plan

Generated from `visuals/inteltps-build-map.html`. Build left to right: foundation, MVP spine, parallel tracks, combine, ship. Blocks list what to build, files, endpoints, what they need first and when they are done.

## Lanes

- **Platform and security** (Member 1): Owns the API skeleton, auth, tenant isolation, uploads and storage, audit, usage limits, CI/CD and deployment.
- **AI and processing** (Member 2): Owns the queue, worker, file extractors, OCR, LLM extraction, validation and the AI accuracy test set.
- **Estimating and data** (Member 3): Owns the schema and ERD, tenders, BoQ and Decimal pricing, review states, checklist and tasks, supplier matching and exports.
- **Frontend and product** (Member 4): Owns every screen, the generated API client, end-to-end tests, contractor interviews, pricing and the demo.

## Foundation (16–19 Oct)

### F1 · Repo, Compose and CI

Foundation (whole team) · Member 1 leads · 16–17 Oct

**Build**
- GitHub organisation and monorepo; protect main and dev
- Folders: backend, frontend, samples, docs, infra
- docker-compose.yml with Postgres 16, Azurite, api, worker, frontend
- make up / make test / make migrate scripts
- ci.yml: ruff, mypy, pytest, Next.js build on every pull request

**Files:** `docker-compose.yml`, `backend/Dockerfile`, `.github/workflows/ci.yml`, `.env.example`

**Needs first:** nothing · **Unblocks:** F2, F4

**Done when**
- [ ] docker compose up serves /health and the Next.js home page on all four laptops
- [ ] CI is green on an empty pull request

### F2 · Database schema + migration 001

Foundation (whole team) · Member 3 leads · 16–19 Oct

**Build**
- SQLAlchemy 2.0 models for all 20 tables
- Status enums: tender, document, job, review
- numeric(14,2) money, numeric(14,3) quantities, UUID keys
- organisation_id and (organisation_id, tender_id) indexes everywhere
- Alembic init and 001_initial migration
- Seed script: demo org, one user per role, one tender

**Files:** `backend/app/core/models/`, `backend/alembic/versions/001_initial.py`, `backend/scripts/seed.py`, `docs/erd.md`

**Needs first:** F1 · **Unblocks:** F3, A1, B1, C2

**Done when**
- [ ] alembic upgrade head works on an empty database
- [ ] Seed loads; ERD exported into the docs

**Requirements:** FR-05, FR-26, FR-28

### F3 · API and JSON contracts

Foundation (whole team) · All four · 17–19 Oct

**Build**
- Pydantic request and response schemas for every module
- Routers stubbed with example responses so the frontend can start
- Shared error format and status codes
- Candidate schemas: BoqLineCandidate, RequirementCandidate, QuoteLineCandidate
- Export openapi.json; generate the TypeScript client

**Files:** `backend/app/modules/*/schemas.py`, `backend/app/ai/schemas.py`, `docs/openapi.json`, `frontend/src/api/`

**Needs first:** F2 · **Unblocks:** A1, D1, B3, C3

**Done when**
- [ ] Frontend can call every stubbed endpoint
- [ ] Schemas merged and marked frozen

### F4 · Azure setup + day-1 checks

Foundation (whole team) · Member 1 + Member 2 · 16–19 Oct

**Build**
- One resource group in one region
- PostgreSQL B1ms, storage account with blob container and queue
- Container Apps environment and Static Web Apps (free)
- Budget alerts at $20 and $50 to all four
- Deploy a small Azure OpenAI model, or set up the fallback provider
- Document Intelligence F0; GitHub OIDC login to Azure

**Files:** `infra/azure-setup.sh`, `docs/deployment.md`

**Needs first:** F1 · **Unblocks:** A2, B1

**Done when**
- [ ] Every resource exists and is reachable from CI
- [ ] A test LLM call returns valid JSON

## MVP spine (20–26 Oct)

### A1 · Core + auth

Platform and security · Member 1 · 20–22 Oct

**Build**
- Settings, DB session dependency, error handler, request id
- OrgScopedRepository base class
- Register, login, logout, me, invites
- argon2id hashes; JWT in httpOnly cookie
- require_role dependency; audit.record() hook

**Files:** `backend/app/core/`, `backend/app/modules/auth/`

**Endpoints:** `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /me`, `POST /invites`

**Needs first:** F2, F3 · **Unblocks:** A2, C1, D1, A4, A5

**Done when**
- [ ] 401 without a token, 403 for a wrong role
- [ ] Every repository query carries organisation_id

**Requirements:** FR-01, FR-02, FR-03, FR-04, FR-05

### A2 · Upload + staging

Platform and security · Member 1 · 22–26 Oct

**Build**
- Upload endpoint: sniff bytes, 20 MB cap, stream to Blob under org/ prefix
- SHA-256 checksum; documents row and extraction_jobs row in one transaction
- Put job id on the queue; return 202 with the job id
- deploy-staging.yml: GHCR image, migrations, Container Apps update

**Files:** `backend/app/modules/documents/`, `backend/app/core/storage.py`, `.github/workflows/deploy-staging.yml`

**Endpoints:** `POST /tenders/{id}/documents`, `GET /documents/{id}`

**Needs first:** A1, F4 · **Unblocks:** A3

**Done when**
- [ ] Upload on staging returns 202 in under 5 seconds

**Requirements:** FR-07, FR-12

### B1 · Queue + worker skeleton

AI and processing · Member 2 · 20–26 Oct

**Build**
- Worker entrypoint: python -m app.worker
- Read the queue; claim the job by idempotency key
- Statuses: queued, running, succeeded, failed
- Retry with backoff, max 3
- First extractor only: PyMuPDF text per page into document_pages
- Container Apps Job with a queue scale rule

**Files:** `backend/app/worker.py`, `backend/app/modules/jobs/`, `backend/app/processing/pdf.py`

**Endpoints:** `GET /jobs/{id}`, `POST /jobs/{id}/retry`

**Needs first:** F2, F4 · **Unblocks:** B2

**Done when**
- [ ] A text PDF uploaded on staging ends with document_pages rows and a succeeded job

**Requirements:** FR-13, FR-15, FR-16

### C1 · Tenders + seed data

Estimating and data · Member 3 · 20–24 Oct

**Build**
- Tenders router, service, repository
- List with search and status filter
- Allowed status transitions only
- Archive; dashboard of closings in the next 14 days
- Collect 3+ real tender packs into samples/ and start the verified answers

**Files:** `backend/app/modules/tenders/`, `samples/`

**Endpoints:** `POST /tenders`, `GET /tenders`, `GET /tenders/{id}`, `PATCH /tenders/{id}`, `POST /tenders/{id}/archive`, `GET /dashboard`

**Needs first:** A1 · **Unblocks:** A5, C2

**Done when**
- [ ] Invalid transition returns 422
- [ ] Archived tenders hidden from the default list

**Requirements:** FR-06, FR-08, FR-10, FR-44

### D1 · App shell, login, upload

Frontend and product · Member 4 · 20–26 Oct

**Build**
- Next.js, Tailwind and shadcn/ui setup; layout and navigation
- Auth guard; login and register pages
- Tender list and create form
- Tender workspace with upload and status polling every 3 s
- Use only the generated API client

**Files:** `frontend/src/app/`, `frontend/src/components/`, `frontend/src/api/`

**Needs first:** F3, A1 · **Unblocks:** D2, D3, D4

**Done when**
- [ ] On staging: log in, create a tender, upload, watch it reach done

**Requirements:** FR-01, FR-02, FR-06, FR-07

## Parallel tracks (27 Oct – 8 Nov)

### A3 · Versions, downloads

Platform and security · Member 1 · 27 Oct – 1 Nov

**Build**
- Re-upload creates version 2 and keeps version 1
- Mark items from the old version stale (calls the review service)
- 5-minute read-only SAS download links after a permission check

**Files:** `backend/app/modules/documents/service.py`

**Endpoints:** `GET /documents/{id}/download`

**Needs first:** A2 · **Unblocks:** A6

**Done when**
- [ ] Old versions kept; stale items flagged

**Requirements:** FR-09

### A4 · Audit + usage limits

Platform and security · Member 1 · 30 Oct – 4 Nov

**Build**
- Audit rows for login, uploads, edits, approvals, exports
- Usage counters; plan limits checked before a job is queued
- Rate limits on login and upload

**Files:** `backend/app/modules/audit/`, `backend/app/modules/usage/`

**Endpoints:** `GET /audit`, `GET /usage`

**Needs first:** A1 · **Unblocks:** A6

**Done when**
- [ ] Over-limit upload returns 402; 6th login in a minute returns 429

**Requirements:** FR-42, FR-47, FR-48, FR-49, FR-50

### A5 · Tenant tests, reminders

Platform and security · Member 1 · 3–8 Nov

**Build**
- Cross-tenant test for every resource and download
- Daily reminder job for deadlines and tasks
- Notifications endpoint

**Files:** `backend/tests/security/`, `backend/app/modules/notifications/`

**Endpoints:** `GET /notifications`

**Needs first:** A1, C1 · **Unblocks:** A6

**Done when**
- [ ] Org A gets 404 on every Org B id

**Requirements:** FR-05, FR-45

### B2 · Extractors + OCR

AI and processing · Member 2 · 27 Oct – 1 Nov

**Build**
- Extractor registry by sniffed MIME type
- pdfplumber tables; openpyxl and pandas keep sheet and row
- python-docx paragraphs and tables
- Document Intelligence for scans; Tesseract fallback

**Files:** `backend/app/processing/`

**Needs first:** B1 · **Unblocks:** B3

**Done when**
- [ ] One fixture per file type parses with page or sheet numbers

**Requirements:** FR-11, FR-13, FR-14

### B3 · LLM extractors

AI and processing · Member 2 · 29 Oct – 5 Nov

**Build**
- LLMClient: Azure OpenAI with fallback provider
- BoQ, requirement and quote extractors returning the frozen schemas
- Spreadsheets mapped straight into BoqLineCandidate, no LLM
- Page-chunked prompts; document text wrapped as data
- Save items as extracted with source document and page

**Files:** `backend/app/ai/`

**Needs first:** B2, F3 · **Unblocks:** B4, C4

**Done when**
- [ ] Sample BoQ produces candidates with valid source pages

**Requirements:** FR-17, FR-18, FR-19, FR-24, FR-33

### B4 · Validators + eval set

AI and processing · Member 2 · 3–8 Nov

**Build**
- Rules: unit present, numeric quantity, null vs zero, outliers → flags
- 20 verified documents with expected answers
- eval.py: field accuracy, precision and recall, cost per document
- Prompt-injection fixture

**Files:** `backend/app/ai/validators.py`, `backend/tests/ai_eval/`

**Needs first:** B3 · **Unblocks:** B5

**Done when**
- [ ] Eval script prints a metrics table

**Requirements:** FR-17, FR-29

### C2 · BoQ and pricing

Estimating and data · Member 3 · 27 Oct – 2 Nov

**Build**
- Edit lines; original_* kept; field_revisions row per change
- Material, labour, markup with org defaults
- pricing.py with Decimal, ROUND_HALF_UP, VAT mode
- Flags for missing or unusual values

**Files:** `backend/app/modules/boq/`, `backend/app/modules/boq/pricing.py`

**Endpoints:** `GET /tenders/{id}/boq`, `PATCH /boq-items/{id}`

**Needs first:** C1, F2 · **Unblocks:** C3, C4, D3, C5

**Done when**
- [ ] Pricing unit tests pass, VAT on and off

**Requirements:** FR-25, FR-26, FR-27, FR-28, FR-29

### C3 · Review + checklist

Estimating and data · Member 3 · 2–6 Nov

**Build**
- Review state machine: extracted, corrected, approved, rejected, stale
- Bulk approve
- Requirements: classify, approve, assign
- Tasks and the checklist view

**Files:** `backend/app/modules/checklist/`, `backend/app/modules/boq/review.py`

**Endpoints:** `POST /tenders/{id}/boq/approve`, `PATCH /requirements/{id}`, `GET /tenders/{id}/checklist`, `POST /tasks`, `PATCH /tasks/{id}`

**Needs first:** C2, F3 · **Unblocks:** D2, D4, C5

**Done when**
- [ ] Only approve() can set approved; illegal transitions return 422

**Requirements:** FR-20, FR-21, FR-22, FR-43, FR-46

### C4 · Supplier matching

Estimating and data · Member 3 · 3–8 Nov

**Build**
- Suppliers and quotations
- Matcher: rapidfuzz + unit normalisation + spec tokens (mm², cores, rating) + validity
- quote_matches with evidence; confirm or reject
- Never auto-select the cheapest

**Files:** `backend/app/modules/suppliers/`

**Endpoints:** `POST /suppliers`, `POST /quotations`, `GET /tenders/{id}/comparisons`, `PATCH /matches/{id}`

**Needs first:** C2, B3 · **Unblocks:** D4

**Done when**
- [ ] Unit mismatch flagged; unconfirmed matches excluded from totals

**Requirements:** FR-31, FR-32, FR-34, FR-35, FR-36, FR-37

### D2 · Review screen

Frontend and product · Member 4 · 27 Oct – 2 Nov

**Build**
- react-pdf source page on the left, fields on the right
- Status badge on every value
- Approve or correct inline; jump to source page

**Files:** `frontend/src/app/tenders/[id]/review/`

**Needs first:** D1, C3 · **Unblocks:** D5

**Done when**
- [ ] A reviewer approves a line without leaving the page

**Requirements:** FR-19, FR-20, FR-25, FR-26

### D3 · BoQ editor

Frontend and product · Member 4 · 31 Oct – 5 Nov

**Build**
- TanStack Table with inline editing
- Markup controls; totals come from the API, never computed in the browser
- Flags highlighted; filter by review status

**Files:** `frontend/src/app/tenders/[id]/boq/`

**Needs first:** D1, C2 · **Unblocks:** D5

**Done when**
- [ ] Edits save and totals refresh from the server

**Requirements:** FR-25, FR-27, FR-28, FR-29

### D4 · Checklist, comparison

Frontend and product · Member 4 · 3–8 Nov

**Build**
- Checklist with assignees, due dates, status
- Supplier comparison with evidence; confirm or reject
- Dashboard widgets; settings for members, defaults, usage

**Files:** `frontend/src/app/tenders/[id]/checklist/`, `frontend/src/app/tenders/[id]/suppliers/`

**Needs first:** D1, C3, C4 · **Unblocks:** D5

**Done when**
- [ ] Every MVP screen reachable from navigation

**Requirements:** FR-22, FR-34, FR-35, FR-36, FR-37, FR-43, FR-44, FR-50

## Combine (9–11 Nov)

### A6 · Hardening + prod deploy

Platform and security · Member 1 · 9–11 Nov

**Build**
- Security tests: id guessing, upload abuse, rate limits
- Backup restore drill, timed and written up
- deploy-prod.yml with manual approval and smoke test
- Error alerts in Application Insights

**Files:** `.github/workflows/deploy-prod.yml`, `docs/security.md`

**Needs first:** A3, A4, A5 · **Unblocks:** P1

**Done when**
- [ ] Production live; restore drill documented

### B5 · AI accuracy report

AI and processing · Member 2 · 9–11 Nov

**Build**
- Run eval on the final set
- Metrics, failure analysis, cost per document
- Write the AI section of the documentation

**Files:** `docs/ai-evaluation.md`

**Needs first:** B4 · **Unblocks:** P1

**Done when**
- [ ] Report covers every metric in spec 7.5

### C5 · Excel + PDF exports

Estimating and data · Member 3 · 9–11 Nov

**Build**
- Excel of approved rows only: version, date, sources column
- Draft exports watermarked
- Checklist PDF with WeasyPrint and the compliance disclaimer
- exports row and audit event per export

**Files:** `backend/app/modules/exports/`

**Endpoints:** `POST /tenders/{id}/exports`, `GET /exports/{id}/download`

**Needs first:** C2, C3 · **Unblocks:** D5, P1

**Done when**
- [ ] Export of 2,000 lines in under 10 seconds

**Requirements:** FR-23, FR-30, FR-38, FR-39, FR-40, FR-41, FR-42

### D5 · E2E tests + polish

Frontend and product · Member 4 · 9–11 Nov

**Build**
- Playwright: login, upload, approve, export
- Empty, loading and error states
- Phone-width and keyboard pass
- Export screen

**Files:** `frontend/tests/e2e/`

**Needs first:** D2, D3, D4, C5 · **Unblocks:** P1

**Done when**
- [ ] E2E suite green against staging

**Requirements:** FR-38

## Ship (12–16 Nov)

### P1 · Pilot, docs, demo

Whole team · All four · 12–16 Nov

**Build**
- Onboard 3–5 testers with permissioned documents
- Measure correction rate and time saved
- Final documentation with cover page, group name, names and student numbers
- Rehearse the 10-minute demo twice; submit repo, docs and live link

**Files:** `docs/`

**Needs first:** A6, B5, C5, D5 · **Unblocks:** nothing

**Done when**
- [ ] Submitted by 16 Nov

## Integration gates

### G1 · Walking skeleton (26 Oct)

Needs: A1, A2, B1, C1, D1

- [ ] Log in on staging as a seeded user
- [ ] Create a tender and upload a text PDF
- [ ] Job runs in the worker and the page shows done
- [ ] CI and staging deploy are automatic

### G2 · Core loop works (MVP) (8 Nov)

Needs: A3, A4, A5, B2, B3, B4, C2, C3, C4, D2, D3, D4

- [ ] Real electrical tender pack in
- [ ] BoQ and requirements extracted with source pages
- [ ] Reviewed, corrected and approved in the UI
- [ ] Quotes matched and confirmed; totals correct to the cent
- [ ] Org A cannot see Org B

### G3 · Pilot release (11 Nov)

Needs: A6, B5, C5, D5

- [ ] Production deployed with approval
- [ ] Approved Excel and checklist PDF export
- [ ] Security tests and E2E suite green
- [ ] Restore drill done

## Contracts

| Contract | What it fixes | Produced by | Used by | Frozen |
| --- | --- | --- | --- | --- |
| Database schema | Tables, columns, enums, keys | Member 3 (F2) | Everyone | 19 Oct; changes only as new Alembic migrations |
| OpenAPI spec | Every endpoint, request and response, error format | Each backend owner (F3) | Member 4 via the generated client | 19 Oct; additive changes only |
| Candidate JSON schemas | Shape of an extracted BoQ line, requirement and quote line | Member 2 (F3) | Member 3 review and matching | 19 Oct |
| Job status | queued, running, succeeded, failed, plus error_code | Member 2 (B1) | API status endpoint and Member 4 polling | 22 Oct |
| Approved-only rule | Only approved rows feed totals and exports | Member 3 (C3) | Exports and the BoQ editor | 6 Nov |
| Image and env vars | One Docker image, two commands, one .env.example | Member 1 (F1, A2) | Everyone | 19 Oct |
