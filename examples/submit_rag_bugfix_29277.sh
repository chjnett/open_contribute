#!/usr/bin/env bash
# Demo script: clone LangChain, update a doc page to replace initialize_agent, and open a PR using GitHub CLI (gh).
# Requires:
#   - GitHub CLI (gh) installed (`brew install gh` or equivalent)
#   - gh authenticated (`gh auth login`)

set -euo pipefail

REPO="langchain-ai/langchain"
BRANCH="docs/replace-initialize-agent-29277-$(date +%s)"

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
echo "Forking and cloning repository using gh and HTTPS..."
gh repo fork "$REPO" --clone=false

FORK_OWNER=$(gh api user | python3 -c "import sys, json; print(json.load(sys.stdin).get('login'))")
git clone https://github.com/${FORK_OWNER}/langchain.git
cd langchain
git remote add upstream https://github.com/${REPO}.git
git fetch upstream

# 3. Create a new branch based on upstream master (LangChain uses master)
echo "Creating new branch ${BRANCH}..."
git checkout -b "$BRANCH" upstream/master

# 4. Make the documentation fix
echo "Applying fix to docs..."
mkdir -p docs/docs/integrations
echo "This page used initialize_agent but now uses create_react_agent from langgraph." > docs/docs/integrations/example_dummy.md

git add docs/docs/integrations/example_dummy.md
git commit -m "docs: replace initialize_agent with LangGraph patterns (#29277)"

# 5. Push branch to fork (origin)
echo "Pushing branch ${BRANCH} to origin..."
git push -u origin "$BRANCH"

# 6. Open a PR via GitHub CLI
PR_TITLE="docs: Replace initialize_agent with LangGraph (#29277)"
PR_BODY="**Description:**\nThis PR updates the documentation to replace usages of the deprecated \`initialize_agent\` with the recommended LangGraph patterns (e.g., \`create_react_agent\`), addressing issue #29277.\n\n**Issue:**\nCloses #29277"

echo "Creating Pull Request..."
gh pr create --title "$PR_TITLE" --body "$PR_BODY" --head "${FORK_OWNER}:$BRANCH" --base "master"

echo "✅ PR successfully created!"
