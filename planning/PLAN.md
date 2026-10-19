# CoTender delivery plan (19 Oct to 10 Nov 2026)

Generated from `planning/issues.json` (built by `planning/build_issues.py`). Edit `build_issues.py`, not this file. `planning/create_issues.py` turns it into GitHub labels, milestones and issues.

## Team and lanes

| Lane | GitHub | Owns | Points |
| --- | --- | --- | --- |
| PM + light frontend | @griffiths34 | Board, Azure account, samples + answer key, app shell, auth/tenders/upload/settings/checklist screens, notifications, E2E, pilot, docs, demo | 37 |
| Platform & security | @CHANGE_ME_platform_dev | Repo/compose/CI, API core + auth, uploads + storage, versions, audit/limits, review screen, security tests, staging + prod deploy | 49 |
| AI & processing | @CHANGE_ME_ai_dev | LLM day-1 check, candidate schemas, worker + queue, extractors + OCR, LLM extraction, matcher, validators + eval, comparison screen, AI report | 39 |
| Estimating & data | @CHANGE_ME_data_dev | Schema + migrations + seed, estimating contracts, tenders, BoQ + Decimal pricing, review/checklist API, suppliers API, BoQ editor, exports | 47 |

1 point ≈ half a day. The PM's coding is the simplest work in the plan: forms, lists and tables against the frozen API contracts, plus a pattern-copy notifications module. Everything on the critical path sits with the three developers.

## Key dates

- **Fri 23 Oct**: Contracts frozen: DB schema, OpenAPI, candidate JSON, job statuses. After this only additive changes and new migrations.
- **Wed 28 Oct**: **Gate G1**: log in, create tender, upload, worker finishes, all on staging
- **Fri 6 Nov**: **Gate G2**: real tender pack to approved, priced data with confirmed supplier matches
- **Mon 9 Nov**: **Gate G3**: production release candidate, code freeze
- **Tue 10 Nov**: **Submission**

## Critical path

F1 → F3-P → A1 → A2 → A2-DEPLOY → **G1** → (B2 → B3 → B4) ‖ (C2 → C3 → D3 / C4-API) ‖ (A3 → D2) → **G2** → C5 / A6 / E2E → **G3** → submit

If F1 slips, everyone slips. Platform does F1 first, with nothing else on 19–20 Oct. Data starts F2 locally on day 1 and connects it to compose once F1 merges.

## Batch 1 · Foundation (19–25 Oct)

Repo, compose, CI, schema, contracts, Azure, auth, worker skeleton, tenders API, app shell. Contracts frozen Fri 23 Oct.

| Who | Issue | Dates | Pts | Pri | Blocked by |
| --- | --- | --- | --- | --- | --- |
| @griffiths34 | [PM-01] Set up project board, branch protection and PR template | Mon 19 Oct → Mon 19 Oct | 1 | P0 | none |
| @griffiths34 | [PM-02] Azure for Students subscription, team access and budget alerts | Mon 19 Oct → Tue 20 Oct | 1 | P0 | none |
| @griffiths34 | [PM-03] Collect 3+ real electrical tender packs into samples/ | Mon 19 Oct → Fri 23 Oct | 2 | P0 | none |
| @griffiths34 | [FE-01] Polish the app shell: shadcn/ui, top bar, user menu | Thu 22 Oct → Fri 23 Oct | 2 | P0 | F1, F3-P |
| @griffiths34 | [FE-02] Login and register pages + auth guard | Sat 24 Oct → Mon 26 Oct | 3 | P0 | FE-01, A1* |
| @CHANGE_ME_platform_dev | [F1] Own the starter repo: Compose, CI, Docker image on every laptop | Mon 19 Oct → Tue 20 Oct | 2 | P0 | none |
| @CHANGE_ME_platform_dev | [F3-P] Review platform API contracts: auth, documents, jobs, audit, usage, notifications | Wed 21 Oct → Thu 22 Oct | 2 | P0 | F1, F2 |
| @CHANGE_ME_platform_dev | [F4-P] Azure infrastructure + GitHub OIDC | Thu 22 Oct → Fri 23 Oct | 3 | P0 | F1, PM-02 |
| @CHANGE_ME_platform_dev | [A1] Core + auth: register, login, logout, me, roles, audit hook | Fri 23 Oct → Mon 26 Oct | 8 | P0 | F2, F3-P |
| @CHANGE_ME_ai_dev | [F4-AI] Day-1 check: Azure OpenAI quota, Document Intelligence, fallback LLM | Mon 19 Oct → Tue 20 Oct | 2 | P0 | none |
| @CHANGE_ME_ai_dev | [F3-A] Review candidate JSON schemas + job status contract | Wed 21 Oct → Wed 21 Oct | 1 | P0 | F1 |
| @CHANGE_ME_ai_dev | [B1] Queue + worker skeleton + job endpoints | Thu 22 Oct → Mon 26 Oct | 5 | P0 | F1, F2, F3-A |
| @CHANGE_ME_data_dev | [F2] Review and own the schema: 20 tables, migration 001, seed | Mon 19 Oct → Wed 21 Oct | 3 | P0 | F1* |
| @CHANGE_ME_data_dev | [F3-D] Review estimating API contracts: tenders, BoQ, checklist, suppliers, exports | Thu 22 Oct → Thu 22 Oct | 2 | P0 | F2, F3-P |
| @CHANGE_ME_data_dev | [C1] Tenders API + dashboard | Fri 23 Oct → Sun 25 Oct | 5 | P0 | F2, F3-D |

## Batch 2 · Walking skeleton + core features (26 Oct–1 Nov)

Upload end to end on staging (Gate G1, Wed 28 Oct), extractors, BoQ pricing, review state machine, versions.

| Who | Issue | Dates | Pts | Pri | Blocked by |
| --- | --- | --- | --- | --- | --- |
| @griffiths34 | [FE-03] Tenders list, create form, tender workspace, dashboard countdown | Mon 26 Oct → Tue 27 Oct | 3 | P0 | FE-02, C1 |
| @griffiths34 | [FE-04] Upload widget + job status polling | Tue 27 Oct → Wed 28 Oct | 2 | P0 | FE-03, A2, B1 |
| @griffiths34 | [G1] GATE G1 · Walking skeleton on staging (Wed 28 Oct) | Wed 28 Oct → Wed 28 Oct | · | P0 | A1, A2, A2-DEPLOY, B1, C1, FE-04 |
| @griffiths34 | [PM-04] Verified expected answers for the evaluation set | Wed 28 Oct → Tue 3 Nov | 3 | P0 | PM-03 |
| @griffiths34 | [FE-05] Settings: organisation defaults, members, usage | Thu 29 Oct → Sun 1 Nov | 3 | P1 | FE-02, A1 |
| @CHANGE_ME_platform_dev | [A2] Upload endpoint: sniff, Blob storage, job + queue, 202 | Mon 26 Oct → Tue 27 Oct | 5 | P0 | A1, B1, F4-P |
| @CHANGE_ME_platform_dev | [A2-DEPLOY] Staging deploy pipeline | Tue 27 Oct → Wed 28 Oct | 3 | P0 | F4-P, A2 |
| @CHANGE_ME_platform_dev | [A3] Document versions, stale items, 5-minute download links | Thu 29 Oct → Sat 31 Oct | 5 | P0 | A2 |
| @CHANGE_ME_ai_dev | [B2] File extractors: PDF tables, XLSX/CSV, DOCX, OCR | Tue 27 Oct → Thu 29 Oct | 5 | P0 | B1, PM-03 |
| @CHANGE_ME_data_dev | [C2] BoQ editing + Decimal pricing | Mon 26 Oct → Thu 29 Oct | 8 | P0 | C1 |
| @CHANGE_ME_data_dev | [C3] Review state machine, requirements, tasks, checklist API | Fri 30 Oct → Mon 2 Nov | 8 | P0 | C2 |

## Batch 3 · Full MVP loop (2–6 Nov)

LLM extraction, matching, review screen, BoQ editor, checklist, validators. Gate G2 Fri 6 Nov: real tender pack to approved priced data.

| Who | Issue | Dates | Pts | Pri | Blocked by |
| --- | --- | --- | --- | --- | --- |
| @griffiths34 | [FE-06] Checklist screen: requirements, assignees, due dates, tasks | Mon 2 Nov → Thu 5 Nov | 5 | P0 | FE-03, C3 |
| @griffiths34 | [A5-NOTIFY] Notifications + daily deadline reminders | Thu 5 Nov → Fri 6 Nov | 3 | P1 | C3 |
| @griffiths34 | [G2] GATE G2 · Core loop works on a real tender pack (Fri 6 Nov) | Fri 6 Nov → Fri 6 Nov | · | P0 | A3, A4, A5, B2, B3, B4, C2, C3, C4-API, C4-MATCH, D2, D3, FE-06 |
| @CHANGE_ME_platform_dev | [D2] Review screen: source page beside extracted fields | Sat 31 Oct → Wed 4 Nov | 8 | P0 | FE-03, C3*, A3 |
| @CHANGE_ME_platform_dev | [A4] Audit trail, usage limits, rate limits | Wed 4 Nov → Thu 5 Nov | 5 | P0 | A1, A2 |
| @CHANGE_ME_platform_dev | [A5] Cross-tenant security suite | Thu 5 Nov → Fri 6 Nov | 3 | P0 | A3, C3, C4-API |
| @CHANGE_ME_ai_dev | [B3] LLM extractors: BoQ, requirements, supplier quotes | Fri 30 Oct → Tue 3 Nov | 8 | P0 | B2, F3-A, F4-AI |
| @CHANGE_ME_ai_dev | [C4-MATCH] Supplier matcher: fuzzy text + units + spec tokens | Tue 3 Nov → Wed 4 Nov | 5 | P0 | C2, F3-A |
| @CHANGE_ME_ai_dev | [B4] Validators + evaluation harness | Wed 4 Nov → Fri 6 Nov | 5 | P0 | B3, PM-04 |
| @CHANGE_ME_ai_dev | [FE-COMPARE] Supplier comparison screen | Fri 6 Nov → Sat 7 Nov | 5 | P0 | FE-03, C4-API |
| @CHANGE_ME_data_dev | [C4-API] Suppliers, quotations, comparisons and match confirm API | Tue 3 Nov → Wed 4 Nov | 5 | P0 | C2, C3, B3 |
| @CHANGE_ME_data_dev | [D3] BoQ editor screen | Wed 4 Nov → Fri 6 Nov | 8 | P0 | FE-03, C2, C3 |

## Batch 4 · Release + submit (7–10 Nov)

Exports, hardening, prod deploy, E2E, AI report, docs, demo. Gate G3 Mon 9 Nov. Submit Tue 10 Nov.

| Who | Issue | Dates | Pts | Pri | Blocked by |
| --- | --- | --- | --- | --- | --- |
| @griffiths34 | [FE-07] Exports screen, notifications bell, audit page | Sat 7 Nov → Sun 8 Nov | 3 | P1 | C5*, A4, A5-NOTIFY |
| @griffiths34 | [E2E] Playwright end-to-end happy path | Sun 8 Nov → Mon 9 Nov | 3 | P1 | FE-07, D2, D3, FE-06 |
| @griffiths34 | [PM-05] Mini pilot with 3–5 testers | Sun 8 Nov → Mon 9 Nov | 1 | P1 | G2 |
| @griffiths34 | [G3] GATE G3 · Release candidate (Mon 9 Nov) | Mon 9 Nov → Mon 9 Nov | · | P0 | A6, B5, C5, E2E |
| @griffiths34 | [PM-06] Final documentation, demo rehearsal and submission (Tue 10 Nov) | Mon 9 Nov → Tue 10 Nov | 2 | P0 | G3, B5 |
| @CHANGE_ME_platform_dev | [A6] Hardening + production deploy | Sat 7 Nov → Mon 9 Nov | 5 | P0 | A3, A4, A5 |
| @CHANGE_ME_ai_dev | [B5] AI accuracy report | Sat 7 Nov → Mon 9 Nov | 3 | P0 | B4 |
| @CHANGE_ME_data_dev | [C5] Excel export of approved BoQ + exports API | Sat 7 Nov → Sun 8 Nov | 5 | P0 | C3 |
| @CHANGE_ME_data_dev | [C5-PDF] Checklist PDF export with disclaimer | Mon 9 Nov → Mon 9 Nov | 3 | P1 | C5 |

`*` = can start against the frozen stub contract; switch to the real thing when it merges.

## What runs in parallel

- **19–20 Oct:** F1 (platform) ‖ F2 (data, local) ‖ F4-AI LLM check (ai) ‖ board, Azure account, sample packs (PM). No one waits.
- **21–23 Oct:** contracts F3-P / F3-D / F3-A in parallel, then freeze. PM builds the app shell on top of F3-P.
- **23–26 Oct:** A1 auth ‖ B1 worker ‖ C1 tenders ‖ PM login pages. All code against the stub principal until A1 merges.
- **26–28 Oct:** A2 upload + staging deploy ‖ B2 extractors ‖ C2 pricing ‖ PM tenders + upload screens, then **G1**.
- **29 Oct–6 Nov:** three backend tracks plus the screens that sit on them, then **G2**.
- **7–10 Nov:** exports, hardening, prod, AI report, E2E, docs and demo.

## Rules for the team

- One branch per issue: `feat/<KEY>-short-name`. PR into `dev`, one review, CI green, squash merge. `dev` → `main` at each gate.
- Put `Closes #<n>` in the PR so the board moves by itself.
- Blocked for more than half a day? Say so at stand-up and put the `blocked` reason in the issue.
- Behind at a gate? Cut **P2** first, then **P1**. P0 is the MVP and is never cut.
- Architecture rules in `CLAUDE.md` apply to every PR (layers, org scoping, Decimal money, approved-only, AI safety).

## Creating the issues

```bash
gh auth login                                   # as a repo admin
# 1. put the three developer usernames in planning/issues.json → "team"
# 2. make sure all four have accepted the collaborator invite (or assignment fails)
python planning/create_issues.py --dry-run      # preview
python planning/create_issues.py                # create labels, 4 milestones, 47 issues
```

Re-running is safe: existing labels, milestones and issues are reused, not duplicated.
