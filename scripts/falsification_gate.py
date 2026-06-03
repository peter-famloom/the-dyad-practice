#!/usr/bin/env python3
# Auto-merge gate for one falsification deposit (called by auto-merge-falsification.yml on the BASE
# checkout — never executes PR code). Decides if a single added falsification/ record may merge with NO
# human gate. Fail-safe: returns non-zero (→ human review) on ANYTHING it can't positively clear.
#
#   falsification_gate.py <ledger_root> <added_file_relpath> <pr_author_login>
#
# Clears ONLY when: (1) the record passes validate_falsification, AND (2) IDENTITY BINDS — the record's
# dyad-id resolves to a directory entry whose locator github-id == the PR author, and the record's human
# field (fr/response) == the PR author. This makes dyad-id + human VERIFIED (not self-reported) — the I1
# bind, and the mechanism that stops a poster faking another dyad's independence axes. (model stays
# self-attested; alt-account spoof remains the v4 residual no mechanism closes.)
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from validate_falsification import validate_fr, validate_response, validate_disposition


def deny(msg):
    print(f"GATE: human-review — {msg}")
    sys.exit(1)


def locator_github_id(ledger_root, dyad_id):
    """The dyad's registered owner github-id, from directory/<dyad>.yaml locator (trusted base)."""
    p = os.path.join(ledger_root, "..", "directory", f"{dyad_id}.yaml")
    if not os.path.isfile(p):
        return None
    loc = (yaml.safe_load(open(p, encoding="utf-8")) or {}).get("locator", "")
    m = re.search(r"github\.com[/:]([^/]+)/", loc)
    return m.group(1) if m else None


def main():
    ledger, rel, author = sys.argv[1], sys.argv[2], sys.argv[3]
    path = os.path.join(os.path.dirname(ledger), rel)  # rel is repo-relative (falsification/…)
    if not os.path.isfile(path):
        deny(f"{rel} not materialized")
    base = os.path.basename(rel)
    data = yaml.safe_load(open(path, encoding="utf-8")) or {}

    # (1) schema + (role → the dyad-id and human that must bind to the author)
    if base == "fr.yaml":
        if not validate_fr(path):
            deny("FR failed validation")
        dyad, human = data.get("submitter_dyad_id"), data.get("submitter_human")
    elif "/responses/" in rel.replace(os.sep, "/"):
        claim_dir = os.path.dirname(os.path.dirname(path))
        frp = os.path.join(claim_dir, "fr.yaml")
        if not os.path.isfile(frp):
            deny("response to a claim whose fr.yaml is not on base (open the FR first)")
        submitter = (yaml.safe_load(open(frp, encoding="utf-8")) or {}).get("submitter_dyad_id")
        if not validate_response(path, submitter):
            deny("response failed validation (incl. I5 self-response)")
        dyad, human = data.get("responder_dyad_id"), data.get("responder_human")
    elif base == "disposition.yaml":
        if not validate_disposition(path):
            deny("disposition failed validation")
        dyad, human = data.get("disposing_dyad_id"), None  # disposition carries no human field
    else:
        deny(f"unrecognized record {base}")

    # (2) identity bind — dyad-id → registered owner == author; record human (if any) == author
    owner = locator_github_id(ledger, dyad)
    if owner is None:
        deny(f"dyad-id {dyad!r} not in directory/ (unregistered)")
    if owner != author:
        deny(f"dyad {dyad!r} is owned by {owner!r}, not the PR author {author!r} (identity spoof)")
    if human is not None and human != author:
        deny(f"record human {human!r} != PR author {author!r} (axis spoof)")

    print(f"GATE: auto-merge — {rel} valid + identity-bound to {author}")
    sys.exit(0)


if __name__ == "__main__":
    main()
