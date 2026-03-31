# Auth, corp_code, and error handling

## Auth rules
- OpenDART uses `crtfc_key` as a 40-character API key.
- Supply the key at runtime through `OPENDART_API_KEY`; never commit secrets.
- The live smoke lane is **opt-in** and must skip cleanly when the key is absent.
- If setup is requested, tell the user to provide their own key rather than inventing one.

## corp_code rules
- Many OpenDART queries require `corp_code`.
- If only a company name is known, resolve it first with the corp-code dataset.
- Use `python3 -m shared.opendart_common.cli corp-code refresh` and `... corp-code search --name <회사명>` for repeatable corp-code flows.
- Use `python3 -m shared.opendart_common.cli corp-code status` to check freshness before trusting cached lookups.

## Common status codes
- `000`: 정상
- `010`: 등록되지 않은 키
- `011`: 사용할 수 없는 키
- `012`: 접근할 수 없는 IP
- `013`: 조회된 데이터가 없음
- `014`: 파일이 존재하지 않음
- `020`: 요청 제한 초과
- `021`: 조회 가능한 회사 수 초과(최대 100건)
- `100`: 필드의 부적절한 값
- `101`: 부적절한 접근
- `800`: 시스템 점검
- `900`: 정의되지 않은 오류
- `901`: 개인정보 보유기간 만료 계정

## Handling guidance
- `013` often means the request was valid but there is no result.
- `020` means back off, cache, and retry later rather than looping aggressively.
- `800` and `900` are operational issues; retry conservatively.
- `100`/`101` usually point to request construction mistakes.
- Live smoke tests should document quota usage, possible `013`, and maintenance windows instead of treating every non-success as a code defect.
