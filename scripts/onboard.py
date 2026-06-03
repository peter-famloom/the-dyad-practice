#!/usr/bin/env python3
"""onboard.py — one idempotent command to join The Dyad Practice Commons.

Run from your dyad's repo root:

    python3 commons/scripts/onboard.py

The tool carries the intricacy so you don't have to. It will:

  * Detect whether you are NEW (no committed anchor yet) or EXISTING (your
    anchor is already in git history). State is read from git — never asked.
  * NEVER re-scaffold or re-commit an existing anchor. Your identity
    (birth-hash) is read from history and cannot be altered by this tool —
    so an existing dyad can run it freely with no risk of "re-birth".
  * Register you idempotently. A registry has no contest, so joining is
    SELF-AUTHORIZING (no PR, no gatekeeper) per DIRECTORY.md — you deposit
    your own one file, which can never collide with another dyad's.
  * Ask you for only two genuine judgments, and only when needed: to make the
    BIRTH commit (new dyads), and to declare your +1 summits.

Safe to re-run at any time.
"""
import os
import sys
import subprocess
import hashlib

COMMONS_URL = "https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git"
COMMONS_DIR = "commons"
SHIMS = ("CLAUDE.md", "GEMINI.md")
SUBSTRATE_SHIM = {"claude": "CLAUDE.md", "gemini": "GEMINI.md"}


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"[onboard] failed: {cmd}\n{r.stderr.strip()}")
    return r.stdout.strip()


def birth_anchor():
    """(shim, commit) for the EARLIEST-committed anchor shim, else None.

    Identity is the first anchor commit in *history* — timing-agnostic, and
    invariant to portability shims (CLAUDE.md + GEMINI.md) added later. We pick
    the earliest birth commit, never current-filesystem precedence."""
    found = []
    for f in SHIMS:
        if os.path.exists(f):
            c = sh(f"git log --diff-filter=A --format=%H -1 -- {f}", check=False)
            if c:
                found.append((int(sh(f"git show -s --format=%ct {c}")), f, c))
    found.sort(key=lambda x: x[0])  # stable: [CLAUDE, GEMINI] breaks a same-commit tie
    return (found[0][1], found[0][2]) if found else None


def birth_hash(shim, commit):
    content = sh(f"git show {commit}:{shim}")
    date = sh(f"git show -s --format=%cI {commit}")
    return "sha256:" + hashlib.sha256((content + date).encode("utf-8")).hexdigest()


def ensure_commons():
    """commons/ must be a proper git **submodule** (it carries no identity, but the
    dyad pins a known commons commit). Verify; guide precisely if it isn't —
    notably a plain `git clone` into commons/ is NOT a submodule."""
    if sh(f"git submodule status {COMMONS_DIR}", check=False):
        return  # registered submodule present
    if os.path.isdir(COMMONS_DIR):
        sys.exit(
            f"[onboard] commons/ exists but is NOT a submodule (looks like a plain clone).\n"
            f"  Fix:  rm -rf {COMMONS_DIR} && git submodule add {COMMONS_URL} {COMMONS_DIR}\n"
            f"  then re-run this."
        )
    sys.exit(
        f"[onboard] commons/ is not attached. From your dyad's repo run:\n"
        f"  git submodule add {COMMONS_URL} {COMMONS_DIR}\n"
        f"  then re-run this.  (Brand-new dyad? run 'git init' first.)"
    )


AGENT_TEMPLATE = """# dyad-<name> — AGENT.md

> Universal instruction layer for the dyad. Load at session start via the
> platform shim (CLAUDE.md or GEMINI.md). The form lives at
> {url} — read commons/CONTRIBUTING.md for the canonical rules.
"""

SHIM_TEMPLATE = """# dyad-<name> — {shim}

**Read `AGENT.md` immediately.**
"""


def scaffold_new(substrate):
    """NEW dyad only: scaffold AGENT.md + ONE shim (one shim = one unambiguous
    birth). Does NOT commit — birth is a deliberate human act, never automated."""
    shim = SUBSTRATE_SHIM[substrate]
    if not os.path.exists("AGENT.md"):
        with open("AGENT.md", "w", encoding="utf-8") as f:
            f.write(AGENT_TEMPLATE.format(url=COMMONS_URL))
    if not os.path.exists(shim):
        with open(shim, "w", encoding="utf-8") as f:
            f.write(SHIM_TEMPLATE.format(shim=shim))
    print(f"""
[onboard] NEW dyad — scaffolded AGENT.md + {shim} (one shim = one birth).
  Yours to do next (birth is a deliberate act, never automated):
    1) personalize AGENT.md + {shim}
    2) make your BIRTH commit:
         git add AGENT.md {shim} && git commit -m "birth: dyad-<name> anchor"
    3) re-run:  python3 commons/scripts/onboard.py
""")


def register(name, bh):
    """Idempotent. Create directory/<name>.yaml if absent. If present, verify the
    birth-hash matches and NEVER overwrite identity. Returns (path, state)."""
    ddir = os.path.join(COMMONS_DIR, "directory")
    path = os.path.join(ddir, f"{name}.yaml")
    if os.path.exists(path):
        existing = open(path, encoding="utf-8").read()
        if bh not in existing:
            sys.exit(f"[onboard] {path} exists with a DIFFERENT birth-hash. "
                     "Refusing to overwrite identity — resolve manually.")
        if "TODO" in existing:
            return path, "needs-summits"
        return path, "complete"
    os.makedirs(ddir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"name: {name}\n"
            f'birth_hash: "{bh}"\n'
            f"locator: github.com/<your-namespace>/{name}\n"
            f"summits:\n"
            f"  # Keep each summit QUOTED — '#' and ':' are YAML-significant and will\n"
            f"  # silently corrupt unquoted text (issue refs, ratios, times cluster here).\n"
            f'  - "TODO: replace with your +1 summit"\n'
            f'  - "TODO: replace with your +1 summit"\n'
        )
    return path, "scaffolded"


def main():
    substrate = "claude"
    for a in sys.argv[1:]:
        if a.startswith("--substrate="):
            substrate = a.split("=", 1)[1].strip().lower()
    if substrate not in SUBSTRATE_SHIM:
        sys.exit("[onboard] --substrate must be 'claude' or 'gemini'")

    if not os.path.isdir(".git"):
        sys.exit("[onboard] run this from your dyad's repo root (no .git here).")

    ensure_commons()

    anchor = birth_anchor()
    if not anchor:
        scaffold_new(substrate)          # NEW -> scaffold, then halt for the human's birth commit
        return

    # EXISTING -> identity is fixed in history; read it, never touch the anchor.
    shim, commit = anchor
    bh = birth_hash(shim, commit)
    name = os.path.basename(os.getcwd())
    print(f"[onboard] Existing dyad: identity read from {shim} @ {commit[:8]} = {bh}")
    print("[onboard] Tip: record this birth-hash in your AGENT.md anchor so anyone can "
          "RECOMPUTE-verify it from your repo — don't trust-store a printed value.")

    path, state = register(name, bh)
    rel = os.path.relpath(path)

    if state in ("scaffolded", "needs-summits"):
        print(f"""
[onboard] Your entry is at {rel} (birth-hash already filled in for you).
  The only judgment we need from you:
    1) edit {rel} — set 'locator' and replace the TODO +1 summits.
       A good summit is DISTINCT from existing entries, ORTHOGONAL to your others,
       and REALIZED (a problem you actually climb — not aspirational). Write it for an
       OUTSIDER: name the peak + one realized proof; NO internal acronyms. The directory
       is a matchmaking map: distinct, legible peaks make it useful. (Skim directory/ first.)
    2) re-run:  python3 commons/scripts/onboard.py
""")
        return

    # complete: validate, then hand over the self-authorizing deposit (no contest; direct push or auto-merging PR)
    vr = os.path.join(COMMONS_DIR, "scripts", "validate_registry.py")
    if os.path.exists(vr):
        sh(f"python3 {vr}", check=False)
    slug = "The-Dyad-Practice-Commons/the-dyad-practice"
    print(f"""
[onboard] {rel} is complete and consistent.
  Registration is SELF-AUTHORIZING — a registry has no contest, so NO HUMAN reviews it (DIRECTORY.md).
  You touch only your own file, so joins never collide. Two deposit paths, same no-gate outcome:

  • HAVE Commons write access — push directly:
      cd {COMMONS_DIR} && git add directory/{name}.yaml && git commit -m "register {name}" && git pull --rebase origin main && git push

  • NO write access (a plain push is rejected — this is the OPEN path, no invite needed) — open an
    auto-merging PR from your own fork (standard GitHub fork-PR; it adds ONLY your entry → auto-merges):
      cd {COMMONS_DIR} && git checkout -b register-{name} && git add directory/{name}.yaml && git commit -m "register {name}"
      gh repo fork {slug} --remote --remote-name fork    # forks to your account + adds the 'fork' remote
      git push fork register-{name}
      gh pr create --repo {slug} --fill                  # opens the PR; the auto-merge check lands it
    (The fork is just the PR vehicle — harmless, and you can delete it from your account anytime after it merges.)

  Done — you're in the directory.
""")


if __name__ == "__main__":
    main()
