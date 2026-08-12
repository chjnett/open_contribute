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
    required = ["name", "description"]
    missing = [k for k in required if k not in meta]
    if missing:
        print(f"Missing required frontmatter fields: {', '.join(missing)}")
        sys.exit(1)

    # The Agent Skills spec allows only these top-level keys. A stray key (a
    # top-level `version:` is the easy mistake) makes the official packager
    # refuse the skill, so reject it here rather than shipping a broken .skill.
    allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    unexpected = sorted(set(meta) - allowed)
    if unexpected:
        print(f"Unexpected frontmatter key(s): {', '.join(unexpected)}. "
              f"Allowed: {', '.join(sorted(allowed))}. "
              f"Version belongs under `metadata.version`.")
        sys.exit(1)

    if not (meta.get("metadata") or {}).get("version"):
        print("Missing `metadata.version` in frontmatter.")
        sys.exit(1)

    import os
    skill_dir = os.path.dirname(path)
    # Match the skill by exact folder name — a substring test would also catch
    # `first-contribution-ko` and demand references it does not carry.
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    required_refs = {
        "first-contribution": [
            "domain-categories.md", "subcategory-map.md", "pr-acceptance-checklist.md",
            "issue-triage-checklist.md", "message-templates.md", "repo-evaluation-criteria.md",
        ],
        "first-contribution-ko": [
            "domain-categories.md", "subcategory-map.md", "pr-acceptance-checklist.md",
            "issue-triage-checklist.md", "message-templates.md", "repo-evaluation-criteria.md",
        ],
        "rag-contribution": [
            "rag-evaluation-criteria.md", "pr-acceptance-checklist.md",
            "issue-triage-checklist.md", "message-templates.md",
        ],
    }
    for ref in required_refs.get(skill_name, []):
        ref_path = os.path.join(skill_dir, "references", ref)
        if not os.path.isfile(ref_path):
            print(f"Missing reference file: {ref_path}")
            sys.exit(1)

    print(f"{skill_name}: frontmatter and references validation passed.")

if __name__ == "__main__":
    main()
