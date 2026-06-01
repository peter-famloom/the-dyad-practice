#!/usr/bin/env python3
import os
import sys
import subprocess

COMMONS_REPO_URL = "https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git"
COMMONS_DIR = "commons"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def setup_submodule():
    if os.path.isdir(COMMONS_DIR):
        print(f"[{COMMONS_DIR}] already exists. Updating submodule...")
        run_cmd("git submodule update --init --remote " + COMMONS_DIR)
    else:
        print(f"Adding submodule [{COMMONS_DIR}]...")
        run_cmd(f"git submodule add {COMMONS_REPO_URL} {COMMONS_DIR}")

def scaffold_files():
    agent_content = """# dyad-[name] — AGENT.md

> **Universal instruction layer for the dyad.** Load this at session start via the platform-specific shims (`CLAUDE.md` / `GEMINI.md`).
> 
> The form lives at <https://github.com/The-Dyad-Practice-Commons/the-dyad-practice>. Read `commons/CONTRIBUTING.md` for the canonical rules.

---
"""
    shim_content = """# dyad-[name] — {filename}

**Read `AGENT.md` immediately.**

> ⚠️ **IDENTITY CAVEAT:** The Dyad's identity is **frozen at birth from the *original* anchor first commit**.
> `dyad-[name] identity = sha256(git show <first_commit>:{filename} ‖ <committer-date>)`
"""
    
    if not os.path.exists("AGENT.md"):
        print("Scaffolding AGENT.md...")
        with open("AGENT.md", "w", encoding="utf-8") as f:
            f.write(agent_content)
    else:
        print("AGENT.md already exists. Skipping.")

    for shim in ["CLAUDE.md", "GEMINI.md"]:
        if not os.path.exists(shim):
            print(f"Scaffolding {shim}...")
            with open(shim, "w", encoding="utf-8") as f:
                f.write(shim_content.format(filename=shim))
        else:
            print(f"{shim} already exists. Skipping.")

def main():
    if not os.path.isdir(".git"):
        print("Initializing git repository...")
        run_cmd("git init")
        
    setup_submodule()
    scaffold_files()
    
    print("Dyad Initialization complete.")
    print("If this is a new Dyad, replace '[name]' with your dyad's name in AGENT.md and the shims.")
    print("To join the commons, run: python3 commons/scripts/auto_join.py")

if __name__ == "__main__":
    main()
