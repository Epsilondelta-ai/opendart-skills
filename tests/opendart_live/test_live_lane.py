from __future__ import annotations

import os
import unittest

from shared.opendart_common.api import OpenDartClient
from shared.opendart_common.corpcode import search_records
from shared.opendart_common.errors import OpenDartAPIError

DEFAULT_CORP_NAME = os.environ.get('OPENDART_LIVE_CORP_NAME', '삼성전자')
DEFAULT_BSNS_YEAR = os.environ.get('OPENDART_LIVE_BSNS_YEAR', '2024')
DEFAULT_REPRT_CODE = os.environ.get('OPENDART_LIVE_REPRT_CODE', '11011')
DEFAULT_FS_DIV = os.environ.get('OPENDART_LIVE_FS_DIV', 'CFS')


class OpenDartLiveSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        api_key = os.environ.get('OPENDART_API_KEY')
        if not api_key:
            raise unittest.SkipTest('OPENDART_API_KEY is not set; live smoke lane is opt-in and skipped by default.')
        cls.client = OpenDartClient(api_key=api_key)
        rows = cls.client.fetch_corp_codes()
        matches = search_records(rows, name=DEFAULT_CORP_NAME, exact=False, limit=1)
        if not matches:
            raise unittest.SkipTest(f'No corp_code match for {DEFAULT_CORP_NAME!r} in live corp-code dataset.')
        cls.corp_code = matches[0].corp_code

    def test_corp_code_refresh(self) -> None:
        status = self.client.corp_code_status()
        self.assertFalse(status['stale'])

    def test_company_overview(self) -> None:
        payload = self.client.company_overview(self.corp_code)
        self.assertEqual(payload['status'], '000')

    def test_disclosure_list(self) -> None:
        try:
            payload = self.client.disclosure_list(corp_code=self.corp_code, bgn_de='20240101', end_de='20241231', page_no='1', page_count='10')
        except OpenDartAPIError as exc:
            self.assertIn(exc.status, {'013'})
        else:
            self.assertEqual(payload['status'], '000')

    def test_financial_endpoint(self) -> None:
        try:
            payload = self.client.call_endpoint(
                'single_company_financials',
                corp_code=self.corp_code,
                bsns_year=DEFAULT_BSNS_YEAR,
                reprt_code=DEFAULT_REPRT_CODE,
                fs_div=DEFAULT_FS_DIV,
            )
        except OpenDartAPIError as exc:
            self.assertIn(exc.status, {'013'})
        else:
            self.assertIsInstance(payload, dict)
            self.assertEqual(payload['status'], '000')
