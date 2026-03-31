---
name: opendart
description: General OpenDART usage, auth setup, corp_code resolution, endpoint selection, and routing to detailed areas.
---

# OpenDART

Use this umbrella skill for broad OpenDART questions, first-time setup, auth/key handling, corp_code lookup, and endpoint selection.

## Use when
- The user says OpenDART, DART, 공시, 기업개황, corp_code, or asks which endpoint/family to use.
- The request spans multiple OpenDART areas.
- You need to decide whether a specialist skill should handle the task.

## Route away when
- 공시정보 detail work belongs in `opendart-disclosures`
- 정기보고서 주요정보 belongs in `opendart-periodic-reports`
- 정기보고서 재무정보 or 활용마당 belongs in `opendart-financials`
- 지분공시 종합정보 belongs in `opendart-equity`
- 주요사항보고서 주요정보 belongs in `opendart-material-events`
- 증권신고서 주요정보 belongs in `opendart-registration`

## Workflow
1. Read `references/service-overview.md` for the OpenDART mental model.
2. Read `references/auth-corpcode-errors.md` before any API call.
3. Use `references/routing-matrix.md` to pick the specialist skill when the request is domain-specific.
4. For repeatable calls or corp-code resolution, use `python3 skills/opendart/scripts/opendart_cli.py ...` or `python3 -m shared.opendart_common.cli ...`.
5. Use `references/guide-family-map.md` to keep family ownership aligned.
6. Use `references/frontmatter-manifest.md` when updating skill metadata.

## Guardrails
- Never store or echo real `crtfc_key` values in repo files.
- Prefer the specialist skill when the request clearly names a domain family.
- Keep this umbrella skill short; the references carry the details.
