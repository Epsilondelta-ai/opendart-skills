# Auth, corp_code, cache, and error handling

## Auth rules
- OpenDART uses `crtfc_key` as the API key.
- Supply the key at runtime through `OPENDART_API_KEY` or an explicit CLI argument.
- Never commit secrets.
- Live tests are opt-in and skip by default when `OPENDART_API_KEY` is absent.

## corp_code rules
- Many OpenDART queries require `corp_code`.
- If only a company name is known, resolve it first with the corp-code dataset.
- Use the local helper:
  - `python3 skills/opendart/scripts/opendart_cli.py corp-code refresh`
  - `python3 skills/opendart/scripts/opendart_cli.py corp-code search --name <회사명>`
  - `python3 skills/opendart/scripts/opendart_cli.py corp-code status`

## Cache freshness
- Default corp-code TTL is 7 days unless `OPENDART_CORP_CODE_TTL_DAYS` overrides it.
- Treat missing cache, missing metadata, and expired TTL as refresh signals.
- Refresh stale corp-code data before debugging downstream no-data or invalid-code cases.

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
- `013` often means a valid request returned no data for the chosen period.
- `020` means back off, cache, and retry later.
- `800` and `900` are operational failures; retry conservatively.
- `100` and `101` usually mean request-construction mistakes.
