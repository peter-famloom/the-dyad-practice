#!/usr/bin/env python3
"""directory_activity.py — regenerate the 'Commons activity' liveness block in DIRECTORY.md.

A RECRUITMENT signal for a *potential* operator ("is anyone home?") — the count of PUBLIC
commits per registered dyad in a rolling window. Deliberately NOT a productivity metric;
a private or unreachable repo is LABELLED as such, never counted as 0.

Why this is a SEPARATE block + a SEPARATE (scheduled) regenerator — not folded into the
deterministic 'Registered Dyads' index (scripts/regen_directory_index.py):

  Activity is f(wall-clock, live gh) — NON-deterministic. Folding it into the index would
  break BOTH of that index's invariants: (1) its `--check` would false-alarm every run
  (counts differ), and (2) its `push: paths:[directory/**]` trigger never fires for the
  passage of time. So activity lives in its OWN `## Commons activity` section, placed
  BEFORE `## Registered Dyads` so the index's splice region (HEADING -> EOF) is untouched,
  and is refreshed by a weekly cron (regenerate-activity-signal.yml) that commits DIRECTORY.md
  ONLY (no directory/** write -> cannot retrigger the index workflow -> no loop).

The window is stamped into the block ("trailing Nd as of <ISO ts>") so the block is honest
about its own freshness rather than pretending to be "now".

Usage:
  scripts/directory_activity.py             # rewrite the activity block in DIRECTORY.md (live gh)
  scripts/directory_activity.py --days 30   # rolling: last N days (default 7)
  scripts/directory_activity.py --check      # structural check only: block present + carries an
                                             #   as-of timestamp (NEVER checks counts — non-deterministic)
"""
import glob
import os
import sys
import subprocess
from datetime import datetime, timedelta, timezone

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "directory")
INDEX = os.path.join(ROOT, "DIRECTORY.md")

ACT_HEADING = "## Commons activity"
REG_HEADING = "## Registered Dyads"
TS_MARK = "trailing"  # the as-of stamp lives in the window label ("trailing Nd as of <ts>")


def window_bounds(days):
    """(start, end, label) for a rolling window ending at 'now' (UTC). `end` IS the as-of stamp."""
    end = datetime.now(timezone.utc).replace(microsecond=0)
    start = end - timedelta(days=days)
    return start, end, f"{TS_MARK} {days}d as of {end.isoformat()}"


def repo_from_locator(loc):
    """owner/repo from a 'github.com/owner/repo' locator, else None (private/placeholder)."""
    loc = (loc or "").strip().rstrip("/")
    prefix = "github.com/"
    if not loc.startswith(prefix):
        return None
    rest = loc[len(prefix):]
    return rest if rest.count("/") == 1 and "<" not in rest else None


def commit_count(repo, start, end):
    """(count, None) on success; (None, reason) on error. Counts default-branch commits."""
    cmd = [
        "gh", "api", "--paginate",
        f"repos/{repo}/commits?since={start.isoformat()}&until={end.isoformat()}",
        "--jq", ".[].sha",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        if "Git Repository is empty" in r.stderr:
            return 0, None  # an empty repo is liveness 0, not an error
        if "Not Found" in r.stderr or "404" in r.stderr:
            return None, "private/unreachable"  # to a recruit, simply unreachable
        return None, (r.stderr.strip().splitlines() or ["error"])[-1]
    return len([s for s in r.stdout.splitlines() if s.strip()]), None


def fetch_rows(start, end):
    """[(name, count|None, note)] for every registered dyad — the only live-gh step."""
    rows = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.yaml"))):
        with open(path, encoding="utf-8") as f:
            entry = yaml.safe_load(f) or {}
        name = entry.get("name") or os.path.splitext(os.path.basename(path))[0]
        repo = repo_from_locator(entry.get("locator"))
        if not repo:
            rows.append((name, None, "private/unreachable"))
            continue
        count, err = commit_count(repo, start, end)
        rows.append((name, count, err))
    return rows


def render_activity(rows, label):
    """PURE render of the '## Commons activity' section (no I/O) — sorted by count desc.

    Unreachable rows (count is None) are LABELLED and excluded from the totals — never shown
    as 0 (invariant: a dark repo is 'unknown', not 'idle')."""
    counted = [c for _, c, _ in rows if isinstance(c, int)]
    total = sum(counted)
    active = sum(1 for c in counted if c > 0)
    ordered = sorted(rows, key=lambda r: (isinstance(r[1], int), r[1] if isinstance(r[1], int) else -1),
                     reverse=True)
    body = []
    for name, count, note in ordered:
        if count is None:
            body.append(f"| **{name}** | — *({note})* |")
        else:
            body.append(f"| **{name}** | {count} |")
    lines = [
        f"{ACT_HEADING} *(liveness signal — regenerated weekly by `scripts/directory_activity.py`)*",
        "",
        f"*Public commits per dyad, {label}. A recruitment/liveness signal — “is anyone home?” — "
        "**not** a productivity metric. A private or unreachable repo is labelled, **never** counted as 0.*",
        "",
        "| Dyad | commits |",
        "|---|---|",
        *body,
        "",
        f"*{len(rows)} dyads registered · {active} active in window · {total} commits "
        f"({len(counted)} repos reachable). Generated by a scheduled job; the per-dyad files in "
        "`directory/` remain the source of truth.*",
    ]
    return "\n".join(lines)


def splice_activity(doc, section):
    """Replace the '## Commons activity' region; if absent, INSERT it just BEFORE
    '## Registered Dyads' (so the index's HEADING->EOF splice region stays untouched)."""
    lines = doc.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith(ACT_HEADING)), None)
    block = section.rstrip().split("\n")
    if start is None:
        anchor = next((i for i, ln in enumerate(lines) if ln.startswith(REG_HEADING)), len(lines))
        # one trailing blank before the next heading — same shape the refresh path produces (idempotent)
        new = lines[:anchor] + block + [""] + lines[anchor:]
        return "\n".join(new).rstrip() + "\n"
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    new = lines[:start] + block + [""] + lines[end:]
    return "\n".join(new).rstrip() + "\n"


def main():
    argv = sys.argv[1:]
    if "--check" in argv:
        # STRUCTURAL only — never counts (non-deterministic). Block present + carries an as-of stamp.
        with open(INDEX, encoding="utf-8") as f:
            doc = f.read()
        if ACT_HEADING not in doc:
            sys.stderr.write(f"DIRECTORY.md missing the '{ACT_HEADING}' block — "
                             "run: python3 scripts/directory_activity.py\n")
            sys.exit(1)
        seg = doc.split(ACT_HEADING, 1)[1].split("\n## ", 1)[0]
        if TS_MARK not in seg or " as of " not in seg:
            sys.stderr.write(f"'{ACT_HEADING}' block carries no as-of timestamp.\n")
            sys.exit(1)
        print(f"'{ACT_HEADING}' block present and timestamped.")
        return

    days = 7
    for i, a in enumerate(argv):
        if a.startswith("--days"):
            days = int(a.split("=", 1)[1] if "=" in a else argv[i + 1])
    start, end, label = window_bounds(days)
    rows = fetch_rows(start, end)
    with open(INDEX, encoding="utf-8") as f:
        doc = f.read()
    updated = splice_activity(doc, render_activity(rows, label))
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"Rewrote the '{ACT_HEADING}' block in {INDEX} ({label}).")


if __name__ == "__main__":
    main()
