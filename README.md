# opendart-skills

[한국어](README.md) | [English](README.en.md)

OpenDART([opendart.fss.or.kr](https://opendart.fss.or.kr/))를 Codex/OMX 환경에서 안전하게 활용하기 위한 **full-scope skill suite**다.

이 저장소는 다음을 포함한다.
- umbrella skill 1개: `opendart`
- specialist skills 6개
- 공통 Python helper layer
- offline-first 검증 스위트
- `OPENDART_API_KEY`가 있을 때만 동작하는 opt-in live smoke test

## 목표

이 프로젝트는 OpenDART의 주요 가이드 영역 전체를 다룬다.

- 공시정보
- 정기보고서 주요정보
- 정기보고서 재무정보
- 활용마당
- 지분공시 종합정보
- 주요사항보고서 주요정보
- 증권신고서 주요정보

핵심 설계 원칙:
- **full-scope**: 축소형 v1이 아니라 전체 범위를 스킬 구조로 담음
- **router + specialist**: broad request는 umbrella skill이 받고, 구체 요청은 specialist skill로 분기
- **shared mechanics**: corp_code, cache, endpoint catalog, status handling을 공통 레이어로 관리
- **offline-first**: 기본 검증은 실제 API 키 없이 가능
- **opt-in live lane**: 실제 OpenDART 호출 검증은 명시적으로만 수행

## 저장소 구조

```text
scripts/
  check_opendart_guide_sync.py

shared/
  opendart_common/
    api.py
    cache.py
    cli.py
    corpcode.py
    endpoint_catalog.py
    errors.py

skills/
  opendart/
  opendart-disclosures/
  opendart-periodic-reports/
  opendart-financials/
  opendart-equity/
  opendart-material-events/
  opendart-registration/

tests/
  opendart_common/
  opendart_live/
  skill_smoke/
```

## Skill 구성

### 1. Umbrella
- `opendart`
  - OpenDART 개요
  - 인증키/`corp_code` 안내
  - endpoint 선택
  - specialist skill routing

### 2. Specialists
- `opendart-disclosures`
- `opendart-periodic-reports`
- `opendart-financials`
- `opendart-equity`
- `opendart-material-events`
- `opendart-registration`

각 skill의 frontmatter 의도와 ownership은 아래 파일에서 관리한다.
- `skills/opendart/references/frontmatter-manifest.md`
- `skills/opendart/references/guide-family-map.md`
- `skills/opendart/references/routing-matrix.md`

## 공통 helper

공통 helper는 `shared/opendart_common/` 아래에 있다.

주요 기능:
- `OpenDartClient`: 공통 API wrapper
- corp-code ZIP/XML 처리 및 검색
- corp-code cache freshness 확인
- representative endpoint catalog
- status code translation
- CLI 기반 수동 점검

### CLI 예시

```bash
python3 skills/opendart/scripts/opendart_cli.py --help
python3 -m shared.opendart_common.cli --help
```

corp-code cache 상태 확인:

```bash
python3 -m shared.opendart_common.cli corp-code status
```

corp-code refresh:

```bash
python3 -m shared.opendart_common.cli --api-key "$OPENDART_API_KEY" corp-code refresh
```

corp-code 검색:

```bash
python3 -m shared.opendart_common.cli corp-code search --name 삼성전자
```

대표 endpoint catalog 보기:

```bash
python3 -m shared.opendart_common.cli endpoint --skill opendart-financials
```

## 요구 사항

- Python 3.11+
- 선택 사항: `OPENDART_API_KEY`

기본 검증에는 API 키가 필요 없다.
실제 OpenDART live smoke test를 돌릴 때만 키가 필요하다.

## 환경 변수

### 기본
- `OPENDART_API_KEY`
  - OpenDART live 요청 시 사용
- `OPENDART_CACHE_DIR`
  - corp-code cache 위치 override
- `OPENDART_CORP_CODE_TTL_DAYS`
  - corp-code cache freshness TTL override

### live lane 선택값
- `OPENDART_LIVE_CORP_NAME`
- `OPENDART_LIVE_BSNS_YEAR`
- `OPENDART_LIVE_REPRT_CODE`
- `OPENDART_LIVE_FS_DIV`

## 검증

### 1. 기본 offline 검증

```bash
python3 -m unittest discover tests
python3 -m compileall shared skills tests scripts
python3 scripts/check_opendart_guide_sync.py
```

### 2. skill smoke 검증

```bash
python3 -m unittest discover tests/skill_smoke
```

이 스위트는 다음을 확인한다.
- frontmatter manifest 일치
- prompt ownership
- boundary prompt coverage
- specialist trigger 충돌 방지

### 3. opt-in live smoke 검증

```bash
OPENDART_API_KEY=... python3 -m unittest discover tests/opendart_live
```

키가 없으면 테스트는 **실패가 아니라 skip** 된다.

live lane 최소 검증 범위:
- corp-code refresh/download
- company overview
- disclosure list
- financial endpoint 1개

## 운영 주의사항

- 실제 OpenDART 호출은 quota를 소모한다.
- `020`은 요청 제한 초과를 의미한다.
- 유효한 요청이어도 `013`(데이터 없음)이 나올 수 있다.
- 점검 시간에는 `800` 또는 기타 운영성 오류가 나올 수 있다.
- corp-code miss를 바로 오류로 단정하지 말고, 먼저 cache freshness를 확인하라.

## 리스크 저감 반영 상태

현재 저장소는 다음 hardening을 반영했다.
- ambiguous / boundary prompt 확장
- prompt ownership 검증 강화
- corp-code cache freshness / stale detection
- stale-cache / no-key CLI guidance
- opt-in live smoke lane
- guide-family drift check
- endpoint catalog growth threshold 문서화

## 참고 문서

- OpenDART 메인: https://opendart.fss.or.kr/
- 개발가이드 메인: https://opendart.fss.or.kr/guide/main.do
- 이용약관: https://opendart.fss.or.kr/intro/terms.do

## 주의

이 저장소는 **재사용 가능한 skill / helper / test 자산만** 버전 관리한다.
세션 상태, 로그, 계획 산출물 등 런타임 산출물은 `.omx/` 아래에 두고 git에서는 제외한다.
