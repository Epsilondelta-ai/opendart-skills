from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PromptRoutingTests(unittest.TestCase):
    def test_prompt_matrix_reference_mentions_each_family(self) -> None:
        text = (ROOT / 'references' / 'prompt-matrix.md').read_text(encoding='utf-8')
        for word in ('공시', '임원', '재무제표', '대량보유', '주요사항보고서', '투자설명서'):
            with self.subTest(word=word):
                self.assertIn(word, text)

    def test_routing_matrix_mentions_internal_sections(self) -> None:
        text = (ROOT / 'references' / 'routing-matrix.md').read_text(encoding='utf-8')
        for section in ('disclosures', 'periodic-reports', 'financials', 'equity', 'material-events', 'registration'):
            with self.subTest(section=section):
                self.assertIn(section, text)
