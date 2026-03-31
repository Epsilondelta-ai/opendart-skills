from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from xml.etree.ElementTree import ParseError

from .cache import corp_code_archive_path, corp_code_cache_status, corp_code_xml_path, write_corp_code_metadata
from .corpcode import CorpRecord, extract_corp_code_xml, parse_corp_code_xml, search_records
from .endpoint_catalog import get_endpoint
from .errors import ensure_success

BASE_URL = "https://opendart.fss.or.kr"


@dataclass
class OpenDartClient:
    api_key: str | None = None
    timeout: int = 30
    opener: Callable = urlopen
    cache_dir: str | None = None

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("OPENDART_API_KEY")

    def require_api_key(self) -> str:
        if not self.api_key:
            raise ValueError("OPENDART_API_KEY is required; live requests are opt-in and skipped by default when absent.")
        return self.api_key

    def build_url(self, path: str, params: dict[str, object | None]) -> str:
        query = {"crtfc_key": self.require_api_key()}
        for key, value in params.items():
            if value is None:
                continue
            query[key] = str(value)
        return f"{BASE_URL}{path}?{urlencode(query)}"

    def _request_bytes(self, path: str, params: dict[str, object | None]) -> bytes:
        request = Request(self.build_url(path, params), headers={"User-Agent": "opendart-skill/1.0"})
        with self.opener(request, timeout=self.timeout) as response:  # type: ignore[misc]
            return response.read()

    def request_json(self, path: str, **params: object | None) -> dict:
        payload = json.loads(self._request_bytes(path, params).decode("utf-8"))
        return ensure_success(payload)

    def request_binary(self, path: str, **params: object | None) -> bytes:
        return self._request_bytes(path, params)

    def fetch_corp_codes(self) -> list[CorpRecord]:
        spec = get_endpoint("corp_code")
        zip_bytes = self.request_binary(spec.path)
        corp_code_archive_path(self.cache_dir).write_bytes(zip_bytes)
        xml_bytes = extract_corp_code_xml(zip_bytes)
        corp_code_xml_path(self.cache_dir).write_bytes(xml_bytes)
        rows = parse_corp_code_xml(xml_bytes)
        write_corp_code_metadata(self.cache_dir)
        return rows

    def corp_code_status(self) -> dict[str, object]:
        return corp_code_cache_status(self.cache_dir)

    def load_cached_corp_codes(self) -> list[CorpRecord]:
        path = corp_code_xml_path(self.cache_dir)
        if not path.exists():
            return []
        xml_bytes = path.read_bytes()
        try:
            return parse_corp_code_xml(xml_bytes)
        except ParseError as exc:
            archive_path = corp_code_archive_path(self.cache_dir)
            if not archive_path.exists():
                raise ValueError(
                    "corp-code XML cache is invalid and could not be repaired because corpCode.zip is missing; run `corp-code refresh`."
                ) from exc
            repaired_xml = extract_corp_code_xml(archive_path.read_bytes())
            path.write_bytes(repaired_xml)
            return parse_corp_code_xml(repaired_xml)

    def search_corp_codes(self, *, name: str | None = None, stock_code: str | None = None, exact: bool = False, limit: int = 20) -> list[CorpRecord]:
        return search_records(self.load_cached_corp_codes(), name=name, stock_code=stock_code, exact=exact, limit=limit)

    def company_overview(self, corp_code: str) -> dict:
        return self.request_json(get_endpoint("company_overview").path, corp_code=corp_code)

    def disclosure_list(self, **params: object | None) -> dict:
        return self.request_json(get_endpoint("disclosure_list").path, **params)

    def call_endpoint(self, endpoint_name: str, **params: object | None) -> dict | bytes:
        spec = get_endpoint(endpoint_name)
        if spec.output == "binary":
            return self.request_binary(spec.path, **params)
        return self.request_json(spec.path, **params)
