# Guide-family ownership map

| OpenDART guide family | Skill owner | Notes |
|---|---|---|
| 공시정보 | `opendart-disclosures` | Filing search, list, original-document, and attachment retrieval |
| 정기보고서 주요정보 | `opendart-periodic-reports` | Dividend, employee, executive, shareholder, audit-related extracts |
| 정기보고서 재무정보 | `opendart-financials` | Financial statements, indicators, and related query/download flows |
| 지분공시 종합정보 | `opendart-equity` | Major shareholding and related equity disclosure workflows |
| 주요사항보고서 주요정보 | `opendart-material-events` | Major event disclosure workflows |
| 증권신고서 주요정보 | `opendart-registration` | Securities registration statement workflows |
| 활용마당 | `opendart-financials` | Financial query/download helper workflows |

## Boundary rule
- If a request names a family above, route to the owning specialist skill.
- If the request is generic or cross-family, stay in the umbrella skill first.
- `corp_code`, 기업개황, setup questions, and API-selection questions remain umbrella-owned even though they support 공시정보 flows.
- Disclosure-only retrieval requests belong in `opendart-disclosures` once setup/corp-code ambiguity is resolved.

## Ownership check
- Every family in this table must have:
  - at least one representative endpoint in the shared catalog
  - at least one reference file in the owning skill
  - at least one prompt entry in `tests/skill_smoke/prompt_matrix.json`
