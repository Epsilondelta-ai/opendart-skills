# Legacy path map

Use this table when updating code, docs, or scripts that still reference removed top-level paths.

| Old path | New path |
|---|---|
| `shared/opendart_common/api.py` | `skills/opendart/scripts/lib/api.py` |
| `shared/opendart_common/cache.py` | `skills/opendart/scripts/lib/cache.py` |
| `shared/opendart_common/cli.py` | `skills/opendart/scripts/lib/cli.py` |
| `shared/opendart_common/corpcode.py` | `skills/opendart/scripts/lib/corpcode.py` |
| `shared/opendart_common/endpoint_catalog.py` | `skills/opendart/scripts/lib/endpoint_catalog.py` |
| `shared/opendart_common/errors.py` | `skills/opendart/scripts/lib/errors.py` |
| `scripts/check_opendart_guide_sync.py` | `skills/opendart/scripts/check_guide_sync.py` |
| `tests/opendart_common/*` | `skills/opendart/tests/*` |
| `tests/opendart_live/test_live_lane.py` | `skills/opendart/tests/test_live_lane.py` |
| `tests/skill_smoke/*` | `skills/opendart/tests/test_prompt_routing.py` and `skills/opendart/references/*` |
| `skills/opendart-disclosures/*` | `skills/opendart/references/family-disclosures.md` |
| `skills/opendart-periodic-reports/*` | `skills/opendart/references/family-periodic-reports.md` |
| `skills/opendart-financials/*` | `skills/opendart/references/family-financials.md` |
| `skills/opendart-equity/*` | `skills/opendart/references/family-equity.md` |
| `skills/opendart-material-events/*` | `skills/opendart/references/family-material-events.md` |
| `skills/opendart-registration/*` | `skills/opendart/references/family-registration.md` |
| `core/opendart/manifests/*` | `skills/opendart/references/*.md` |
| `core/opendart/families/*` | `skills/opendart/references/family-*.md` |
| `adapters/codex/*` | no direct replacement; use the self-contained `skills/opendart/` package |

## Recommended migration flow
1. Run `python3 skills/opendart/scripts/check_legacy_references.py <target-dir>`.
2. Review the reported matches.
3. Replace each old path with the mapped new path from this table.
4. Re-run the checker until it reports no legacy references.
