# CoTender (IntelTPS)

Tender preparation for electrical subcontractors in South Africa: upload a tender pack, let the
system extract BoQ lines and requirements with page references, review and approve them, price
with exact decimals, compare supplier quotes, track a compliance checklist and export to Excel.
**AI suggests, people approve.**

Due **Tue 10 Nov 2026**. The plan, owners and dates are in [`planning/PLAN.md`](planning/PLAN.md);
the rules every PR follows are in [`CLAUDE.md`](CLAUDE.md).

## Run it locally

Needs Docker Desktop.

```bash
make up        # copies .env.example to .env, starts postgres, azurite, api, worker, frontend
make migrate   # create the 20 tables
make seed      # demo org, one user per role, one tender (password DemoPass123!)
make test      # backend tests against Postgres
```

- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

No `make`? Use the commands inside the [`Makefile`](Makefile) directly, e.g.
`docker compose exec api alembic upgrade head`.

## What's in the starter kit and what isn't

The repo starts with a **skeleton so nobody waits on anybody**. The real features are the
team's work, tracked as GitHub issues.

| Ready to build on | Still to build (see issues) |
| --- | --- |
| Docker Compose stack, CI (lint, types, tests, build), one Docker image | Azure + deploy pipelines (F4-P, A2-DEPLOY, A6) |
| All 20 tables, enums, Decimal columns, migration 001, seed | Real login with JWT cookies (A1); stub treats everyone as demo admin |
| `OrgScopedRepository` + cross-tenant test template | Every service and repository except the tenders template |
| Every endpoint in CLAUDE.md as a **stub** returning example data | Upload, worker, extractors, LLM, matching, pricing, review, exports |
| Candidate schemas the AI must return (`app/ai/schemas.py`) | Validators and the evaluation set |
| Next.js shell, nav, typed API client, a placeholder page per screen | Every screen marked "To build in issue …" |

Search the code for `TODO(` to find where each issue starts, e.g. `TODO(C2)`.

## How we work

See [CONTRIBUTING.md](CONTRIBUTING.md): branch per issue, pull request, green CI, squash merge. `main` is protected.

## Layout

```
backend/   FastAPI app, worker, Alembic, tests   (app/core, app/modules/<module>, app/ai, app/processing)
frontend/  Next.js (App Router, TypeScript, Tailwind), static export
docs/      spec, architecture, build plan, user stories, openapi.json, erd.md
planning/  plan, issue list and the script that creates the GitHub issues
infra/     Azure scripts (to come) and local Postgres init
samples/   tender packs and verified answers (to come, PM-03)
```
