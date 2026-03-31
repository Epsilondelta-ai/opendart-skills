# Routing matrix

| Prompt shape | Skill |
|---|---|
| "OpenDART", "DART", "corp_code", "기업개황", "어떤 API를 써야 해?" | `opendart` |
| "공시 목록", "공시 검색", "첨부/원문 찾기" | `opendart-disclosures` |
| "정기보고서 주요정보", "임원", "직원", "배당", "감사" | `opendart-periodic-reports` |
| "재무제표", "재무지표", "활용마당", "재무 다운로드" | `opendart-financials` |
| "지분공시", "대량보유", "최대주주", "특수관계인" | `opendart-equity` |
| "주요사항보고서", "주요사항 공시" | `opendart-material-events` |
| "증권신고서", "신고서 주요정보" | `opendart-registration` |

## Routing rule
- Prefer the most specific skill that matches the user wording.
- Keep the umbrella skill as the default landing surface for mixed or ambiguous prompts.

## Umbrella vs disclosures boundary
- Stay in `opendart` when the user is:
  - asking what `corp_code` is
  - asking how to choose between 기업개황 and 공시 APIs
  - combining setup, corp-code resolution, and filing lookup in one request
  - asking for cross-family routing help
- Route to `opendart-disclosures` when the user is:
  - already focused on 공시 목록/검색
  - asking for 원문, 첨부, or filing detail retrieval
  - saying corp-code is already known and only disclosure retrieval remains
- Boundary prompts must be represented in `tests/skill_smoke/prompt_matrix.json` so routing regressions fail in tests.
