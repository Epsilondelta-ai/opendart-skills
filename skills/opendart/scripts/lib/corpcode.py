from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class CorpRecord:
    corp_code: str
    corp_name: str
    corp_eng_name: str = ""
    stock_code: str = ""
    modify_date: str = ""


def parse_corp_code_xml(xml_data: bytes | str) -> list[CorpRecord]:
    if isinstance(xml_data, bytes):
        root = ET.fromstring(xml_data)
    else:
        root = ET.fromstring(xml_data.encode("utf-8"))
    rows: list[CorpRecord] = []
    for node in root.findall("list"):
        values = {child.tag: (child.text or "").strip() for child in node}
        rows.append(
            CorpRecord(
                corp_code=values.get("corp_code", ""),
                corp_name=values.get("corp_name", ""),
                corp_eng_name=values.get("corp_eng_name", ""),
                stock_code=values.get("stock_code", ""),
                modify_date=values.get("modify_date", ""),
            )
        )
    return rows


def extract_corp_code_xml(zip_bytes: bytes) -> bytes:
    with ZipFile(BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if name.lower().endswith('.xml'):
                return zf.read(name)
    raise ValueError('corpCode zip did not contain an xml file')


def load_records_from_zip(zip_bytes: bytes) -> list[CorpRecord]:
    return parse_corp_code_xml(extract_corp_code_xml(zip_bytes))


def search_records(
    records: list[CorpRecord],
    *,
    name: str | None = None,
    stock_code: str | None = None,
    exact: bool = False,
    limit: int | None = 20,
) -> list[CorpRecord]:
    name_query = name.casefold() if name else None
    matches: list[CorpRecord] = []
    for record in records:
        if name_query:
            record_name = record.corp_name.casefold()
            ok = record_name == name_query if exact else name_query in record_name
            if not ok:
                continue
        if stock_code and record.stock_code != stock_code:
            continue
        matches.append(record)
        if limit is not None and len(matches) >= limit:
            break
    return matches
