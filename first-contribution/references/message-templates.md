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

## 4. Getting the PR in front of the right people

Everything in this section is about **routing and clarity**, not pressure. A PR stalls far more often because nobody who owns that code knows it exists than because they saw it and declined.

### Check CODEOWNERS routing — and be very slow to claim it's broken

Look up `.github/CODEOWNERS` for the team that owns the code you touched. Usually the answer is "it routed fine and there is nothing to do," and that is the outcome you should expect.

**Do not conclude there is a routing gap from the reviewer list alone.** Many orgs replace a team review request with individual members of that team, which looks identical to mis-routing if you only read `requested_reviewers`. Read the timeline instead:

```bash
gh api "repos/{owner}/{repo}/issues/{n}/timeline?per_page=100" \
  --jq '.[]|select(.event=="review_requested" or .event=="review_request_removed")
        | "\(.event): \(.requested_team.slug // .requested_reviewer.login)"'
```

Worked example — `grafana/grafana#130614` showed four individual frontend reviewers and no team, which looked like the owning squad had been missed. The timeline said otherwise: `sharing-squad` was auto-requested from CODEOWNERS, then removed and replaced by four of its members. Routing had worked correctly the whole time; there was nothing to flag, and a comment claiming a gap would have been simply wrong.

Only when a file genuinely matches no rule — verified by reading the CODEOWNERS entries themselves, not a truncated search — is it worth one comment:

> "CODEOWNERS routes the {feature} paths to @{team}, but `{file}` isn't covered by a rule so this didn't reach them — flagging in case it belongs on their queue."

**A caution about how that mistake happened.** The first pass ran `grep shortLinks CODEOWNERS | head -5`, the matching line was the sixth, and the absence of output became "not covered." Never let an output limit decide a factual claim you are about to make in public — drop the `head`, or count the matches first.

### Tell the issue thread the PR is up

People watching the issue are not automatically watching your fork's PR. One short comment on the issue closes that gap and lets anyone hitting the same bug find the fix.

> "Opened #{pr} for this — {one clause on the approach}."

### Community channels

If `CONTRIBUTING.md` links a Slack/Discord/forum (Grafana links a community Slack and forums), a single post is reasonable **after** the PR has sat unreviewed for a while. Link it, one sentence of context, and ask whether it's on the right team's radar. Post once, in the right channel, and never `@here`/`@everyone`.

## 5. The one nudge

If nothing happens, you get **one** follow-up, and it should carry new information.

**Wait first.** On a large repo, one to two weeks of silence is normal, not a snub — external PR CI is often held for maintainer approval, so "no checks running" is not evidence of neglect either.

**Make the nudge worth reading.** Something changed, or you resolved something:

> "Rebased on main and CI is green. Happy to adjust the approach if the `bootData` route isn't what you'd prefer."

**Then stop.** If a second nudge is needed weeks later, prefer a different channel (the community Slack) over a second comment on the same thread. Maintainers are often volunteers with a queue in the hundreds; silence is usually bandwidth, not rejection.

## 6. Things that lose you the review

These read as pressure and reliably backfire:

- `@`-mentioning several maintainers at once, or anyone with no connection to the area
- "Any update?" / "bump" / "please review" with no new information
- Following up within days, or repeatedly
- DMing a maintainer who hasn't invited it
- Commenting on unrelated issues or PRs to draw attention to yours
- Opening a duplicate issue because the first one got no traction
- Re-opening the argument after a maintainer has declined a direction

The reliable levers are the boring ones: keep the PR small, keep it mergeable, reply to review comments quickly, and make the reviewer's job take two minutes instead of twenty.
