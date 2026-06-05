#!/usr/bin/env python3
# Contracted, token-thrifty CLI over the falsification ledger (falsification/CONTRACT.md) — the channel's
# pull-based AWARENESS mechanism. The contract is pull-only (N2/N3: no push/flood); discovery is therefore
# a cheap, informative pull: `list --unread` surfaces what's NEW to YOU (read-state is per-consumer-local,
# never in the shared ledger), open-axis advertises where an independent attack still adds coverage, and a
# staleness flag is the I10 dead-mechanism detector (an open FR no one has attacked). WRITES go through the
# installed validator (validate_falsification) so records can't drift from the spec; `respond` auto-pins
# target_claim_hash so a responder needn't hand-compute the FR's bytes.
#
#   falsify.py list [--domain D] [--unread] [--stale-days N]   # discover: open FRs + open-axis + STALE flag
#   falsify.py show <claim_id>                                  # read one (marks it seen)
#   falsify.py submit <fr.yaml>                                 # validate + open a new FR
#   falsify.py respond <claim_id> <response.yaml>               # auto-pins target_claim_hash, validates, appends
#
# --ledger PATH (or $FALSIFY_LEDGER); defaults to commons/falsification or falsification.
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from validate_falsification import validate_fr, validate_response

AXES = ("model", "human", "corpus")


def find_ledger(arg):
    for p in (arg, os.environ.get("FALSIFY_LEDGER"), "commons/falsification", "falsification"):
        if p and os.path.isdir(p):
            return p
    sys.exit("no ledger found (pass --ledger or set FALSIFY_LEDGER)")


def seen_path():  # per-consumer-local read-state — in the consumer's cwd, gitignore it; NEVER in the ledger
    return os.path.join(os.getcwd(), ".falsify-seen.json")


def load_seen():
    import json
    try:
        return set(json.load(open(seen_path())))
    except (FileNotFoundError, ValueError):
        return set()


def mark_seen(cid):
    import json
    s = load_seen(); s.add(cid)
    json.dump(sorted(s), open(seen_path(), "w"))


def read(p):
    return yaml.safe_load(open(p, encoding="utf-8")) or {}


def responses(cdir):
    rdir = os.path.join(cdir, "responses")
    return [read(os.path.join(rdir, r)) for r in sorted(os.listdir(rdir))
            if r.endswith((".yaml", ".yml"))] if os.path.isdir(rdir) else []


def open_axes(cdir):
    """Independence axes NOT yet attacked = AXES − ∪(responses' divergent_axes). Advertises where an
    independent responder still adds coverage (the disjoint-tiling goal)."""
    covered = set().union(*[set(r.get("divergent_axes") or []) for r in responses(cdir)]) if responses(cdir) else set()
    return [a for a in AXES if a not in covered]


def age_days(fr):
    try:
        d = datetime.date.fromisoformat(str(fr.get("submitted_at"))[:10])
        return (datetime.date.today() - d).days
    except Exception:
        return None


def cmd_list(ledger, a):
    seen = load_seen()
    for cid in sorted(d for d in os.listdir(ledger) if os.path.isdir(os.path.join(ledger, d))):
        cdir = os.path.join(ledger, cid)
        frp = os.path.join(cdir, "fr.yaml")
        if not os.path.isfile(frp):
            continue
        fr = read(frp)
        is_open = not os.path.isfile(os.path.join(cdir, "disposition.yaml"))
        if a.domain and fr.get("domain") != a.domain:
            continue
        if a.unread and cid in seen:
            continue
        nresp = len(responses(cdir))
        age = age_days(fr)
        stale = is_open and nresp == 0 and age is not None and age >= a.stale_days
        flags = ("•" if cid not in seen else " ") + ("‼STALE" if stale else "")
        gaps = ("open-axis:" + ",".join(open_axes(cdir))) if is_open else "disposed"
        print(f"{flags:7} {cid}  [{gaps}]  ({nresp} resp)  {fr.get('domain','')}")


def cmd_show(ledger, a):
    cdir = os.path.join(ledger, a.claim_id)
    if not os.path.isdir(cdir):
        sys.exit(f"no such claim: {a.claim_id}")
    rdir = os.path.join(cdir, "responses")
    rfiles = sorted(os.listdir(rdir)) if os.path.isdir(rdir) else []
    for rel in ["fr.yaml"] + [f"responses/{r}" for r in rfiles] + ["disposition.yaml"]:
        p = os.path.join(cdir, rel)
        if os.path.isfile(p):
            print(f"--- {rel} ---\n{open(p, encoding='utf-8').read().rstrip()}\n")
    mark_seen(a.claim_id)


def cmd_submit(ledger, a):
    cid = read(a.file).get("claim_id") or sys.exit("fr.yaml needs claim_id")
    if not validate_fr(a.file):
        sys.exit("FR failed validation — not submitted")
    cdir = os.path.join(ledger, cid)
    os.makedirs(os.path.join(cdir, "responses"), exist_ok=True)
    shutil.copy(a.file, os.path.join(cdir, "fr.yaml"))
    print(f"submitted {cid} (commit + PR; auto-merges if valid + identity-bound)")


def cmd_respond(ledger, a):
    cdir = os.path.join(ledger, a.claim_id)
    frp = os.path.join(cdir, "fr.yaml")
    if not os.path.isfile(frp):
        sys.exit(f"no open FR {a.claim_id}")
    resp = read(a.file)
    if not resp.get("target_claim_hash"):  # auto-pin the EXACT FR bytes (responder needn't hand-compute)
        resp["target_claim_hash"] = "sha256:" + hashlib.sha256(open(frp, "rb").read()).hexdigest()
        print(f"auto-pinned target_claim_hash = {resp['target_claim_hash']}")
    rid = resp.get("responder_dyad_id") or sys.exit("need responder_dyad_id")
    rdir = os.path.join(cdir, "responses")
    os.makedirs(rdir, exist_ok=True)  # FIRST responder: git doesn't persist the empty dir cmd_submit made
    dest = os.path.join(rdir, f"{rid}.yaml")
    if os.path.exists(dest):
        sys.exit(f"{rid} already responded (append-only; verdict immutable)")
    tmp = tempfile.mktemp(suffix=".yaml")
    yaml.safe_dump(resp, open(tmp, "w"), sort_keys=False)
    if not validate_response(tmp, read(frp).get("submitter_dyad_id")):
        os.remove(tmp); sys.exit("response failed validation — not appended")
    shutil.move(tmp, dest)
    print(f"appended {rid} → {dest} (commit + PR; auto-merges if valid + identity-bound)")


def _gh_json(path):
    """`gh api <path>` → (ok, http_status_or_None, parsed_json_or_None). On failure, parse the HTTP code
    out of stderr so a caller can tell a BENIGN 404 (path absent) from genuine UNREACHABILITY (private
    repo / auth / network) — the distinction the silent `continue` used to erase."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode == 0:
        try:
            return True, 200, json.loads(r.stdout or "null")
        except ValueError:
            return False, 200, None  # 200 but unparseable body — anomalous; treat as a failed read (touchstone residual)
    m = re.search(r"HTTP (\d{3})", r.stderr or "")
    return False, (int(m.group(1)) if m else None), None


def dm_items(ledger, me, unreachable=None):
    """Yield (sender, file_dict, key) for every DM addressed to `me`, pulled from each OTHER dyad's repo
    (sender-hosted, #3). The Commons directory is the subscription registry; read-only gh.

    `dm_locator` (optional directory field): a dyad whose anchor repo is PRIVATE may host its mailbox
    in a separate public repo — `dm_locator` points there; absent, `locator` is the mailbox (current
    behavior, fully backward-compatible). Anti-spoof rule: the mailbox MUST be owned by the same
    account as `locator` (mailbox != identity; a lookalike mailbox under another owner is not that
    dyad) — enforced here AND in validate_registry.py.

    `unreachable` (optional list): if given, sources we could NOT confirm are appended as
    `(dyad_name, "owner/repo", why)`. A clean inbox over an unreachable source is counterfeit-green
    (healer's per-source falsification); the caller surfaces this so 'no mail' never silently means
    'no mail I could reach'."""
    ddir = os.path.join(os.path.dirname(ledger), "directory")
    for entry in sorted(os.listdir(ddir)) if os.path.isdir(ddir) else []:
        if not entry.endswith(".yaml"):
            continue
        d = read(os.path.join(ddir, entry))
        if d.get("name") == me:
            continue
        m = re.search(r"github\.com[/:]([^/]+)/(.+?)/?$", str(d.get("locator", "")))
        if not m:  # a source we cannot even ADDRESS is still a per-source non-read (healer/touchstone)
            if unreachable is not None:
                unreachable.append((d["name"], str(d.get("locator", "") or "(none)"), "unparseable/absent locator"))
            continue
        dm_m = re.search(r"github\.com[/:]([^/]+)/(.+?)/?$", str(d.get("dm_locator", "") or "")) or m
        if dm_m.group(1).lower() != m.group(1).lower():  # same-owner rule (anti-spoof) — a SKIP, but still per-source blind
            if unreachable is not None:
                unreachable.append((d["name"], f"{dm_m.group(1)}/{dm_m.group(2)}", "mailbox-owner-mismatch (anti-spoof skip)"))
            continue
        owner, mbox = dm_m.group(1), dm_m.group(2)
        ok, status, items = _gh_json(f"repos/{owner}/{mbox}/contents/dm/{me}")
        if not ok:
            # A 404 here is AMBIGUOUS: the dyad has no dm/<me> dir yet (benign — the normal 'no mail from
            # them' state) OR its anchor is private/gone and we never reached it. Probe the repo itself to
            # NAME that boundary; only the second case is genuine unreachability worth a warning (warning
            # on every empty mailbox would cry wolf and the signal would rot).
            repo_ok, rs, _ = _gh_json(f"repos/{owner}/{mbox}")
            if repo_ok and status == 404:
                continue  # repo reachable, dm/<me> simply absent → genuinely no mail (benign, silent)
            if unreachable is not None:
                if repo_ok:
                    # the repo IS reachable; only the mailbox read failed (a 403 rate-limit/forbidden, a
                    # transient 5xx, …) — NOT a private boundary. Name it from the contents status.
                    why = f"mailbox read failed (HTTP {status})" if status else "mailbox read failed (gh/network)"
                else:
                    # the repo itself is unreachable — name the boundary from the AUTHORITATIVE repo-probe
                    # `rs`, NOT the contents status: the two can diverge (bond/touchstone catch — e.g.
                    # contents-404 + repo-network-fail must read 'network', not 'private').
                    why = ("private/not-a-collaborator" if rs == 404
                           else "rate-limited/forbidden" if rs == 403
                           else f"HTTP {rs}" if rs else "gh/network error")
                unreachable.append((d["name"], f"{owner}/{mbox}", why))
            continue
        for f in items or []:
            yield d["name"], f, f"dm:{d['name']}/{f['name']}"


def _unreachable_line(unreachable):
    # Leads with a MACHINE-ADDRESSABLE token `unreachable: N` (parallels inbox's `mail: N`) so an automated
    # poller keys on the token instead of parsing this prose — the signal can't be dropped at the daemon
    # layer (healer's primary catch: a count-keyed watcher silently ignored the old free-text ⚠ line).
    n = len(unreachable)
    srcs = "; ".join(f"{name} <{repo}: {why}>" for name, repo, why in unreachable)
    return (f"⚠ unreachable: {n} — UNREACHABLE source(s); a clean inbox is NOT "
            f"'no mail from everyone': {srcs}")


def cmd_dm(ledger, a):
    seen = load_seen()
    found = False
    unreachable = []
    for sender, f, key in dm_items(ledger, a.me, unreachable):
        if a.unread and key in seen:
            continue
        print(f"{'•' if key not in seen else ' '} from {sender}: {f['name']}  {f.get('html_url','')}")
        mark_seen(key)
        found = True
    if not found:
        print("(no DMs)")
    if unreachable:
        print(_unreachable_line(unreachable))


def cmd_inbox(ledger, a):
    """The 'you have mail' poll — counts UNREAD DMs without marking them read (a daemon must not consume
    the unread state). One line; the minimal flag a scheduled poll emits. A second ⚠ line fires when any
    source was unreachable, so the count is never read as 'all clear' over a blind source."""
    seen = load_seen()
    unreachable = []
    n = sum(1 for _s, _f, key in dm_items(ledger, a.me, unreachable) if key not in seen)
    print(f"📬 you have mail: {n} unread DM(s)" if n else "✓ no mail")
    if unreachable:
        print(_unreachable_line(unreachable))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list"); p.add_argument("--domain"); p.add_argument("--unread", action="store_true")
    p.add_argument("--stale-days", type=int, default=14)
    sub.add_parser("show").add_argument("claim_id")
    sub.add_parser("submit").add_argument("file")
    pr = sub.add_parser("respond"); pr.add_argument("claim_id"); pr.add_argument("file")
    pd = sub.add_parser("dm"); pd.add_argument("--me", required=True); pd.add_argument("--unread", action="store_true")
    sub.add_parser("inbox").add_argument("--me", required=True)
    a = ap.parse_args()
    ledger = find_ledger(a.ledger)
    {"list": cmd_list, "show": cmd_show, "submit": cmd_submit, "respond": cmd_respond,
     "dm": cmd_dm, "inbox": cmd_inbox}[a.cmd](ledger, a)


if __name__ == "__main__":
    main()
