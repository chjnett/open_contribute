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

**CLA** — 법적 계약이고 보통 cla-assistant 같은 봇이 강제합니다. **사용자를 대신해 CLA에 서명하거나 동의하지 마세요.** 링크를 안내하고, 오직 본인만 서명할 수 있다고 분명히 말한 뒤 나머지 작업을 계속하세요. Grafana의 CLA는 머지만 막고 다른 건 막지 않으므로, 서명 대기 중에도 PR을 열고 리뷰받을 수 있습니다.

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

## 6. 제출 후 — 성공을 보고하기 전에 체크 상태를 읽을 것
- 외부 PR은 대부분의 CI가 **메인테이너 승인 대기**로 잡힙니다("N workflows awaiting approval"). 이건 정상 절차지 실패가 아니므로 그렇게 설명하세요.
- 사용자가 조치해야 하는 것(서명 안 된 CLA)과 그냥 기다리는 것(리뷰어 배정, `policy-bot 0/1 rules approved`)을 구분해서 알려주세요.
- 상황을 보고하기 전에 `gh pr checks <n>`으로 실제 체크 목록을 다시 읽으세요.
