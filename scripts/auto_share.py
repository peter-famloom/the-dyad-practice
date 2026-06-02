#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def compute_birth_hash():
    # We navigate up because this script is run from within the dyad root, but wait...
    # Actually, the user runs `commons/scripts/auto_share.py` from their Dyad root.
    anchor_file = None
    for f in ["CLAUDE.md", "GEMINI.md"]:
        if os.path.exists(f):
            anchor_file = f
            break
    
    if not anchor_file:
        print("Error: Could not find CLAUDE.md or GEMINI.md in the current directory.")
        sys.exit(1)

    first_commit = run_cmd(f"git log --diff-filter=A --format=%H -1 -- {anchor_file}")
    content = run_cmd(f"git show {first_commit}:{anchor_file}")
    date_str = run_cmd(f"git show -s --format=%cI {first_commit}")
    raw_data = content + date_str
    hash_val = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    return f"sha256:{hash_val}"

def main():
    if len(sys.argv) < 2:
        print("Usage: ./commons/scripts/auto_share.py <discipline-name>")
        sys.exit(1)
        
    discipline_name = sys.argv[1]
    
    if not os.path.isdir("commons"):
        print("Error: 'commons' submodule not found.")
        sys.exit(1)

    print("Computing birth-hash for provenance...")
    birth_hash = compute_birth_hash()
    
    # We are scaffold the library inside the commons submodule
    lib_dir = f"commons/library/{discipline_name}"
    ledger_dir = f"{lib_dir}/ledger"
    
    os.makedirs(ledger_dir, exist_ok=True)
    
    playbook_file = f"{lib_dir}/PLAYBOOK.md"
    if not os.path.exists(playbook_file):
        print(f"Scaffolding {playbook_file}...")
        content = f"""---
origin: "{birth_hash}"
unit-kind: playbook
schema-version: discipline-ontology@2026-05-31
trigger: "Fill in the trigger condition here"
---
# Playbook: {discipline_name}

## The Move
*(Write the one-liner recipe here - the move that creates the +1)*

## Context
*(Explain when to use this playbook and what problem it solves)*
"""
        with open(playbook_file, "w", encoding="utf-8") as f:
            f.write(content)
            
    ledger_file = f"{ledger_dir}/{birth_hash.replace('sha256:', '')}-1.md"
    if not os.path.exists(ledger_file):
        print(f"Scaffolding {ledger_file}...")
        ledger_content = f"""# Testimonial 1
- **contributor:** `{birth_hash}`

## The Output
*(Describe how this playbook produced a +1 in your specific use case)*
"""
        with open(ledger_file, "w", encoding="utf-8") as f:
            f.write(ledger_content)

    print("\n--- ACTION REQUIRED ---")
    print(f"1. Open {playbook_file} and define the playbook.")
    print(f"2. Open {ledger_file} and write your testimonial (evidence).")
    print(f"3. cd commons && git checkout -b share/{discipline_name}")
    print("4. git add library/ && git commit -m 'Share: {discipline_name}' && git push && gh pr create")

if __name__ == "__main__":
    main()
