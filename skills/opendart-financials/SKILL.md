---
name: opendart-financials
description: OpenDART 정기보고서 재무정보 and 활용마당 financial query/download workflows.
---

# Financials

Use this specialist skill for 재무제표, 재무지표, 비교 조회, 활용마당 financial query/download.

## Workflow
- Stay within this skill for the family listed in the manifest.
- Start with this skill's `references/` files for endpoint and recipe guidance.
- Use `python3 -m shared.opendart_common.cli endpoint --skill opendart-financials` to inspect the representative endpoint catalog.
- Use the umbrella `opendart` skill if the request is broad or ambiguous.
- Refer back to `skills/opendart/references/guide-family-map.md` when in doubt.

## Guardrails
- Do not broaden the scope beyond the family owned here.
- Keep examples and endpoint notes in the reference files.
- Prefer concise responses focused on the owning family.
