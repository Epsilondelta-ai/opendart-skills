---
name: opendart-registration
description: OpenDART 증권신고서 주요정보 workflows.
---

# Registration

Use this specialist skill for 증권신고서 주요정보와 신고서 요약.

## Workflow
- Stay within this skill for the family listed in the manifest.
- Start with this skill's `references/` files for endpoint and recipe guidance.
- Use `python3 -m shared.opendart_common.cli endpoint --skill opendart-registration` to inspect the representative endpoint catalog.
- Use the umbrella `opendart` skill if the request is broad or ambiguous.
- Refer back to `skills/opendart/references/guide-family-map.md` when in doubt.

## Guardrails
- Do not broaden the scope beyond the family owned here.
- Keep examples and endpoint notes in the reference files.
- Prefer concise responses focused on the owning family.
