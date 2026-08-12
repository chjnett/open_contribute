# Issue Triage Checklist

Run through this for **every** issue before recommending it. Skipping this is the most common way this skill fails the user — a confidently-recommended dead issue is worse than no recommendation at all.

## Step 1 — Fetch the actual issue page
Use `web_fetch` on the issue's URL (`https://github.com/{owner}/{repo}/issues/{n}`), not just the search API result — the API's `comments` count doesn't tell you what the comments actually say.

## Step 2 — Check the Development section
Near the bottom of the issue sidebar, GitHub shows "Development" with any linked pull requests. If there's an open (or even recently-closed) PR linked here, this issue is claimed or already resolved. Skip it — don't recommend, even if the issue itself is still technically "open" (issues often stay open until the linked PR actually merges).

## Step 3 — Check Assignees
"No one assigned" is necessary but not sufficient (see Step 2 and 4) — plenty of people work on issues without formally requesting assignment. But if someone *is* assigned, skip it.

## Step 4 — Read the last 2-3 comments
Look for phrases like:
- "this looks resolved"
- "fixed in #XXXX" / "landed in <commit>"
- "I have a PR ready"
- "duplicate of #XXXX"
- "closing as stale" / "candidate for closing"

A recent comment timestamp is *not* a green flag by itself — recent activity is just as often someone flagging the issue as done as it is genuine new discussion. Read what the comment actually says.

## Step 5 — Sanity check issue age against the label
Old good-first-issue labels (1+ years) on popular/high-traffic repos are disproportionately likely to already be claimed, simply because more people have had the chance to find them. Prefer issues created more recently when the label itself is recent, but don't auto-reject old ones — some sit untouched for legitimate reasons (niche area, unclear scope). Just weight recency as a soft signal, and Steps 2-4 as the hard filter.

## Step 6 — If everything in the label is stale
This happens often on popular repos. When it does, don't keep guessing at more issues from the same picked-over list — say so plainly and pivot to:
- The project's Discord/Slack `#contributing` channel (check README/CONTRIBUTING.md for a link) — ask a maintainer directly for a currently-open recommendation.
- A GitHub search filtered to `no:assignee sort:created-desc` on the good-first-issue label, to at least surface whatever is newest.
- Recently-opened, self-contained bug reports without the label at all, if the person is comfortable with slightly less hand-holding.
