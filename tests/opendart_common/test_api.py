from __future__ import annotations

import json
import tempfile
import unittest
from io import BytesIO, StringIO
from pathlib import Path
from zipfile import ZipFile
from contextlib import redirect_stderr, redirect_stdout

from shared.opendart_common.api import OpenDartClient
from shared.opendart_common.cli import main as cli_main


class FakeResponse:
    def __init__(self, data: bytes):
        self.data = data

    def read(self) -> bytes:
        return self.data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class OpenDartClientTests(unittest.TestCase):
    def test_build_url_includes_api_key(self) -> None:
        client = OpenDartClient(api_key='test-key')
        url = client.build_url('/api/company.json', {'corp_code': '00126380'})
        self.assertIn('crtfc_key=test-key', url)
        self.assertIn('corp_code=00126380', url)

    def test_company_overview_uses_company_endpoint(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            return FakeResponse(json.dumps({'status': '000', 'message': 'ok', 'corp_name': '삼성전자'}).encode('utf-8'))

        client = OpenDartClient(api_key='key', opener=opener)
        payload = client.company_overview('00126380')
        self.assertEqual(payload['corp_name'], '삼성전자')
        self.assertIn('/api/company.json', calls[0])

    def test_call_endpoint_dispatches_financials(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            return FakeResponse(json.dumps({'status': '000', 'message': 'ok', 'list': []}).encode('utf-8'))

        client = OpenDartClient(api_key='key', opener=opener)
        client.call_endpoint('single_company_financials', corp_code='00126380', bsns_year='2024', reprt_code='11011', fs_div='CFS')
        self.assertIn('/api/fnlttSinglAcnt.json', calls[0])

    def test_fetch_corp_codes_caches_xml_and_metadata(self) -> None:
        buf = BytesIO()
        with ZipFile(buf, 'w') as zf:
            zf.writestr('CORPCODE.xml', '<result><list><corp_code>00126380</corp_code><corp_name>삼성전자</corp_name><corp_eng_name>Samsung Electronics</corp_eng_name><stock_code>005930</stock_code><modify_date>20240101</modify_date></list></result>')

        def opener(request, timeout=30):
            return FakeResponse(buf.getvalue())

        with tempfile.TemporaryDirectory() as tmpdir:
            client = OpenDartClient(api_key='key', opener=opener, cache_dir=tmpdir)
            rows = client.fetch_corp_codes()
            self.assertEqual(rows[0].corp_name, '삼성전자')
            self.assertTrue((Path(tmpdir) / 'corpCode.xml').exists())
            self.assertTrue((Path(tmpdir) / 'corpCode.meta.json').exists())
            self.assertFalse(client.corp_code_status()['stale'])

    def test_missing_key_raises(self) -> None:
        client = OpenDartClient(api_key=None)
        with self.assertRaises(ValueError):
            client.build_url('/api/company.json', {'corp_code': '00126380'})

    def test_cli_warns_on_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text('<result></result>', encoding='utf-8')
            err = StringIO()
            out = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                cli_main(['--cache-dir', tmpdir, 'corp-code', 'search', '--name', '삼성'])
            self.assertIn('warning: corp-code cache is stale', err.getvalue())
