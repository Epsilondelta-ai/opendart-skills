# Frontmatter manifest

This file is the source of truth for intended skill metadata.

| Skill directory | name | description |
|---|---|---|
| `skills/opendart/` | `opendart` | General OpenDART usage, auth setup, corp_code resolution, endpoint selection, and routing to detailed areas. |
| `skills/opendart-disclosures/` | `opendart-disclosures` | OpenDART 공시정보 search, filing lookup, and attachment/original-document workflows. |
| `skills/opendart-periodic-reports/` | `opendart-periodic-reports` | OpenDART 정기보고서 주요정보 workflows. |
| `skills/opendart-financials/` | `opendart-financials` | OpenDART 정기보고서 재무정보 and 활용마당 financial query/download workflows. |
| `skills/opendart-equity/` | `opendart-equity` | OpenDART 지분공시 종합정보 workflows. |
| `skills/opendart-material-events/` | `opendart-material-events` | OpenDART 주요사항보고서 주요정보 workflows. |
| `skills/opendart-registration/` | `opendart-registration` | OpenDART 증권신고서 주요정보 workflows. |

## Manifest rule
- SKILL.md frontmatter must match this file exactly for `name` and purpose.
- Keep specialist descriptions narrow enough to avoid collisions with the umbrella skill.
