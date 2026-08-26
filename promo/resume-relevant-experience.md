# Relevant Experience — Open Source Contribution Track Record

> 프로필: AI/ML 백엔드 엔지니어 지망, Python 생태계에서 실전 오픈소스 기여 활동. 프로세스 주도적으로 버그를 찾아 수정부터 리뷰 협업까지 완주.

## 핵심 실적 (2026-08 기준)

- **3개의 Pull Request가 머지됨** (실제 검증된 오픈소스 레포), 추가로 **17개 PR이 리뷰/승인 진행 중** — 총 20개 PR 중 절대다수가 "재현 → 근본 원인 → 최소 수정 → 승인"까지 완주
- **AI-RAG 및 데이터 인프라 도메인**에 집중: 벡터 검색(Chroma · Qdrant), 지식 그래프(Graphiti), LLM 파이프라인(LlamaIndex · vLLM · LiteLLM), 데이터 파이프라인(dlt)

## 머지된 Pull Requests

| 레포 | PR | 수정 내용 |
|---|---|---|
| [celery/billiard#452](https://github.com/celery/billiard/pull/452) | 병렬 워커에서 `BaseException`이 래핑되어 호출자에게 전파되지 않는 버그 수정 | 병렬처리 예외 전파 보장 |
| [dlt-hub/dlt#4367](https://github.com/dlt-hub/dlt/pull/4367) | Incremental `lag`가 `last_value=0`(falsy)일 때 커서를 되감는 버그 — `is not None` 검사로 수정 | 데이터 파이프라인 상태 관리 |
| [grafana/grafana#130906](https://github.com/grafana/grafana/pull/130906) | 짧은 URL이 short-URL 리소스의 namespace를 org ID로 잘못 사용 — on-prem은 org ID, Cloud는 생략 | 프런트엔드 URL 로직 + 서명 커밋 |

## 리뷰/승인 진행 중인 주요 PR

| 레포 | PR | 수정 내용 |
|---|---|---|
| [LLaMA-Factory#10759](https://github.com/hiyouga/LLaMA-Factory/pull/10759) | `top_p`/`repetition_penalty` `or 1.0` 조용한 재작성 제거 — config 파싱 시점에 검증, 전 엔진 일관화 | 리뷰어 "ready" |
| [pola-rs/polars#28911](https://github.com/pola-rs/polars/pull/28911) | `DataFrame.n_unique(subset=다중열)`이 첫 열만 세는 버그 — struct로 묶어 수정 | ribb 테스트 통과 |
| [run-llama/llama_index#22724](https://github.com/run-llama/llama_index/pull/22724) | mcp 2.x `streamable_http_client` 3-튜플 unpack 크래시 수정 | 리뷰어 실재 재현 완료 |

## 업무 역량을 보여주는 프로세스

- **근본 원인 분석 중심**: 이슈의 내·외부 신호를 교차 검증(기존 테스트가 버그를 명세하는지, 커밋 히스토리에서 이미 수정됐는지, 형제 구현과 일관성) 후, 실제 코드로 버그 재현을 먼저 검증하고 수정
- **리뷰어 협업**: 신규 보안(서명 커밋)부터 성능·설계 우려까지 리뷰어 피드백을 수용하고, 제안된 대안이 실제로 유효한지 로컬에서 검증해 정확한 해법을 제시
- **테스트 우선**: 수정마다 회귀 테스트/재현 케이스 추가, 플랫폼별 CI 실패 시 pre-existing 이슈인지 구분

## 기술 스택

Python · PyTorch · SQLAlchemy · Kubernetes · Git/GitHub · CI/CD · 테스트(pytest) · 데이터 파이프라인(dlt) · LLM 인프라(vLLM · LlamaIndex · LiteLLM)

---

### Resume 활용 팁
- PDF로 저장해 제출하려면 이 파일의 표를 지원서 텍스트로 변환해 **3-5줄 불릿으로 압축**하는 걸 권장합니다.
- 예: "Open-source contributor with 3 merged PRs across celery/billiard, dlt, and grafana, plus 17 in review across polars, llama_index, vLLM, LiteLLM — focused on RAG/data infrastructure bug fixes from root-cause analysis through maintainer collaboration."
