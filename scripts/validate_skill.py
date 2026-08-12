#!/usr/bin/env python3
import sys, yaml, re

def load_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # frontmatter is between the first two lines containing ---
    if not lines[0].strip() == "---":
        raise ValueError("SKILL.md must start with '---' frontmatter delimiter")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("Closing '---' not found in SKILL.md frontmatter")
    front = "".join(lines[1:end_idx])
    data = yaml.safe_load(front)
    return data, lines[end_idx+1:]

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <path-to-SKILL.md>")
        sys.exit(1)
    path = sys.argv[1]
    try:
        meta, _ = load_frontmatter(path)
    except Exception as e:
        print(f"Error parsing frontmatter: {e}")
        sys.exit(1)
    required = ["name", "description", "version"]
    missing = [k for k in required if k not in meta]
    if missing:
        print(f"Missing required frontmatter fields: {', '.join(missing)}")
        sys.exit(1)
    
    import os
    skill_dir = os.path.dirname(path)
    if "first-contribution" in skill_dir:
        required_refs = [
            os.path.join(skill_dir, "references", "domain-categories.md"),
            os.path.join(skill_dir, "references", "subcategory-map.md"),
            os.path.join(skill_dir, "references", "pr-acceptance-checklist.md")
        ]
        for ref_path in required_refs:
            if not os.path.isfile(ref_path):
                print(f"Missing reference file: {ref_path}")
                sys.exit(1)

    print("SKILL.md frontmatter and references validation passed.")

if __name__ == "__main__":
    main()
