#!/usr/bin/env bash
# Package every Claude skill in this repo into a .skill zip file.
# Assumes this script is run from the repository root.
#
# A .skill file is a zip whose top-level entry is the skill folder itself
# (first-contribution/SKILL.md, ...), which is what Claude.ai / Cowork expect.

set -euo pipefail

shopt -s nullglob

found=0
for skill_md in */SKILL.md; do
  skill_dir="$(dirname "$skill_md")"
  output_file="${skill_dir}.skill"
  found=1

  rm -f "$output_file"

  # -x excludes build noise that would otherwise ride along in the archive.
  zip -r "$output_file" "$skill_dir" \
    -x '*.DS_Store' '*/__pycache__/*' '*.pyc' > /dev/null

  echo "Packaged $output_file"
done

if [[ "$found" -eq 0 ]]; then
  echo "No skill folders found (expected at least one */SKILL.md)" >&2
  exit 1
fi
