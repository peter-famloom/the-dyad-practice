#!/usr/bin/env python3
"""automerge_self_update_run.py — CI driver for auto-merge-self-update.yml (I/O around the pure gate).

STAGED FOR THE COMMONS — install path: the-dyad-practice/scripts/automerge_self_update_run.py
Reads the PR's changed files + the base/head entry (trusted base content via the API, never executing
PR code), validates the head entry with the Commons validator, asks the pure gate `decide()`, then either
self-merges (own-entry update, frozen fields intact) or comments and leaves it for human review.

Env: REPO, PR, AUTHOR, BASE_SHA, HEAD_SHA, GH_TOKEN. Exit 0 always (fail-safe: only ever UNDER-merges).
"""
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from automerge_self_update_gate import decide  # noqa: E402
from validate_registry import validate_file  # noqa: E402

REPO = os.environ["REPO"]
PR = os.environ["PR"]
AUTHOR = os.environ["AUTHOR"]
BASE_SHA = os.environ["BASE_SHA"]
HEAD_SHA = os.environ["HEAD_SHA"]


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def comment(body):
    subprocess.run(["gh", "pr", "comment", PR, "--body", body], check=False)


def entry_at(filename, ref):
    try:
        raw = gh("api", f"repos/{REPO}/contents/{filename}?ref={ref}", "--jq", ".content")
        return yaml.safe_load(base64.b64decode(raw))
    except Exception:
        return None


def main():
    files = [{"filename": f["filename"], "status": f["status"]}
             for f in json.loads(gh("api", f"repos/{REPO}/pulls/{PR}/files", "--paginate"))]

    base_entry = head_entry = None
    validate_ok = False
    if len(files) == 1 and files[0]["filename"].startswith("directory/"):
        fn = files[0]["filename"]
        base_entry = entry_at(fn, BASE_SHA)
        head_entry = entry_at(fn, HEAD_SHA)
        if isinstance(head_entry, dict):
            # validate_file enforces filename == '<name>.yaml'; write under the real basename
            tmp = os.path.join(tempfile.mkdtemp(), os.path.basename(fn))
            with open(tmp, "w") as f:
                yaml.safe_dump(head_entry, f)
            validate_ok = bool(validate_file(tmp))
            shutil.rmtree(os.path.dirname(tmp), ignore_errors=True)

    merge, reason = decide(files, base_entry, head_entry, AUTHOR, validate_ok)
    if not merge:
        comment(f"🤖 **Not a self-authorizing self-update** — {reason}. "
                f"Routed to human review (CONTRIBUTING §2).")
        print("::notice::review —", reason)
        return
    r = subprocess.run(["gh", "pr", "merge", PR, "--squash", "--delete-branch"], check=False)
    if r.returncode != 0:
        subprocess.run(["gh", "pr", "merge", PR, "--squash"], check=False)
    comment(f"✅ **Self-authorizing self-update** — {reason}. No human gate (you own this entry).")
    print("::notice::merged —", reason)


if __name__ == "__main__":
    main()
