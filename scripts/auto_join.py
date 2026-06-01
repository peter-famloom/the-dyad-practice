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
    # Birth anchor = the shim added in the EARLIEST anchor commit (a historical fact),
    # NOT current-filesystem precedence. A dyad may later add the other shim for LLM
    # portability (CLAUDE.md + GEMINI.md); that later addition must NEVER change identity.
    # Selecting by precedence would re-key a GEMINI-born dyad's identity onto a
    # later-added CLAUDE.md (identity corruption). So we pick by earliest birth commit.
    candidates = []
    for f in ["CLAUDE.md", "GEMINI.md"]:
        if os.path.exists(f):
            first_commit = run_cmd(f"git log --diff-filter=A --format=%H -1 -- {f}")
            if first_commit:
                epoch = run_cmd(f"git show -s --format=%ct {first_commit}")
                candidates.append((int(epoch), f, first_commit))

    if not candidates:
        print("Error: no committed CLAUDE.md or GEMINI.md anchor found to derive a birth-hash.")
        print("New dyad: commit your anchor first. Existing dyad: check out the repo with its history.")
        sys.exit(1)

    # Earliest birth commit wins. Python's stable sort preserves [CLAUDE, GEMINI] order,
    # giving a deterministic tiebreak for the DIP-excluded both-shims-in-one-commit case.
    candidates.sort(key=lambda c: c[0])
    _, anchor_file, first_commit = candidates[0]
    print(f"Birth anchor: {anchor_file} @ {first_commit[:8]} (earliest anchor commit)")

    content = run_cmd(f"git show {first_commit}:{anchor_file}")
    date_str = run_cmd(f"git show -s --format=%cI {first_commit}")  # %cI kept in the hash — formula unchanged

    raw_data = content + date_str
    hash_val = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    return f"sha256:{hash_val}"

def main():
    if not os.path.isdir("commons"):
        print("Error: 'commons' submodule not found. Please run init_dyad.py first.")
        sys.exit(1)
        
    print("Computing birth-hash...")
    birth_hash = compute_birth_hash()
    print(f"Birth hash: {birth_hash}")
    
    dyad_name = os.path.basename(os.getcwd())
    yaml_path = f"commons/directory/{dyad_name}.yaml"
    
    if os.path.exists(yaml_path):
        print(f"File {yaml_path} already exists. Skipping scaffolding.")
    else:
        print(f"Scaffolding {yaml_path}...")
        yaml_content = f"""name: {dyad_name}
birth_hash: "{birth_hash}"
locator: github.com/pltrinh1122/{dyad_name}
summits:
  - TODO: replace with your +1 summit 1
  - TODO: replace with your +1 summit 2
"""
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)
            
    print("\n--- ACTION REQUIRED ---")
    print(f"1. Open {yaml_path} and fill in your 'summits'.")
    print("2. Run 'python3 commons/scripts/validate_registry.py' to verify.")
    print(f"3. cd commons && git checkout -b join/{dyad_name} && git add directory/{dyad_name}.yaml && git commit -m 'Join {dyad_name}' && git push")

if __name__ == "__main__":
    main()
