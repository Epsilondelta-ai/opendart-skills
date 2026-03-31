# opendart-skills

[한국어](README.md) | [English](README.en.md)

A **full-scope OpenDART skill suite** for using OpenDART ([opendart.fss.or.kr](https://opendart.fss.or.kr/)) safely in Codex/OMX environments.

This repository includes:
- one umbrella skill: `opendart`
- six specialist skills
- a shared Python helper layer
- an offline-first verification suite
- an opt-in live smoke-test lane that only runs when `OPENDART_API_KEY` is available

## Goals

This project covers the major OpenDART guide families end to end:

- Disclosure information
- Key information from periodic reports
- Financial information from periodic reports
- Utility / financial query-download workflows
- Equity disclosure information
- Major event report information
- Registration statement information

Core design principles:
- **full scope**: represent the whole domain instead of shipping a narrowed-down v1
- **router + specialists**: the umbrella skill handles broad requests and routes detailed requests to specialist skills
- **shared mechanics**: centralize corp code lookup, cache handling, endpoint cataloging, and status translation
- **offline first**: default verification works without a real API key
- **opt-in live lane**: real OpenDART calls are verified only when explicitly enabled

## Repository layout

```text
scripts/
  check_opendart_guide_sync.py

shared/
  opendart_common/
    api.py
    cache.py
    cli.py
    corpcode.py
    endpoint_catalog.py
    errors.py

skills/
  opendart/
  opendart-disclosures/
  opendart-periodic-reports/
  opendart-financials/
  opendart-equity/
  opendart-material-events/
  opendart-registration/

tests/
  opendart_common/
  opendart_live/
  skill_smoke/
```

## Skill structure

### 1. Umbrella
- `opendart`
  - OpenDART overview
  - auth / `corp_code` guidance
  - endpoint selection
  - routing to specialist skills

### 2. Specialists
- `opendart-disclosures`
- `opendart-periodic-reports`
- `opendart-financials`
- `opendart-equity`
- `opendart-material-events`
- `opendart-registration`

Frontmatter intent and ownership are managed in:
- `skills/opendart/references/frontmatter-manifest.md`
- `skills/opendart/references/guide-family-map.md`
- `skills/opendart/references/routing-matrix.md`

## Shared helper layer

The shared helper layer lives under `shared/opendart_common/`.

Key features:
- `OpenDartClient`: common API wrapper
- corp-code ZIP/XML parsing and search
- corp-code cache freshness checks
- representative endpoint catalog
- status code translation
- CLI-based manual inspection tools

### CLI examples

```bash
python3 skills/opendart/scripts/opendart_cli.py --help
python3 -m shared.opendart_common.cli --help
```

Check corp-code cache status:

```bash
python3 -m shared.opendart_common.cli corp-code status
```

Refresh corp-code cache:

```bash
python3 -m shared.opendart_common.cli --api-key "$OPENDART_API_KEY" corp-code refresh
```

Search corp codes:

```bash
python3 -m shared.opendart_common.cli corp-code search --name Samsung
```

Inspect the representative endpoint catalog:

```bash
python3 -m shared.opendart_common.cli endpoint --skill opendart-financials
```

## Requirements

- Python 3.11+
- optional: `OPENDART_API_KEY`

The default verification flow does not require a real API key.
A key is only needed for the opt-in live smoke-test lane.

## Environment variables

### Core
- `OPENDART_API_KEY`
  - used for live OpenDART requests
- `OPENDART_CACHE_DIR`
  - overrides the corp-code cache location
- `OPENDART_CORP_CODE_TTL_DAYS`
  - overrides corp-code cache freshness TTL

### Live-lane options
- `OPENDART_LIVE_CORP_NAME`
- `OPENDART_LIVE_BSNS_YEAR`
- `OPENDART_LIVE_REPRT_CODE`
- `OPENDART_LIVE_FS_DIV`

## Verification

### 1. Default offline verification

```bash
python3 -m unittest discover tests
python3 -m compileall shared skills tests scripts
python3 scripts/check_opendart_guide_sync.py
```

### 2. Skill smoke verification

```bash
python3 -m unittest discover tests/skill_smoke
```

This suite checks:
- frontmatter-manifest consistency
- prompt ownership
- boundary prompt coverage
- specialist trigger collision prevention

### 3. Opt-in live smoke verification

```bash
OPENDART_API_KEY=... python3 -m unittest discover tests/opendart_live
```

If the key is absent, the test lane **skips instead of failing**.

Minimal live coverage:
- corp-code refresh/download
- company overview
- disclosure list
- one financial endpoint

## Operational cautions

- Real OpenDART calls consume quota.
- `020` means request limit exceeded.
- Even valid requests can return `013` when no data exists for the selected period.
- Maintenance windows may produce `800` or other service-side failures.
- Do not assume a corp-code miss is final before checking cache freshness.

## Implemented hardening

This repository already includes the following risk-reduction work:
- ambiguous / boundary prompt expansion
- stronger prompt ownership verification
- corp-code cache freshness / stale detection
- stale-cache / no-key CLI guidance
- opt-in live smoke-test lane
- guide-family drift checks
- documented endpoint catalog growth thresholds

## References

- OpenDART main: https://opendart.fss.or.kr/
- OpenDART guide main: https://opendart.fss.or.kr/guide/main.do
- Terms: https://opendart.fss.or.kr/intro/terms.do

## Note

This repository versions only **reusable skill, helper, and test assets**.
Runtime session artifacts such as state, logs, and planning output belong under `.omx/` and are intentionally excluded from git.
