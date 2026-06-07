#!/usr/bin/env python3
"""automerge_self_update_gate.py — decide whether a directory ENTRY-UPDATE PR may self-authorize.

STAGED FOR THE COMMONS — install path: the-dyad-practice/scripts/automerge_self_update_gate.py
Authored by dyad-steward; INSTALLED BY THE FOUNDING OPERATOR (drives the protected .github/ workflow
auto-merge-self-update.yml). Sibling of the registration auto-merge: that one handles pure ADDs
(self-registration); THIS one handles a dyad MODIFYING ITS OWN entry (summits/locator/dm_locator).

The hard part vs the add-case: an update has prior state to protect. So a modify auto-merges only when
ALL hold — (1) exactly one changed file, status=modified, path directory/<name>.yaml; (2) the PR author
OWNS the entry (author == the github owner in the BASE entry's locator — read from base, untrusted head
cannot forge it); (3) birth_hash AND name are UNCHANGED (frozen identity); (4) the head entry passes the
registry validator. Anything else -> left for human review (fail-safe: can only UNDER-merge).

`decide()` is a pure function (no I/O) so it is unit-tested by bin/test_automerge_gate.py (No-Pure-G).
"""
import re

NAME_PATH_RE = re.compile(r"^directory/dyad-[a-z0-9]+(-[a-z0-9]+)*\.yaml$")


def owner_of(locator):
    """github owner from a locator like 'github.com/pltrinh1122/dyad-steward' (scheme optional)."""
    if not isinstance(locator, str):
        return ""
    s = re.sub(r"^https?://", "", locator.strip()).strip("/")
    parts = s.split("/")
    # expect host / owner / repo...
    return parts[1] if len(parts) >= 2 and parts[0].endswith("github.com") else ""


def decide(files, base_entry, head_entry, pr_author, validate_ok):
    """Return (merge: bool, reason: str). PURE — caller supplies files/entries/author/validate result."""
    if len(files) != 1:
        return False, f"not a single-file change ({len(files)} files) — split it"
    f = files[0]
    status = f.get("status")
    fn = f.get("filename", "")
    if status != "modified":
        return False, f"status={status!r}, not a modify (a new entry goes through the registration auto-merge)"
    if not NAME_PATH_RE.match(fn):
        return False, f"path {fn!r} is not a directory/<name>.yaml entry"
    if not isinstance(base_entry, dict):
        return False, "no readable BASE entry — cannot authorize an update without prior state"
    if not isinstance(head_entry, dict):
        return False, "head entry is not a mapping"
    if head_entry.get("name") != base_entry.get("name"):
        return False, "`name` is FROZEN (identity) — change rejected"
    if head_entry.get("birth_hash") != base_entry.get("birth_hash"):
        return False, "`birth_hash` is FROZEN (identity) — change rejected"
    owner = owner_of(base_entry.get("locator", ""))
    if not owner or owner.lower() != str(pr_author).lower():
        return False, f"PR author {pr_author!r} != entry owner {owner!r} — you may only self-update your OWN entry"
    if not validate_ok:
        return False, "head entry fails registry validation"
    return True, "self-update of your OWN entry; birth_hash+name intact; valid — auto-merge (no contest)"
