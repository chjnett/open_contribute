한국어 | [English](./README.md)

# first-contribution

"오픈소스에 기여하고 싶다"에서 실제 PR 제출까지 데려다주는 [Claude Skill](https://www.anthropic.com/news/skills)입니다 — 3개월 전에 이미 죽었어야 할 `good first issue`를 붙잡고 한나절을 날리는 일 없이요.

`good first issue` 라벨은 생각보다 자주 거짓말을 합니다. 인기 레포일수록 2023년에 붙은 라벨은 이미 다른 PR로 해결됐거나 조용히 마무리됐는데 이슈만 안 닫힌 경우가 흔해요. 신나서 코드를 읽기 시작했는데 6개월 전에 이미 걸려있는 PR을 발견하는 식이죠. 이 스킬은 정확히 그 일이 같은 레포에서 한 오후에 두 번 연속 일어나서 만들었습니다.

## 구성

- **`first-contribution/`** — 영어로 응답하는 스킬
- **`first-contribution-ko/`** — 같은 스킬, 한국어로 응답 ([영문 안내](./README.md))

각 폴더에는 다음이 들어있습니다:
- **`SKILL.md`** — 전체 워크플로우: 레포 평가, 이슈 검증, 아웃리치 초안 작성, 기여 가이드
- **`references/repo-evaluation-criteria.md`** — "이 레포가 진짜 초보자 친화적인가"를 판단하는 채점 기준
- **`references/issue-triage-checklist.md`** — 추천 전에 죽은/이미 손탄 이슈를 걸러내는 6단계 체크리스트
- **`references/message-templates.md`** — 이슈 클레임 코멘트, `#contributing` 채널 아웃리치, PR 설명의 톤/구조 가이드

## 작동 방식

1. **뭘 찾는지 먼저 좁힘** — 도메인, 스택, 경험 수준을 검색 전에 확인해서, 추측이 아니라 실제 선호도에 기반한 추천을 만듭니다.
2. **실제 데이터로 후보 레포 평가** — GitHub API에서 오픈 이슈 수, good-first-issue 개수, 마지막 활동 시점, 외부 기여자 비율 같은 실시간 수치를 가져옵니다.
3. **추천 전에 죽은 이슈를 걸러냄** — 연결된 PR, 담당자를 확인하고, 최근 코멘트 몇 개를 실제로 읽어서 "이거 해결된 듯" 신호를 잡아냅니다.
4. **커뮤니티 채널을 찾고 아웃리치 초안까지 작성** — README에서 Discord/Slack 링크를 뽑고, 이슈 클레임 코멘트 초안을 쓰고, 라벨이 전멸했다면 뻔한 "어떻게 기여하나요?" 대신 구체적인 요청을 `#contributing` 채널용으로 작성합니다.
5. **실제 수정 작업을 함께 진행** — 레포를 클론하고, `CONTRIBUTING.md`를 읽고, 관련 파일로 스코프를 좁히고, 수정안을 작성하고, diff를 설명하고, 실제 테스트를 돌리고, 프로젝트 스타일에 맞는 PR 설명을 작성합니다.

## 패키징 방식

이 레포 자체가 [Agent Skill](https://www.anthropic.com/news/skills)입니다 — 각 언어별 폴더 루트에 필수 `name`/`description` frontmatter가 있는 `SKILL.md`와, 필요할 때 로드되는 `references/` 폴더가 있습니다. Agent Skills는 Claude Code, Claude.ai, Cowork에서 네이티브로 읽히고, 같은 폴더 형식을 그대로 다른 SKILL.md 호환 코딩 에이전트에서도 씁니다.

## 설치

### 가장 쉬운 방법 — 코딩 에이전트에 이 프롬프트를 붙여넣기

아래 블록을 Claude Code나 SKILL.md를 지원하는 에이전트에 복사해서 넣으세요. 한국어로 응답하는 버전을 원하면 폴더명을 `first-contribution-ko`로 바꾸세요.

```
first-contribution 에이전트 스킬만 설치해줘, 다른 건 건드리지 마.

1. 내 스킬 디렉토리를 확인해 (Claude Code → ~/.claude/skills/,
   그 외엔 해당 툴의 문서화된 스킬 디렉토리).
2. https://github.com/chjnett/open_contribute 를 임시 폴더에 클론해.
3. first-contribution/ 하위 폴더를 (한국어 버전을 원하면 first-contribution-ko/를)
   <스킬 디렉토리>/first-contribution/ 으로 복사해.
4. 복사된 폴더 루트에 SKILL.md가 있는지 확인해.
5. 다른 파일, 설정, 스킬은 건드리지 마. 최종 설치 경로만 알려주고 끝내.
```

설치 후 에이전트를 재시작(혹은 새 세션 시작)하면 스킬을 인식합니다.

### 직접 설치하기

**Claude Code** — `~/.claude/skills/` (전역) 또는 `.claude/skills/` (프로젝트별)

```bash
git clone https://github.com/chjnett/open_contribute /tmp/open_contribute
cp -r /tmp/open_contribute/first-contribution-ko ~/.claude/skills/first-contribution-ko
# 영어 버전을 원한다면:
cp -r /tmp/open_contribute/first-contribution ~/.claude/skills/first-contribution
```

**Claude.ai / Cowork** — 릴리즈에서 패키징된 `.skill` 파일(`first-contribution-ko.skill` 등)을 업로드하거나, 설정 → 스킬에서 `SKILL.md` + `references/` 폴더를 직접 업로드하세요.

## 사용하기

설치 후엔 그냥 원하는 걸 자연스럽게 말하면 됩니다 — 별도 명령어 없이 의도만으로 트리거됩니다:

> "오픈소스 기여 시작하고 싶어, 좋은 레포랑 이슈 찾아줘"
> "이 레포 초보자한테 괜찮아? [github 링크]"
> "러스트 프로젝트 중에 good-first-issue 찾아줘"

## 직접 배포하기

레포를 public으로 유지하고, 각 스킬 폴더 루트에 `SKILL.md`와 명확한 `description`을 두면 됩니다 — 이 한 줄이 모든 에이전트가 스킬을 언제 실행할지 판단하는 기준입니다. 더 나아가고 싶다면 [anthropics/skills](https://github.com/anthropics/skills)에 PR을 보내거나, 스킬 디렉토리 사이트에 등록하거나, Claude Code 플러그인 마켓플레이스로 묶어보세요.

## 진행 상황

실제로 기여하면서 실사용 결과를 바탕으로 공개적으로 계속 다듬는 중입니다. 죽은 이슈를 추천하거나, 레포 판단이 틀리거나, 프로젝트 관례를 놓치는 경우를 발견하시면 이슈로 알려주세요 — 정확히 그런 피드백이 체크리스트를 더 정교하게 만듭니다.

## 라이선스

[MIT](./LICENSE). 자유롭게 쓰고, 포크하고, 확장하세요.
