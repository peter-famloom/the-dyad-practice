#!/usr/bin/env python3
"""Regression tests for directory_activity.py — asserts plan_directory_autogen's four invariants.

Deterministic by construction: exercises the PURE render/splice functions with synthetic rows +
a fixed label, and PARSES the cron workflow. No live gh, no wall-clock — so CI is stable.

Run:  python3 scripts/test_directory_activity.py   (also collectable by pytest)
"""
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import directory_activity as da  # noqa: E402
import regen_directory_index as ri  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "regenerate-activity-signal.yml")

FIXED_LABEL = "trailing 7d as of 2026-06-09T12:00:00+00:00"
ROWS = [
    ("dyad-steward", 12, None),
    ("dyad-bond", 0, None),
    ("dyad-krishna", None, "private/unreachable"),
]

SAMPLE_DOC = """# DIRECTORY.md — registry

intro prose here.

## Registered Dyads *(index — truth is in `directory/`)*

| Dyad | entry | +1 summit(s) |
|---|---|---|
| **dyad-steward** | [`directory/dyad-steward.yaml`](directory/dyad-steward.yaml) | process-integrity |

*generated index note.*
"""


def _registry_region(doc):
    """The exact bytes of the '## Registered Dyads' -> EOF region (the index's splice jurisdiction)."""
    return doc[doc.index(ri.HEADING):]


# ── inv (2): the block carries an embedded as-of timestamp ───────────────────────────────
def test_block_carries_timestamp():
    out = da.render_activity(ROWS, FIXED_LABEL)
    assert " as of " in out and "2026-06-09T12:00:00+00:00" in out, "as-of timestamp missing from block"


# ── inv (4): unreachable dyads stay labelled, never counted as 0 ─────────────────────────
def test_unreachable_labelled_not_zero():
    out = da.render_activity(ROWS, FIXED_LABEL)
    assert "**dyad-krishna** | — *(private/unreachable)*" in out, "unreachable not labelled"
    assert "**dyad-krishna** | 0" not in out, "unreachable wrongly rendered as 0"
    # totals exclude the unreachable row: 2 reachable, 1 active (steward=12), 12 commits
    assert "2 active in window" not in out  # only steward (>0) is active
    assert "1 active in window · 12 commits (2 repos reachable)" in out, "totals miscounted unreachable"


# ── inv (1): the registry index region is byte-identical after an activity splice ────────
def test_registry_index_untouched_on_insert():
    spliced = da.splice_activity(SAMPLE_DOC, da.render_activity(ROWS, FIXED_LABEL))
    assert da.ACT_HEADING in spliced, "activity block not inserted"
    assert spliced.index(da.ACT_HEADING) < spliced.index(ri.HEADING), "activity must precede the index"
    assert _registry_region(spliced) == _registry_region(SAMPLE_DOC), "registry region was mutated"


def test_registry_index_untouched_on_refresh():
    once = da.splice_activity(SAMPLE_DOC, da.render_activity(ROWS, FIXED_LABEL))
    newer = [("dyad-steward", 99, None), ("dyad-bond", 3, None), ("dyad-krishna", None, "private/unreachable")]
    twice = da.splice_activity(once, da.render_activity(newer, FIXED_LABEL))
    assert _registry_region(twice) == _registry_region(SAMPLE_DOC), "registry drifted on activity refresh"
    assert "**dyad-steward** | 99" in twice and "**dyad-steward** | 12" not in twice, "block not refreshed"


def test_splice_structurally_idempotent():
    once = da.splice_activity(SAMPLE_DOC, da.render_activity(ROWS, FIXED_LABEL))
    twice = da.splice_activity(once, da.render_activity(ROWS, FIXED_LABEL))
    assert once == twice, "re-splicing the same data changed the document"


# ── inv (3): the scheduled regen commits DIRECTORY.md only — no directory/** loop ────────
def test_workflow_no_retrigger_loop():
    with open(WORKFLOW, encoding="utf-8") as f:
        raw = f.read()
    wf = yaml.safe_load(raw)
    on = wf[True] if True in wf else wf.get("on")  # PyYAML parses bare `on:` as boolean True
    assert "schedule" in on, "activity regen must be schedule-driven (time is the trigger)"
    push = on.get("push") or {}
    paths = (push.get("paths") or []) if isinstance(push, dict) else []
    assert "directory/**" not in paths, "must NOT trigger on directory/** (that is the index workflow)"
    assert "git add DIRECTORY.md" in raw, "the regen step must stage DIRECTORY.md"
    # it must NOT stage anything under directory/ — that would retrigger the index workflow (a loop)
    assert "add directory/" not in raw and "add ." not in raw, "must commit DIRECTORY.md ONLY (no loop)"


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())
