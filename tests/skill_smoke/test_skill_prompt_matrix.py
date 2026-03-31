import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / 'tests' / 'skill_smoke' / 'prompt_matrix.json'
UMBRELLA = 'opendart'
SPECIALISTS = {
    'opendart-disclosures': '공시정보',
    'opendart-periodic-reports': '정기보고서 주요정보',
    'opendart-financials': '정기보고서 재무정보',
    'opendart-equity': '지분공시 종합정보',
    'opendart-material-events': '주요사항보고서 주요정보',
    'opendart-registration': '증권신고서 주요정보',
}
OWNERSHIP_KEYWORDS = {
    'opendart-disclosures': ('공시', '원문', '첨부', '목록'),
    'opendart-periodic-reports': ('정기보고서', '임원', '직원', '배당', '감사'),
    'opendart-financials': ('재무', '재무제표', '재무지표', '활용마당'),
    'opendart-equity': ('지분', '대량보유', '최대주주', '특수관계인'),
    'opendart-material-events': ('주요사항보고서', '합병', '분할', '이벤트'),
    'opendart-registration': ('증권신고서', '신고서', '투자설명서', '모집', '매출'),
}
BOUNDARY_MARKERS = ('말고', '대신', '이미', '먼저', '어느 skill', '어떤 API')


class PromptMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads(MATRIX.read_text(encoding='utf-8'))

    def test_expected_skill_coverage(self):
        skills = {entry['expected_skill'] for entry in self.entries}
        self.assertIn(UMBRELLA, skills)
        self.assertTrue(set(SPECIALISTS).issubset(skills))

    def test_each_entry_has_required_fields(self):
        for entry in self.entries:
            with self.subTest(entry=entry):
                self.assertIn('prompt', entry)
                self.assertIn('expected_skill', entry)
                self.assertIn('family', entry)
                self.assertIn('intent', entry)
                self.assertTrue(entry['prompt'].strip())

    def test_prompts_are_unique(self):
        prompts = [entry['prompt'] for entry in self.entries]
        counts = Counter(prompts)
        duplicates = {prompt: count for prompt, count in counts.items() if count > 1}
        self.assertFalse(duplicates, duplicates)

    def test_umbrella_entries_stay_generic_or_cross_family(self):
        for entry in self.entries:
            if entry['expected_skill'] != UMBRELLA:
                continue
            with self.subTest(prompt=entry['prompt']):
                if entry['intent'] == 'generic':
                    self.assertNotRegex(entry['prompt'], r'정기보고서 주요정보|지분공시 종합정보|주요사항보고서 주요정보|증권신고서 주요정보')
                else:
                    self.assertTrue(any(marker in entry['prompt'] for marker in BOUNDARY_MARKERS))

    def test_specialist_entries_include_owned_keywords(self):
        for entry in self.entries:
            skill = entry['expected_skill']
            if skill == UMBRELLA:
                continue
            with self.subTest(prompt=entry['prompt'], skill=skill):
                self.assertTrue(any(keyword in entry['prompt'] for keyword in OWNERSHIP_KEYWORDS[skill]))

    def test_each_specialist_has_boundary_coverage(self):
        boundary_counts = defaultdict(int)
        for entry in self.entries:
            if entry['intent'] == 'boundary':
                boundary_counts[entry['expected_skill']] += 1
        self.assertGreaterEqual(boundary_counts[UMBRELLA], 2)
        for skill in SPECIALISTS:
            with self.subTest(skill=skill):
                self.assertGreaterEqual(boundary_counts[skill], 1)

    def test_each_specialist_has_minimum_prompt_count(self):
        counts = Counter(entry['expected_skill'] for entry in self.entries)
        for skill in SPECIALISTS:
            with self.subTest(skill=skill):
                self.assertGreaterEqual(counts[skill], 4)
