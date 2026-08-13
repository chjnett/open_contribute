# PR 제출 전 품질 점검 체크리스트 (PR 수락률 최적화)

`gh pr create`를 실행하기 전에 에이전트는 **반드시** 이 체크리스트를 지켜야 합니다. 처음 기여하는 사람이 낸 PR이 이 항목들 중 하나라도 어기면, 무시되거나 닫히거나 방치될 가능성이 매우 높습니다.

## 0. 이슈 할당 확인 (필수)
- **사용자가 해당 이슈에 공식적으로 할당(assign)되기 전에는 PR을 열지 마세요.**
- LangChain 같은 큰 레포에는 할당되지 않은 사람의 PR을 자동으로 닫아버리는 봇이 있습니다.
- `gh issue view <이슈번호>`로 확인하세요. Assignees 목록에 사용자가 없으면 **중단**하고, 선점 코멘트를 남긴 뒤 메인테이너가 할당해줄 때까지 기다려야 한다고 알려주세요.
- 모든 프로젝트가 이렇지는 않습니다 — Grafana는 할당 없이도 외부 PR을 받습니다. 어느 쪽이든 가정하지 말고 그 레포의 실제 관례를 확인하고, 어느 경우인지 사용자에게 알려주세요.

## 1. 로컬 CI / 테스트 확인 (타협 불가)
- `CONTRIBUTING.md`에서 정확한 로컬 테스트 명령을 확인하세요(`make test`, `npm run test`, `pytest`, `cargo test` 등 제각각입니다).
- PR을 제안하기 전에 `bash_tool`로 **직접 실행**하세요.
- 버그 수정이라면 그 수정이 테스트로 덮이는지 확인하세요. (테스트를 작성했는가? 수정 전에는 실패하고 수정 후에는 통과하는가?)

**정말로 실행할 수 없다면**, 실행한 것처럼 굴지 말고 그렇다고 말하세요. 아주 큰 레포는 셋업 비용이 실재합니다 — Grafana의 `yarn install`은 수 GB가 필요한데 항상 여유가 있는 건 아닙니다. 중간에 발견하지 말고 시작 전에 `df -h`로 확인하고, 체크리스트 항목 하나 채우겠다고 사용자의 디스크를 채우지 마세요.

**"테스트 파일 하나만 돌리면 되지 않나"는 우회로가 아닙니다.** `yarn test path/to/one.test.ts`도 `node_modules`가 있어야 하고, yarn/pnpm 워크스페이스에는 파일 하나만 커버하는 부분 설치가 없습니다. 가벼운 탈출구처럼 들리지만 아닙니다 — 설치가 안 들어가면 단일 테스트도 안 들어갑니다.

로컬 테스트를 건너뛰었다면 PR 설명에 **어느 파일을 실행하지 않았는지, 왜인지, 리뷰어가 어느 부분을 특히 봐야 하는지**를 반드시 적으세요. 메인테이너는 "테스트를 못 돌렸고 여기를 봐달라"는 쪽을, 조용히 CI에 도박을 거는 쪽보다 훨씬 잘 받아들입니다.

## 1b. 기존 테스트가 버그를 명세하고 있을 수 있음
테스트가 초록불이라고 동작이 옳은 건 아닙니다. 버그가 배포됐다면 왜 테스트가 그걸 통과시켰는지 물어보세요 — 많은 경우 테스트가 깨진 출력을 기대값으로 박아두고 있습니다.

`grafana/grafana#130567`에서는 짧은 URL을 org ID 대신 리소스 namespace로 만들고 있었는데, 테스트가 그걸 고정하고 있었습니다:

```ts
metadata: { namespace: 'org-5' }
expect(result).toBe('...?orgId=org-5');   // 버그가 기대값으로
```

두 가지 결론:

- **그 기대값을 수정의 일부로 함께 고치고**, PR에 그렇게 적으세요 — 버그가 리뷰를 어떻게 빠져나갔는지 설명해줍니다.
- **변경한 함수를 또 누가 호출하는지 확인하세요.** 다른 진입점으로 같은 코드 경로를 지나던 무관한 테스트 2건이 깨질 뻔했고, 공용 `beforeEach`에 기본값을 넣어야 했습니다. 변경이 고립돼 있다고 단정하기 전에 테스트 파일 전체에서 함수명을 grep 하세요.

## 1c. 수정 방식은 기존 픽스처가 결정하게 하세요
한 버그에 그럴듯한 수정이 여러 개일 때, 대개 테스트 픽스처가 대부분을 걸러냅니다. 고르기 전에 픽스처부터 읽으세요.

Directus의 M2A 버그에서 가장 자연스러운 가드는 "이 타입 조건이 실제 컬렉션인가?", 즉 `typeCondition in schema.collections`였습니다. 그런데 `parse-query.test.ts`의 목 스키마는 `{ relations: [...] }`뿐이고 `collections` 키가 아예 없습니다 — 그대로 갔으면 `undefined`에서 던졌을 것이고, `?? {}`로 방어했어도 기존 M2A 테스트가 전부 반대 분기를 타서 깨졌을 겁니다.

같은 relation 객체가 이미 `meta.one_allowed_collections`를 들고 있었고, 픽스처가 그건 채워두고 있었습니다(`['child']`, `['ComponentText']`). 그쪽을 기준으로 삼으니 버그도 고쳐지고 기존 케이스도 전부 통과했습니다.

정리하면: 접근을 확정하기 전에 기존 테스트 케이스마다 손으로 로직을 따라가 보고, 의존하려는 데이터가 픽스처에 실제로 있는지 확인하세요. 몇 분이면 되고, CI 초록불과 리뷰어가 실패를 지켜보는 것의 차이입니다.

## 2. 린트와 포매팅
- 많은 레포가 CI에서 포매팅 검사를 강제합니다(`black`, `ruff`, `prettier`, `eslint` 등).
- `CONTRIBUTING.md`나 `package.json`/`Makefile`에서 포매팅 명령을 찾아 실행하세요(`make lint`, `npm run format` 등).
- 사소한 공백이나 스타일 오류가 남은 코드를 제출하지 마세요.

## 3. 커밋 메시지 스타일 맞추기
- 최근 커밋 10개를 확인하세요: `git log --oneline -n 10`. 클론이 없다면 `gh api "repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc" --jq '[.[]|select(.merged_at!=null)][].title'`로 확인할 수 있습니다.
- Conventional Commits(`feat:`, `fix:`, `docs:`)를 쓰나요, 아니면 영역 접두사(`Alerting: Prevent race condition`)를 쓰나요?
- 커밋 제목에 이슈 번호를 넣어야 하나요? (예: `Fix memory leak (#123)`)
- **조치:** 사용자의 커밋 메시지를 그 레포의 기존 관례에 정확히 맞춰 다시 작성하세요.

## 4. Sign-off, 서명, CLA는 서로 다른 세 가지
이걸 혼동하면 왕복 한 번을 낭비합니다. 그 레포가 무엇을 요구하는지 확인하세요 — 둘 이상일 수도 있습니다.

**DCO sign-off** — `git commit -s`로 붙는 `Signed-off-by:` 트레일러입니다. 텍스트일 뿐 키와 무관합니다. 안전한 기본값: 항상 붙이세요.

**검증된 커밋 서명(Verified)** — GPG/SSH 암호 서명이고 GitHub에 `Verified`로 표시됩니다. 브랜치 규칙으로 강제할 수 있으며, 서명 없는 커밋은 "Commits must have verified signatures"로 머지가 막힙니다. `git commit -s`로는 **충족되지 않습니다.** 확인:

```bash
gh api "repos/{owner}/{repo}/commits?sha={branch}" --jq '.[].commit.verification | "\(.verified) \(.reason)"'
```

사용자에게 서명 키가 없다면 대신 만들어주지 마세요 — 이 레포는 서명된 커밋을 요구한다고 알리고 직접 설정하게 하거나, GitHub이 대신 서명해주는 §4b의 API 방식을 쓰세요.

**CLA** — 법적 계약입니다. **사용자를 대신해 CLA에 서명하거나 동의하지 마세요.** 그리고 짧은 "ㅇㅇ"이나 "진행해"는 *작업*에 대한 동의이지 법적 문서에 대한 숙지된 동의가 아닙니다. 약관 본문을 안내하고 본인만 수락할 수 있다고 분명히 말한 뒤 나머지는 계속 진행하세요 — 대기 중인 CLA는 보통 머지만 막으므로 PR을 열고 리뷰받는 데는 지장이 없습니다.

CLA는 최소 두 가지 형태가 있고, 두 번째가 무심코 넘어가기 쉽습니다:

- **외부 서명 서비스** (cla-assistant 등). Grafana가 이 방식입니다 — 봇이 링크를 코멘트로 달고, 사용자가 앱 권한을 승인하고 거기서 서명합니다. 대신 해줄 수 없는 게 명백합니다.
- **PR 안의 파일 수정.** Directus는 PR에서 `contributors.yml`에 본인 GitHub 사용자명을 추가하게 합니다. 기계적으로는 한 줄 diff라 얼마든지 할 수 있지만, **그 수정이 곧 서명 행위**입니다. 정체를 알아보고 사용자에게 넘기세요.

어느 형태인지는 추측하지 말고 워크플로를 읽어서 확인하세요:

```bash
gh api "repos/{owner}/{repo}/contents/.github/workflows" --jq '.[].name' | grep -i cla
```

## 4b. 클론 없이 커밋하기 (그리고 Verified 받기)
아주 큰 레포에 작은 변경을 넣을 때, 클론 비용이 변경 자체보다 클 수 있습니다. API로 커밋할 수 있는데, 두 경로가 **동등하지 않습니다**:

- **REST Contents API** (`PUT /repos/{owner}/{repo}/contents/{path}`)는 **서명 없는** 커밋을 만듭니다. 서명을 요구하는 레포에서는 조용히 막힌 PR을 만들어냅니다.
- **GraphQL `createCommitOnBranch`**는 **GitHub이 서명한** 커밋을 만들어 `Verified`로 표시됩니다. API로 커밋할 땐 항상 이쪽을 쓰세요.

```bash
gh api graphql --input payload.json   # {"query": "mutation($input: CreateCommitOnBranchInput!){...}", "variables": {...}}
```

이 mutation은 `expectedHeadOid`와 base64 파일 내용을 받아 모든 변경을 담은 커밋 하나를 만듭니다.

**PR 브랜치를 base로 리셋하는 걸 별도 단계로 하지 마세요.** 브랜치가 base보다 앞선 커밋이 0개가 되면 GitHub이 PR을 자동으로 닫습니다. ref를 새 커밋으로 곧장 force-update 하거나, 브랜치를 옮기기 전에 새 커밋을 먼저 만드세요. 이미 닫혔다면 브랜치에 커밋이 다시 생긴 뒤 `gh pr reopen <n>`으로 복구됩니다.

## 5. PR 템플릿 준수
- `.github/PULL_REQUEST_TEMPLATE.md`(또는 `.github/PULL_REQUEST_TEMPLATE/` 아래 템플릿들)가 있는지 확인하세요.
- 있다면 `gh pr create --body "..."`가 그 템플릿을 **반드시** 채워야 합니다. 새 구조를 임의로 만들지 마세요.
- PR과 관련된 체크박스(`[ ]`)는 전부 `[x]`로 표시하세요.
- GitHub가 이슈를 자동 연결하도록 `Fixes #이슈번호` 또는 `Closes #이슈번호`를 정확히 포함하세요.
- 실제로 설계 선택지가 있다면 리뷰어에게 대안을 제시하세요. "X에서 파생하는 대신 Y에서 읽는 쪽을 원하시면 말씀해 주세요, 그렇게 고치겠습니다" 같은 한 줄은 비용이 없고, 독단적이지 않고 협업적으로 읽힙니다.

## 5b. 이런 유형의 PR이 함께 담아야 하는 릴리스 도구 파일
코드가 맞아도 곁다리 파일 하나가 없어서 CI가 깨질 수 있습니다. 커밋 전에 릴리스 도구를 확인하세요:

```bash
gh api "repos/{owner}/{repo}/contents/.changeset" --jq 'length'   # changesets 사용?
```

[changesets](https://github.com/changesets/changesets)를 쓰는 레포라면 버그 수정에도 `.changeset/<이름>.md`가 필요합니다. 영향받는 패키지와 과거형 설명을 적습니다:

```markdown
---
'@directus/api': patch
---

Fixed GraphQL fragments declared on an M2A union type resolving their fields as null
```

관례를 한 번에 파악하는 가장 확실한 방법은 **같은 유형으로 최근 머지된 PR의 파일 목록**을 읽는 것입니다 — changeset, 테스트 위치, 함께 나가는 문서·스펙 수정이 전부 보입니다:

```bash
gh api "repos/{owner}/{repo}/pulls/{n}/files" --jq '.[].filename'
```

## 6. 제출 후 — 성공을 보고하기 전에 체크 상태를 읽을 것
- 외부 PR은 대부분의 CI가 **메인테이너 승인 대기**로 잡힙니다("N workflows awaiting approval"). 이건 정상 절차지 실패가 아니므로 그렇게 설명하세요.
- 사용자가 조치해야 하는 것(서명 안 된 CLA)과 그냥 기다리는 것(리뷰어 배정, `policy-bot 0/1 rules approved`)을 구분해서 알려주세요.
- 상황을 보고하기 전에 `gh pr checks <n>`으로 실제 체크 목록을 다시 읽으세요.
- **"성공"한 봇 워크플로가 아무 일도 안 했을 수 있습니다.** Directus의 `cla-comment.yml`은 초록불로 끝났는데 코멘트는 하나도 안 달렸습니다 — 아티팩트 다운로드 단계가 `continue-on-error`라 조용히 no-op 했기 때문입니다. "봇 기다리세요"라고 했으면 사용자는 영원히 기다렸을 겁니다. 기대한 코멘트가 안 보이면 워크플로 파일을 읽고 실제로 무엇이 필요한지 확인하세요 — 체크의 색깔로 추측하지 마세요.
- 실패한 체크는 단계 이름까지 읽을 가치가 있습니다. Directus의 `Check / fail`은 `Preserve CLA result`라는 단계가 `exit 1` 한 것이었고, 코드와는 무관했습니다.

**내 PR에 대한 남의 요약은 행동하기 전에 직접 검증하세요.** 사용자든 동료든 다른 도구든, 자신 있는 요약은 상태에 대한 *주장*이지 상태가 아닙니다. 타임라인과 체크 목록을 직접 대조하세요 — 특히 제안이 재촉일 때 그렇습니다. 틀린 진단에 재촉을 써버리면, 그게 내가 가진 단 한 번이었으니까요.

`grafana/grafana#130614`의 실제 사례. 그 요약은 메인테이너가 PR을 스쿼드 보드로 옮겼고, 워크플로 28개가 승인 대기 중이며, 메인테이너에게 승인을 요청하는 코멘트를 달아야 한다고 했습니다. 셋 다 틀렸습니다:

| 주장 | API가 말한 것 |
| --- | --- |
| 메인테이너가 보드로 옮김 | 타임라인 행위자는 전부 작성자 또는 `github-actions[bot]` |
| 워크플로 28개 승인 대기 | `action_required` 런 0개, 보고된 체크는 전부 통과 |
| 워크플로 승인을 요청하라 | 승인 대기 중인 게 없어서 요청할 대상 자체가 없음 |

```bash
gh api "repos/{owner}/{repo}/issues/{n}/timeline?per_page=100" \
  --jq '.[]|select(.event|test("added_to_project|moved_columns_in_project|review_requested"))|"\(.event) by \(.actor.login)"'
gh api "repos/{owner}/{repo}/actions/runs?event=pull_request" --jq '[.workflow_runs[]|select(.status=="action_required")]|length'
```

그대로 따랐다면 PR 올린 지 하루도 안 돼 메인테이너 둘을 동시에 `@` 하면서, 막혀 있지도 않은 것을 요청하는 셈이었습니다 — 메시지 템플릿 §6의 안티패턴 세 개를 한 번에 밟는 겁니다.

## 7. 끝내기 전에 프로젝트 자체 가이드와 대조하세요
**`CONTRIBUTING.md`는 껍데기인 경우가 많습니다.** Directus의 것은 `directus.com/docs/community/contribution/pull-requests`를 가리키는 3줄이고, 구속력 있는 내용은 전부 그 페이지에 있습니다 — CLA 방식, 필수 changeset, 과거형 설명 규칙. 링크를 따라가세요. 레포만 읽으면 정작 권위 있는 출처를 놓칩니다.

PR을 올린 뒤에는 가이드의 요구사항을 실제 제출물과 한 줄씩 대조하고, 준수했다고 단언하는 대신 대조 결과를 보고하세요. CI가 초록불이어도 어긋난 점은 밝히세요: 이 PR은 가이드가 지시한 `pnpm changeset` 대신 changeset 파일을 직접 작성했습니다. 레포를 클론하지 않았기 때문입니다. 결과물도 같고 체크도 통과했지만 절차는 달랐고, 조용히 넘어가기보다 한 문장 적을 가치가 있습니다.
