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
    anchor_file = None
    for f in ["CLAUDE.md", "GEMINI.md"]:
        if os.path.exists(f):
            anchor_file = f
            break
    
    if not anchor_file:
        print("Error: Could not find CLAUDE.md or GEMINI.md in the current directory.")
        sys.exit(1)

    first_commit = run_cmd(f"git log --diff-filter=A --format=%H -1 -- {anchor_file}")
    if not first_commit:
        print(f"Warning: {anchor_file} is not committed yet. Please commit your anchor file to generate a birth-hash.")
        sys.exit(1)

    content = run_cmd(f"git show {first_commit}:{anchor_file}")
    date_str = run_cmd(f"git show -s --format=%cI {first_commit}")

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
