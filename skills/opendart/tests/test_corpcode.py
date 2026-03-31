from __future__ import annotations

import sys
import unittest
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.corpcode import extract_corp_code_xml, load_records_from_zip, parse_corp_code_xml, search_records

XML = """<result>
<list><corp_code>00126380</corp_code><corp_name>삼성전자</corp_name><corp_eng_name>Samsung Electronics</corp_eng_name><stock_code>005930</stock_code><modify_date>20240101</modify_date></list>
<list><corp_code>00164779</corp_code><corp_name>현대자동차</corp_name><corp_eng_name>Hyundai Motor</corp_eng_name><stock_code>005380</stock_code><modify_date>20240101</modify_date></list>
</result>""".encode('utf-8')


def make_zip() -> bytes:
    buf = BytesIO()
    with ZipFile(buf, 'w') as zf:
        zf.writestr('CORPCODE.xml', XML)
    return buf.getvalue()


class CorpCodeTests(unittest.TestCase):
    def test_parse_corp_code_xml(self) -> None:
        rows = parse_corp_code_xml(XML)
        self.assertEqual(rows[0].corp_name, '삼성전자')

    def test_extract_and_load_zip(self) -> None:
        rows = load_records_from_zip(make_zip())
        self.assertEqual(len(rows), 2)
        self.assertEqual(extract_corp_code_xml(make_zip()), XML)

    def test_search_records(self) -> None:
        rows = parse_corp_code_xml(XML)
        self.assertEqual(search_records(rows, name='삼성')[0].corp_code, '00126380')
        self.assertEqual(search_records(rows, stock_code='005380')[0].corp_name, '현대자동차')
