from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .api import OpenDartClient
from .endpoint_catalog import ENDPOINTS, EXPECTED_GUIDE_FAMILIES, list_endpoints
from .errors import STATUS_LABELS, describe_status


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def runtime_error(message: str, *, hint: str | None = None, exit_code: int = 2) -> int:
    payload = {"status": "error", "message": message}
    if hint:
        payload["hint"] = hint
    print_json(payload)
    return exit_code


def cmd_corp_refresh(args: argparse.Namespace) -> int:
    try:
        client = OpenDartClient(api_key=args.api_key, cache_dir=args.cache_dir)
        rows = client.fetch_corp_codes()
    except ValueError as exc:
        return runtime_error(str(exc), hint="Use --api-key or export OPENDART_API_KEY before refreshing corp-code data.")
    print_json({"rows": len(rows), "cache_dir": args.cache_dir, "status": client.corp_code_status()})
    return 0


def cmd_corp_search(args: argparse.Namespace) -> int:
    client = OpenDartClient(api_key=args.api_key, cache_dir=args.cache_dir)
    status = client.corp_code_status()
    try:
        rows = client.search_corp_codes(name=args.name, stock_code=args.stock_code, exact=args.exact, limit=args.limit)
    except ValueError as exc:
        if status["reason"] == "missing_xml_cache" and not status.get("archive_exists") and not status.get("records_exists"):
            print_json({"message": "missing corp-code cache; run `corp-code refresh` first", "cache_status": status, "results": []})
            return 2
        return runtime_error(str(exc), hint="Refresh corp-code cache or provide OPENDART_API_KEY so search can auto-refresh.")
    status = client.corp_code_status()
    if status["stale"]:
        print(f"warning: corp-code cache is stale ({status['reason']}); run `corp-code refresh` before relying on these results.", file=sys.stderr)
    print_json({"cache_status": status, "results": [asdict(row) for row in rows]})
    return 0


def cmd_corp_status(args: argparse.Namespace) -> int:
    print_json(OpenDartClient(cache_dir=args.cache_dir).corp_code_status())
    return 0


def cmd_company(args: argparse.Namespace) -> int:
    try:
        print_json(OpenDartClient(api_key=args.api_key, cache_dir=args.cache_dir).company_overview(args.corp_code))
        return 0
    except ValueError as exc:
        return runtime_error(str(exc), hint="Company overview is a live call; provide OPENDART_API_KEY.")


def cmd_list(args: argparse.Namespace) -> int:
    try:
        payload = OpenDartClient(api_key=args.api_key, cache_dir=args.cache_dir).disclosure_list(
            corp_code=args.corp_code,
            bgn_de=args.bgn_de,
            end_de=args.end_de,
            last_reprt_at=args.last_reprt_at,
            pblntf_ty=args.pblntf_ty,
            page_no=args.page_no,
            page_count=args.page_count,
        )
        print_json(payload)
        return 0
    except ValueError as exc:
        return runtime_error(str(exc), hint="Disclosure search is a live call; provide OPENDART_API_KEY.")


def cmd_endpoint(args: argparse.Namespace) -> int:
    items = [{
        "name": item.name,
        "family": item.family,
        "section": item.section,
        "path": item.path,
        "required_params": list(item.required_params),
        "description": item.description,
        "source_url": item.source_url,
    } for item in list_endpoints(family=args.family, section=args.section)]
    print_json({"expected_guide_families": list(EXPECTED_GUIDE_FAMILIES), "items": items})
    return 0


def cmd_call(args: argparse.Namespace) -> int:
    try:
        client = OpenDartClient(api_key=args.api_key, cache_dir=args.cache_dir)
        params = dict(item.split("=", 1) for item in args.param)
        payload = client.call_endpoint(args.endpoint, **params)
        if isinstance(payload, bytes):
            print_json({"bytes": len(payload), "endpoint": args.endpoint})
        else:
            print_json(payload)
        return 0
    except ValueError as exc:
        return runtime_error(str(exc), hint="Representative endpoint calls are live requests; provide OPENDART_API_KEY.")


def cmd_status(args: argparse.Namespace) -> int:
    print_json({"code": args.code, "label": describe_status(args.code), "known": args.code in STATUS_LABELS})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python3 skills/opendart/scripts/opendart_cli.py", description="Self-contained OpenDART skill helper CLI")
    parser.add_argument("--api-key", help="OpenDART API key; defaults to OPENDART_API_KEY")
    parser.add_argument("--cache-dir", help="override cache directory")
    sub = parser.add_subparsers(dest="command", required=True)

    corp = sub.add_parser("corp-code", help="corp-code cache operations")
    corp_sub = corp.add_subparsers(dest="corp_command", required=True)
    refresh = corp_sub.add_parser("refresh", help="download and cache corpCode.zip")
    refresh.set_defaults(func=cmd_corp_refresh)
    search = corp_sub.add_parser("search", help="search cached corp codes")
    search.add_argument("--name")
    search.add_argument("--stock-code")
    search.add_argument("--exact", action="store_true")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_corp_search)
    corp_status = corp_sub.add_parser("status", help="inspect corp-code cache freshness")
    corp_status.set_defaults(func=cmd_corp_status)

    company = sub.add_parser("company", help="fetch company overview")
    company.add_argument("--corp-code", required=True)
    company.set_defaults(func=cmd_company)

    listing = sub.add_parser("list", help="run disclosure list search")
    listing.add_argument("--corp-code")
    listing.add_argument("--bgn-de")
    listing.add_argument("--end-de")
    listing.add_argument("--last-reprt-at")
    listing.add_argument("--pblntf-ty")
    listing.add_argument("--page-no")
    listing.add_argument("--page-count")
    listing.set_defaults(func=cmd_list)

    endpoint = sub.add_parser("endpoint", help="show representative endpoint entries")
    endpoint.add_argument("--family")
    endpoint.add_argument("--section")
    endpoint.set_defaults(func=cmd_endpoint)

    call = sub.add_parser("call", help="call a representative endpoint")
    call.add_argument("endpoint", choices=sorted(ENDPOINTS))
    call.add_argument("--param", action="append", default=[], metavar="KEY=VALUE")
    call.set_defaults(func=cmd_call)

    status = sub.add_parser("status", help="translate OpenDART status codes")
    status.add_argument("code")
    status.set_defaults(func=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
