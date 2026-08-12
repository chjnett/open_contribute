# PR 제출 전 품질 점검 체크리스트 (PR 수락률 최적화)

`gh pr create`를 실행하기 전에 에이전트는 **반드시** 이 체크리스트를 지켜야 합니다. 처음 기여하는 사람이 낸 PR이 이 항목들 중 하나라도 어기면, 무시되거나 닫히거나 방치될 가능성이 매우 높습니다.

## 0. 이슈 할당 확인 (필수)
- **사용자가 해당 이슈에 공식적으로 할당(assign)되기 전에는 PR을 열지 마세요.**
- LangChain 같은 큰 레포에는 할당되지 않은 사람의 PR을 자동으로 닫아버리는 봇이 있습니다.
- `gh issue view <이슈번호>`로 확인하세요. Assignees 목록에 사용자가 없으면 **중단**하고, 선점 코멘트를 남긴 뒤 메인테이너가 할당해줄 때까지 기다려야 한다고 알려주세요.

## 1. 로컬 CI / 테스트 확인 (타협 불가)
- `CONTRIBUTING.md`에서 정확한 로컬 테스트 명령을 확인하세요(`make test`, `npm run test`, `pytest`, `cargo test` 등 제각각입니다).
- PR을 제안하기 전에 `bash_tool`로 **직접 실행**하세요.
- 버그 수정이라면 그 수정이 테스트로 덮이는지 확인하세요. (테스트를 작성했는가? 수정 전에는 실패하고 수정 후에는 통과하는가?)

## 2. 린트와 포매팅
- 많은 레포가 CI에서 포매팅 검사를 강제합니다(`black`, `ruff`, `prettier`, `eslint` 등).
- `CONTRIBUTING.md`나 `package.json`/`Makefile`에서 포매팅 명령을 찾아 실행하세요(`make lint`, `npm run format` 등).
- 사소한 공백이나 스타일 오류가 남은 코드를 제출하지 마세요.

## 3. 커밋 메시지 스타일 맞추기
- 최근 커밋 10개를 확인하세요: `git log --oneline -n 10`.
- Conventional Commits(`feat:`, `fix:`, `docs:`)를 쓰는 레포인가요?
- 커밋 제목에 이슈 번호를 넣어야 하나요? (예: `Fix memory leak (#123)`)
- **조치:** 사용자의 커밋 메시지를 그 레포의 기존 관례에 정확히 맞춰 다시 작성하세요.

## 4. DCO / Sign-off 요구사항
- DCO(Developer Certificate of Origin)를 요구하는 레포인지 확인하세요. `DCO` 파일이 있는지, `CONTRIBUTING.md`에 언급이 있는지 보면 됩니다.
- **안전한 기본값:** 항상 `git commit -s -m "..."`로 `Signed-off-by` 줄을 자동으로 붙이세요. 손해 볼 일은 거의 없고, DCO 검사 실패를 막아줍니다.

## 5. PR 템플릿 준수
- `.github/PULL_REQUEST_TEMPLATE.md`(또는 `.github/PULL_REQUEST_TEMPLATE/` 아래 템플릿들)가 있는지 확인하세요.
- 있다면 `gh pr create --body "..."`가 그 템플릿을 **반드시** 채워야 합니다. 새 구조를 임의로 만들지 마세요.
- PR과 관련된 체크박스(`[ ]`)는 전부 `[x]`로 표시하세요.
- GitHub가 이슈를 자동 연결하도록 `Fixes #이슈번호` 또는 `Closes #이슈번호`를 정확히 포함하세요.
