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
