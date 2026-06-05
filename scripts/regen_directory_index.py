#!/usr/bin/env python3
"""Regenerate the 'Registered Dyads' index table in DIRECTORY.md from directory/*.yaml.

The index is a DETERMINISTIC, regenerable VIEW over the per-dyad files — DIRECTORY.md itself
says it "is regenerable from `directory/` (deterministic — anyone can rebuild it); it is not a
gate and may lag." Rendering a dyad in this index is NOT editing its sovereign
`directory/<name>.yaml`, so the index can list every registered dyad *without* "asserting on
their behalf" (the category error that had left it listing 1 of N). This script makes the
rebuild mechanical so the index never drifts behind the per-dyad files again.

Usage:
  regen_directory_index.py            # rewrite DIRECTORY.md in place
  regen_directory_index.py --check    # exit 1 if the index is stale (CI-friendly); no write
"""
import glob
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "directory")
INDEX = os.path.join(ROOT, "DIRECTORY.md")

HEADING = "## Registered Dyads"
# The index shows each summit's PEAK — the head before the first delimiter. Both separators are
# already the lived convention in directory/*.yaml ("peak — realized proof" / "Peak: elaboration").
PEAK_DELIMS = (" — ", ": ")
PEAK_MAX = 100

GEN_NOTE = (
    "*This table is a generated index over `directory/*.yaml` — rebuild it with "
    "`python3 scripts/regen_directory_index.py` (deterministic; not a gate). Listing a dyad here "
    "renders its own self-authored entry; it does not edit another dyad's file. The `+1 summit` "
    "column shows each summit's peak; the full text lives in the linked entry.*"
)


def peak(summit):
    """The matchmaking headline: the head before the first peak-delimiter, whitespace-collapsed."""
    s = " ".join(summit.split())
    hits = [s.find(d) for d in PEAK_DELIMS if s.find(d) != -1]
    if hits:
        s = s[: min(hits)]
    s = s.strip().rstrip(".")
    if len(s) > PEAK_MAX:
        s = s[: PEAK_MAX - 1].rstrip() + "…"
    return s


def render():
    """Render the full '## Registered Dyads' section from directory/*.yaml (sorted by name)."""
    rows = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.yaml"))):
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        name = data["name"]
        rel = "directory/%s.yaml" % name
        peaks = " · ".join(peak(s) for s in data["summits"])
        rows.append("| **%s** | [`%s`](%s) | %s |" % (name, rel, rel, peaks))
    lines = [
        "%s *(index — truth is in `directory/`)*" % HEADING,
        "",
        "| Dyad | entry | +1 summit(s) |",
        "|---|---|---|",
        *rows,
        "",
        GEN_NOTE,
    ]
    return "\n".join(lines)


def splice(doc, section):
    """Replace from the HEADING line to the next '## ' heading (or EOF) with `section`."""
    lines = doc.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith(HEADING)), None)
    if start is None:
        return doc.rstrip() + "\n\n" + section.rstrip() + "\n"
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    new = lines[:start] + section.rstrip().split("\n") + lines[end:]
    return "\n".join(new).rstrip() + "\n"


def main():
    check = "--check" in sys.argv[1:]
    with open(INDEX, encoding="utf-8") as f:
        doc = f.read()
    updated = splice(doc, render())
    if check:
        if updated != doc:
            sys.stderr.write(
                "DIRECTORY.md index is STALE vs directory/*.yaml — "
                "run: python3 scripts/regen_directory_index.py\n"
            )
            sys.exit(1)
        print("DIRECTORY.md index is up to date.")
        return
    if updated != doc:
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(updated)
        print("Rewrote %s" % INDEX)
    else:
        print("DIRECTORY.md already up to date.")


if __name__ == "__main__":
    main()
