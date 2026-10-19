"""Builds planning/issues.json (the issue list). Edit here, then:  python planning/build_issues.py planning/issues.json && python planning/render_plan.py planning/issues.json planning/PLAN.md"""
import json
import sys

T = lambda *xs: list(xs)  # noqa: E731

milestones = [
    {"key": "B1", "title": "Batch 1 · Foundation (19–25 Oct)", "due": "2026-10-25",
     "description": "Repo, compose, CI, schema, contracts, Azure, auth, worker skeleton, tenders API, app shell. Contracts frozen Fri 23 Oct."},
    {"key": "B2", "title": "Batch 2 · Walking skeleton + core features (26 Oct–1 Nov)", "due": "2026-11-01",
     "description": "Upload end to end on staging (Gate G1, Wed 28 Oct), extractors, BoQ pricing, review state machine, versions."},
    {"key": "B3", "title": "Batch 3 · Full MVP loop (2–6 Nov)", "due": "2026-11-06",
     "description": "LLM extraction, matching, review screen, BoQ editor, checklist, validators. Gate G2 Fri 6 Nov: real tender pack to approved priced data."},
    {"key": "B4", "title": "Batch 4 · Release + submit (7–10 Nov)", "due": "2026-11-10",
     "description": "Exports, hardening, prod deploy, E2E, AI report, docs, demo. Gate G3 Mon 9 Nov. Submit Tue 10 Nov."},
]

labels = [
    ("lane:platform", "1d76db", "Platform and security: API core, auth, uploads, storage, audit, CI/CD, deploy"),
    ("lane:ai", "5319e7", "AI and processing: queue, worker, extractors, OCR, LLM, validators, matching, eval"),
    ("lane:data", "0e8a16", "Estimating and data: schema, tenders, BoQ, pricing, review, checklist, suppliers, exports"),
    ("lane:frontend", "fbca04", "Next.js screens"),
    ("lane:pm", "c5def5", "Project management, samples, pilot, docs, demo"),
    ("type:feature", "a2eeef", "New functionality"),
    ("type:infra", "bfd4f2", "Repo, CI, cloud, deployment"),
    ("type:contract", "d93f0b", "Frozen contract: schema, OpenAPI, candidate JSON, job status"),
    ("type:test", "c2e0c6", "Tests and evaluation"),
    ("type:docs", "0075ca", "Documentation"),
    ("type:gate", "b60205", "Integration gate: whole team checks this together"),
    ("priority:P0", "b60205", "MVP: must work by Gate G2"),
    ("priority:P1", "d93f0b", "Should have for submission"),
    ("priority:P2", "fef2c0", "Stretch: cut first if behind"),
    ("pts:1", "ededed", "Estimate: ~half a day"),
    ("pts:2", "ededed", "Estimate: ~1 day"),
    ("pts:3", "ededed", "Estimate: ~1.5 days"),
    ("pts:5", "ededed", "Estimate: ~2.5 days"),
    ("pts:8", "ededed", "Estimate: ~4 days"),
]

LANE_LABEL = {"platform": "lane:platform", "ai": "lane:ai", "data": "lane:data", "pm": "lane:pm"}

issues = []


def add(key, title, owner, batch, start, due, pts, prio, typ, deps, goal, tasks, done,
        files=None, endpoints=None, refs=None, frontend=False, stub_ok=()):
    lbls = [LANE_LABEL[owner], f"type:{typ}", f"priority:{prio}"]
    if pts:
        lbls.append(f"pts:{pts}")
    if frontend:
        lbls.append("lane:frontend")
    issues.append({
        "key": key, "title": f"[{key}] {title}", "owner": owner, "milestone": batch,
        "start": start, "due": due, "points": pts, "priority": prio, "labels": lbls,
        "depends_on": deps, "stub_ok": list(stub_ok), "goal": goal, "tasks": tasks, "done": done,
        "files": files or [], "endpoints": endpoints or [], "refs": refs or [],
    })


# ---------------------------------------------------------------- Batch 1 · 19–25 Oct
add("PM-01", "Set up project board, branch protection and PR template", "pm", "B1",
    "2026-10-19", "2026-10-19", 1, "P0", "infra", [],
    "Everyone can see who is doing what this week, and nothing lands on main without review.",
    T("Run `planning/create_issues.py` to create labels, milestones and all issues",
      "Create a GitHub Project (board view) with columns Backlog / This week / In progress / In review / Done; add every issue; group by milestone",
      "Add a Start date and Due date field to the Project and copy the dates from each issue",
      "Create `dev` branch; protect `main` and `dev` (PR required, 1 approval, CI must pass once F1 lands)",
      "Add `.github/pull_request_template.md` (what changed, issue link `Closes #`, how tested, screenshots)",
      "Agree working rules in README: branch per issue `feat/<key>-short-name`, PR into `dev`, squash merge",
      "Book a 15-min daily stand-up and a weekly batch review (Sundays)"),
    T("All issues on the board with owners and dates", "Direct pushes to main are blocked"),
    files=T(".github/pull_request_template.md", "README.md"))

add("PM-02", "Azure for Students subscription, team access and budget alerts", "pm", "B1",
    "2026-10-19", "2026-10-20", 1, "P0", "infra", [],
    "The team has one Azure subscription to deploy into, with alerts before the $100 credit runs out.",
    T("Activate Azure for Students on one account; create resource group `rg-cotender` in one region (South Africa North or West Europe)",
      "Invite the platform and AI developers as Contributors on the resource group",
      "Create budget alerts at $20 and $50 emailed to all four members",
      "Start `docs/costs.md`: a table of each resource, SKU and expected monthly cost"),
    T("Platform dev can create resources in the resource group", "Budget alerts visible in Cost Management"),
    refs=T("build-plan F4"))

add("PM-03", "Collect 3+ real electrical tender packs into samples/", "pm", "B1",
    "2026-10-19", "2026-10-23", 2, "P0", "test", [],
    "The AI dev has real RFQ/BoQ files (PDF text, scanned PDF, XLSX, DOCX) to build and test extractors against.",
    T("Get at least 3 electrical tender packs from municipal/public portals or contacts, with permission to use them",
      "Include at least: one text PDF RFQ, one scanned PDF, one XLSX BoQ, one DOCX, one supplier quotation",
      "Put them in `samples/<pack-name>/` with a `README.md` per pack (source, permission, what's inside)",
      "Remove personal information (names, ID numbers, phone numbers) where possible",
      "Keep files under 20 MB / 50 pages each (our upload limit)"),
    T("samples/ has 3+ packs covering PDF, scan, XLSX and DOCX", "AI dev confirms the files are usable"),
    files=T("samples/"), refs=T("build-plan C1", "spec 7.5"))

add("F1", "Monorepo layout, Docker Compose and CI", "platform", "B1",
    "2026-10-19", "2026-10-20", 5, "P0", "infra", [],
    "Every developer runs the same stack with one command, and every PR is checked automatically. This blocks everyone, so it goes first.",
    T("Folders from CLAUDE.md: `backend/app/{core,modules/*,processing,ai}`, `backend/tests/{unit,integration,security,ai_eval}`, `frontend/`, `samples/`, `docs/`, `infra/`",
      "`backend/pyproject.toml` (FastAPI, SQLAlchemy 2, psycopg 3, Alembic, pydantic-settings; dev: pytest, ruff, mypy, httpx)",
      "`backend/app/main.py` with `GET /health`; `backend/app/worker.py` idle loop placeholder",
      "`backend/Dockerfile`: python:3.12-slim + libmagic; one image, two commands (api, worker)",
      "Minimal Next.js (App Router, TypeScript, Tailwind, `output: 'export'`) in `frontend/`",
      "`docker-compose.yml`: postgres:16, azurite (blob + queue), api (uvicorn --reload), worker, frontend (npm run dev)",
      "`.env.example` with every variable, `Makefile` (up, down, migrate, seed, test, lint)",
      "`.github/workflows/ci.yml`: ruff, mypy, pytest with a postgres service, `npm ci && npm run build`"),
    T("`docker compose up` serves /health on :8000 and the Next.js page on :3000 on all four laptops",
      "CI is green on an empty PR"),
    files=T("docker-compose.yml", "backend/Dockerfile", ".github/workflows/ci.yml", ".env.example", "Makefile"),
    refs=T("build-plan F1", "CLAUDE.md Repo layout"))

add("F2", "Database schema: 20 models, migration 001, seed, OrgScopedRepository", "data", "B1",
    "2026-10-19", "2026-10-21", 8, "P0", "contract", ["F1"],
    "Lock the data model everyone builds on. Can start locally on day 1 and plug into compose once F1 merges.",
    T("SQLAlchemy 2.0 models for all 20 tables in `backend/app/core/models/` (ERD in docs/architecture.md)",
      "UUID primary keys; `organisation_id` on every tenant-owned table; `(organisation_id, tender_id)` index on tender child tables",
      "Postgres enums: tender status, document processing status, job status (queued/running/succeeded/failed), review status (extracted/corrected/approved/rejected/stale), match status, task status",
      "`numeric(14,2)` money, `numeric(14,3)` quantities; `original_*` columns on every extracted field; `flags` jsonb",
      "`extraction_jobs.idempotency_key` unique; one confirmed match per BoQ line (partial unique index)",
      "Alembic init + `001_initial` (downgrade drops the enums too)",
      "`OrgScopedRepository` base in `app/core/repository.py`: every select/update/delete filtered by organisation_id; other org returns not found",
      "`scripts/seed.py`: demo org, one user per role (admin, estimator, project_manager, reviewer), one tender; safe to run twice",
      "`docs/erd.md` generated from the models"),
    T("`alembic upgrade head` works on an empty database; downgrade to base works",
      "Seed loads", "Cross-tenant test proves Org B cannot read/update/delete Org A rows through OrgScopedRepository"),
    files=T("backend/app/core/models/", "backend/alembic/versions/001_initial.py", "backend/scripts/seed.py", "backend/app/core/repository.py", "docs/erd.md"),
    refs=T("build-plan F2", "CLAUDE.md rules 2-7", "FR-05, FR-26, FR-28"), stub_ok=T("F1"))

add("F4-AI", "Day-1 check: Azure OpenAI quota, Document Intelligence, fallback LLM", "ai", "B1",
    "2026-10-19", "2026-10-20", 2, "P0", "infra", [],
    "Find out on day 1 whether the student subscription can run an LLM at all, so extraction isn't blocked in week 2.",
    T("Try to deploy a gpt-4o-mini class model in Azure OpenAI; record quota and region",
      "If quota is zero: pick a fallback provider with JSON-schema structured output and get a key",
      "Create Document Intelligence (F0) and run Layout on one scanned sample page",
      "Small script: one LLM call returns JSON that validates against a toy Pydantic model",
      "Write findings in `docs/ai-providers.md` (provider, model, region, cost per 1K tokens, limits); keys go to the team password manager, never the repo"),
    T("A test LLM call returns valid JSON", "Decision on primary + fallback provider written down"),
    refs=T("build-plan F4", "CLAUDE.md Stack: LLM"))

add("F3-P", "API contracts: error format, router conventions, auth/documents/jobs/audit/usage/notifications schemas", "platform", "B1",
    "2026-10-21", "2026-10-22", 3, "P0", "contract", ["F1", "F2"],
    "Give the frontend and the other backend lanes a stable API to code against before the real logic exists.",
    T("Standard error handler: `{\"error\": {\"code\", \"message\", \"details\"}}` for 402/404/409/422/429",
      "Request id middleware; `/api/v1` router mounting per module",
      "Pydantic request/response schemas for auth, documents, jobs, audit, usage, notifications, organisation",
      "Stub routers returning example responses; a stub `get_current_principal` dependency (user id, org id, role) that A1 will replace",
      "`scripts/export_openapi.py` writes `docs/openapi.json`; CI fails if it is out of date"),
    T("Every platform-lane endpoint from CLAUDE.md appears in openapi.json with examples"),
    files=T("backend/app/core/errors.py", "backend/app/modules/*/schemas.py", "docs/openapi.json"),
    refs=T("build-plan F3", "CLAUDE.md rule 11, API list"))

add("F3-D", "API contracts: tenders, BoQ, checklist, suppliers, exports schemas + stubs", "data", "B1",
    "2026-10-22", "2026-10-22", 3, "P0", "contract", ["F2", "F3-P"],
    "Freeze the shape of the estimating endpoints so the frontend can build screens in parallel.",
    T("Pydantic schemas for tenders, dashboard, boq items (incl. original_* and flags), requirements, tasks, checklist, suppliers, quotations, comparisons, matches, exports",
      "Money and quantities serialised as strings (Decimal), never floats",
      "Stub routers with example responses for every estimating endpoint",
      "Regenerate `docs/openapi.json`"),
    T("Every estimating endpoint in openapi.json with examples", "Contracts marked frozen Fri 23 Oct (later changes additive only)"),
    files=T("backend/app/modules/{tenders,boq,checklist,suppliers,exports}/schemas.py"),
    refs=T("build-plan F3"))

add("F3-A", "Candidate JSON schemas + job status contract", "ai", "B1",
    "2026-10-21", "2026-10-21", 2, "P0", "contract", ["F1"],
    "Fix the exact shape the AI returns so review and matching can be built before the extractors work.",
    T("`backend/app/ai/schemas.py`: BoqLineCandidate, RequirementCandidate, QuoteLineCandidate (every item has source_document_id + source_page)",
      "Quantities/prices as Decimal-compatible strings; null = missing (not 0)",
      "Job status values queued/running/succeeded/failed + error_code list, documented in `docs/jobs.md`",
      "Unit tests: valid sample passes, missing source_page is rejected or flagged no_source"),
    T("Schemas merged and marked frozen"),
    files=T("backend/app/ai/schemas.py", "docs/jobs.md"),
    refs=T("build-plan F3", "CLAUDE.md rules 7, 9"))

add("F4-P", "Azure infrastructure + GitHub OIDC", "platform", "B1",
    "2026-10-22", "2026-10-23", 3, "P0", "infra", ["F1", "PM-02"],
    "Create the cloud pieces staging deploys into, scripted so they can be recreated.",
    T("`infra/azure-setup.sh` (az CLI): PostgreSQL Flexible B1ms, storage account with private blob container + queue, Container Apps environment, Static Web Apps (free), Application Insights",
      "GitHub OIDC federated credential so Actions can log in to Azure without secrets in the repo",
      "Images on GHCR", "`docs/deployment.md`: what exists, how to recreate it, where secrets live"),
    T("Every resource exists and is reachable from a CI job"),
    files=T("infra/azure-setup.sh", "docs/deployment.md"), refs=T("build-plan F4"))

add("FE-01", "Frontend app shell + generated API client", "pm", "B1",
    "2026-10-22", "2026-10-23", 3, "P0", "feature", ["F1", "F3-P"],
    "One layout and one typed API client that every screen reuses.",
    T("Add shadcn/ui; base layout with sidebar nav (Dashboard, Tenders, Suppliers, Settings) and a top bar",
      "`npm run gen:api` generates a typed client from `docs/openapi.json` into `frontend/src/api/` (e.g. openapi-typescript + openapi-fetch)",
      "Fetch wrapper sends cookies (`credentials: 'include'`) and shows the standard error message",
      "Empty placeholder pages for each nav item"),
    T("Nav works; a page calls `GET /health` through the generated client", "`npm run build` passes in CI"),
    files=T("frontend/src/app/layout.tsx", "frontend/src/api/", "frontend/src/components/"),
    refs=T("build-plan D1"), frontend=True)

add("B1", "Queue + worker skeleton + job endpoints", "ai", "B1",
    "2026-10-22", "2026-10-26", 5, "P0", "feature", ["F1", "F2", "F3-A"],
    "A queued job gets picked up by the worker and ends as succeeded or failed, with retries, without duplicates.",
    T("`python -m app.worker`: read job id from the Storage Queue (Azurite locally)",
      "Claim job queued → running; skip if idempotency key already succeeded",
      "Retry with backoff, max 3, then failed + error_code; original file untouched",
      "First extractor only: PyMuPDF text per page into `document_pages`",
      "`GET /jobs/{id}`, `POST /jobs/{id}/retry` (router → service → repository)",
      "Tests: success, corrupt file → failed, retry doesn't duplicate pages"),
    T("A text PDF job ends with document_pages rows and a succeeded job (locally; on staging after A2)"),
    files=T("backend/app/worker.py", "backend/app/modules/jobs/", "backend/app/processing/pdf.py"),
    endpoints=T("GET /jobs/{id}", "POST /jobs/{id}/retry"),
    refs=T("build-plan B1", "US-03", "FR-13, FR-15, FR-16"))

add("A1", "Core + auth: register, login, logout, me, roles, audit hook", "platform", "B1",
    "2026-10-23", "2026-10-26", 8, "P0", "feature", ["F2", "F3-P"],
    "Real authentication and role checks replace the stub principal, so every other endpoint is protected.",
    T("Settings, DB session dependency, structured JSON logging (ids only)",
      "argon2id password hashes; JWT access (30 min) + refresh (7 days) in httpOnly/Secure/SameSite=Lax cookies",
      "`POST /auth/register` creates org + admin membership; login, logout, `GET /me`",
      "`require_role(...)` dependency; organisation_id only from the verified token",
      "`POST /invites`, `PATCH /members/{id}` (admin only)",
      "`audit.record()` hook used by services", "slowapi limit on login"),
    T("401 without a token, 403 for a wrong role", "Every repository query carries organisation_id",
      "Cross-tenant test for memberships/invites"),
    files=T("backend/app/core/", "backend/app/modules/auth/"),
    endpoints=T("POST /auth/register", "POST /auth/login", "POST /auth/logout", "GET /me", "POST /invites", "PATCH /members/{id}"),
    refs=T("build-plan A1", "FR-01..FR-05"))

add("C1", "Tenders API + dashboard", "data", "B1",
    "2026-10-23", "2026-10-25", 5, "P0", "feature", ["F2", "F3-D"],
    "Users create and manage tender workspaces; the dashboard shows closing dates.",
    T("Tenders router/service/repository (repository inherits OrgScopedRepository)",
      "Create with required title, reference, client, closing date; status starts `draft`",
      "List with search and status filter; archived hidden by default",
      "Allowed status transitions only (invalid → 422); archive endpoint",
      "`GET /dashboard`: tenders closing in the next 14 days with countdown",
      "Audit event on create/update/archive", "Uses the stub principal until A1 merges, then the real one"),
    T("Invalid transition returns 422", "Archived tenders hidden from the default list", "Org B gets 404 on Org A's tender"),
    files=T("backend/app/modules/tenders/"),
    endpoints=T("POST /tenders", "GET /tenders", "GET /tenders/{id}", "PATCH /tenders/{id}", "POST /tenders/{id}/archive", "GET /dashboard"),
    refs=T("build-plan C1", "US-01", "FR-06, FR-08, FR-10, FR-44"))

add("FE-02", "Login and register pages + auth guard", "pm", "B1",
    "2026-10-24", "2026-10-26", 3, "P0", "feature", ["FE-01", "A1"],
    "People can sign up their company, log in and stay logged in; logged-out users get sent to login.",
    T("Register page (company name, your name, email, password) and login page with shadcn forms",
      "Auth guard: call `GET /me` on load; redirect to /login on 401",
      "Logout button in the top bar", "Show the standard error message on failure",
      "Build against the stub first; switch to the real endpoints when A1 merges"),
    T("Seeded users can log in and out locally"),
    files=T("frontend/src/app/(auth)/"), refs=T("build-plan D1", "FR-01, FR-02"), frontend=True,
    stub_ok=T("A1"))

# ---------------------------------------------------------------- Batch 2 · 26 Oct–1 Nov
add("A2", "Upload endpoint: sniff, Blob storage, job + queue, 202", "platform", "B2",
    "2026-10-26", "2026-10-27", 5, "P0", "feature", ["A1", "B1", "F4-P"],
    "An upload is safely stored and queued for processing, and the user gets an answer in under 5 seconds.",
    T("`POST /tenders/{id}/documents` (multipart): sniff MIME from bytes (PDF, XLSX, CSV, DOCX only), 20 MB / 50 page cap",
      "Stream to Blob `org/{org}/tenders/{tender}/{doc}/v{n}` computing SHA-256 on the way",
      "Insert `documents` + `extraction_jobs` (idempotency key = doc id + checksum + job type) in one transaction",
      "Put job id on the queue; return 202 with document id and job id",
      "`GET /documents/{id}`; `app/core/storage.py` blob + queue client (Azurite locally)",
      "Tests: wrong type → 422 with a clear message, too big → 422, other org → 404"),
    T("Upload returns 202 in under 5 s with a 10 MB PDF"),
    files=T("backend/app/modules/documents/", "backend/app/core/storage.py"),
    endpoints=T("POST /tenders/{id}/documents", "GET /documents/{id}"),
    refs=T("build-plan A2", "US-02", "CLAUDE.md rule 8", "FR-07, FR-12"))

add("A2-DEPLOY", "Staging deploy pipeline", "platform", "B2",
    "2026-10-27", "2026-10-28", 3, "P0", "infra", ["F4-P", "A2"],
    "Every merge to dev deploys to staging automatically, so the team tests the real thing.",
    T("`.github/workflows/deploy-staging.yml`: build image → GHCR → run `alembic upgrade head` → update API container app + worker job",
      "Frontend static export → Static Web Apps", "Worker as a Container Apps Job with a queue-length scale rule",
      "Seed staging with the demo org"),
    T("Merge to dev updates staging without manual steps"),
    files=T(".github/workflows/deploy-staging.yml"), refs=T("build-plan A2, B1"))

add("FE-03", "Tenders list, create form, tender workspace, dashboard countdown", "pm", "B2",
    "2026-10-26", "2026-10-27", 3, "P0", "feature", ["FE-02", "C1"],
    "Users can create a tender and see all their tenders with closing countdowns.",
    T("Tenders list (TanStack Table): search, status filter, closing date",
      "New tender form: title, reference, client, location, closing date+time (required fields enforced)",
      "Tender workspace page with tabs: Documents, Review, BoQ, Checklist, Suppliers, Exports (empty placeholders)",
      "Dashboard: tenders closing in the next 14 days with a countdown badge"),
    T("Create a tender and see it in the list and on the dashboard"),
    files=T("frontend/src/app/tenders/", "frontend/src/app/dashboard/"),
    refs=T("build-plan D1", "US-01"), frontend=True)

add("FE-04", "Upload widget + job status polling", "pm", "B2",
    "2026-10-27", "2026-10-28", 2, "P0", "feature", ["FE-03", "A2", "B1"],
    "Users see their file was received and watch processing finish.",
    T("Drag-and-drop upload on the Documents tab (PDF, DOCX, XLSX, CSV; show size limit)",
      "After 202, poll `GET /jobs/{id}` every 3 s; badges: queued, running, succeeded, failed",
      "Failed shows the error and a Retry button (`POST /jobs/{id}/retry`)",
      "Documents list shows filename, version, uploaded by, status"),
    T("Upload a PDF and watch it reach succeeded"),
    files=T("frontend/src/app/tenders/[id]/documents/"), refs=T("US-02, US-03"), frontend=True)

add("G1", "GATE G1 · Walking skeleton on staging (Wed 28 Oct)", "pm", "B2",
    "2026-10-28", "2026-10-28", 0, "P0", "gate", ["A1", "A2", "A2-DEPLOY", "B1", "C1", "FE-04"],
    "Prove the spine works end to end before parallel feature work piles up. PM runs the check with the whole team.",
    T("Log in on staging as a seeded user", "Create a tender and upload a text PDF",
      "Job runs in the worker and the page shows succeeded", "CI and staging deploy are automatic",
      "If anything fails: open a P0 bug issue, assign it, and re-check next day"),
    T("All four checks pass on staging"), refs=T("build-plan G1"))

add("B2", "File extractors: PDF tables, XLSX/CSV, DOCX, OCR", "ai", "B2",
    "2026-10-27", "2026-10-29", 5, "P0", "feature", ["B1", "PM-03"],
    "Every supported file type turns into page- or sheet-numbered text/rows the LLM step can use.",
    T("Extractor registry keyed by sniffed MIME type", "pdfplumber tables for text PDFs",
      "openpyxl/pandas keep sheet name and row number", "python-docx paragraphs and tables",
      "Scanned pages → Document Intelligence Layout; Tesseract fallback (P2 if time is short)",
      "Record ocr_used and confidence on document_pages",
      "One fixture per file type in tests (small files, not the full samples)"),
    T("One fixture per file type parses with page or sheet numbers"),
    files=T("backend/app/processing/"), refs=T("build-plan B2", "US-03", "FR-11, FR-13, FR-14"))

add("C2", "BoQ editing + Decimal pricing", "data", "B2",
    "2026-10-26", "2026-10-29", 8, "P0", "feature", ["C1"],
    "Estimators edit BoQ lines and get totals that are correct to the cent.",
    T("`GET /tenders/{id}/boq` (lines + totals), `PATCH /boq-items/{id}`",
      "Edits change the live column, keep `original_*`, write a `field_revisions` row; status → corrected",
      "Material, labour, markup fields with org defaults (FR-27)",
      "`pricing.py`: pure Decimal functions, ROUND_HALF_UP to 2 places per line, VAT mode from org (ZAR 15% default)",
      "Totals use approved lines only; null quantity = missing, 0 = zero",
      "Flags for missing quantity/unit/price and outliers",
      "Unit tests first for pricing.py (VAT on/off, rounding edge cases, null vs zero)"),
    T("Pricing unit tests pass, VAT on and off", "Cross-tenant test for boq items"),
    files=T("backend/app/modules/boq/", "backend/app/modules/boq/pricing.py"),
    endpoints=T("GET /tenders/{id}/boq", "PATCH /boq-items/{id}"),
    refs=T("build-plan C2", "CLAUDE.md rules 3-5", "FR-25..FR-29"))

add("A3", "Document versions, stale items, 5-minute download links", "platform", "B2",
    "2026-10-29", "2026-10-31", 5, "P0", "feature", ["A2"],
    "Re-uploading keeps history, and old extracted items are marked stale so nobody approves against an outdated document.",
    T("Re-upload of the same document creates version n+1 and keeps older versions",
      "Mark items from the old version `stale` (call the review service from C3; stub until it lands)",
      "`GET /documents/{id}/download`: permission check, then 5-minute read-only SAS URL",
      "Tests: version 2 keeps version 1, expired link refused, other org 404"),
    T("Old versions kept; stale items flagged; download link expires after 5 min"),
    files=T("backend/app/modules/documents/service.py"),
    endpoints=T("GET /documents/{id}/download"), refs=T("build-plan A3", "US-02", "FR-09"))

add("C3", "Review state machine, requirements, tasks, checklist API", "data", "B2",
    "2026-10-30", "2026-11-02", 8, "P0", "feature", ["C2"],
    "Users approve, correct or reject extracted items, and requirements turn into an assignable checklist.",
    T("Review states extracted → corrected → approved | rejected; any → stale; only `approve()` sets approved (stamps user + time)",
      "Items flagged `no_source` cannot be approved", "`POST /tenders/{id}/boq/approve` (bulk approve)",
      "`GET /tenders/{id}/requirements`, `PATCH /requirements/{id}`: classify mandatory/conditional/optional, approve, assign (project manager can assign but not edit)",
      "`POST /tasks`, `PATCH /tasks/{id}`; `GET /tenders/{id}/checklist`",
      "Checklist response carries the compliance wording (extracted to support preparation, not a ruling)",
      "Audit events on approve/reject/assign"),
    T("Only approve() can set approved; illegal transitions return 422", "Cross-tenant tests for requirements and tasks"),
    files=T("backend/app/modules/checklist/", "backend/app/modules/boq/review.py"),
    endpoints=T("POST /tenders/{id}/boq/approve", "GET /tenders/{id}/requirements", "PATCH /requirements/{id}", "GET /tenders/{id}/checklist", "POST /tasks", "PATCH /tasks/{id}"),
    refs=T("build-plan C3", "US-05, US-06, US-07", "CLAUDE.md rule 6", "FR-20..FR-22, FR-43, FR-46"))

add("FE-05", "Settings: organisation defaults, members, usage", "pm", "B2",
    "2026-10-29", "2026-11-01", 3, "P1", "feature", ["FE-02", "A1"],
    "Admins manage their workspace without asking a developer.",
    T("Organisation page: name, registration number, default markup %, VAT mode (`GET/PATCH /organisation`)",
      "Members page: list, invite by email + role, change role / deactivate (admin only; hide for others)",
      "Usage page: pages processed and exports this month vs plan limit (`GET /usage`; stub until A4)"),
    T("Admin can invite a member and change the default markup"),
    files=T("frontend/src/app/settings/"), refs=T("FR-04, FR-47"), frontend=True)

add("PM-04", "Verified expected answers for the evaluation set", "pm", "B2",
    "2026-10-28", "2026-11-03", 3, "P0", "test", ["PM-03"],
    "The AI accuracy report needs a hand-checked answer key; without it B4 and B5 can't measure anything.",
    T("With the AI dev, agree the answer format (JSON matching the candidate schemas, see F3-A)",
      "For 10 documents: type out every BoQ line (item no, description, unit, quantity) and every requirement with its page number",
      "AI dev does the other 10 (target 20 documents total)",
      "Second person spot-checks 2 documents each",
      "Save as `samples/<pack>/expected.json`"),
    T("10 verified answer files committed and spot-checked"),
    files=T("samples/*/expected.json"), refs=T("build-plan B4", "spec 7.5"))

# ---------------------------------------------------------------- Batch 3 · 2–6 Nov
add("B3", "LLM extractors: BoQ, requirements, supplier quotes", "ai", "B3",
    "2026-10-30", "2026-11-03", 8, "P0", "feature", ["B2", "F3-A", "F4-AI"],
    "Turn extracted pages into reviewable candidate items with source pages. AI suggests, people approve.",
    T("`LLMClient` interface: Azure OpenAI + fallback provider, JSON-schema structured output, timeout + retry",
      "BoQ, requirement and quote-line extractors returning the frozen candidate schemas",
      "Spreadsheets mapped straight into BoqLineCandidate (no LLM)",
      "Page-chunked prompts; document text wrapped in delimiters and declared as data; only needed pages sent",
      "Output that fails Pydantic validation is rejected and the job fails with an error_code",
      "Worker saves items as `extracted` with source_document_id + source_page, replacing this job's previous candidates in the same transaction",
      "Record token usage per job"),
    T("Sample BoQ produces candidates with valid source pages", "Re-running a job does not duplicate items"),
    files=T("backend/app/ai/"), refs=T("build-plan B3", "US-04", "CLAUDE.md rule 9", "FR-17..FR-19, FR-24, FR-33"))

add("D2", "Review screen: source page beside extracted fields", "platform", "B3",
    "2026-10-31", "2026-11-04", 8, "P0", "feature", ["FE-03", "C3", "A3"],
    "Reviewers check each extracted value against the page it came from and approve or correct it without leaving the screen.",
    T("Split view: react-pdf renders the source page on the left (via the download link), fields on the right",
      "List of BoQ lines and requirements with status badges (extracted, corrected, approved, rejected, stale) and flags",
      "Click an item → jump to its source page", "Inline correct → PATCH; Approve / Reject buttons; bulk approve",
      "Items flagged no_source show why they can't be approved", "Keyboard: up/down to move, A to approve"),
    T("A reviewer approves a line without leaving the page"),
    files=T("frontend/src/app/tenders/[id]/review/"),
    refs=T("build-plan D2", "US-06", "FR-19, FR-20, FR-25, FR-26"), frontend=True,
    stub_ok=T("C3"))

add("FE-06", "Checklist screen: requirements, assignees, due dates, tasks", "pm", "B3",
    "2026-11-02", "2026-11-05", 5, "P0", "feature", ["FE-03", "C3"],
    "The team sees every requirement still needing action, who owns it and when it's due.",
    T("Checklist table: requirement, mandatory/conditional/optional, source page link, review status, assignee, due date, status",
      "Filters: mandatory only, unassigned, overdue", "Assign a member and set a due date inline",
      "Tasks list per tender: create, assign, change status",
      "Fixed disclaimer banner: extracted to support preparation, not a ruling that the bid complies"),
    T("Assign a requirement and mark a task done; disclaimer visible"),
    files=T("frontend/src/app/tenders/[id]/checklist/"),
    refs=T("build-plan D4", "US-05, US-07", "CLAUDE.md rule 13", "FR-22, FR-23, FR-43, FR-46"), frontend=True)

add("C4-MATCH", "Supplier matcher: fuzzy text + units + spec tokens", "ai", "B3",
    "2026-11-03", "2026-11-04", 5, "P0", "feature", ["C2", "F3-A"],
    "Suggest which supplier quote line matches each BoQ line, with evidence, and never pick the cheapest automatically.",
    T("Pure function `match(boq_lines, quote_lines) -> suggestions` in `app/modules/suppliers/matcher.py`",
      "rapidfuzz text score + unit normalisation (m, metre, lm; each, no, ea) + spec tokens (mm², cores, A rating, IP rating)",
      "Evidence per suggestion: text score, unit match, spec match/conflict, price, quote validity",
      "Low score or unit/spec conflict → stays `suggested` and flagged",
      "Unit tests with real cable/DB-board/luminaire lines from the samples"),
    T("Unit mismatch flagged; table-driven tests pass"),
    files=T("backend/app/modules/suppliers/matcher.py"),
    refs=T("build-plan C4", "CLAUDE.md rule 10", "FR-34, FR-36, FR-37"))

add("C4-API", "Suppliers, quotations, comparisons and match confirm API", "data", "B3",
    "2026-11-03", "2026-11-04", 5, "P0", "feature", ["C2", "C3", "B3"],
    "Estimators record suppliers, upload quotes and confirm or reject matches; only confirmed matches feed prices.",
    T("`POST/GET /suppliers`", "`POST /quotations` (links an uploaded document; quote lines come from the B3 quote extractor)",
      "Run the matcher (C4-MATCH) and store `quote_matches` with evidence",
      "`GET /tenders/{id}/comparisons`: per BoQ line, all supplier options side by side",
      "`PATCH /matches/{id}` confirm/reject; one confirmed match per line; confirmed price feeds the BoQ unit cost",
      "Cross-tenant tests"),
    T("Unconfirmed matches excluded from totals", "Org B gets 404 on Org A suppliers/quotes"),
    files=T("backend/app/modules/suppliers/"),
    endpoints=T("POST /suppliers", "GET /suppliers", "POST /quotations", "GET /tenders/{id}/comparisons", "PATCH /matches/{id}"),
    refs=T("build-plan C4", "FR-31, FR-32, FR-35"))

add("B4", "Validators + evaluation harness", "ai", "B3",
    "2026-11-04", "2026-11-06", 5, "P0", "test", ["B3", "PM-04"],
    "Catch bad extractions with rules, and measure accuracy against the answer key.",
    T("`ai/validators.py`: unit present, numeric quantity, null vs zero, outliers, disqualifier keywords, low OCR confidence, missing source → flags",
      "`tests/ai_eval/eval.py`: field accuracy, precision and recall for BoQ lines and requirements, cost per document",
      "Prompt-injection fixture (document says 'ignore instructions…') must not change behaviour",
      "Run against the 20 verified documents"),
    T("Eval script prints a metrics table"),
    files=T("backend/app/ai/validators.py", "backend/tests/ai_eval/"),
    refs=T("build-plan B4", "FR-17, FR-29"))

add("D3", "BoQ editor screen", "data", "B3",
    "2026-11-04", "2026-11-06", 8, "P0", "feature", ["FE-03", "C2", "C3"],
    "Estimators price the BoQ in a spreadsheet-like table; totals always come from the server.",
    T("TanStack Table with inline editing for quantity, unit, material, labour, markup",
      "Missing quantity shown differently from 0", "Flags highlighted; filter by review status",
      "Original value shown on hover when a field was corrected",
      "Totals panel (subtotal, VAT, total) refreshed from `GET /tenders/{id}/boq` after each save, never computed in the browser"),
    T("Edits save and totals refresh from the server"),
    files=T("frontend/src/app/tenders/[id]/boq/"),
    refs=T("build-plan D3", "FR-25, FR-27..FR-29"), frontend=True)

add("A4", "Audit trail, usage limits, rate limits", "platform", "B3",
    "2026-11-04", "2026-11-05", 5, "P0", "feature", ["A1", "A2"],
    "Every important action is recorded, and plan limits stop over-use before a job is queued.",
    T("Audit rows for login, uploads, edits, approvals, exports (ids and action only, no document text)",
      "`usage_counters` per org per month; plan limits checked before a job is queued → 402",
      "slowapi limits on login and upload → 429", "`GET /audit` (admin), `GET /usage`"),
    T("Over-limit upload returns 402; 6th login in a minute returns 429"),
    files=T("backend/app/modules/audit/", "backend/app/modules/usage/"),
    endpoints=T("GET /audit", "GET /usage"), refs=T("build-plan A4", "FR-42, FR-47..FR-49"))

add("A5", "Cross-tenant security suite", "platform", "B3",
    "2026-11-05", "2026-11-06", 3, "P0", "test", ["A3", "C3", "C4-API"],
    "Prove that one company can never see another's data.",
    T("Parametrised test: for every resource endpoint, Org A token + Org B id → 404",
      "Downloads and exports included", "Run in CI"),
    T("Org A gets 404 on every Org B id"),
    files=T("backend/tests/security/"), refs=T("build-plan A5", "FR-05"))

add("A5-NOTIFY", "Notifications + daily deadline reminders", "pm", "B3",
    "2026-11-05", "2026-11-06", 3, "P1", "feature", ["C3"],
    "People get reminded about closing dates, requirement due dates and tasks.",
    T("Daily job (worker command or scheduled Container Apps Job) creates notifications for tenders closing in 3 days and items due tomorrow / overdue",
      "`GET /notifications`, mark as read", "Email only if configured (P2)"),
    T("Seeded overdue task produces a notification"),
    files=T("backend/app/modules/notifications/"), endpoints=T("GET /notifications"),
    refs=T("build-plan A5", "US-07", "FR-44, FR-45"))

add("FE-COMPARE", "Supplier comparison screen", "ai", "B3",
    "2026-11-06", "2026-11-07", 5, "P0", "feature", ["FE-03", "C4-API"],
    "Estimators compare supplier options per BoQ line with the evidence and confirm the right one.",
    T("Suppliers page: list/create suppliers; upload a quotation for a tender",
      "Comparison table per BoQ line: each supplier's description, unit, spec, price, validity, score",
      "Highlight unit/spec conflicts and expired quotes", "Confirm / Reject buttons; no 'pick cheapest' button"),
    T("Confirm a match and see the BoQ price update"),
    files=T("frontend/src/app/tenders/[id]/suppliers/", "frontend/src/app/suppliers/"),
    refs=T("build-plan D4", "FR-34..FR-37"), frontend=True)

add("G2", "GATE G2 · Core loop works on a real tender pack (Fri 6 Nov)", "pm", "B3",
    "2026-11-06", "2026-11-06", 0, "P0", "gate",
    ["A3", "A4", "A5", "B2", "B3", "B4", "C2", "C3", "C4-API", "C4-MATCH", "D2", "D3", "FE-06"],
    "The MVP loop works on staging. Anything not done by now gets cut or simplified.",
    T("Real electrical tender pack in", "BoQ and requirements extracted with source pages",
      "Reviewed, corrected and approved in the UI", "Quotes matched and confirmed; totals correct to the cent",
      "Org A cannot see Org B", "PM: move any unfinished P1/P2 issues out or cut them"),
    T("All checks pass on staging"), refs=T("build-plan G2"))

# ---------------------------------------------------------------- Batch 4 · 7–10 Nov
add("C5", "Excel export of approved BoQ + exports API", "data", "B4",
    "2026-11-07", "2026-11-08", 5, "P0", "feature", ["C3"],
    "Contractors take the approved estimate into their own spreadsheet.",
    T("`POST /tenders/{id}/exports` (kind, draft or final), `GET /exports/{id}/download` (SAS link)",
      "openpyxl write-only: approved rows only, version, generation date, source document + page column, totals",
      "Draft exports watermarked 'DRAFT', include unapproved rows marked as such",
      "Compliance register sheet with the disclaimer", "`exports` row + audit event per export"),
    T("Export of 2,000 lines in under 10 seconds", "Final export contains approved rows only"),
    files=T("backend/app/modules/exports/"),
    endpoints=T("POST /tenders/{id}/exports", "GET /exports/{id}/download"),
    refs=T("build-plan C5", "US-08", "FR-30, FR-38, FR-40..FR-42"))

add("C5-PDF", "Checklist PDF export with disclaimer", "data", "B4",
    "2026-11-09", "2026-11-09", 3, "P1", "feature", ["C5"],
    "A printable compliance checklist the team can sign off.",
    T("HTML template (Jinja) for the checklist: tender details, requirement, classification, source page, assignee, status",
      "Render with WeasyPrint (add its system libraries to the Dockerfile)",
      "Fixed disclaimer and generation date in the footer; 'DRAFT' watermark for drafts",
      "Plug into the exports service from C5 as kind `checklist_pdf`"),
    T("PDF downloads with disclaimer and source pages"),
    files=T("backend/app/modules/exports/templates/checklist.html"),
    refs=T("build-plan C5", "US-08", "FR-23, FR-39"))

add("FE-07", "Exports screen, notifications bell, audit page", "pm", "B4",
    "2026-11-07", "2026-11-08", 3, "P1", "feature", ["C5", "A4", "A5-NOTIFY"],
    "Finish the remaining small screens so every MVP feature is reachable from navigation.",
    T("Exports tab: Generate Excel (draft/final), Checklist PDF; list of past exports with version, date, who, download",
      "Notifications bell in the top bar with unread count", "Audit log page (admin only) with filters",
      "Empty, loading and error states on every page you own"),
    T("Every MVP screen reachable from navigation"),
    files=T("frontend/src/app/tenders/[id]/exports/", "frontend/src/app/settings/audit/"),
    refs=T("build-plan D4, D5", "FR-41, FR-42"), frontend=True, stub_ok=T("C5"))

add("B5", "AI accuracy report", "ai", "B4",
    "2026-11-07", "2026-11-09", 3, "P0", "docs", ["B4"],
    "The written evidence that the extraction works, and where it doesn't.",
    T("Run eval on the final 20-document set", "Metrics per field and per file type; cost per document",
      "Failure analysis with examples; prompt-injection result", "Write `docs/ai-evaluation.md` (spec section 7.5)"),
    T("Report covers every metric in spec 7.5"),
    files=T("docs/ai-evaluation.md"), refs=T("build-plan B5"))

add("A6", "Hardening + production deploy", "platform", "B4",
    "2026-11-07", "2026-11-09", 5, "P0", "infra", ["A3", "A4", "A5"],
    "Production is live, safe and recoverable.",
    T("Security tests: id guessing, upload abuse (fake extension, zip bomb, oversize), rate limits",
      "`deploy-prod.yml` with manual approval and a smoke test", "Application Insights error alerts",
      "Backup restore drill on Postgres, timed and written up", "`docs/security.md` incl. POPIA notes"),
    T("Production live; restore drill documented"),
    files=T(".github/workflows/deploy-prod.yml", "docs/security.md"), refs=T("build-plan A6"))

add("E2E", "Playwright end-to-end happy path", "pm", "B4",
    "2026-11-08", "2026-11-09", 3, "P1", "test", ["FE-07", "D2", "D3", "FE-06"],
    "One automated test that proves the whole MVP still works before we submit.",
    T("Playwright test: log in → create tender → upload sample PDF → wait for succeeded → approve a line → export Excel",
      "Use `npx playwright codegen` against staging to record it, then tidy",
      "Run in CI against staging after deploy"),
    T("E2E suite green against staging"),
    files=T("frontend/tests/e2e/"), refs=T("build-plan D5"), frontend=True)

add("G3", "GATE G3 · Release candidate (Mon 9 Nov)", "pm", "B4",
    "2026-11-09", "2026-11-09", 0, "P0", "gate", ["A6", "B5", "C5", "E2E"],
    "Code freeze. From here only bug fixes, docs and the demo.",
    T("Production deployed with approval", "Approved Excel (and checklist PDF if done) export",
      "Security tests and E2E green", "Restore drill done"),
    T("All checks pass in production"), refs=T("build-plan G3"))

add("PM-05", "Mini pilot with 3–5 testers", "pm", "B4",
    "2026-11-08", "2026-11-09", 1, "P1", "test", ["G2"],
    "Real users try it once so the report can quote correction rate and time saved.",
    T("Onboard 3–5 testers (permissioned documents only)", "Measure correction rate (edits per extracted item) and rough time saved",
      "Collect 3 quotes/feedback points for the documentation"),
    T("Pilot results table in docs"), refs=T("build-plan P1"))

add("PM-06", "Final documentation, demo rehearsal and submission (Tue 10 Nov)", "pm", "B4",
    "2026-11-09", "2026-11-10", 2, "P0", "docs", ["G3", "B5"],
    "Hand in on time with everything the brief asks for.",
    T("Final documentation: cover page, group name, names and student numbers, architecture, AI evaluation, security, pilot results",
      "README: what it is, live link, how to run locally, demo accounts",
      "Rehearse the 10-minute demo twice (script + backup recording)",
      "Submit repo link, docs and live link by Tue 10 Nov"),
    T("Submitted by 10 Nov"), files=T("docs/", "README.md"), refs=T("build-plan P1"))


# ---------------------------------------------------------------- starter kit adjustments
# The repo ships a starter kit (compose, CI, schema + migration 001, seed, stub routers for
# every endpoint, Next.js shell). Foundation issues become "review, own and finish" tasks.
STARTER = "**Starter kit provided.** The skeleton for this is already in the repo; your job is to review it, own it and finish what's listed below.\n\n"
OVERRIDES = {
    "F1": dict(title="Own the starter repo: Compose, CI, Docker image on every laptop", points=2,
        goal=STARTER + "Every developer runs the same stack with one command, and every PR is checked automatically.",
        tasks=T("Run `make up` on all four laptops (Windows, Mac, Linux); fix anything that breaks and document it in README",
                "Confirm `docker compose up` serves http://localhost:8000/docs and http://localhost:3000",
                "Make CI required on `main` and `dev` (branch protection) once the first PR is green",
                "Add Dependabot (pip + npm) and a `pip-audit` / `npm audit` CI step",
                "Read `backend/app/core/` end to end so you can answer questions about it")),
    "F2": dict(title="Review and own the schema: 20 tables, migration 001, seed", points=3,
        goal=STARTER + "Lock the data model everyone builds on before the freeze on Fri 23 Oct.",
        tasks=T("Walk the team through `backend/app/core/models/` and `docs/erd.md` (30 min)",
                "Check every table and enum against the spec (section 6) and docs/architecture.md; list gaps",
                "Before the freeze you may edit `001_initial.py` directly; after Fri 23 Oct only new migrations",
                "Check `scripts/seed.py` covers what C1/A1 tests need; extend if not",
                "Regenerate `docs/erd.md` (`make erd`) after any change",
                "Keep `tests/security/test_org_scoped_repository.py` as the template everyone copies")),
    "F3-P": dict(title="Review platform API contracts: auth, documents, jobs, audit, usage, notifications", points=2,
        goal=STARTER + "Stub routers already return example data for every endpoint. Make sure the shapes are right before the freeze.",
        tasks=T("Review schemas in `app/modules/{auth,documents,jobs,audit,usage,notifications,organisation}/schemas.py`",
                "Check the role on every stub matches the role matrix in docs/architecture.md",
                "Add request-id middleware (header `X-Request-ID`, logged with every line)",
                "`make openapi` and commit `docs/openapi.json` + regenerated frontend client")),
    "F3-D": dict(title="Review estimating API contracts: tenders, BoQ, checklist, suppliers, exports", points=2,
        goal=STARTER + "Freeze the shape of the estimating endpoints so the frontend can build screens in parallel.",
        tasks=T("Review schemas in `app/modules/{tenders,boq,checklist,suppliers,exports}/schemas.py`",
                "Money and quantities stay strings (DecimalStr), never floats",
                "Adjust example data so it looks like a real electrical BoQ",
                "`make openapi` and commit")),
    "F3-A": dict(title="Review candidate JSON schemas + job status contract", points=1,
        goal=STARTER + "Fix the exact shape the AI returns, so review and matching can be built before the extractors work.",
        tasks=T("Review `backend/app/ai/schemas.py` against 2 real sample BoQs and RFQs; add missing fields",
                "Write `docs/jobs.md`: job statuses, error_code list, retry rules",
                "Extend `tests/unit/test_candidate_schemas.py`")),
    "FE-01": dict(title="Polish the app shell: shadcn/ui, top bar, user menu", points=2,
        goal=STARTER + "Layout, nav, typed API client and placeholder pages exist. Make the shell look and feel finished.",
        tasks=T("Add shadcn/ui (button, input, table, badge, dialog, toast) and use it in the shell",
                "Top bar: tender search box, notifications bell (placeholder), user menu with logout",
                "Responsive sidebar (collapses on phone width)",
                "Shared `StatusBadge` component for extracted / corrected / approved / rejected / stale")),
    "PM-01": dict(tasks=T("Run `planning/create_issues.py` to create labels, milestones and all issues",
                "Create a GitHub Project (board view) with columns Backlog / This week / In progress / In review / Done; add every issue; group by milestone",
                "Add Start date and Due date fields to the Project and copy the dates from each issue",
                "Create `dev` branch; protect `main` and `dev` (PR required, 1 approval, CI must pass)",
                "Agree working rules in README: branch per issue `feat/<key>-short-name`, PR into `dev`, squash merge",
                "Book a 15-min daily stand-up and a weekly batch review (Sundays)")),
}
for i in issues:
    o = OVERRIDES.get(i["key"], {})
    if "title" in o:
        i["title"] = f"[{i['key']}] {o['title']}"
    for f in ("goal", "tasks"):
        if f in o:
            i[f] = o[f]
    if "points" in o:
        i["points"] = o["points"]
        i["labels"] = [l for l in i["labels"] if not l.startswith("pts:")] + [f"pts:{o['points']}"]
    i["files"] = [f.replace("frontend/src/app/tenders/[id]/", "frontend/src/app/(app)/tenders/view/")
                   .replace("frontend/src/app/tenders/", "frontend/src/app/(app)/tenders/")
                   .replace("frontend/src/app/dashboard/", "frontend/src/app/(app)/dashboard/")
                   .replace("frontend/src/app/settings/", "frontend/src/app/(app)/settings/")
                   .replace("frontend/src/app/suppliers/", "frontend/src/app/(app)/suppliers/")
                  for f in i["files"]]
    if i["endpoints"] and i["key"] not in OVERRIDES:
        mods = sorted({f.split("/modules/")[1].split("/")[0] for f in i["files"] if "/modules/" in f})
        where = ", ".join(f"`app/modules/{m}/router.py`" for m in mods) or "the module router"
        i["tasks"] = [f"Replace the stub in {where} with router → service → repository; keep the response schema (frozen contract) and add a cross-tenant test"] + i["tasks"]
    if any("frontend/src/app/(app)" in f or "frontend/src/app/(auth)" in f for f in i["files"]):
        i["tasks"] = ["Replace the `<Placeholder>` page; call the API only through `src/api/client.ts`"] + i["tasks"]

NON_CODE = {"PM-01", "PM-02", "PM-03", "PM-04", "PM-05", "PM-06", "F4-AI", "G1", "G2", "G3", "B5"}
for i in issues:
    i["code"] = i["key"] not in NON_CODE

# ------------------------------------------------------------------- checks
keys = {i["key"] for i in issues}
order = {i["key"]: n for n, i in enumerate(issues)}
for i in issues:
    for d in i["depends_on"]:
        assert d in keys, (i["key"], d)
        assert order[d] < order[i["key"]], f"{i['key']} listed before its dependency {d}"

doc = {
    "repo": "lethaboGS/CoTender",
    "team": {
        "pm": "griffiths34",
        "platform": "lethaboGS",
        "ai": "S-iba",
        "data": "SIYABULELA11",
    },
    "milestones": milestones,
    "labels": [{"name": n, "color": c, "description": d} for n, c, d in labels],
    "issues": issues,
}
json.dump(doc, open(sys.argv[1], "w", encoding="utf-8"), indent=2, ensure_ascii=False)

from collections import defaultdict
pts = defaultdict(int)
for i in issues:
    pts[i["owner"]] += i["points"]
print(len(issues), "issues", dict(pts))
