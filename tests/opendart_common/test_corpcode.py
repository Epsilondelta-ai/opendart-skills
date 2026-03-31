from __future__ import annotations

import unittest
from io import BytesIO
from zipfile import ZipFile

from shared.opendart_common.corpcode import extract_corp_code_xml, load_records_from_zip, parse_corp_code_xml, search_records

XML = """<result>
<list><corp_code>00126380</corp_code><corp_name>삼성전자</corp_name><corp_eng_name>Samsung Electronics</corp_eng_name><stock_code>005930</stock_code><modify_date>20240101</modify_date></list>
<list><corp_code>00164779</corp_code><corp_name>현대자동차</corp_name><corp_eng_name>Hyundai Motor</corp_eng_name><stock_code>005380</stock_code><modify_date>20240101</modify_date></list>
</result>""".encode("utf-8")


def make_zip() -> bytes:
    buf = BytesIO()
    with ZipFile(buf, 'w') as zf:
        zf.writestr('CORPCODE.xml', XML)
    return buf.getvalue()


class CorpCodeTests(unittest.TestCase):
    def test_parse_corp_code_xml(self) -> None:
        rows = parse_corp_code_xml(XML)
        self.assertEqual(rows[0].corp_name, '삼성전자')
        self.assertEqual(rows[1].stock_code, '005380')

    def test_extract_and_load_zip(self) -> None:
        zip_bytes = make_zip()
        self.assertEqual(extract_corp_code_xml(zip_bytes), XML)
        rows = load_records_from_zip(zip_bytes)
        self.assertEqual(len(rows), 2)

    def test_search_records(self) -> None:
        rows = parse_corp_code_xml(XML)
        self.assertEqual(search_records(rows, name='삼성')[0].corp_code, '00126380')
        self.assertEqual(search_records(rows, stock_code='005380')[0].corp_name, '현대자동차')
