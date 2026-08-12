#!/usr/bin/env bash
# Package the Claude skill into a .skill zip file
# Assumes this script is run from the repository root

set -euo pipefail

SKILL_DIR="first-contribution"
OUTPUT_FILE="first-contribution.skill"

# Remove any previous artifact
if [[ -f "$OUTPUT_FILE" ]]; then
  rm -f "$OUTPUT_FILE"
fi

# Zip the skill folder preserving directory structure
zip -r "$OUTPUT_FILE" "$SKILL_DIR" > /dev/null

echo "Packaged $OUTPUT_FILE"
