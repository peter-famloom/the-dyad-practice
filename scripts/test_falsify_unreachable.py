#!/usr/bin/env python3
# Co-located regression test for falsify.py's per-source UNREACHABLE detection (Commons-owned). Guards the
# fix for healer's falsification: a clean inbox must never silently mean 'no mail I could reach'. Plain
# Python, no framework — runnable now. Mocks `subprocess.run` so it drives the REAL _gh_json / dm_items.
# v2: adds the panel-review cases (bond/healer/touchstone) — boundary named from the repo-probe not the
# contents status, 403≠private, anti-spoof/bad-locator skips routed, unparseable-200 not escaping.
import os
import sys
import tempfile
import types

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess

import falsify

ME = "dyad-steward"
C = "/contents/dm/dyad-steward"
# (rc, stdout, stderr) per gh-api path. Endpoints: "<repo>/contents/dm/<me>" and the repo-probe "<repo>".
RESPONSES = {
    # reachable WITH a DM → 200 + list (no probe)
    "repos/o-mail/box" + C: (0, '[{"name":"2026-06-03-hi.md","html_url":"u"}]', ""),
    # public, no dm/<me> dir → contents 404, repo reachable → BENIGN (silent)
    "repos/o-nomail/box" + C: (1, "", "gh: Not Found (HTTP 404)"),
    "repos/o-nomail/box": (0, '{"full_name":"o-nomail/box"}', ""),
    # private/gone anchor → contents 404 AND repo 404 → UNREACHABLE (private)
    "repos/o-priv/box" + C: (1, "", "gh: Not Found (HTTP 404)"),
    "repos/o-priv/box": (1, "", "gh: Not Found (HTTP 404)"),
    # transport failure both calls → UNREACHABLE (network)
    "repos/o-net/box" + C: (1, "", "error connecting to api.github.com: timeout"),
    "repos/o-net/box": (1, "", "error connecting to api.github.com: timeout"),
    # 403 on contents but repo REACHABLE → NOT private; "mailbox read failed (HTTP 403)" (bond/touchstone)
    "repos/o-403/box" + C: (1, "", "gh: Forbidden (HTTP 403)"),
    "repos/o-403/box": (0, '{"full_name":"o-403/box"}', ""),
    # DIVERGENT: contents 404 but the repo-probe NETWORK-fails → why must come from the probe ("network"),
    # not the contents 404 (which the old code mislabeled "private") — touchstone #3.
    "repos/o-div/box" + C: (1, "", "gh: Not Found (HTTP 404)"),
    "repos/o-div/box": (1, "", "error connecting to api.github.com: timeout"),
    # 200 with an UNPARSEABLE body → must NOT escape as 'no mail'; flagged (touchstone residual)
    "repos/o-garb/box" + C: (0, "{not valid json", ""),
    "repos/o-garb/box": (0, '{"full_name":"o-garb/box"}', ""),
}


def fake_run(argv, capture_output=True, text=True):
    rc, out, err = RESPONSES[argv[2]]  # ["gh", "api", path]
    return types.SimpleNamespace(returncode=rc, stdout=out, stderr=err)


def setup_dir():
    root = tempfile.mkdtemp()
    ddir = os.path.join(root, "directory"); os.makedirs(ddir)
    os.makedirs(os.path.join(root, "falsification"))
    # (name, locator-owner, dm_locator-owner-or-None)
    rows = [("dyad-mail", "o-mail", None), ("dyad-nomail", "o-nomail", None), ("dyad-priv", "o-priv", None),
            ("dyad-net", "o-net", None), ("dyad-403", "o-403", None), ("dyad-divergent", "o-div", None),
            ("dyad-garbage", "o-garb", None), ("dyad-mismatch", "o-x", "o-y"), (ME, "o-self", None)]
    for name, owner, dmowner in rows:
        body = f"name: {name}\nlocator: https://github.com/{owner}/box\n"
        if dmowner:
            body += f"dm_locator: https://github.com/{dmowner}/box\n"
        open(os.path.join(ddir, f"{name}.yaml"), "w").write(body)
    return os.path.join(root, "falsification")


FAILS = []


def check(cond, label):
    print(("PASS" if cond else "FAIL") + f"  {label}")
    if not cond:
        FAILS.append(label)


def main():
    subprocess.run = fake_run
    ledger = setup_dir()
    unreachable = []
    items = list(falsify.dm_items(ledger, ME, unreachable))
    why = {name: w for name, _repo, w in unreachable}
    repo = {name: r for name, r, _w in unreachable}

    check(len(items) == 1 and items[0][0] == "dyad-mail", "reachable DM yielded (dyad-mail)")
    check("dyad-nomail" not in why, "benign 404 (no dm dir) NOT flagged")
    check(why.get("dyad-priv") == "private/not-a-collaborator", "private anchor named from repo-probe")
    check(why.get("dyad-net") == "gh/network error", "network failure named")
    # bond/touchstone: repo reachable + contents 403 → mailbox-read-failed, NOT private
    check(why.get("dyad-403") == "mailbox read failed (HTTP 403)", "403-with-repo-OK is NOT mislabeled private")
    # touchstone #3: why derives from the repo-probe (rs), not the contents status
    check(why.get("dyad-divergent") == "gh/network error",
          "divergent (contents-404 + repo-network) named from probe, not 'private'")
    # touchstone residual: a 200 with garbage body must not escape the flag
    check(why.get("dyad-garbage") == "mailbox read failed (HTTP 200)", "unparseable-200 flagged, not escaped")
    # healer/touchstone: the anti-spoof owner-mismatch skip is routed through unreachable, not silent
    check(why.get("dyad-mismatch") == "mailbox-owner-mismatch (anti-spoof skip)"
          and repo.get("dyad-mismatch") == "o-y/box", "anti-spoof owner-mismatch routed (not silent)")

    ok, status, _ = falsify._gh_json("repos/o-priv/box")
    check(ok is False and status == 404, "_gh_json extracts HTTP 404")
    ok2, status2, _ = falsify._gh_json("repos/o-garb/box" + C)
    check(ok2 is False and status2 == 200, "_gh_json: unparseable-200 → (False, 200, None)")

    line = falsify._unreachable_line(unreachable)
    check(line.startswith("⚠ unreachable: ") and "no mail from everyone" in line,
          "warning line leads with machine-addressable `unreachable: N` token")

    print("\nALL PASS" if not FAILS else f"\n{len(FAILS)} FAILED: {FAILS}")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
