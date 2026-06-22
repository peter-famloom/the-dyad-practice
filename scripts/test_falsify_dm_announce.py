#!/usr/bin/env python3
# Co-located regression test for falsify.py's DM consume-on-display announce (PR #70). Guards the steering
# output that names the read-state `dm` consumes — and PINS the precise gating, since the claim "already-seen
# runs stay silent" was scoped (touchstone #70/2): only the `seen:` line is gated; default-mode `dm` still
# REPRINTS the listing, whole-run silence holds ONLY under --unread. Plain Python, no framework. Mocks
# `subprocess.run` so it drives the REAL dm_items/cmd_dm; runs in a tmp cwd so .falsify-seen.json is isolated.
import contextlib
import io
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
# One reachable sender with one DM carrying a blob `sha` (the read-key is path@sha post-#69).
RESPONSES = {
    "repos/o-x/box" + C: (0, '[{"name":"msg.md","sha":"abc123","html_url":"u"}]', ""),
}


def fake_run(argv, capture_output=True, text=True):
    rc, out, err = RESPONSES[argv[2]]
    return types.SimpleNamespace(returncode=rc, stdout=out, stderr=err)


def setup_dir():
    root = tempfile.mkdtemp()
    ddir = os.path.join(root, "directory"); os.makedirs(ddir)
    os.makedirs(os.path.join(root, "falsification"))
    for name, owner in [("dyad-x", "o-x"), (ME, "o-self")]:
        open(os.path.join(ddir, f"{name}.yaml"), "w").write(
            f"name: {name}\nlocator: https://github.com/{owner}/box\n")
    return os.path.join(root, "falsification")


FAILS = []


def check(cond, label):
    print(("PASS" if cond else "FAIL") + f"  {label}")
    if not cond:
        FAILS.append(label)


def run_dm(ledger, unread):
    a = types.SimpleNamespace(me=ME, unread=unread)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        falsify.cmd_dm(ledger, a)
    return buf.getvalue()


def main():
    subprocess.run = fake_run
    ledger = setup_dir()
    cwd = os.getcwd()
    work = tempfile.mkdtemp()
    os.chdir(work)  # isolate .falsify-seen.json
    try:
        # 1. fresh run announces, with a machine-addressable prefix
        out1 = run_dm(ledger, unread=False)
        seen_lines = [ln for ln in out1.splitlines() if ln.startswith("seen: ")]
        check("• from dyad-x: msg.md" in out1, "fresh run lists the DM (• prefix)")
        check(len(seen_lines) == 1 and "marked 1 DM(s) read" in seen_lines[0],
              "fresh run announces consume (seen: 1)")
        check(seen_lines and seen_lines[0].startswith("seen: "),
              "announce leads with machine-addressable `seen: ` token (mirrors unreachable:)")

        # 2. (finding-2 correction) default-mode already-seen re-run REPRINTS the listing but emits NO seen: line
        out2 = run_dm(ledger, unread=False)
        check(" from dyad-x: msg.md" in out2, "default already-seen re-run STILL reprints the per-DM line")
        check(not any(ln.startswith("seen: ") for ln in out2.splitlines()),
              "default already-seen re-run is gated: no seen: line (consumed=0)")
        check("(no DMs)" not in out2, "default already-seen re-run is NOT whole-run silent")

        # 3. --unread already-seen re-run IS whole-run silent (the only path that claim holds)
        out3 = run_dm(ledger, unread=True)
        check(out3.strip() == "(no DMs)", "--unread already-seen re-run is whole-run silent")
    finally:
        os.chdir(cwd)

    print("\n" + ("ALL PASS" if not FAILS else f"FAILURES: {FAILS}"))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
