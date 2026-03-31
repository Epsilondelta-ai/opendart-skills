from __future__ import annotations

import json
import sys
import tempfile
import unittest
from io import BytesIO, StringIO
from pathlib import Path
from zipfile import ZipFile
from contextlib import redirect_stderr, redirect_stdout

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.api import OpenDartClient
from lib.cli import main as cli_main


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

    def test_company_overview_uses_company_endpoint(self) -> None:
        calls = []
        def opener(request, timeout=30):
            calls.append(request.full_url)
            return FakeResponse(json.dumps({'status': '000', 'message': 'ok', 'corp_name': '삼성전자'}).encode('utf-8'))
        payload = OpenDartClient(api_key='key', opener=opener).company_overview('00126380')
        self.assertEqual(payload['corp_name'], '삼성전자')
        self.assertIn('/api/company.json', calls[0])

    def test_fetch_corp_codes_preserves_xml_escaping_and_metadata(self) -> None:
        corp_xml = (
            '<result><list><corp_code>00126380</corp_code><corp_name>AT&amp;T Korea</corp_name>'
            '<corp_eng_name>AT&amp;T Korea</corp_eng_name><stock_code>005930</stock_code>'
            '<modify_date>20240101</modify_date></list></result>'
        )
        buf = BytesIO()
        with ZipFile(buf, 'w') as zf:
            zf.writestr('CORPCODE.xml', corp_xml)

        def opener(request, timeout=30):
            return FakeResponse(buf.getvalue())

        with tempfile.TemporaryDirectory() as tmpdir:
            client = OpenDartClient(api_key='key', opener=opener, cache_dir=tmpdir)
            rows = client.fetch_corp_codes()
            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertIn('AT&amp;T Korea', Path(tmpdir, 'corpCode.xml').read_text(encoding='utf-8'))
            self.assertIn('AT&T Korea', Path(tmpdir, 'corpCode.records.json').read_text(encoding='utf-8'))
            self.assertFalse(client.corp_code_status()['stale'])

    def test_search_repairs_invalid_xml_cache_from_zip_archive(self) -> None:
        valid_xml = (
            '<result><list><corp_code>00126380</corp_code><corp_name>AT&amp;T Korea</corp_name>'
            '<corp_eng_name>AT&amp;T Korea</corp_eng_name><stock_code>005930</stock_code>'
            '<modify_date>20240101</modify_date></list></result>'
        )
        buf = BytesIO()
        with ZipFile(buf, 'w') as zf:
            zf.writestr('CORPCODE.xml', valid_xml)

        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text(
                '<result><list><corp_code>00126380</corp_code><corp_name>AT&T Korea</corp_name></list></result>',
                encoding='utf-8',
            )
            Path(tmpdir, 'corpCode.zip').write_bytes(buf.getvalue())
            client = OpenDartClient(cache_dir=tmpdir)

            rows = client.search_corp_codes(name='AT&T')

            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertIn('AT&amp;T Korea', Path(tmpdir, 'corpCode.xml').read_text(encoding='utf-8'))

    def test_search_repairs_invalid_xml_cache_from_records_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text(
                '<result><list><corp_code>00126380</corp_code><corp_name>AT&T Korea</corp_name></list></result>',
                encoding='utf-8',
            )
            Path(tmpdir, 'corpCode.records.json').write_text(
                json.dumps(
                    [
                        {
                            'corp_code': '00126380',
                            'corp_name': 'AT&T Korea',
                            'corp_eng_name': 'AT&T Korea',
                            'stock_code': '005930',
                            'modify_date': '20240101',
                        }
                    ],
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding='utf-8',
            )
            client = OpenDartClient(cache_dir=tmpdir)

            rows = client.search_corp_codes(name='AT&T')

            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertIn('AT&amp;T Korea', Path(tmpdir, 'corpCode.xml').read_text(encoding='utf-8'))

    def test_search_repairs_missing_xml_cache_from_records_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.records.json').write_text(
                json.dumps(
                    [
                        {
                            'corp_code': '00126380',
                            'corp_name': 'AT&T Korea',
                            'corp_eng_name': 'AT&T Korea',
                            'stock_code': '005930',
                            'modify_date': '20240101',
                        }
                    ],
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding='utf-8',
            )
            client = OpenDartClient(cache_dir=tmpdir)

            rows = client.search_corp_codes(name='AT&T')

            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertIn('AT&amp;T Korea', Path(tmpdir, 'corpCode.xml').read_text(encoding='utf-8'))

    def test_search_auto_refreshes_when_local_cache_is_missing_and_api_key_exists(self) -> None:
        corp_xml = (
            '<result><list><corp_code>00126380</corp_code><corp_name>AT&amp;T Korea</corp_name>'
            '<corp_eng_name>AT&amp;T Korea</corp_eng_name><stock_code>005930</stock_code>'
            '<modify_date>20240101</modify_date></list></result>'
        )
        buf = BytesIO()
        with ZipFile(buf, 'w') as zf:
            zf.writestr('CORPCODE.xml', corp_xml)

        def opener(request, timeout=30):
            return FakeResponse(buf.getvalue())

        with tempfile.TemporaryDirectory() as tmpdir:
            client = OpenDartClient(api_key='key', opener=opener, cache_dir=tmpdir)

            rows = client.search_corp_codes(name='AT&T')

            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertTrue(Path(tmpdir, 'corpCode.xml').exists())
            self.assertTrue(Path(tmpdir, 'corpCode.zip').exists())
            self.assertTrue(Path(tmpdir, 'corpCode.records.json').exists())

    def test_search_falls_back_to_records_snapshot_when_zip_is_corrupt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text(
                '<result><list><corp_code>00126380</corp_code><corp_name>AT&T Korea</corp_name></list></result>',
                encoding='utf-8',
            )
            Path(tmpdir, 'corpCode.zip').write_bytes(b'not-a-zip')
            Path(tmpdir, 'corpCode.records.json').write_text(
                json.dumps(
                    [
                        {
                            'corp_code': '00126380',
                            'corp_name': 'AT&T Korea',
                            'corp_eng_name': 'AT&T Korea',
                            'stock_code': '005930',
                            'modify_date': '20240101',
                        }
                    ],
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding='utf-8',
            )
            client = OpenDartClient(cache_dir=tmpdir)

            rows = client.search_corp_codes(name='AT&T')

            self.assertEqual(rows[0].corp_name, 'AT&T Korea')
            self.assertIn('AT&amp;T Korea', Path(tmpdir, 'corpCode.xml').read_text(encoding='utf-8'))

    def test_cli_warns_on_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text('<result></result>', encoding='utf-8')
            err = StringIO(); out = StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                cli_main(['--cache-dir', tmpdir, 'corp-code', 'search', '--name', '삼성'])
            self.assertIn('warning: corp-code cache is stale', err.getvalue())
