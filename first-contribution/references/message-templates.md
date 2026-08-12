# Message Templates & Tone Guide

These aren't fill-in-the-blank templates — every message should be written specifically for the repo, issue, and person's actual background. Use the structures below as a shape, not a script to paste verbatim.

## 1. Issue claim comment

**Purpose:** Signal intent so nobody else duplicates the work, and give the maintainer enough to say "sounds good" without a back-and-forth.

**Structure (2-4 sentences):**
1. State you'd like to work on this.
2. One sentence on planned approach *if* the issue is even slightly ambiguous (skip this for trivial issues — it's padding).
3. Optional: ask one specific clarifying question if something in the issue is genuinely unclear (better than guessing wrong and redoing work).

**Casual variant example shape:**
> "I'd like to take this one — planning to [approach in one clause]. Let me know if that sounds right before I dig in."

**More-detail variant example shape:**
> "I'll pick this up. My plan: [1-2 concrete steps]. One question — [specific ambiguity], or should I default to [reasonable assumption]?"

**Avoid:**
- Long intros about being new to open source (maintainers don't need a biography)
- Vague "I'll try to fix this" with zero indication you've read the issue
- Asking questions already answered in the issue body or CONTRIBUTING.md

## 2. Discord/Slack `#contributing` outreach

**Purpose:** Get a specific, useful reply fast — not "welcome! check the good first issue label" (which the user already tried).

**Structure:**
1. One line on relevant background — language/stack, *not* a full resume.
2. What you're looking for, specifically: "a currently-open, unclaimed good-first-issue" is more useful than "something to work on."
3. If relevant: mention that the labeled issues you checked turned out to be already claimed — this signals you did the homework and saves the maintainer from re-suggesting the same list.

**Example shape:**
> "Hey — looking to make a first contribution here, comfortable with [stack]. Checked the good-first-issue label but the top few had linked PRs already. Any currently-open ones you'd point me to, or areas that could use hands?"

**Avoid:**
- Generic "hi, how do I contribute" with no context — gets deprioritized in busy channels
- Asking for a full mentor/onboarding session up front — most maintainers don't have bandwidth for that as a first message

## 3. Pull request description

**Purpose:** Get reviewed quickly by matching what the project's own recent PRs look like.

**Structure:**
1. Look at 2-3 recently merged PRs in the repo first — note title format (e.g. `[BUG] short description` vs. `fix: short description`), and whether they use a template (`.github/PULL_REQUEST_TEMPLATE.md`).
2. If a template exists, use it — don't improvise a different structure.
3. If not: what changed, why, how it was tested, and a link back to the issue (`Closes #1234`).

**Avoid:**
- Over-explaining implementation details already visible in the diff
- Under-explaining *why* a non-obvious choice was made
- Skipping the "how tested" section even for small changes — reviewers ask for it anyway if it's missing, costing a review round-trip
