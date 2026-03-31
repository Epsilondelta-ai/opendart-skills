# OpenDART service overview

OpenDART is the FSS public API for corporate disclosures and financial data.

## Core concepts
- `crtfc_key`: API authorization key. Treat as a secret.
- `corp_code`: OpenDART corporation identifier used by many endpoints.
- Output: JSON, XML, or ZIP/binary depending on endpoint.
- Discovery: use the umbrella skill to select the right family, then route to a specialist skill.

## Family map
- 공시정보 -> `opendart-disclosures`
- 정기보고서 주요정보 -> `opendart-periodic-reports`
- 정기보고서 재무정보 -> `opendart-financials`
- 지분공시 종합정보 -> `opendart-equity`
- 주요사항보고서 주요정보 -> `opendart-material-events`
- 증권신고서 주요정보 -> `opendart-registration`
- 활용마당 -> `opendart-financials`

## Shared helper paths
- Wrapper CLI: `python3 skills/opendart/scripts/opendart_cli.py --help`
- Shared CLI: `python3 -m shared.opendart_common.cli --help`
- Guide sync check: `python3 scripts/check_opendart_guide_sync.py`
- Use the shared CLI for corp-code refresh/search, company overview, disclosure list, endpoint catalog, and representative endpoint calls.

## Verification lanes
- **Offline-first default**: unit/smoke tests and guide-sync checks run without credentials.
- **Opt-in live lane**: `python3 -m unittest discover tests/opendart_live` only when `OPENDART_API_KEY` is set.
- Live smoke coverage is intentionally minimal: corp-code refresh, company overview, one disclosure query, and one financial endpoint.

## Operational notes
- Resolve corp names to `corp_code` before making detail queries.
- Prefer the smallest family that still covers the request.
- If the request spans families, answer with the umbrella skill first and then split the task.
- Expect no-data (`013`) and maintenance windows; live smoke tests should treat those as operational caveats, not blanket regressions.
