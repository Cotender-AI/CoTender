"""Regenerate planning/PLAN.md from issues.json:  python planning/render_plan.py planning/issues.json planning/PLAN.md"""
import json, sys
from datetime import date
d = json.load(open(sys.argv[1])); out = open(sys.argv[2], "w")
team = d["team"]; iss = d["issues"]
ROLE = {"pm": "PM + light frontend", "platform": "Platform & security", "ai": "AI & processing", "data": "Estimating & data"}
fd = lambda s: (lambda x: f"{x.strftime('%a')} {x.day} {x.strftime('%b')}")(date.fromisoformat(s))
w = lambda *a: print(*a, file=out)
w("# CoTender delivery plan (19 Oct to 10 Nov 2026)\n")
w("Generated from `planning/issues.json` (built by `planning/build_issues.py`). Edit `build_issues.py`, not this file. `planning/create_issues.py` turns it into GitHub labels, milestones and issues.\n")
w("## Team and lanes\n")
w("| Lane | GitHub | Owns | Points |\n| --- | --- | --- | --- |")
owns = {"pm": "Board, Azure account, samples + answer key, app shell, auth/tenders/upload/settings/checklist screens, notifications, E2E, pilot, docs, demo",
        "platform": "Repo/compose/CI, API core + auth, uploads + storage, versions, audit/limits, review screen, security tests, staging + prod deploy",
        "ai": "LLM day-1 check, candidate schemas, worker + queue, extractors + OCR, LLM extraction, matcher, validators + eval, comparison screen, AI report",
        "data": "Schema + migrations + seed, estimating contracts, tenders, BoQ + Decimal pricing, review/checklist API, suppliers API, BoQ editor, exports"}
for r in ["pm", "platform", "ai", "data"]:
    w(f"| {ROLE[r]} | @{team[r]} | {owns[r]} | {sum(i['points'] for i in iss if i['owner']==r)} |")
w("\n1 point ≈ half a day. The PM's coding is the simplest work in the plan: forms, lists and tables against the frozen API contracts, plus a pattern-copy notifications module. Everything on the critical path sits with the three developers.\n")
w("## Key dates\n")
for k, t in [("Fri 23 Oct", "Contracts frozen: DB schema, OpenAPI, candidate JSON, job statuses. After this only additive changes and new migrations."),
             ("Wed 28 Oct", "**Gate G1**: log in, create tender, upload, worker finishes, all on staging"),
             ("Fri 6 Nov", "**Gate G2**: real tender pack to approved, priced data with confirmed supplier matches"),
             ("Mon 9 Nov", "**Gate G3**: production release candidate, code freeze"),
             ("Tue 10 Nov", "**Submission**")]:
    w(f"- **{k}**: {t}")
w("\n## Critical path\n")
w("F1 → F3-P → A1 → A2 → A2-DEPLOY → **G1** → (B2 → B3 → B4) ‖ (C2 → C3 → D3 / C4-API) ‖ (A3 → D2) → **G2** → C5 / A6 / E2E → **G3** → submit\n")
w("If F1 slips, everyone slips. Platform does F1 first, with nothing else on 19–20 Oct. Data starts F2 locally on day 1 and connects it to compose once F1 merges.\n")
for m in d["milestones"]:
    w(f"## {m['title']}\n\n{m['description']}\n")
    w("| Who | Issue | Dates | Pts | Pri | Blocked by |\n| --- | --- | --- | --- | --- | --- |")
    rows = sorted([i for i in iss if i["milestone"] == m["key"]], key=lambda i: (["pm","platform","ai","data"].index(i["owner"]), i["start"]))
    for i in rows:
        deps = ", ".join(k + ("*" if k in i["stub_ok"] else "") for k in i["depends_on"]) or "none"
        w(f"| @{team[i['owner']]} | {i['title']} | {fd(i['start'])} → {fd(i['due'])} | {i['points'] or '·'} | {i['priority']} | {deps} |")
    w("")
w("`*` = can start against the frozen stub contract; switch to the real thing when it merges.\n")
w("## What runs in parallel\n")
w("- **19–20 Oct:** F1 (platform) ‖ F2 (data, local) ‖ F4-AI LLM check (ai) ‖ board, Azure account, sample packs (PM). No one waits.")
w("- **21–23 Oct:** contracts F3-P / F3-D / F3-A in parallel, then freeze. PM builds the app shell on top of F3-P.")
w("- **23–26 Oct:** A1 auth ‖ B1 worker ‖ C1 tenders ‖ PM login pages. All code against the stub principal until A1 merges.")
w("- **26–28 Oct:** A2 upload + staging deploy ‖ B2 extractors ‖ C2 pricing ‖ PM tenders + upload screens, then **G1**.")
w("- **29 Oct–6 Nov:** three backend tracks plus the screens that sit on them, then **G2**.")
w("- **7–10 Nov:** exports, hardening, prod, AI report, E2E, docs and demo.\n")
w("## Rules for the team\n")
w("- One branch per issue: `feat/<KEY>-short-name`. PR into `dev`, one review, CI green, squash merge. `dev` → `main` at each gate.")
w("- Put `Closes #<n>` in the PR so the board moves by itself.")
w("- Blocked for more than half a day? Say so at stand-up and put the `blocked` reason in the issue.")
w("- Behind at a gate? Cut **P2** first, then **P1**. P0 is the MVP and is never cut.")
w("- Architecture rules in `CLAUDE.md` apply to every PR (layers, org scoping, Decimal money, approved-only, AI safety).\n")
w("## Creating the issues\n")
w("```bash\ngh auth login                                   # as a repo admin\n# 1. put the three developer usernames in planning/issues.json → \"team\"\n# 2. make sure all four have accepted the collaborator invite (or assignment fails)\npython planning/create_issues.py --dry-run      # preview\npython planning/create_issues.py                # create labels, 4 milestones, 47 issues\n```\n")
w("Re-running is safe: existing labels, milestones and issues are reused, not duplicated.")
