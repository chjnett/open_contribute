# Community posts

Three platform-specific drafts. Post the **blog link** (or repo) rather than pasting
the whole article, to avoid duplicate-content/link-spam flags.

---

## 1. Reddit — r/ClaudeAI (and r/ClaudeCode)

**Title:**

I built a Claude Code skill that finds open-source issues you can actually get merged —
it measures whether a repo merges outsider PRs before recommending anything

**Body:**

The standard advice is "filter by `good first issue` and go." I did that and kept
finding issues that were already claimed, already fixed, or on repos that barely merge
outside PRs.

So I built `first-contribution`, a Claude Code plugin that runs a funnel before
recommending anything:

1. filter repos on availability (open, unassigned issues?),
2. gate on the **merge reality** — % of open PRs 90+ days old + % of merges from
   outside the top-5 authors,
3. triage every candidate issue against an 8-step checklist ending with "does the bug
   still exist in current code?",
4. walk the claim → fork → fix → tests → PR → follow-up.

It's produced two real PRs from a cold start, both in review:
- grafana/grafana#130614 (wrong org ID in copied short URLs)
- directus/directus#28092 (GraphQL fragments on an M2A union resolved to null)

Install:
```
/plugin marketplace add chjnett/open_contribute
/plugin install first-contribution@open-contribute
```

Repo (MIT, EN + KO + RAG variants): https://github.com/chjnett/open_contribute

Happy to answer questions — especially about the "share of merges from outside the
top-5 authors" metric, which is the part I'm least sure generalizes.

---

## 2. dev.to

Publish `blog-post.md` verbatim. Use tags: `#claude`, `#opensource`, `#github`,
`#ai`, `#beginners`.

---

## 3. GeekNews (news.hada.io) — 한국어

**제목:**

"good first issue" 라벨은 거짓말한다 — 실제로 측정해보고 스킬로 만들었습니다

**본문 (링크 첨부용 요약):**

오픈소스 입문자에게 늘 들려주는 조언이 "good first issue 라벨로 검색해봐"입니다.
저도 그렇게 했다가 두 번 다 헛수고를 했습니다. 라벨은 이미 선점됐거나, 이미
고쳐졌거나, 아니면 외부 PR을 거의 머지하지 않는 레포에 붙어 있었습니다.

15개 인기 레포를 같은 날 같은 방식으로 측정해봤습니다:
- `grafana/grafana`는 외부(top-5 커미터 밖) PR의 약 70%를 머지하지만,
- `chroma-core/chroma`(29k 스타, 매일 커밋)는 **8%**만 머지하고, good first issue로
  열린 PR **17건 중 17건**이 전부 머지에 실패했습니다.
- "치명적·8일 전·미할당" 이슈가 이미 v3.3.14에서 수정된 경우도 있었습니다. 티켓만
  안 닫힌 거죠.

그래서 추천 전에 이걸 전부 검증하는 에이전트 스킬 `first-contribution`을 만들었고,
실제로 콜드 스타트로 grafana/directus에 PR 2건을 만들어냈습니다(둘 다 리뷰 중).

설치: `/plugin marketplace add chjnett/open_contribute` →
`/plugin install first-contribution@open-contribute`
레포(MIT, 한글 버전 포함): https://github.com/chjnett/open_contribute

---

## 4. 디스콰이엇 (disquiet.io) — 한국어

**제목:**

오픈소스 첫 기여, "라벨을 믿지 말고 측정하라" — good first issue 검증 스킬

**본문:**

"good first issue" 라벨이 실제로 기여 가능한 이슈를 가리키는 경우가 생각보다
적다는 걸 두 번의 실패 끝에 알게 됐습니다. 라벨 이슈가 이미 선점됐거나, 이미
수정됐는데 티켓만 안 닫혔거나, 레포 자체가 외부 PR을 거의 안 받는 경우가 대부분.

15개 레포를 측정해보니 외부 PR 머지율이 70%인 곳(grafana)과 8%인 곳(chroma)이
겉으로는 똑같이 건강해 보였습니다. 이 "겉보기"를 걷어내는 측정 로직을 에이전트
스킬로 만들었고, 실제로 grafana/directus PR 2건을 만들어냈습니다.

레포(한글 버전 포함): https://github.com/chjnett/open_contribute
설치: `/plugin marketplace add chjnett/open_contribute`

스킬의 판단 기준(특히 "외부 top-5 커미터 밖 머지 비율" 지표)에 대한 피드백을
특히 환영합니다.
