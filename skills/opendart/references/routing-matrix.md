# Routing matrix

| Prompt shape | Internal family section |
|---|---|
| "OpenDART", "DART", "corp_code", "기업개황", "어떤 API를 써야 해?" | umbrella / overview |
| "공시 목록", "공시 검색", "첨부", "원문" | disclosures |
| "정기보고서 주요정보", "임원", "직원", "배당", "감사" | periodic-reports |
| "재무제표", "재무지표", "활용마당", "재무 다운로드" | financials |
| "지분공시", "대량보유", "최대주주", "특수관계인" | equity |
| "주요사항보고서", "합병", "분할", "이벤트" | material-events |
| "증권신고서", "신고서 주요정보", "투자설명서", "모집", "매출" | registration |

## Routing rule
- Prefer the most specific family section that matches the request wording.
- Use the umbrella overview first when the request is mixed, generic, or starts with auth/corp_code setup.
