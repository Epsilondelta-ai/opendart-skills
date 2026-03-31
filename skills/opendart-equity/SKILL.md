---
name: opendart-equity
description: OpenDART 지분공시 종합정보 workflows.
---

# Equity

Use this specialist skill for 대량보유, 임원/주요주주 소유상황, 지분공시 종합정보.

## Workflow
- Stay within this skill for the family listed in the manifest.
- Start with this skill's `references/` files for endpoint and recipe guidance.
- Use `python3 -m shared.opendart_common.cli endpoint --skill opendart-equity` to inspect the representative endpoint catalog.
- Use the umbrella `opendart` skill if the request is broad or ambiguous.
- Refer back to `skills/opendart/references/guide-family-map.md` when in doubt.

## Guardrails
- Do not broaden the scope beyond the family owned here.
- Keep examples and endpoint notes in the reference files.
- Prefer concise responses focused on the owning family.
