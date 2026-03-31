# OpenDART service overview

OpenDART is the FSS public API for corporate disclosures and financial data.

## Core concepts
- `crtfc_key`: OpenDART API key. Treat as a secret.
- `corp_code`: OpenDART corporation identifier used across many endpoints.
- Output can be JSON, XML, or ZIP/binary depending on the endpoint.

## Families handled inside this skill
- 공시정보
- 정기보고서 주요정보
- 정기보고서 재무정보
- 활용마당
- 지분공시 종합정보
- 주요사항보고서 주요정보
- 증권신고서 주요정보

## Portable package rule
This skill is designed so `skills/opendart/` is the main package. The helper code, references, and tests live under this directory.
