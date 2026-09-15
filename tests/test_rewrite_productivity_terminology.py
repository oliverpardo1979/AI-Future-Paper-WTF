"""AI efficiency names B; research productivity retains its distinct meaning."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AITerminologyTests(unittest.TestCase):
    def test_ai_efficiency_is_the_manuscript_term(self):
        files = [ROOT / 'main_rewrite.tex', *sorted((ROOT / 'sections_rewrite').rglob('*.tex'))]
        matches = []
        for path in files:
            text = path.read_text(encoding='utf-8')
            matches.extend((path.name, match.group()) for match in
                           re.finditer(r'AI(?:\s+|-)productivity', text))
        self.assertEqual(matches, [])

    def test_definition_and_literature_bridge(self):
        text = (ROOT / 'sections_rewrite/03_model.tex').read_text(encoding='utf-8')
        self.assertIn('AI efficiency: AI services obtained per unit of compute', text)
        self.assertIn('algorithmic efficiency', text)
        self.assertIn(r'\citep{hernandezbrown2020,erdilbesiroglu2022}', text)
        self.assertIn('X=BU.', text)
        self.assertIn(r'\dot B=\chi(BM)^\eta\psi(B)', text)
        self.assertIn('The parameter \\(\\chi\\) shifts research productivity.', text)
        self.assertIn('$A$ efficiency units', text)

    def test_legacy_equation_labels_are_unchanged(self):
        text = (ROOT / 'sections_rewrite/05_uncapped_equilibria.tex').read_text(encoding='utf-8')
        self.assertIn(r'\label{eq:rewrite-uncapped-unit-efficiency-growth}', text)
        self.assertIn(r'\eqref{eq:rewrite-uncapped-unit-efficiency-growth}', text)


if __name__ == '__main__':
    unittest.main()
