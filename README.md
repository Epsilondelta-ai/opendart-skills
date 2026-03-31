# opendart-skills

[한국어](README.md) | [English](README.en.md)

이 저장소의 핵심 deliverable은 **self-contained OpenDART skill package**인 `skills/opendart/`다.

즉, 이 저장소는 다음처럼 이해하면 된다:

```text
skills/
  opendart/
    SKILL.md
    references/
    scripts/
    tests/
```

## 핵심 원칙
- `skills/opendart/` 하나가 메인 패키지다.
- `shared/`, `core/`, `adapters/` 같은 상위 구조에 의존하지 않는다.
- helper 코드도 `skills/opendart/scripts/` 안에 있다.
- OpenDART family 구분은 separate top-level skill이 아니라 이 skill 내부 reference/routing으로 처리한다.

## 포함 범위
- 공시정보
- 정기보고서 주요정보
- 정기보고서 재무정보
- 활용마당
- 지분공시 종합정보
- 주요사항보고서 주요정보
- 증권신고서 주요정보

## 주요 진입점
- skill 설명: `skills/opendart/SKILL.md`
- reference: `skills/opendart/references/`
- helper scripts: `skills/opendart/scripts/`
- tests: `skills/opendart/tests/`

## CLI 예시
```bash
python3 skills/opendart/scripts/opendart_cli.py --help
python3 skills/opendart/scripts/opendart_cli.py corp-code status
python3 skills/opendart/scripts/check_guide_sync.py
```

## 검증
```bash
python3 -m unittest discover skills/opendart/tests
python3 -m compileall skills/opendart/scripts
python3 skills/opendart/scripts/check_guide_sync.py
```

live smoke lane:
```bash
OPENDART_API_KEY=... python3 -m unittest discover skills/opendart/tests -p 'test_live_lane.py'
```

## 이동성
다른 환경에서 쓰려면 기본적으로 `skills/opendart/` 디렉토리만 가져가면 된다.

## Migration notes
- old top-level helper locations such as `shared/`, `core/`, `adapters/`, and repo-level `tests/` were collapsed into `skills/opendart/`.
- if you previously referenced repo-level paths directly, switch to the equivalents under `skills/opendart/`.
- the intended portable unit is now the `skills/opendart/` directory itself.

Legacy path checker:
```bash
python3 skills/opendart/scripts/check_legacy_references.py <target-dir>
```
