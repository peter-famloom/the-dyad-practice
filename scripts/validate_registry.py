#!/usr/bin/env python3
import os
import sys
import yaml

REQUIRED_FIELDS = {'name', 'birth_hash', 'locator', 'summits'}

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
            
        for field in ['name', 'birth_hash', 'locator']:
            if not isinstance(data[field], str) or not data[field].strip():
                print(f"FAIL {filepath}: '{field}' must be a non-empty string.")
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
