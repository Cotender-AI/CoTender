#!/usr/bin/env python3
"""Create CoTender labels, milestones and issues on GitHub from planning/issues.json.

Usage (from the repo root, with the GitHub CLI logged in as a repo admin):
    gh auth login
    python planning/create_issues.py --dry-run     # print what would be created
    python planning/create_issues.py               # create everything

Safe to re-run: labels are upserted, milestones and issues that already exist
(matched by title) are reused, never duplicated. The issue number for each key is
saved in planning/issue-map.json.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE / "issues.json"
MAP_FILE = HERE / "issue-map.json"
BATCH_NAMES = {"B1": "Batch 1", "B2": "Batch 2", "B3": "Batch 3", "B4": "Batch 4"}


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def fmt_day(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"


def render_body(issue: dict, plan: dict, numbers: dict[str, int], blocks: list[str]) -> str:
    team = plan["team"]
    by_key = {i["key"]: i for i in plan["issues"]}

    def ref(key: str) -> str:
        n = numbers.get(key)
        return f"#{n}" if n else f"`{key}` ({by_key[key]['title']})"

    header = (
        f"**Owner:** @{team[issue['owner']]} · **{BATCH_NAMES[issue['milestone']]}** · "
        f"**{fmt_day(issue['start'])} → {fmt_day(issue['due'])}** · "
        f"**Estimate:** {issue['points']} pts · **Priority:** {issue['priority']}"
    )
    lines = [header, ""]
    if issue["depends_on"]:
        hard = [ref(k) for k in issue["depends_on"] if k not in issue.get("stub_ok", [])]
        soft = [ref(k) for k in issue["depends_on"] if k in issue.get("stub_ok", [])]
        if hard:
            lines.append(f"**Blocked by:** {', '.join(hard)}")
        if soft:
            lines.append(
                f"**Start against the frozen stubs, switch over when merged:** {', '.join(soft)}"
            )
    if blocks:
        lines.append(f"**Blocks:** {', '.join(ref(k) for k in blocks)}")
    lines += ["", "## Goal", issue["goal"], "", "## Tasks"]
    lines += [f"- [ ] {t}" for t in issue["tasks"]]
    if issue["files"]:
        lines += ["", "## Files", ", ".join(f"`{f}`" for f in issue["files"])]
    if issue["endpoints"]:
        lines += ["", "## Endpoints", ", ".join(f"`{e}`" for e in issue["endpoints"])]
    lines += ["", "## Done when"]
    lines += [f"- [ ] {d}" for d in issue["done"]]
    if issue.get("code", True):
        lines += [
            "- [ ] Tests pass in CI (incl. a cross-tenant test for any new resource)",
            "- [ ] PR reviewed by one teammate and merged into `dev`",
        ]
    if issue["refs"]:
        lines += ["", "## References", ", ".join(issue["refs"]) + " (see `docs/` and `CLAUDE.md`)"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print, don't create")
    ap.add_argument("--no-assign", action="store_true", help="create issues without assignees")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    repo = plan["repo"]
    blocks: dict[str, list[str]] = {i["key"]: [] for i in plan["issues"]}
    for i in plan["issues"]:
        for dep in i["depends_on"]:
            blocks[dep].append(i["key"])

    if args.dry_run:
        for i in plan["issues"]:
            print("=" * 80, f"\n{i['title']}  [{i['milestone']}]  labels={i['labels']}\n")
            print(render_body(i, plan, {}, blocks[i["key"]]))
        print(f"\n{len(plan['issues'])} issues, {len(plan['milestones'])} milestones, "
              f"{len(plan['labels'])} labels (dry run, nothing created)")
        return 0

    unset = [role for role, user in plan["team"].items() if user.startswith("CHANGE_ME")]
    if unset and not args.no_assign:
        print(f"Fill in GitHub usernames for {unset} in planning/issues.json (team), "
              "or run with --no-assign.", file=sys.stderr)
        return 1

    # Labels (upsert)
    for lb in plan["labels"]:
        gh("label", "create", lb["name"], "--repo", repo, "--color", lb["color"],
           "--description", lb["description"], "--force")
    print(f"labels: {len(plan['labels'])} ok")

    # Milestones (reuse by title)
    existing = json.loads(gh("api", f"repos/{repo}/milestones?state=all&per_page=100").stdout)
    ms_title = {m["title"]: m["title"] for m in existing}
    milestone_of: dict[str, str] = {}
    for m in plan["milestones"]:
        if m["title"] not in ms_title:
            gh("api", f"repos/{repo}/milestones", "-f", f"title={m['title']}",
               "-f", f"description={m['description']}", "-f", f"due_on={m['due']}T21:59:00Z")
        milestone_of[m["key"]] = m["title"]
    print(f"milestones: {len(plan['milestones'])} ok")

    # Issues (reuse by title)
    numbers: dict[str, int] = json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else {}
    listed = json.loads(gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "500",
                           "--json", "number,title").stdout)
    by_title = {x["title"]: x["number"] for x in listed}
    for i in plan["issues"]:
        if i["key"] in numbers or i["title"] in by_title:
            numbers[i["key"]] = numbers.get(i["key"]) or by_title[i["title"]]
            print(f"  exists  #{numbers[i['key']]:<4} {i['title']}")
            continue
        body = render_body(i, plan, numbers, [])  # "Blocks" filled in after all exist
        cmd = ["issue", "create", "--repo", repo, "--title", i["title"], "--body", body,
               "--milestone", milestone_of[i["milestone"]]]
        for lb in i["labels"]:
            cmd += ["--label", lb]
        user = plan["team"][i["owner"]]
        res = gh(*cmd, *([] if args.no_assign else ["--assignee", user]), check=False)
        if res.returncode != 0 and not args.no_assign:
            print(f"  ! could not assign @{user} (not a collaborator yet?), creating unassigned")
            res = gh(*cmd, check=False)
        if res.returncode != 0:
            print(f"  ! failed: {i['title']}\n{res.stderr}", file=sys.stderr)
            return 1
        numbers[i["key"]] = int(res.stdout.strip().rstrip("/").split("/")[-1])
        MAP_FILE.write_text(json.dumps(numbers, indent=2))
        print(f"  created #{numbers[i['key']]:<4} {i['title']}")

    # Second pass: real #numbers for "Blocked by" and "Blocks"
    for i in plan["issues"]:
        gh("issue", "edit", str(numbers[i["key"]]), "--repo", repo,
           "--body", render_body(i, plan, numbers, blocks[i["key"]]))
    MAP_FILE.write_text(json.dumps(numbers, indent=2))
    print(f"done: {len(numbers)} issues linked. Map saved to {MAP_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
