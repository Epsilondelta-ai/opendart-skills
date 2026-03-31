from __future__ import annotations

import unittest

from shared.opendart_common.errors import OpenDartAPIError, describe_status, ensure_success


class ErrorsTests(unittest.TestCase):
    def test_describe_status_knows_known_code(self) -> None:
        self.assertEqual(describe_status("020"), "요청 제한 초과")

    def test_ensure_success_raises_for_failure(self) -> None:
        with self.assertRaises(OpenDartAPIError) as ctx:
            ensure_success({"status": "100", "message": "bad field"})
        self.assertEqual(ctx.exception.status, "100")

    def test_ensure_success_returns_payload_for_success(self) -> None:
        payload = {"status": "000", "message": "ok", "list": []}
        self.assertIs(ensure_success(payload), payload)
