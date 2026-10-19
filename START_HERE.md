# Start here

1. Unzip this folder into your empty repo folder (so `CLAUDE.md` sits at the repo root).
2. Open a terminal there and run `claude`. Claude Code reads `CLAUDE.md` automatically.
3. Paste the first prompt below.

## First prompt (foundation F1 + F2)

```
Read CLAUDE.md, docs/build-plan.md (blocks F1 and F2) and docs/architecture.md.
Scaffold the foundation:
- F1: monorepo layout from CLAUDE.md, backend/Dockerfile, docker-compose.yml (postgres 16, azurite, api, worker, frontend), .env.example, Makefile, and .github/workflows/ci.yml (ruff, mypy, pytest with a postgres service, Next.js build).
- F2: SQLAlchemy 2.0 models for all 20 tables with the enums, numeric precisions, UUID keys and (organisation_id, tender_id) indexes from the rules; Alembic init and 001_initial migration; scripts/seed.py with a demo org, one user per role and one tender.
- Add OrgScopedRepository in app/core and one cross-tenant test that proves it.
Stop when `docker compose up` serves /health, `alembic upgrade head` runs on an empty database, and pytest passes. Show me the file tree and anything you were unsure about.
```

## Next prompts

- F3 contracts: "Do block F3 from docs/build-plan.md: Pydantic schemas for every module, stubbed routers returning examples, the standard error handler, ai/schemas.py candidate models, export docs/openapi.json."
- Then one block at a time from your own lane, e.g. "Do block C2 from docs/build-plan.md. Write tests first for pricing.py."

## Docs in this pack

- `CLAUDE.md`: project context and rules Claude Code follows
- `docs/build-plan.md`: every build block with files, endpoints, dependencies and done checks
- `docs/architecture.md`: modules, FR traceability, API role matrix, ERD, NFRs, business rules, processing sequence
- `docs/user-stories.md`: US-01 to US-08 with acceptance criteria and a sample compliance register
- `docs/visuals/*.html`: the three interactive pages; open in a browser
- `docs/spec/IntelTPS_spec.pdf`: the original brief
