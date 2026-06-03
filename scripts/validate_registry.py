#!/usr/bin/env python3
import os
import re
import sys
import yaml

REQUIRED_FIELDS = {'name', 'birth_hash', 'locator', 'summits'}
# A dyad name: 'dyad-' prefix + kebab-case segments. Keeps the directory self-documenting and
# spoof-resistant (a generic/garbage row like "Project Template" can't land). Filename must equal
# '<name>.yaml'; the birth-hash must be a real sha256 digest, not a placeholder.
NAME_RE = re.compile(r'^dyad-[a-z0-9]+(-[a-z0-9]+)*$')
HASH_RE = re.compile(r'^sha256:[0-9a-f]{64}$')

def validate_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not isinstance(data, dict):
            print(f"FAIL {filepath}: Root must be a dictionary.")
            return False
            
        missing = REQUIRED_FIELDS - set(data.keys())
        if missing:
            print(f"FAIL {filepath}: Missing required fields {missing}")
            return False
            
        if not isinstance(data['summits'], list) or not data['summits']:
            print(f"FAIL {filepath}: 'summits' must be a non-empty list of strings.")
            return False

        for s in data['summits']:
            if not isinstance(s, str) or not s.strip():
                print(f"FAIL {filepath}: every summit must be a non-empty string, got "
                      f"{type(s).__name__}: {s!r}. (Unquoted '#' or ':' in YAML silently "
                      f"corrupts a summit into a comment/dict — quote the scalar.)")
                return False

        for field in ['name', 'birth_hash', 'locator']:
            if not isinstance(data[field], str) or not data[field].strip():
                print(f"FAIL {filepath}: '{field}' must be a non-empty string.")
                return False

        if not NAME_RE.match(data['name']):
            print(f"FAIL {filepath}: name {data['name']!r} must be 'dyad-<kebab>' "
                  f"(lowercase, e.g. dyad-krishna) — {NAME_RE.pattern}.")
            return False

        expected = data['name'] + '.yaml'
        if os.path.basename(filepath) != expected:
            print(f"FAIL {filepath}: filename must equal '{expected}' (match the 'name' field) — "
                  "deposit only your own file.")
            return False

        if not HASH_RE.match(data['birth_hash']):
            print(f"FAIL {filepath}: birth_hash {data['birth_hash']!r} must be a real "
                  "'sha256:<64 hex>' digest, not a placeholder.")
            return False

        if 'dm_locator' in data:  # optional: public mailbox for private-anchor dyads
            if not isinstance(data['dm_locator'], str) or not data['dm_locator'].strip():
                print(f"FAIL {filepath}: 'dm_locator' (optional) must be a non-empty string when present.")
                return False
            # SAME regex shape as falsify.py dm_items (owner AND repo) — a repo-less dm_locator that
            # passes validation but can't resolve at read time is a silent black-hole (bond, PR #44).
            # Scope of this rule (touchstone, PR #44): it blocks FOREIGN-OWNER lookalike mailboxes —
            # one pre-filter layer, not the whole anti-spoof bar. Root of trust remains account
            # ownership + the deposit merge-gate; intra-account dyad routing is by recipient dir name;
            # binding the mailbox to birth_hash is named future hardening.
            owner = re.search(r"github\.com[/:]([^/]+)/(.+?)/?$", data['locator'])
            dm = re.search(r"github\.com[/:]([^/]+)/(.+?)/?$", data['dm_locator'])
            if not dm:
                print(f"FAIL {filepath}: 'dm_locator' must be 'github.com/<owner>/<repo>' — owner-only "
                      "values pass no mail (falsify.py requires owner+repo to resolve the mailbox).")
                return False
            if not owner or dm.group(1).lower() != owner.group(1).lower():
                print(f"FAIL {filepath}: 'dm_locator' must be owned by the same account as 'locator' "
                      "(blocks foreign-owner lookalike mailboxes — one anti-spoof layer).")
                return False

        print(f"PASS {filepath}")
        return True
    except yaml.YAMLError as e:
        print(f"FAIL {filepath}: Invalid YAML syntax - {e}")
        return False
    except Exception as e:
        print(f"FAIL {filepath}: {e}")
        return False

def main():
    directory_path = os.path.join(os.path.dirname(__file__), '..', 'directory')
    if not os.path.exists(directory_path):
        print(f"Error: directory path {directory_path} not found.")
        sys.exit(1)
        
    all_passed = True
    yaml_files = [f for f in os.listdir(directory_path) if f.endswith('.yaml')]
    
    if not yaml_files:
        print("No YAML files found in directory/")
        sys.exit(0)
        
    for filename in yaml_files:
        filepath = os.path.join(directory_path, filename)
        if not validate_file(filepath):
            all_passed = False
            
    if all_passed:
        print("All registry files are valid.")
        sys.exit(0)
    else:
        print("Validation failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
