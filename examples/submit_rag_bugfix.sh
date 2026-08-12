#!/usr/bin/env bash
# Demo script: clone LangChain, make a tiny fix, and open a PR using GitHub CLI (gh).
# Requires:
#   - GitHub CLI (gh) installed (`brew install gh` or equivalent)
#   - gh authenticated (`gh auth login`)

set -euo pipefail

REPO="langchain-ai/langchain"
BRANCH="bugfix/readme-typo-$(date +%s)"

# 1. Check if GitHub CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Please install it (e.g., 'brew install gh' on Mac) and try again."
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "Error: You are not logged into GitHub CLI."
    echo "Please run 'gh auth login' and follow the interactive prompts to authenticate."
    exit 1
fi

# 2. Automated Fork & Clone using gh
echo "Forking and cloning repository using gh..."
gh repo fork "$REPO" --clone=true
cd langchain

# 3. Create a new branch based on upstream main/master
# Check what the default branch is for upstream (assuming master for langchain)
DEFAULT_BRANCH=$(git remote show upstream | sed -n '/HEAD branch/s/.*: //p')
echo "Creating new branch ${BRANCH} from upstream/${DEFAULT_BRANCH}..."
git checkout -b "$BRANCH" "upstream/${DEFAULT_BRANCH}"

# 4. Make a tiny documentation fix
echo "Applying fix to docs..."
sed -i '' 's/LangChain/LangChain (RAG)/g' README.md

git add README.md
git commit -m "docs: clarify LangChain as a RAG framework"

# 5. Push branch to fork (origin)
echo "Pushing branch ${BRANCH} to origin..."
git push -u origin "$BRANCH"

# 6. Open a PR via GitHub CLI
PR_TITLE="docs: clarify LangChain as a RAG framework"
PR_BODY="This PR updates the README to make it explicit that LangChain is a Retrieval‑Augmented Generation (RAG) framework. No functional changes."

echo "Creating Pull Request..."
gh pr create --title "$PR_TITLE" --body "$PR_BODY" --head "$(gh api user | grep -o '"login": "[^"]*' | cut -d'"' -f4):$BRANCH" --base "$DEFAULT_BRANCH"

echo "✅ PR successfully created!"
