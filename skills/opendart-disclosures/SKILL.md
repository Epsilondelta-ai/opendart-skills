---
name: opendart-disclosures
description: OpenDART 공시정보 search, filing lookup, and attachment/original-document workflows.
---

# Disclosures

Use this specialist skill for 공시 목록, 공시 검색, 원문/첨부 탐색, filing lookup.

## Workflow
- Stay within this skill for the family listed in the manifest.
- Start with this skill's `references/` files for endpoint and recipe guidance.
- Use `python3 -m shared.opendart_common.cli endpoint --skill opendart-disclosures` to inspect the representative endpoint catalog.
- Use the umbrella `opendart` skill if the request is broad or ambiguous.
- Refer back to `skills/opendart/references/guide-family-map.md` when in doubt.

## Guardrails
- Do not broaden the scope beyond the family owned here.
- Keep examples and endpoint notes in the reference files.
- Prefer concise responses focused on the owning family.
