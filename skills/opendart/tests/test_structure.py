from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StructureTests(unittest.TestCase):
    def test_no_repo_level_layer_imports_remain_in_scripts(self) -> None:
        bad_import_patterns = (
            r'from\s+shared\.opendart_common',
            r'import\s+shared\.opendart_common',
            r'from\s+core\.',
            r'import\s+core\.',
            r'from\s+adapters\.',
            r'import\s+adapters\.',
        )
        for path in (ROOT / 'scripts').rglob('*.py'):
            text = path.read_text(encoding='utf-8')
            for pattern in bad_import_patterns:
                with self.subTest(path=path, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text))

    def test_readmes_describe_single_skill_portability(self) -> None:
        repo_root = ROOT.parents[1]
        for name in ('README.md', 'README.en.md'):
            text = (repo_root / name).read_text(encoding='utf-8')
            with self.subTest(name=name):
                self.assertIn('skills/opendart/', text)
                self.assertIn('portable', text.lower())
